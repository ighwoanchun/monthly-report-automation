"""데이터 분석 (기본 통계)"""
import pandas as pd
import numpy as np
from datetime import datetime


class DataAnalyzer:
    def __init__(self, data: dict):
        self.monthly = data["monthly"]
        self.hire_raw = data["hire_raw"]
        self.apply_raw = data["apply_raw"]
        self._prepare_data()

    def _prepare_data(self):
        """데이터 타입 변환"""
        # 숫자형 컬럼 변환
        numeric_cols = [
            "total_sales",
            "hire_cnt",
            "pass_cnt",
            "matchup_cnt",
            "new_com_accept",
            "recruit_fee",
            "flat_rate_fee",
            "ad_sales",
            "working_days",
        ]
        for col in numeric_cols:
            if col in self.monthly.columns:
                self.monthly[col] = pd.to_numeric(self.monthly[col], errors="coerce")

        # hire_raw 숫자형 변환
        hire_numeric = ["hire_count", "lead_time_to_doc_pass", "lead_time_doc_pass_to_hire", "total_lead_time"]
        for col in hire_numeric:
            if col in self.hire_raw.columns:
                self.hire_raw[col] = pd.to_numeric(self.hire_raw[col], errors="coerce")

        # apply_raw 숫자형 변환
        apply_numeric = ["applicant_count", "doc_pass_count", "hire_count"]
        for col in apply_numeric:
            if col in self.apply_raw.columns:
                self.apply_raw[col] = pd.to_numeric(self.apply_raw[col], errors="coerce")

    def get_latest_month(self) -> str:
        """가장 최근 월 반환"""
        return self.monthly["report_month"].iloc[-1]

    def get_summary_stats(self) -> dict:
        """Executive Summary용 핵심 지표"""
        latest = self.monthly.iloc[-1]
        prev = self.monthly.iloc[-2] if len(self.monthly) > 1 else latest

        def calc_mom(current, previous):
            if pd.isna(previous) or previous == 0:
                return 0
            return round((current - previous) / previous * 100, 1)

        return {
            "report_month": latest["report_month"],
            "total_sales": int(latest["total_sales"]) if not pd.isna(latest["total_sales"]) else 0,
            "total_sales_mom": calc_mom(latest["total_sales"], prev["total_sales"]),
            "hire_cnt": int(latest["hire_cnt"]) if not pd.isna(latest["hire_cnt"]) else 0,
            "hire_cnt_mom": calc_mom(latest["hire_cnt"], prev["hire_cnt"]),
            "pass_cnt": int(latest["pass_cnt"]) if not pd.isna(latest["pass_cnt"]) else 0,
            "pass_cnt_mom": calc_mom(latest["pass_cnt"], prev["pass_cnt"]),
            "new_com_accept": int(latest["new_com_accept"]) if not pd.isna(latest["new_com_accept"]) else 0,
            "new_com_accept_mom": calc_mom(latest["new_com_accept"], prev["new_com_accept"]),
        }

    def prepare_ai_context(self) -> str:
        """AI 분석용 컨텍스트 생성"""
        summary = self.get_summary_stats()

        # 월통합분석 최근 4개월
        monthly_recent = self.monthly.tail(4).to_markdown(index=False)

        # 합격기준 직군별 요약 (최신 월)
        latest_month = self.monthly["report_month"].iloc[-1]
        hire_latest = self.hire_raw[self.hire_raw["hire_month"] == latest_month] if "hire_month" in self.hire_raw.columns else self.hire_raw
        
        hire_by_job = hire_latest.groupby("job_category", dropna=False).agg({
            "hire_count": "sum"
        }).sort_values("hire_count", ascending=False).head(15)

        # 지원기준 직군별 요약
        apply_latest = self.apply_raw[self.apply_raw["apply_month"] == latest_month] if "apply_month" in self.apply_raw.columns else self.apply_raw
        
        apply_by_job = apply_latest.groupby("job_category", dropna=False).agg({
            "applicant_count": "sum",
            "doc_pass_count": "sum",
            "hire_count": "sum"
        }).sort_values("applicant_count", ascending=False).head(15)

        context = f"""
## 월통합분석 데이터 (최근 4개월)
{monthly_recent}

## 합격기준리드타임 요약 (최신 월, 직군별 합격 수)
{hire_by_job.to_markdown()}

## 지원기준리드타임 요약 (최신 월, 직군별)
{apply_by_job.to_markdown()}

## 핵심 지표 요약
- 분석 월: {summary['report_month']}
- 총 매출: {summary['total_sales']:,}원 (MoM {summary['total_sales_mom']:+}%)
- 합격 수: {summary['hire_cnt']}건 (MoM {summary['hire_cnt_mom']:+}%)
- 서류통과 수: {summary['pass_cnt']}명 (MoM {summary['pass_cnt_mom']:+}%)
- 신규기업 가입: {summary['new_com_accept']}건 (MoM {summary['new_com_accept_mom']:+}%)

## 전체 Raw 데이터 (합격기준 - 상위 50행)
{hire_latest.head(50).to_markdown(index=False)}

## 전체 Raw 데이터 (지원기준 - 상위 50행)
{apply_latest.head(50).to_markdown(index=False)}
"""
        return context
