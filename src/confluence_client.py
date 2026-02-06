"""Confluence 문서 업로드"""
import re
from atlassian import Confluence
from datetime import datetime
from .config import Config


class ConfluenceClient:
    def __init__(self):
        self.confluence = Confluence(
            url=Config.CONFLUENCE_URL,
            username=Config.CONFLUENCE_EMAIL,
            password=Config.CONFLUENCE_API_TOKEN,
        )

    def _get_or_create_year_page(self, year: int) -> str:
        """년도 페이지 가져오기 (없으면 생성)"""
        year_title = f"{year}년"
        
        # 년도 페이지 찾기
        existing = self.confluence.get_page_by_title(
            space=Config.CONFLUENCE_SPACE,
            title=year_title,
        )
        
        if existing:
            return existing["id"]
        
        # 없으면 생성 (부모 페이지 하위에)
        result = self.confluence.create_page(
            space=Config.CONFLUENCE_SPACE,
            title=year_title,
            body="<p>월간 분석 리포트 모음</p>",
            parent_id=Config.CONFLUENCE_PARENT_PAGE_ID,
        )
        print(f"   📁 {year_title} 폴더 생성됨")
        return result["id"]

    def upload_report(self, content: str, report_date: datetime = None) -> str:
        """리포트를 Confluence 페이지로 업로드
        
        구조: 부모페이지 > 년도 > 월별 리포트
        """
        if report_date is None:
            report_date = datetime.now()
        
        year = report_date.year
        month = report_date.month
        title = f"{year}년 {month}월 채용 실적 분석 리포트"
        
        # 년도 폴더 가져오기/생성
        year_page_id = self._get_or_create_year_page(year)
        
        # 기존 페이지 확인
        existing = self.confluence.get_page_by_title(
            space=Config.CONFLUENCE_SPACE,
            title=title,
        )

        body = self._markdown_to_confluence(content)

        if existing:
            # 기존 페이지 업데이트
            self.confluence.update_page(
                page_id=existing["id"],
                title=title,
                body=body,
            )
            page_id = existing["id"]
            print(f"   📝 기존 페이지 업데이트: {title}")
        else:
            # 새 페이지 생성 (년도 폴더 하위에)
            result = self.confluence.create_page(
                space=Config.CONFLUENCE_SPACE,
                title=title,
                body=body,
                parent_id=year_page_id,  # 년도 페이지 하위에 생성
            )
            page_id = result["id"]
            print(f"   📄 새 페이지 생성: {title}")

        return f"{Config.CONFLUENCE_URL}/wiki/spaces/{Config.CONFLUENCE_SPACE}/pages/{page_id}"

    def _markdown_to_confluence(self, markdown: str) -> str:
        """마크다운을 Confluence Storage Format으로 변환"""
        html = markdown

        # 코드 블록 보존 (먼저 처리)
        code_blocks = []
        def save_code_block(match):
            code_blocks.append(match.group(0))
            return f"{{CODE_BLOCK_{len(code_blocks)-1}}}"
        
        html = re.sub(r"```[\s\S]*?```", save_code_block, html)

        # 헤더 변환
        html = re.sub(r"^### (.+)$", r"<h3>\1</h3>", html, flags=re.MULTILINE)
        html = re.sub(r"^## (.+)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
        html = re.sub(r"^# (.+)$", r"<h1>\1</h1>", html, flags=re.MULTILINE)

        # 굵은 글씨
        html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)

        # 이탤릭
        html = re.sub(r"\*(.+?)\*", r"<em>\1</em>", html)

        # 테이블 변환 (간단 버전)
        lines = html.split("\n")
        in_table = False
        new_lines = []
        
        for line in lines:
            if line.strip().startswith("|") and line.strip().endswith("|"):
                if not in_table:
                    new_lines.append("<table>")
                    in_table = True
                
                # 구분선 스킵
                if re.match(r"^\|[\s\-:|]+\|$", line.strip()):
                    continue
                
                cells = [c.strip() for c in line.strip().split("|")[1:-1]]
                row = "<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>"
                new_lines.append(row)
            else:
                if in_table:
                    new_lines.append("</table>")
                    in_table = False
                new_lines.append(line)
        
        if in_table:
            new_lines.append("</table>")
        
        html = "\n".join(new_lines)

        # 코드 블록 복원
        for i, block in enumerate(code_blocks):
            code_content = block.strip("`").strip()
            if code_content.startswith("\n"):
                code_content = code_content[1:]
            html = html.replace(f"{{CODE_BLOCK_{i}}}", f"<pre>{code_content}</pre>")

        # 줄바꿈
        html = html.replace("\n\n", "</p><p>")
        html = f"<p>{html}</p>"

        return html
