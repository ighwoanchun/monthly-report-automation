"""Google Sheets 데이터 읽기"""
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from .config import Config


class SheetsClient:
    def __init__(self):
        self.creds = Credentials.from_service_account_file(
            Config.GOOGLE_CREDENTIALS_PATH,
            scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"],
        )
        self.service = build("sheets", "v4", credentials=self.creds)

    def read_sheet(self, sheet_name: str) -> pd.DataFrame:
        """시트 데이터를 DataFrame으로 읽기"""
        result = (
            self.service.spreadsheets()
            .values()
            .get(spreadsheetId=Config.GOOGLE_SHEET_ID, range=f"{sheet_name}!A:Z")
            .execute()
        )

        values = result.get("values", [])
        if not values:
            return pd.DataFrame()

        # 첫 행을 컬럼명으로
        df = pd.DataFrame(values[1:], columns=values[0])
        return df

    def get_all_data(self) -> dict:
        """모든 시트 데이터 읽기"""
        data = {}
        for key, sheet_name in Config.SHEETS.items():
            print(f"  📖 {sheet_name} 시트 읽는 중...")
            data[key] = self.read_sheet(sheet_name)
        return data
