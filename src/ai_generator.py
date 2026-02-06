"""Gemini API를 사용한 리포트 생성 (무료)"""
import google.generativeai as genai
from pathlib import Path
from .config import Config


class AIReportGenerator:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        self.prompt_template = self._load_prompt()

    def _load_prompt(self) -> str:
        """프롬프트 템플릿 로드"""
        prompt_path = Path(__file__).parent.parent / "prompts" / "analysis_prompt.md"
        if prompt_path.exists():
            return prompt_path.read_text(encoding="utf-8")
        return self._default_prompt()

    def _default_prompt(self) -> str:
        return """
당신은 채용 플랫폼 데이터 분석 전문가입니다.

## 용어 정의
- pass_cnt = 서류통과 수 (합격 아님)
- hire_cnt = 합격 수 (최종 합격)
- new_com_accept = 신규기업 가입
- recruit_fee = 수수료 매출

## 데이터 구분
- 합격기준리드타임_raw: "해당 월에 합격한 사람들" → Part A 실적 분석
- 지원기준리드타임_raw: "해당 월에 지원한 사람들" → Part B 예측 분석

## 전환율 참조
지원→합격: 당월 11.3%, 전월 45.2%★, 전전월 25.8%
서류통과→합격: 당월 26%, 전월 37.5%★, 전전월 14%

## 리포트 구조
### Part A. 실적 분석 (합격기준)
1. Executive Summary
2. 월별 KPI 추이
3. 매출 구조
4. 합격자 분석 (직군별/기업규모별/리드타임)
5. 성과 평가

### Part B. 파이프라인 분석 (지원기준)
6. 지원 현황
7. 퍼널 전환 분석
8. 익월 예측

### 공통
9. 리스크 & 기회
10. 액션 아이템

## 주의사항
- 직군별 합계는 월통합분석의 hire_cnt와 일치해야 함
- TOP 10 외 직군은 "기타"로 묶고 구성 명시
- 미분류(null) 데이터는 "미분류"로 표시

마크다운 형식으로 작성해주세요.
"""

    def generate_report(self, data_context: str) -> str:
        """전체 리포트 생성"""
        prompt = f"{self.prompt_template}\n\n## 분석 데이터\n{data_context}"

        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=8000,
                temperature=0.3,
            ),
        )

        return response.text

    def generate_summary(self, full_report: str) -> str:
        """Slack용 요약 생성"""
        prompt = f"""
다음 리포트에서 Slack 공유용 Executive Summary를 추출해주세요.

[포맷]
*핵심 성과*
• 총 매출: ₩XX.X억 (±X.X% MoM)
• 합격 수: XXX건 (±X.X% MoM)
• 신규기업: XXX건 (±X.X% MoM)

*⚠️ Alert* (1-2개)
*📈 Opportunity* (1-2개)

---
리포트 내용:
{full_report[:4000]}
"""
        response = self.model.generate_content(prompt)
        return response.text
