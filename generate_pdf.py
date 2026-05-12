# -*- coding: utf-8 -*-
"""Voyna 기획서 .md → .pdf 변환 스크립트 (markdown-pdf)"""

from pathlib import Path
from markdown_pdf import MarkdownPdf, Section

BASE = Path(r"C:\Users\송 하 준\Documents\알토대학원\수업과제\벤처 스타트업\기획서")
MD = BASE / "GPS_여행배지앱_기획서.md"
PDF = BASE / "Voyna_기획서_v2.pdf"

# 한국어 폰트 + 깔끔한 스타일
CSS = """
body { font-family: "Malgun Gothic", "맑은 고딕", "Apple SD Gothic Neo", sans-serif; font-size: 10pt; line-height: 1.5; color: #1d1d1f; }
h1 { font-size: 18pt; color: #0071e3; border-bottom: 2px solid #0071e3; padding-bottom: 4px; margin-top: 18pt; }
h2 { font-size: 14pt; color: #0051a8; margin-top: 14pt; }
h3 { font-size: 12pt; color: #4472c4; margin-top: 10pt; }
h4 { font-size: 10.5pt; color: #4472c4; margin-top: 8pt; }
p { margin: 4pt 0; }
ul, ol { margin: 4pt 0; padding-left: 20pt; }
li { margin: 2pt 0; }
table { border-collapse: collapse; margin: 6pt 0; width: 100%; font-size: 9pt; }
th { background: #0071e3; color: white; padding: 5pt 8pt; text-align: left; font-weight: bold; border: 1px solid #aaa; }
td { padding: 4pt 8pt; border: 1px solid #ccc; vertical-align: top; }
tr:nth-child(even) td { background: #eef4ff; }
code { background: #f4f4f4; padding: 1pt 4pt; border-radius: 3px; font-family: "Courier New", monospace; font-size: 9pt; color: #c8102e; }
pre { background: #f4f4f4; border: 1px solid #ccc; border-radius: 4px; padding: 8pt; font-family: "Courier New", monospace; font-size: 8.5pt; line-height: 1.4; overflow-x: auto; }
pre code { background: transparent; padding: 0; color: #333; }
blockquote { border-left: 3px solid #0071e3; background: #eef4ff; padding: 6pt 10pt; margin: 6pt 0; color: #2c3e64; font-style: italic; }
hr { border: 0; border-top: 1px solid #0071e3; margin: 10pt 0; }
strong { font-weight: bold; color: #0051a8; }
em { font-style: italic; }
.cover-title { font-size: 30pt; color: #0071e3; font-weight: bold; text-align: center; margin-top: 80pt; }
.cover-sub { font-size: 14pt; color: #0051a8; text-align: center; margin-top: 4pt; }
.cover-slogan { font-size: 11pt; color: #555; font-style: italic; text-align: center; margin-top: 30pt; }
.cover-meta { font-size: 9pt; color: #888; text-align: center; margin-top: 50pt; }
"""

def main():
    pdf = MarkdownPdf(toc_level=0, optimize=True)
    pdf.meta["title"] = "Voyna (보이나) 기획서 v2.0"
    pdf.meta["author"] = "AlexSong0674"
    pdf.meta["subject"] = "GPS 기반 여행 인증 배지 앱 기획서"

    # 표지 페이지
    cover_md = """
<div class="cover-title">Voyna (보이나)</div>
<div class="cover-sub">GPS 기반 여행 인증 배지 앱</div>
<div class="cover-slogan">"발걸음이 기록이 되고, 기록이 추억이 된다"</div>
<div class="cover-meta">
초안: 2026-05-09 &nbsp;|&nbsp; 개정: 2026-05-12 (v2.0)<br>
Voyage + Navigation의 합성어, 한국어 '보이나'의 이중 의미
</div>
"""
    pdf.add_section(Section(cover_md, paper_size="A4"), user_css=CSS)

    # 본문 — TOC 내부 링크는 한국어 앵커 문제로 텍스트로만 변환
    import re
    md_text = MD.read_text(encoding="utf-8")
    # [텍스트](#anchor) → 텍스트  (내부 앵커 링크 제거)
    md_text = re.sub(r'\[([^\]]+)\]\(#[^\)]+\)', r'\1', md_text)
    pdf.add_section(Section(md_text, paper_size="A4"), user_css=CSS)

    pdf.save(str(PDF))
    print(f"PDF saved: {PDF}")

if __name__ == "__main__":
    main()
