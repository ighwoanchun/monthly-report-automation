"""Slack 알림 전송 (Bot Token + Channel ID 방식)"""
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from .config import Config


class SlackClient:
    def __init__(self):
        self.client = WebClient(token=Config.SLACK_BOT_TOKEN)
        self.channel = Config.SLACK_CHANNEL_ID

    def send_message(self, summary: str, confluence_url: str):
        """Slack에 리포트 요약 전송"""
        try:
            self.client.chat_postMessage(
                channel=self.channel,
                blocks=[
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "📊 월간 채용 실적 분석 리포트",
                            "emoji": True,
                        },
                    },
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": summary},
                    },
                    {"type": "divider"},
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"📎 *전체 리포트:* <{confluence_url}|Confluence에서 보기>",
                        },
                    },
                ],
                text=f"📊 월간 채용 실적 분석 리포트\n{confluence_url}",
            )
        except SlackApiError as e:
            print(f"Slack 전송 실패: {e.response['error']}")
            raise

    def send_error(self, error_message: str):
        """에러 발생 시 알림"""
        try:
            self.client.chat_postMessage(
                channel=self.channel,
                blocks=[
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "❌ 월간 리포트 생성 실패",
                            "emoji": True,
                        },
                    },
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": f"```{error_message}```"},
                    },
                ],
                text=f"❌ 월간 리포트 생성 실패: {error_message}",
            )
        except SlackApiError as e:
            print(f"Slack 에러 알림 실패: {e.response['error']}")
