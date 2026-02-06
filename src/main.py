"""메인 실행 스크립트"""
import sys
from datetime import datetime
from .sheets_client import SheetsClient
from .analyzer import DataAnalyzer
from .ai_generator import AIReportGenerator
from .confluence_client import ConfluenceClient
from .slack_client import SlackClient


def main():
    print(f"\n{'='*60}")
    print(f"📊 월간 분석 리포트 자동화 시작")
    print(f"   실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    slack = None
    
    try:
        # Slack 클라이언트 초기화 (에러 알림용)
        slack = SlackClient()
        
        # Step 1: Google Sheets 데이터 읽기
        print("📖 Step 1: Google Sheets 데이터 읽기...")
        sheets = SheetsClient()
        data = sheets.get_all_data()
        print("   ✅ 완료\n")

        # Step 2: 데이터 분석
        print("📈 Step 2: 데이터 분석...")
        analyzer = DataAnalyzer(data)
        context = analyzer.prepare_ai_context()
        print(f"   분석 월: {analyzer.get_latest_month()}")
        print("   ✅ 완료\n")

        # Step 3: AI 리포트 생성
        print("🤖 Step 3: AI 리포트 생성 (Gemini)...")
        ai = AIReportGenerator()
        report = ai.generate_report(context)
        summary = ai.generate_summary(report)
        print("   ✅ 완료\n")

        # Step 4: Confluence 업로드
        print("📝 Step 4: Confluence 업로드...")
        confluence = ConfluenceClient()
        confluence_url = confluence.upload_report(report)
        print(f"   URL: {confluence_url}")
        print("   ✅ 완료\n")

        # Step 5: Slack 공유
        print("💬 Step 5: Slack 알림 전송...")
        slack.send_message(summary, confluence_url)
        print("   ✅ 완료\n")

        print(f"{'='*60}")
        print("🎉 월간 리포트 자동화 완료!")
        print(f"   Confluence: {confluence_url}")
        print(f"{'='*60}\n")

    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        print(f"\n❌ 오류 발생: {error_msg}")
        
        # Slack으로 에러 알림
        if slack:
            try:
                slack.send_error(error_msg)
            except:
                pass
        
        sys.exit(1)


if __name__ == "__main__":
    main()
