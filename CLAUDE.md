# Voyna (보이나) 프로젝트 — CLAUDE.md

> 알토대학원 벤처 스타트업 수업 과제  
> 작성일: 2026-05-09 / 개정: 2026-05-12 (v2.0) / 2026-05-15 (산출물 미러링 규칙 추가)  
> GitHub: https://github.com/AlexSong0674/test

---

## ⚠️ 작업 규칙 (꼭 지킬 것)

### 산출물 자동 미러링 (사용자 편의 — 항상 적용)

이 프로젝트는 git worktree 환경(`.claude\worktrees\<id>\`)에서 작업되어,
사용자는 메인 `기획서\` 폴더만 탐색기에서 접근합니다.

**규칙:** 사용자가 직접 열어볼 만한 파일(문서·이미지·발표 자료 등)을 worktree에 생성/수정한 직후,
**메인 `기획서\` 폴더에도 같은 이름으로 복사**한다.

대상 (확장자 기준):
- `.docx`, `.pdf`, `.pptx`, `.xlsx`, `.png`, `.jpg`, `.svg`, `.html`, `.md` (요약본/슬라이드/배포물)

대상 외 (복사 안 함):
- 소스 코드 (`.ts`, `.js`, `.css` 등) — Voyna-Demo 리포 별도 관리
- spec/plan md (`docs/superpowers/...`) — git 히스토리로 보존, 사용자가 메인 폴더에서 안 열어봄
- `.git`, `node_modules`, `dist`, 임시 파일

미러링 명령 예시:
```bash
cp "<worktree>/Voyna_새파일.pdf" "/c/Users/송 하 준/Documents/알토대학원/수업과제/벤처 스타트업/기획서/"
```

미러링 후 사용자에게 "메인 기획서 폴더에도 복사됨"을 한 줄로 알려준다.

---

## 프로젝트 한 줄 요약

**Voyna** (보이나) — GPS 기반으로 여행지를 방문하면 자동으로 인증 배지를 획득하는 게이미피케이션 여행 앱.  
*Voyage + Navigation* 합성어 + 한국어 "보이나"의 이중 의미.  
**"발걸음이 기록이 되고, 기록이 추억이 된다"**

---

## 디렉토리 구조

```
기획서/
├── CLAUDE.md                        ← 이 파일 (프로젝트 컨텍스트)
├── GPS_여행배지앱_기획서.md          ← 메인 기획서 (마크다운)
├── GPS_여행배지앱_기획서.docx        ← 기획서 Word 버전
├── GPS_여행배지앱_기획서.pdf         ← 기획서 PDF 버전
├── StampGo_시각자료.html             ← 앱 화면 와이어프레임 + 다이어그램 (브라우저로 열기)
├── index.html                       ← 루트 랜딩 페이지 (GitHub Pages용)
├── generate_docx.py                 ← docx 생성 스크립트
├── mock-site/
│   └── index.html                   ← StampGo 마케팅 랜딩 페이지 (mock 사이트)
└── .claude/
    ├── launch.json                  ← 로컬 미리보기 서버 설정 (python http.server:3456)
    └── settings.local.json
```

---

## 서비스 개요

### 타겟 사용자
| 단계 | 주요 타겟 |
|------|-----------|
| MVP | 국내 여행을 즐기는 20~40대 한국인 |
| 확장 1단계 | 국내 여행 마니아, 스탬프 투어 팬 |
| 확장 2단계 | 한국을 방문하는 외국인 관광객 |
| 장기 | 해외 여행지 도전을 원하는 한국인 |

### 핵심 기능 (MVP)
- **GPS 자동 인증** — 여행 모드 ON 시 반경 50~200m 이내 명소 자동 감지
- **배지 수집** — 일반 / 희귀 / 특별 / 프리미어 4등급
- **자동 + 확인형 배지 획득 이원화** — 일반은 자동, 희귀·특별은 "확인" 팝업 후 획득 (소장 가치 강화)
- **XP & 레벨** — 배지 획득 시 경험치 적립, Lv1~99
- **칭호 시스템** — 조건 달성 시 부여 (동네 탐험가 → 전설의 여행자)
- **랭킹** — 전체 / 지역 / 친구 랭킹
- **맥락 기반 추천** — 근접·연계·희소성·시즌 기반 미수집 배지 유도

### 앱 화면 구성 (4 탭)
1. **홈** — 본인 레벨·칭호·최근 배지·다음 도전 카드
2. **탐험 맵** — 현재 위치 + 주변 배지 (네이버맵/카카오맵)
3. **배지** — 종류별·지역별 컬렉션 + 여행 정보
4. **더보기** — 이벤트, 미션, 설정

---

## 기술 스택 (MVP 권장)

| 레이어 | 도구 | 비고 |
|--------|------|------|
| 앱 프론트엔드 | **FlutterFlow** | iOS/Android 동시 빌드, 노코드 UI |
| 백엔드/DB | **Supabase** (PostgreSQL) | 무료 플랜으로 MVP 가능 |
| 인증 | Supabase Auth | 카카오 / 구글 소셜 로그인 |
| 지도 (MVP) | **카카오맵 API** ⭐ | FlutterFlow 연동 우선 / 월 300만 건 무료 |
| 지도 (V1.1+) | **네이버맵 API** | 사용자 친숙도 최고, MVP 검증 후 추가 |
| 지도 (해외) | 구글맵 API | 해외 확장 시 전환 |
| 푸시 알림 | FCM (Firebase) | 근처 배지 알림 |
| 관리자 화면 | Lovable / Retool | 배지·장소 관리 대시보드 |

### 핵심 DB 테이블

```
users           - id, nickname, level, xp, title, created_at
locations       - id, name, lat, lng, radius, category
badges          - id, location_id, grade, xp_reward, is_premium
user_badges     - user_id, badge_id, obtained_at, lat, lng
xp_log          - user_id, amount, reason, created_at
seasons         - id, name, start_at, end_at
subscriptions   - user_id, plan, expires_at
```

---

## 배지 & 레벨 시스템

### 배지 등급
| 등급 | 조건 | XP |
|------|------|----|
| 일반 (Common) | 누구나 방문 시 | +50 XP |
| 희귀 (Rare) | 첫 100명 / 저명도 장소 | +150 XP |
| 특별 (Special) | 시즌·이벤트 한정 | +200~400 XP |
| 프리미어 (Premier) | 구독자 전용 | +500 XP |

### 레벨업 XP 공식
```
필요 XP(Lv n) = 100 × n^1.6  (소수점 버림)
예: Lv1→2: 100XP / Lv10→11: 2,512XP / Lv50→51: 39,821XP
```

### 주요 칭호
| 칭호 | 조건 |
|------|------|
| 동네 탐험가 | 배지 5개 |
| 국내 여행러 | 3개 광역시·도 배지 보유 |
| 지도 마니아 | 배지 30개 |
| 전국 방랑자 | 모든 광역시·도 1개 이상 |
| 산악인 | 국립공원 배지 10개 이상 |
| 전설의 여행자 | Lv99 + 배지 200개 이상 |

---

## 수익 모델 로드맵

| Phase | 기간 | 목표 | 수익 |
|-------|------|------|------|
| 1 | 0~4개월 | MAU 3,000 | 없음 (사용자 확보) |
| **1.5** | **4~6개월** | **광고 시범 도입** | **네이티브 광고 (월 50~150만 원)** |
| 2 | 6~12개월 | 구독 전환율 5% | Voyna+ 월 2,900원 / 연 24,900원 (광고 제거) |
| 3 | 12~24개월 | MRR 500만 원 | 굿즈 + B2B 가맹 배지 + 관광청 협업 |
| 4 | 24개월~ | 글로벌 진출 | 인바운드 + 예약 커미션 |
| 5 | 장기 | 여행테크 플랫폼 | 데이터 기반 광고·인사이트 |

## 경쟁사 (블루오션)
직접 경쟁사 없음. 간접 영감 사례:
- **포켓몬GO**: GPS+수집 게임화 (게임 전용)
- **트랭글**: 등산 GPS 인증 (등산 한정)
- **대항해시대**: 탐험 RPG (가상 세계)
- **Foursquare/Swarm**: 위치 체크인 (UX 노후)
- **티켓플레이스 도장투어**: 단발성 이벤트

→ Voyna 우위: 여행 전체 게임화 + 자동/확인 이원화 + B2B·글로벌 확장성

---

## KPI 목표

| 시점 | 지표 |
|------|------|
| MVP 1개월 | 가입자 500명, DAU 100명, 1인당 배지 3개 |
| 3개월 | MAU 3,000명, D30 리텐션 20% |
| 6개월 | MAU 10,000명, 구독 전환율 5% |
| 12개월 | MAU 30,000명, MRR 500만 원 |

---

## 지금까지 만든 산출물

| 파일 | 설명 |
|------|------|
| `GPS_여행배지앱_기획서.md` | 전체 기획서 (서비스 개요·기능명세·기술스택·리스크 등) |
| `GPS_여행배지앱_기획서.docx/.pdf` | 제출용 문서 |
| `StampGo_시각자료.html` | 앱 화면 와이어프레임 5종 + 사용자 흐름 다이어그램 + 아키텍처 + 배지 시스템 + 로드맵 + 기획서 비교표 |
| `index.html` / `mock-site/index.html` | StampGo 마케팅 랜딩 페이지 (Hero·기능·사용법·배지·칭호·로드맵·CTA·Footer) |

---

## 로컬 미리보기 실행

```bash
# mock 사이트 로컬 서버 (python 필요)
python -m http.server 3456 --directory mock-site
# → http://localhost:3456
```

또는 Claude Code에서 `preview_start "stampgo-mock"` 으로 자동 실행.

---

## Git 저장소

- **Remote:** https://github.com/AlexSong0674/test
- **Branch:** main
- **커밋 히스토리:**
  1. `Initial commit` — 기획서·시각자료·docx·pdf·generate_docx.py
  2. `Add StampGo mock landing site and preview config` — mock-site/index.html + .claude/launch.json
  3. `Add index.html to root for GitHub Pages` — GitHub Pages 루트 배포용

### GitHub Pages 활성화 방법
1. 저장소 → Settings → Pages
2. Source: `Deploy from a branch` → `main` / `/ (root)`
3. 저장 후 `https://alexsong0674.github.io/test` 로 접속

---

## 다음 단계 (논의 중)

- [ ] **Voyna 도메인·상표권 등록** (voyna.app / voyna.co.kr / 키프리스 확인)
- [ ] App Store 출시를 위한 경로 결정 (FlutterFlow 우선)
- [ ] Apple Developer 계정 등록 ($99/년)
- [ ] Supabase 프로젝트 생성 및 DB 스키마 구현 (v2.0 스키마)
- [ ] 카카오맵 API 키 발급 (MVP) + 네이버맵 사전 신청 (V1.1)
- [ ] 배지 디자인 제작 (Canva 또는 외주) — 등급별 4종 + 시즌 한정
- [ ] 단위 경제 (CAC / LTV) 수치 추가
- [ ] 팀 구성 (앱 개발자·디자이너·콘텐츠 매니저)
- [ ] 위치정보사업자 신고 필요 여부 법률 검토

---

## 개발 환경 참고

- OS: Windows (bash/Node.js 없음 → Python http.server 사용)
- Python: 3.8.3 / 3.14.2 설치됨
- Git 사용자: AlexSong0674 (alexsong0674@gmail.com)
