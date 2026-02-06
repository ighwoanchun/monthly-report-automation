"""설정 관리"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Google Sheets
    GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
    GOOGLE_CREDENTIALS_PATH = os.getenv(
        "GOOGLE_CREDENTIALS_PATH", "credentials/service-account.json"
    )

    # 분석 대상 시트
    SHEETS = {
        "monthly": "월통합분석",
        "hire_raw": "합격기준리드타임_raw",
        "apply_raw": "지원기준리드타임_raw",
    }

    # Gemini API (무료)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = "gemini-2.0-flash"

    # Confluence
    CONFLUENCE_URL = os.getenv("CONFLUENCE_URL")
    CONFLUENCE_EMAIL = os.getenv("CONFLUENCE_EMAIL")
    CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
    CONFLUENCE_SPACE = os.getenv("CONFLUENCE_SPACE", "DATA")
    CONFLUENCE_PARENT_PAGE_ID = os.getenv("CONFLUENCE_PARENT_PAGE_ID")

    # Slack (Bot Token + Channel ID 방식)
    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")  # xoxb-...
    SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")  # C01234567
