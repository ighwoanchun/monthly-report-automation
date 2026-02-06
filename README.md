# 📊 월간 채용 분석 리포트 자동화

매월 1일 자동으로 채용 플랫폼 실적 분석 리포트를 생성하여 Confluence에 업로드하고 Slack으로 알림을 보냅니다.

## 🚀 기능

- **Google Sheets** 데이터 자동 수집
- **Claude API**를 활용한 AI 분석 리포트 생성
- **Confluence** 자동 업로드
- **Slack** 요약 알림

## 📁 프로젝트 구조

```
monthly-report-automation/
├── src/
│   ├── __init__.py
│   ├── config.py           # 설정 관리
│   ├── sheets_client.py    # Google Sheets 연동
│   ├── analyzer.py         # 데이터 분석
│   ├── ai_generator.py     # Claude AI 리포트 생성
│   ├── confluence_client.py # Confluence 업로드
│   ├── slack_client.py     # Slack 알림
│   └── main.py             # 메인 실행
├── prompts/
│   └── analysis_prompt.md  # AI 프롬프트
├── credentials/
│   └── .gitkeep
├── .github/workflows/
│   └── monthly-report.yml  # GitHub Actions
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 🔧 설정 방법

### 1. 저장소 클론

```bash
git clone https://github.com/your-username/monthly-report-automation.git
cd monthly-report-automation
```

### 2. 환경 설정

```bash
# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
# .env 파일을 열어서 값 입력
```

### 3. API 키 발급

#### Google Sheets API
1. [Google Cloud Console](https://console.cloud.google.com) 접속
2. 새 프로젝트 생성
3. APIs & Services → Enable APIs → "Google Sheets API" 활성화
4. Credentials → Create Credentials → Service Account
5. 키 생성 (JSON) → `credentials/service-account.json`으로 저장
6. Google Sheet에서 서비스 계정 이메일에 "뷰어" 권한 부여

#### Claude API
1. [Anthropic Console](https://console.anthropic.com) 접속
2. API Keys → Create Key
3. `.env`에 `ANTHROPIC_API_KEY` 설정

#### Confluence API
1. [Atlassian API Token](https://id.atlassian.com/manage-profile/security/api-tokens) 접속
2. Create API token
3. `.env`에 설정

#### Slack Webhook
1. [Slack Apps](https://api.slack.com/apps) → Create New App
2. Incoming Webhooks 활성화
3. Webhook URL을 `.env`에 설정

### 4. GitHub Secrets 설정

Repository → Settings → Secrets and variables → Actions → New repository secret

| Secret 이름 | 설명 |
|------------|------|
| `GOOGLE_SERVICE_ACCOUNT` | 서비스 계정 JSON 전체 내용 |
| `GOOGLE_SHEET_ID` | Google Sheet ID |
| `ANTHROPIC_API_KEY` | Claude API 키 |
| `CONFLUENCE_URL` | https://your-domain.atlassian.net |
| `CONFLUENCE_EMAIL` | Atlassian 계정 이메일 |
| `CONFLUENCE_API_TOKEN` | Confluence API 토큰 |
| `CONFLUENCE_SPACE` | Confluence 스페이스 키 |
| `SLACK_WEBHOOK_URL` | Slack Webhook URL |

## 💻 로컬 실행

```bash
# 환경변수 로드 후 실행
python -m src.main
```

## ⏰ 자동 실행

GitHub Actions가 **매월 1일 오전 9시 (한국시간)**에 자동 실행됩니다.

수동 실행: Repository → Actions → Monthly Report Automation → Run workflow

## 💰 비용

| 항목 | 비용 |
|------|------|
| Claude API (월 1회) | ~$0.15~0.30 |
| GitHub Actions | 무료 |
| **총계** | **~$0.30/월** |

## 📋 리포트 구조

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

## 🔧 커스터마이징

### 프롬프트 수정
`prompts/analysis_prompt.md` 파일을 수정하여 리포트 형식을 변경할 수 있습니다.

### 시트 구조 변경
`src/config.py`의 `SHEETS` 딕셔너리를 수정하세요.

## 📝 라이선스

MIT License
