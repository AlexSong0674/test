# -*- coding: utf-8 -*-
"""GPS 여행배지앱 기획서 → DOCX 생성 스크립트"""

from docx import Document
from docx.shared import Pt, RGBColor, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

OUTPUT_PATH = r"C:\Users\송 하 준\Documents\알토대학원\수업과제\벤처 스타트업\기획서\GPS_여행배지앱_기획서.docx"

# ── 헬퍼 함수 ─────────────────────────────────────────────────────────────

def set_font(run, name="맑은 고딕", size=None, bold=False, color=None, italic=False):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    if size:
        run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)

def para_spacing(para, before=0, after=6, line=None):
    pf = para.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    if line:
        pf.line_spacing = Pt(line)

def set_cell_bg(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)

def set_cell_borders(cell, color="CCCCCC"):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    for side in ["top", "left", "bottom", "right"]:
        border = OxmlElement(f"w:{side}")
        border.set(qn("w:val"), "single")
        border.set(qn("w:sz"), "4")
        border.set(qn("w:space"), "0")
        border.set(qn("w:color"), color)
        tcBorders.append(border)
    tcPr.append(tcBorders)

def add_cell_text(cell, text, bold=False, size=9.5, color=None, align=None):
    para = cell.paragraphs[0]
    para.clear()
    if align == "center":
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run(text)
    set_font(run, size=size, bold=bold, color=color)
    para.paragraph_format.space_before = Pt(2)
    para.paragraph_format.space_after = Pt(2)

def set_para_shading(para, hex_color):
    pPr = para._element.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    pPr.append(shd)

def add_para_border(para, color="CCCCCC"):
    pPr = para._element.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    for side in ["top", "left", "bottom", "right"]:
        b = OxmlElement(f"w:{side}")
        b.set(qn("w:val"), "single")
        b.set(qn("w:sz"), "4")
        b.set(qn("w:space"), "4")
        b.set(qn("w:color"), color)
        pBdr.append(b)
    pPr.append(pBdr)

def add_hr(doc, color="3366CC"):
    para = doc.add_paragraph()
    pPr = para._element.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bot = OxmlElement("w:bottom")
    bot.set(qn("w:val"), "single")
    bot.set(qn("w:sz"), "6")
    bot.set(qn("w:space"), "1")
    bot.set(qn("w:color"), color)
    pBdr.append(bot)
    pPr.append(pBdr)
    para.paragraph_format.space_before = Pt(0)
    para.paragraph_format.space_after = Pt(4)

def add_heading1(doc, text):
    para = doc.add_paragraph()
    para.style = doc.styles["Heading 1"]
    run = para.add_run(text)
    set_font(run, size=15, bold=True, color=(31, 73, 125))
    para_spacing(para, before=14, after=6)
    return para

def add_heading2(doc, text):
    para = doc.add_paragraph()
    para.style = doc.styles["Heading 2"]
    run = para.add_run(text)
    set_font(run, size=12, bold=True, color=(31, 73, 125))
    para_spacing(para, before=10, after=4)
    return para

def add_heading3(doc, text):
    para = doc.add_paragraph()
    para.style = doc.styles["Heading 3"]
    run = para.add_run(text)
    set_font(run, size=10.5, bold=True, color=(68, 114, 196))
    para_spacing(para, before=8, after=3)
    return para

def add_body(doc, text, bold_parts=None):
    para = doc.add_paragraph()
    # 볼드 처리: **text** 파싱
    parts = parse_bold(text)
    for part_text, is_bold in parts:
        run = para.add_run(part_text)
        set_font(run, size=10, bold=is_bold)
    para_spacing(para, before=0, after=4)
    return para

def parse_bold(text):
    """**bold** 마크다운을 (text, is_bold) 튜플 리스트로 파싱"""
    import re
    result = []
    pattern = re.compile(r'\*\*(.+?)\*\*')
    last = 0
    for m in pattern.finditer(text):
        if m.start() > last:
            result.append((text[last:m.start()], False))
        result.append((m.group(1), True))
        last = m.end()
    if last < len(text):
        result.append((text[last:], False))
    if not result:
        result = [(text, False)]
    return result

def add_bullet(doc, text, level=0, bold_parts=True):
    para = doc.add_paragraph(style="List Bullet")
    parts = parse_bold(text)
    for part_text, is_bold in parts:
        run = para.add_run(part_text)
        set_font(run, size=10, bold=is_bold)
    para.paragraph_format.left_indent = Cm(0.5 + level * 0.5)
    para_spacing(para, before=0, after=2)
    return para

def add_numbered(doc, text, num):
    para = doc.add_paragraph()
    run_num = para.add_run(f"{num}. ")
    set_font(run_num, size=10, bold=False)
    parts = parse_bold(text)
    for part_text, is_bold in parts:
        run = para.add_run(part_text)
        set_font(run, size=10, bold=is_bold)
    para.paragraph_format.left_indent = Cm(0.5)
    para_spacing(para, before=0, after=2)
    return para

def add_quote(doc, text):
    para = doc.add_paragraph()
    para.paragraph_format.left_indent = Cm(0.8)
    pPr = para._element.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single")
    left.set(qn("w:sz"), "12")
    left.set(qn("w:space"), "4")
    left.set(qn("w:color"), "3366CC")
    pBdr.append(left)
    pPr.append(pBdr)
    set_para_shading(para, "EEF4FF")
    run = para.add_run(text)
    set_font(run, size=10, italic=True, color=(44, 62, 100))
    para_spacing(para, before=4, after=4)
    return para

def add_code_block(doc, text):
    lines = text.strip().split("\n")
    for i, line in enumerate(lines):
        para = doc.add_paragraph()
        set_para_shading(para, "F4F4F4")
        add_para_border(para, "CCCCCC")
        run = para.add_run(line if line else " ")
        run.font.name = "Courier New"
        run._element.rPr.rFonts.set(qn("w:eastAsia"), "맑은 고딕")
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(51, 51, 51)
        para.paragraph_format.space_before = Pt(0)
        para.paragraph_format.space_after = Pt(0)
        para.paragraph_format.left_indent = Cm(0.3)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_checkbox_list(doc, items):
    for item in items:
        para = doc.add_paragraph()
        run = para.add_run("☐  " + item)
        set_font(run, size=10)
        para.paragraph_format.left_indent = Cm(0.5)
        para_spacing(para, before=0, after=2)


# ── 표 생성 헬퍼 ────────────────────────────────────────────────────────────

def make_table(doc, headers, rows, col_widths, header_bg="1F497D", row_alt_bg="EEF4FF"):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    table.style = "Table Grid"

    # 헤더 행
    hdr_row = table.rows[0]
    for i, (cell, hdr) in enumerate(zip(hdr_row.cells, headers)):
        set_cell_bg(cell, header_bg)
        set_cell_borders(cell, "AAAAAA")
        para = cell.paragraphs[0]
        para.clear()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.add_run(hdr)
        set_font(run, size=9.5, bold=True, color=(255, 255, 255))
        para.paragraph_format.space_before = Pt(3)
        para.paragraph_format.space_after = Pt(3)
        cell.width = Cm(col_widths[i])

    # 데이터 행
    for r_idx, row_data in enumerate(rows):
        row = table.add_row()
        bg = row_alt_bg if r_idx % 2 == 0 else "FFFFFF"
        for i, (cell, val) in enumerate(zip(row.cells, row_data)):
            set_cell_bg(cell, bg)
            set_cell_borders(cell, "CCCCCC")
            is_bold = val.startswith("**") and val.endswith("**")
            clean = val.strip("*")
            add_cell_text(cell, clean, bold=is_bold, size=9.5)
            cell.width = Cm(col_widths[i])

    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return table


# ── 문서 생성 ────────────────────────────────────────────────────────────────

def build_document():
    doc = Document()

    # 페이지 설정 (A4)
    section = doc.sections[0]
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)

    # 기본 스타일 폰트
    doc.styles["Normal"].font.name = "맑은 고딕"
    doc.styles["Normal"].font.size = Pt(10)
    doc.styles["Normal"].element.rPr.rFonts.set(qn("w:eastAsia"), "맑은 고딕")

    # ── 표지 ──────────────────────────────────────────────────────────────
    doc.add_paragraph()
    title_para = doc.add_paragraph()
    title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title_para.add_run("GPS 기반 여행지 인증 배지 앱 서비스")
    set_font(title_run, size=22, bold=True, color=(31, 73, 125))
    title_para.paragraph_format.space_after = Pt(4)

    sub_para = doc.add_paragraph()
    sub_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_run = sub_para.add_run("앱 서비스 기획서 (MVP)")
    set_font(sub_run, size=15, bold=False, color=(68, 114, 196))
    sub_para.paragraph_format.space_after = Pt(16)

    add_hr(doc)

    meta_para = doc.add_paragraph()
    meta_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    meta_run = meta_para.add_run("초안 작성일: 2026-05-09     |     작성자: 창업자 (코딩 비전공 창업가)")
    set_font(meta_run, size=9.5, color=(100, 100, 100), italic=True)
    meta_para.paragraph_format.space_after = Pt(20)

    doc.add_page_break()

    # ── 목차 (수동) ────────────────────────────────────────────────────────
    add_heading1(doc, "목  차")
    toc_items = [
        "1. 서비스 개요",
        "2. 핵심 가치 제안",
        "3. 사용자 여정",
        "4. 기능 명세 (MVP)",
        "5. 레벨 및 배지 시스템",
        "6. 수익 모델 로드맵",
        "7. 기술 스택 검토",
        "8. 지도 라이브러리 비교",
        "9. 단계별 확장 전략",
        "10. 리스크 및 대응 방안",
        "부록 A. MVP 개발 체크리스트",
        "부록 B. 주요 지표 (KPI)",
    ]
    for item in toc_items:
        p = doc.add_paragraph()
        run = p.add_run(item)
        set_font(run, size=10.5)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.left_indent = Cm(0.5)
    doc.add_page_break()

    # ══════════════════════════════════════════════════════════════════════
    # 1. 서비스 개요
    # ══════════════════════════════════════════════════════════════════════
    add_heading1(doc, "1. 서비스 개요")
    add_hr(doc)

    add_heading2(doc, "1.1 서비스 명 (가칭)")
    p = doc.add_paragraph()
    for txt, bold in [("StampGo", True), ("  (또는 ", False), ("배지로", True), (" / ", False), ("TripStamp", True), (")", False)]:
        r = p.add_run(txt)
        set_font(r, size=10, bold=bold)
    para_spacing(p, after=6)

    add_heading2(doc, "1.2 한 줄 정의")
    add_quote(doc, "GPS 기반으로 여행지를 방문하면 자동으로 인증 배지를 획득하는 게이미피케이션 여행 앱")

    add_heading2(doc, "1.3 서비스 배경")
    for item in [
        "국내 여행 인구 증가 및 '인증' 문화 확산 (SNS 체크인, 스탬프 투어 유행)",
        "기존 종이 스탬프 투어의 디지털 전환 수요",
        "방문 기록을 게임처럼 수집하는 재미 요소에 대한 높은 수요",
        "외국인 관광객의 한국 여행 경험 디지털화 필요성",
    ]:
        add_bullet(doc, item)

    add_heading2(doc, "1.4 타겟 사용자")
    make_table(doc,
        headers=["단계", "주요 타겟"],
        rows=[
            ["MVP", "국내 여행을 즐기는 20~40대 한국인"],
            ["확장 1단계", "국내 여행 마니아, 스탬프 투어 팬"],
            ["확장 2단계", "한국을 방문하는 외국인 관광객"],
            ["장기", "해외 여행지 도전을 원하는 한국인"],
        ],
        col_widths=[4, 12],
    )

    # ══════════════════════════════════════════════════════════════════════
    # 2. 핵심 가치 제안
    # ══════════════════════════════════════════════════════════════════════
    add_heading1(doc, "2. 핵심 가치 제안")
    add_hr(doc)

    add_quote(doc, '"발걸음이 기록이 되고, 기록이 배지가 된다"')

    for item in [
        "**여행자**: 내가 간 곳을 증명하고, 수집하는 재미",
        "**경쟁 요소**: 랭킹과 레벨로 다른 여행자와 겨루는 성취감",
        "**발견 요소**: 미수집 배지가 새로운 여행지로 유도",
        "**희소성**: 프리미어 배지로 차별화된 소장 가치",
    ]:
        add_bullet(doc, item)

    # ══════════════════════════════════════════════════════════════════════
    # 3. 사용자 여정
    # ══════════════════════════════════════════════════════════════════════
    add_heading1(doc, "3. 사용자 여정")
    add_hr(doc)

    add_heading2(doc, "3.1 핵심 원칙")
    add_bullet(doc, "**앱 활성화 시에만 GPS 인식 및 배지 획득** 작동")
    add_bullet(doc, "사용자가 원할 때만 동작 → 배터리·프라이버시 부담 최소화", level=1)
    add_bullet(doc, "방해받고 싶지 않은 사용자도 수용 (향후 구독 혜택으로 연계 가능)", level=1)

    add_heading2(doc, "3.2 기본 플로우")
    add_code_block(doc,
        "앱 실행 → 홈 화면(지도/배지 현황) → [여행 모드 ON]\n"
        "    → GPS 활성화 → 반경 내 여행지 감지 (50~200m 기준)\n"
        "    → 방문 인증 팝업 → 배지 획득 애니메이션\n"
        "    → XP 적립 → 레벨/칭호 업데이트 확인\n"
        "    → [여행 모드 OFF]"
    )

    add_heading2(doc, "3.3 신규 사용자 온보딩")
    for i, item in enumerate([
        "회원가입 (SNS 간편 로그인)",
        "닉네임 및 프로필 설정",
        "주변 배지 획득 가능 장소 지도 미리 보기 (흥미 유발)",
        "튜토리얼: 첫 배지 획득 유도 (가까운 명소 1곳)",
        "홈 화면으로 전환, 전국 배지 지도 확인",
    ], 1):
        add_numbered(doc, item, i)

    add_heading2(doc, "3.4 미수집 배지 방문 유도 알고리즘")
    add_body(doc, "미수집 배지는 단순 리스트 노출이 아닌 **맥락 기반 추천**으로 방문 동기를 만든다.")
    for item in [
        '**근접 유도**: 현재 위치에서 반경 N km 내 미수집 배지 하이라이트',
        '**연계 유도**: 이미 획득한 배지와 같은 지역/테마의 미수집 배지 추천',
        '**희소성 유도**: "이 배지를 가진 사람은 전체의 5%입니다" 등 희귀도 표시',
        '**시즌 유도**: 특정 기간(계절, 축제 시즌) 한정 획득 가능 배지 알림',
        '**스트릭 유도**: 연속 방문 일수/횟수 유지 동기 부여',
    ]:
        add_bullet(doc, item)

    # ══════════════════════════════════════════════════════════════════════
    # 4. 기능 명세 (MVP)
    # ══════════════════════════════════════════════════════════════════════
    add_heading1(doc, "4. 기능 명세 (MVP)")
    add_hr(doc)

    add_heading2(doc, "4.1 MVP 범위 (우선 구현)")
    make_table(doc,
        headers=["기능", "설명", "우선순위"],
        rows=[
            ["회원가입/로그인", "SNS 간편 로그인 (카카오, 구글)", "P0"],
            ["GPS 인식", "앱 활성화 시 위치 감지", "P0"],
            ["여행지 DB", "초기 주요 국내 명소 50~100곳", "P0"],
            ["배지 획득", "방문 인증 시 자동 배지 부여", "P0"],
            ["배지 컬렉션", "획득/미획득 배지 목록 및 지도", "P0"],
            ["XP 및 레벨", "배지 획득 시 XP 적립, 레벨 표시", "P0"],
            ["프로필", "레벨, 칭호, 배지 수 표시", "P1"],
            ["랭킹", "레벨/배지 수 기준 전체·지역 랭킹", "P1"],
            ["미수집 배지 추천", "근접 및 연계 기반 추천", "P1"],
            ["푸시 알림", "근처 미수집 배지 알림 (선택)", "P2"],
            ["소셜 공유", "배지 획득 시 SNS 공유 기능", "P2"],
        ],
        col_widths=[4, 9.5, 2.5],
    )

    add_heading2(doc, "4.2 MVP 이후 단계별 추가 기능")
    make_table(doc,
        headers=["단계", "기능"],
        rows=[
            ["V1.1", "칭호 시스템, 시즌 한정 배지"],
            ["V1.2", "구독 모델, 프리미어 배지"],
            ["V1.3", "여행 친구 팔로우, 방문 기록 타임라인"],
            ["V2.0", "외국인 지원 (영어/일어/중국어), 해외 배지"],
        ],
        col_widths=[3, 13],
    )

    doc.add_page_break()

    # ══════════════════════════════════════════════════════════════════════
    # 5. 레벨 및 배지 시스템
    # ══════════════════════════════════════════════════════════════════════
    add_heading1(doc, "5. 레벨 및 배지 시스템")
    add_hr(doc)

    add_heading2(doc, "5.1 레벨 시스템")
    for item in [
        "**레벨 범위**: 1 ~ 99",
        "**경험치(XP) 획득**: 배지 획득, 미션 완료, 연속 방문 등",
        "**레벨업 필요 XP 공식**: 레벨이 오를수록 기하급수적으로 증가",
    ]:
        add_bullet(doc, item)

    add_code_block(doc,
        "필요 XP(Lv n) = 100 × n^1.6   (소수점 버림)\n"
        "\n"
        "예시:\n"
        "  Lv  1 →  2:     100 XP\n"
        "  Lv  5 →  6:     952 XP\n"
        "  Lv 10 → 11:   2,512 XP\n"
        "  Lv 20 → 21:   8,103 XP\n"
        "  Lv 50 → 51:  39,821 XP\n"
        "  Lv 98 → 99: 146,779 XP"
    )

    add_body(doc, "배지 등급별 XP 지급량:")
    make_table(doc,
        headers=["배지 등급", "지급 XP"],
        rows=[
            ["일반 (Common)", "50 XP"],
            ["희귀 (Rare)", "150 XP"],
            ["특별 (Special)", "300 XP"],
            ["프리미어 (Premier, 구독 전용)", "500 XP"],
            ["시즌 한정", "200~400 XP"],
        ],
        col_widths=[9, 7],
    )

    add_heading2(doc, "5.2 칭호(타이틀) 시스템")
    add_body(doc, "칭호는 레벨 구간 외에 **특정 조건**을 달성해야 부여되는 방식으로 이중 레이어 구성:")
    make_table(doc,
        headers=["칭호", "부여 조건", "설명"],
        rows=[
            ["동네 탐험가", "배지 5개 달성", "시작하는 여행자"],
            ["국내 여행러", "3개 광역시·도 배지 보유", "지역 확장 중"],
            ["지도 마니아", "배지 30개 달성", "수집에 빠진 사람"],
            ["전국 방랑자", "모든 광역시·도 1개 이상 배지 보유", "전국 답파"],
            ["산악인", "국립공원 배지 10개 이상", "자연을 사랑하는 여행자"],
            ["도시 헌터", "5대 광역시 배지 완전 수집", "도시 여행 전문가"],
            ["고수 여행자", "Lv 50 달성", "중급 여행자"],
            ["전설의 여행자", "Lv 99 달성 + 배지 200개 이상", "최고 등급 칭호"],
            ["시즌 챔피언", "시즌 랭킹 1위", "기간 한정 칭호"],
            ["선구자", "MVP 초기 이용자 (베타 기간 내 가입)", "명예 칭호"],
        ],
        col_widths=[4, 7, 5],
    )
    add_quote(doc, "칭호는 프로필에 1개만 장착 가능 → 희소성과 자랑 욕구 자극")

    add_heading2(doc, "5.3 배지 등급 체계")
    add_code_block(doc,
        "[일반 배지]    → 누구나 방문 시 획득\n"
        "[희귀 배지]    → 특정 조건(첫 100명 방문 등) 또는 저명도 장소\n"
        "[특별 배지]    → 시즌·이벤트 한정\n"
        "[프리미어 배지] → 구독자만 획득 가능 (동일 장소라도 고급 디자인 배지)"
    )
    for item in [
        "미수집 배지는 지도 상에서 **실루엣(흐림 처리)**로 표시 → 수집 욕구 자극",
        '프리미어 배지는 미구독 사용자에게 잠금 표시 + "구독하면 획득 가능" 안내',
    ]:
        add_bullet(doc, item)

    doc.add_page_break()

    # ══════════════════════════════════════════════════════════════════════
    # 6. 수익 모델 로드맵
    # ══════════════════════════════════════════════════════════════════════
    add_heading1(doc, "6. 수익 모델 로드맵")
    add_hr(doc)

    add_heading2(doc, "Phase 1 — 사용자 기반 확보 (0~6개월)")
    for item in [
        "**무료 서비스** 운영, 일반 배지 전체 무료",
        "목표: MAU 1만 명, 배지 수집 데이터 축적",
        "수익: 없음 (투자 또는 자비)",
    ]:
        add_bullet(doc, item)

    add_heading2(doc, "Phase 2 — 구독 모델 도입 (6~12개월)")
    add_bullet(doc, "**프리미엄 구독** (월 2,900원 / 연 24,900원)")
    for item in [
        "프리미어 배지 획득 권한",
        "광고 제거",
        "고급 통계 (방문 히스토리, 이동 거리 등)",
        "신규 배지 사전 오픈 혜택",
    ]:
        add_bullet(doc, item, level=1)

    add_heading2(doc, "Phase 3 — 굿즈 및 배지 판매 (12~24개월)")
    for item in [
        "**한정판 실물 굿즈**: 배지 디자인 기반 스티커팩, 엽서, 아크릴 키링",
        "**디지털 배지 컬렉션**: 특별 이벤트 배지 유료 판매 (NFT 미적용, 앱 내 구매)",
        "**지역 관광청·브랜드 협업 배지**: B2B 수익 (관광 마케팅 예산 활용)",
    ]:
        add_bullet(doc, item)

    add_heading2(doc, "Phase 4 — 여행 콘텐츠 플랫폼 (24개월~)")
    for item in [
        "여행 코스 추천 및 여행 정보 연동",
        "여행 크리에이터 콘텐츠 연동 (배지 장소 기반)",
        "제휴 숙소·식당 예약 연결 (커미션 수익)",
    ]:
        add_bullet(doc, item)

    add_heading2(doc, "Phase 5 — 여행테크 앱 전환 (장기)")
    for item in [
        "외국인 대상 한국 여행 가이드 앱으로 확장",
        "해외 여행지 배지 확대 (일본, 동남아, 유럽 등)",
        "여행 데이터 기반 광고·인사이트 서비스",
    ]:
        add_bullet(doc, item)

    doc.add_page_break()

    # ══════════════════════════════════════════════════════════════════════
    # 7. 기술 스택 검토
    # ══════════════════════════════════════════════════════════════════════
    add_heading1(doc, "7. 기술 스택 검토")
    add_hr(doc)

    add_heading2(doc, "7.1 MVP 빌드 도구 비교")
    make_table(doc,
        headers=["도구", "장점", "단점", "추천 용도"],
        rows=[
            ["Lovable", "AI 코드 생성, 웹앱 UI 빠른 프로토타이핑, Supabase 연동 용이", "모바일 앱 네이티브 기능 제한, GPS 정밀도 한계", "웹 기반 MVP, 관리자 대시보드"],
            ["Replit", "즉시 실행 환경, 백엔드 API 빠른 구축, 협업 용이", "UI/UX 완성도 낮음, 복잡한 앱 관리 어려움", "백엔드 API 서버, 프로토타입"],
            ["FlutterFlow ⭐", "네이티브 앱(iOS/Android) 동시 생성, GPS 디바이스 기능 직접 지원, 노코드 수준 UI", "러닝커브 존재, 복잡한 로직은 Dart 직접 작성 필요", "GPS 앱 MVP에 가장 적합"],
            ["Bubble", "강력한 노코드 웹앱, 복잡한 로직 구현 가능", "웹앱 전용, 모바일 앱 변환 품질 낮음", "웹 버전 MVP"],
            ["Glide", "스프레드시트 기반 앱 초고속 제작", "기능 제한 많음, GPS 활용 어려움", "적합하지 않음"],
        ],
        col_widths=[3.5, 5.5, 4.5, 3.5],
    )

    add_heading2(doc, "7.2 추천 기술 조합")
    add_code_block(doc,
        "[추천 스택]\n"
        "- 앱 프론트엔드:  FlutterFlow (GPS 네이티브 기능 + iOS/Android 동시 빌드)\n"
        "- 백엔드/DB:      Supabase (무료 플랜으로 MVP 가능, PostgreSQL 기반)\n"
        "- 인증:           Supabase Auth (카카오/구글 소셜 로그인)\n"
        "- 지도:           카카오맵 API (국내 MVP) → 구글맵 API (해외 확장 시)\n"
        "- 배포:           Supabase + FlutterFlow 내 직접 배포\n"
        "- 관리자 화면:    Lovable 또는 Retool로 별도 제작"
    )
    add_quote(doc, "Lovable + Replit 조합으로 시작할 경우: 웹앱(PWA)으로 먼저 MVP를 검증하고, 사용자 반응 확인 후 FlutterFlow로 네이티브 앱 전환을 권장함.")

    add_heading2(doc, "7.3 데이터베이스 설계 (핵심 테이블)")
    add_code_block(doc,
        "users           - 사용자 정보, 레벨, XP, 칭호\n"
        "locations       - 여행지 정보 (위경도, 이름, 카테고리, 반경)\n"
        "badges          - 배지 정보 (등급, 이미지, 해당 장소)\n"
        "user_badges     - 사용자-배지 획득 기록 (획득 시각, 좌표)\n"
        "xp_log          - XP 적립 이력\n"
        "seasons         - 시즌 배지 기간 관리\n"
        "subscriptions   - 구독 상태 관리"
    )

    # ══════════════════════════════════════════════════════════════════════
    # 8. 지도 라이브러리 비교
    # ══════════════════════════════════════════════════════════════════════
    add_heading1(doc, "8. 지도 라이브러리 비교")
    add_hr(doc)

    make_table(doc,
        headers=["항목", "카카오맵", "네이버맵", "구글맵"],
        rows=[
            ["국내 지도 품질", "★★★★★", "★★★★★", "★★★★☆"],
            ["국내 POI 데이터", "매우 풍부", "매우 풍부", "다소 부족"],
            ["무료 사용량", "월 300만 건 (무료)", "월 200만 건 (무료)", "월 $200 크레딧"],
            ["SDK 지원", "iOS, Android, Web", "iOS, Android, Web", "iOS, Android, Web"],
            ["해외 지도 지원", "미지원", "미지원", "★★★★★"],
            ["국내 대중교통 연동", "우수", "우수", "보통"],
            ["개발 문서 (한국어)", "충실", "충실", "영문 중심"],
            ["Flutter 연동", "비공식 패키지", "공식 지원 약함", "공식 패키지 있음"],
        ],
        col_widths=[5, 4, 4, 4],
    )

    add_heading2(doc, "추천 전략")
    add_code_block(doc,
        "MVP (국내):     카카오맵 API\n"
        "                → 국내 여행지 POI 가장 정확, 무료 한도 넉넉, 한국어 문서 충실\n"
        "\n"
        "해외 확장 시:   구글맵 API로 전환 또는 병행\n"
        "                → 국내는 카카오, 해외는 구글로 분기 처리\n"
        "\n"
        "네이버맵 고려:  국내 한정이라면 카카오와 유사하나,\n"
        "                FlutterFlow 연동 편의성은 카카오 > 네이버"
    )

    doc.add_page_break()

    # ══════════════════════════════════════════════════════════════════════
    # 9. 단계별 확장 전략
    # ══════════════════════════════════════════════════════════════════════
    add_heading1(doc, "9. 단계별 확장 전략")
    add_hr(doc)

    add_heading2(doc, "9.1 국내 콘텐츠 확장")
    add_code_block(doc,
        "MVP 런칭:  주요 관광지 50~100곳 (5대 광역시 + 제주)\n"
        "V1.1:      전국 시군구 대표 명소 확장 (300곳+)\n"
        "V1.2:      지역 숨은 명소, 로컬 맛집·카페 연동\n"
        "V1.3:      지역 관광청 협업 공식 배지 코스 도입"
    )

    add_heading2(doc, "9.2 외국인 관광객 확장 (인바운드)")
    for item in [
        "앱 다국어 지원: 영어, 일본어, 중국어(간체/번체)",
        "외국인 인기 명소 중심 배지 재구성",
        "한국 관광공사 또는 지자체 협업 공식 파트너 배지",
        "입국 직후 공항에서 첫 배지 획득 유도 (인천공항 배지 등)",
    ]:
        add_bullet(doc, item)

    add_heading2(doc, "9.3 해외 여행지 확장 (아웃바운드)")
    for item in [
        "한국인 여행 인기 국가부터 확장: 일본 → 동남아 → 유럽",
        "현지 파트너사/로컬 크리에이터와 배지 장소 큐레이션",
        "글로벌 여행자 커뮤니티로 성장 목표",
    ]:
        add_bullet(doc, item)

    # ══════════════════════════════════════════════════════════════════════
    # 10. 리스크 및 대응 방안
    # ══════════════════════════════════════════════════════════════════════
    add_heading1(doc, "10. 리스크 및 대응 방안")
    add_hr(doc)

    make_table(doc,
        headers=["리스크", "내용", "대응 방안"],
        rows=[
            ["GPS 정확도", "실내·도심 밀집 지역 위치 오류", "인증 반경 조정(50~200m), 수동 인증 보완 옵션"],
            ["사용자 어뷰징", "GPS 조작으로 허위 방문", "방문 시간·이동 패턴 이상 감지 알고리즘, 신고 기능"],
            ["배터리 소모", "GPS 상시 사용 시 배터리 과소비", "여행 모드 ON/OFF 방식으로 사용자 선택"],
            ["콘텐츠 부족", "배지 장소 수가 적으면 조기 이탈", "MVP 전 최소 100곳 DB 준비, 단계적 업데이트 공지"],
            ["경쟁 서비스", "유사 서비스 출현", "배지 디자인 품질, 커뮤니티, B2B 파트너십으로 차별화"],
            ["개인정보", "위치 정보 수집 민감성", "위치는 여행 모드 ON 시에만 수집, 명확한 동의 UI"],
        ],
        col_widths=[3.5, 5.5, 7],
    )

    doc.add_page_break()

    # ══════════════════════════════════════════════════════════════════════
    # 부록 A
    # ══════════════════════════════════════════════════════════════════════
    add_heading1(doc, "부록 A. MVP 개발 체크리스트")
    add_hr(doc)

    add_checkbox_list(doc, [
        "서비스명 및 도메인 확정",
        "Supabase 프로젝트 생성 및 DB 스키마 설계",
        "FlutterFlow 프로젝트 생성 및 Supabase 연동",
        "카카오맵 API 키 발급 및 연동",
        "회원가입/로그인 (카카오 소셜 로그인) 구현",
        "초기 여행지 DB 50곳 입력 (위경도 포함)",
        "배지 디자인 초안 제작 (Canva 또는 외주)",
        "GPS 여행 모드 ON/OFF 기능 구현",
        "방문 감지 → 배지 획득 로직 구현",
        "배지 컬렉션 화면 구현",
        "XP 및 레벨 표시 구현",
        "테스트 (실외 GPS 현장 테스트 필수)",
        "TestFlight(iOS) / 내부 테스트(Android) 배포",
        "베타 테스터 10~20명 피드백 수집",
    ])

    # ══════════════════════════════════════════════════════════════════════
    # 부록 B
    # ══════════════════════════════════════════════════════════════════════
    add_heading1(doc, "부록 B. 주요 지표 (KPI)")
    add_hr(doc)

    make_table(doc,
        headers=["단계", "목표 지표"],
        rows=[
            ["MVP 런칭 1개월", "가입자 500명, DAU 100명, 1인당 평균 배지 3개"],
            ["3개월", "MAU 3,000명, 리텐션 D30 20% 이상"],
            ["6개월", "MAU 10,000명, 구독 전환율 5%"],
            ["12개월", "MAU 30,000명, MRR 500만 원"],
        ],
        col_widths=[4.5, 11.5],
    )

    # 맺음말
    doc.add_paragraph()
    closing = doc.add_paragraph()
    closing.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = closing.add_run("이 기획서는 초기 기획 단계의 내부 문서이며, 시장 반응에 따라 지속적으로 업데이트됩니다.")
    set_font(run, size=9.5, italic=True, color=(120, 120, 120))

    doc.save(OUTPUT_PATH)
    print(f"✅ DOCX 저장 완료: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_document()
