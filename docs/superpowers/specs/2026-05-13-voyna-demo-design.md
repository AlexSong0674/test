# Voyna Demo App — 설계 명세 (Spec)

> **작성일:** 2026-05-13 (수)
> **마감:** 2026-05-15 (금) 저녁 — **3일 일정**
> **목적:** 알토대학원 벤처 스타트업 수업 발표 데모용 MVP 웹 앱
> **본 프로젝트와의 관계:** 12주 네이티브 앱 출시 일정([`docs/superpowers/plans/2026-05-12-voyna-mvp-implementation.md`](../plans/2026-05-12-voyna-mvp-implementation.md))과 **완전히 별도**. 코드 리포지토리·배포 파이프라인·이슈 트래킹 모두 분리.

---

## 1. 목표 & 비목표

### 목표 (In Scope)
- 청중 앞에서 시연 가능한 **반응형 웹 데모** (스마트폰 브라우저 + 빔프로젝터 양쪽 커버)
- 모바일 브라우저로 실기기 시연, 노트북 화면으로 시나리오 시연 둘 다 지원
- Voyna 브랜드의 핵심 게이미피케이션 UX(자동 배지 획득·레벨업·칭호) 체험 가능
- 정식 출시 전 사용자·교수·심사위원에게 "이 앱이 어떤 경험을 줄지" 직관적으로 전달
- 본 프로젝트 12주 plan과 자원·코드가 충돌하지 않도록 별도 리포지토리(`AlexSong0674/Voyna-Demo`)에서 운영

### 비목표 (Out of Scope — 본 프로젝트로 이관)
- Apple App Store 출시, TestFlight 베타
- 카카오 OAuth 로그인 (비즈앱 심사 대기 부담)
- 푸시 알림(FCM), SNS 친구·랭킹
- Supabase 백엔드, RLS 정책, Edge Functions
- AdMob 광고, 구독(Voyna+)
- 30곳 모든 배지의 정성 디자인 (데모에는 핵심 5~10개만)

---

## 2. 확정된 의사결정

| 항목 | 결정 | 비고 |
|------|------|------|
| 데모 형태 | 웹 앱 (PWA형) | 모바일 브라우저 + 빔프로젝터 양쪽 |
| 명소 수 | **31곳** = 서울 핵심 30곳 + ASSIST 강의실 | ASSIST는 실기기 GPS 깜짝 시연용 |
| 배지 디자인 | **(iii) 핵심 5~10개만 정성껏 + 나머지 회색 자물쇠** | 미수집 상태로 "수집 욕구" 연출 |
| 로그인 | **구글 OAuth (Firebase Auth)** | 카카오 로그인은 본 프로젝트로 이관 |
| 데이터베이스 | 정적 JSON(`locations.json` / `badges.json`) + `localStorage`(사용자 상태) | Supabase는 본 프로젝트로 |
| 기술 스택 | **Vite + Vanilla TypeScript** | React 없음 (데모 규모엔 과잉) |
| 지도 | **카카오맵 JS SDK** | 키 즉시 발급, Places API로 명소 검색 |
| GitHub 분리 | **새 리포지토리 `AlexSong0674/Voyna-Demo`** | 기존 기획서 리포(`AlexSong0674/test`)는 문서 전용 유지 |
| Spec 위치 | 기획서 리포의 `docs/superpowers/specs/` | 의사결정 기록은 한 곳에 모음 |
| 배포 | **GitHub Pages + GitHub Actions** | `main` push → 자동 빌드·배포 |

---

## 3. 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│  Browser (Mobile Safari / Chrome / Desktop)             │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Vite + Vanilla TS SPA                           │   │
│  │  ├─ 4-Tab Router (Home / Map / Badges / More)    │   │
│  │  ├─ Badge Engine (거리 판정·XP·레벨·칭호)        │   │
│  │  └─ Components (modals, toasts, badge cards)     │   │
│  └──────────────────────────────────────────────────┘   │
│         │              │              │                 │
│         ▼              ▼              ▼                 │
│  ┌──────────┐  ┌────────────┐  ┌──────────────────┐     │
│  │ Firebase │  │ KakaoMap   │  │ localStorage     │     │
│  │ Auth     │  │ JS SDK     │  │ (user state)     │     │
│  │ (Google) │  │            │  │                  │     │
│  └──────────┘  └────────────┘  └──────────────────┘     │
│         │                                               │
│         ▼                                               │
│  Static JSON Catalog                                    │
│  ├─ locations.json (31곳)                               │
│  └─ badges.json (31종)                                  │
└─────────────────────────────────────────────────────────┘
```

**모든 상태는 클라이언트 측에 머무름.** 서버 호출은 (1) Firebase Google 인증, (2) 카카오맵 타일 로드 두 가지뿐.

---

## 4. 디렉터리 구조 (Voyna-Demo 리포)

```
Voyna-Demo/
├── README.md
├── package.json
├── tsconfig.json
├── vite.config.ts
├── index.html
├── .github/
│   └── workflows/
│       └── deploy.yml          # main push → Pages 배포
├── src/
│   ├── main.ts                 # 부트스트랩 + 라우터
│   ├── auth/
│   │   ├── firebase.ts         # Firebase init (env: VITE_FB_*)
│   │   └── login-page.ts       # 구글 로그인 화면
│   ├── pages/
│   │   ├── home.ts             # 홈 탭
│   │   ├── map.ts              # 카카오맵 + 텔레포트 패널
│   │   ├── badges.ts           # 컬렉션 그리드
│   │   └── more.ts             # 프로필·설정·데모 리셋
│   ├── components/
│   │   ├── tab-bar.ts          # 하단 4탭
│   │   ├── badge-card.ts       # 잠금/획득 상태
│   │   ├── level-up-modal.ts   # 레벨업 애니메이션
│   │   ├── badge-acquired-modal.ts  # 배지 획득 팝업
│   │   └── title-toast.ts      # 칭호 획득 토스트
│   ├── core/
│   │   ├── state.ts            # localStorage 래퍼
│   │   ├── geo.ts              # Haversine + 현재 위치
│   │   ├── badge-engine.ts     # 거리 판정·XP·레벨·칭호
│   │   ├── catalog.ts          # JSON 로더
│   │   └── titles.ts           # 칭호 조건표
│   ├── data/
│   │   ├── locations.json
│   │   └── badges.json
│   └── styles/
│       └── main.css            # Voyna 브랜드 컬러
├── public/
│   ├── badges/
│   │   ├── gyeongbok.png       # 핵심 5~10종 (AI 디자인)
│   │   ├── ...
│   │   └── locked.png          # 회색 자물쇠
│   ├── icons/
│   └── favicon.ico
└── docs/
    ├── DEMO_SCRIPT.md          # 시연 진행 시나리오
    └── KAKAO_FIREBASE_SETUP.md # 키 발급·환경변수 가이드
```

---

## 5. 데이터 모델

### `locations.json` (31개 엔트리)

```jsonc
{
  "id": "assist",
  "name": "ASSIST 강의실",
  "lat": 37.5500,    // 실제 좌표로 교체 예정
  "lng": 126.9700,
  "radius": 50,      // m
  "category": "교육",
  "grade": "special"
}
```

서울 30곳은 기획서 리포의 [`data/seoul_50_locations.md`](../../../data/seoul_50_locations.md)에서 12주 plan과 동일한 30곳 선별 사용.

### `badges.json` (31개 엔트리)

```jsonc
{
  "id": "gyeongbok",
  "name": "조선의 정궁",
  "description": "경복궁을 방문하여 조선의 역사를 마주하다",
  "grade": "special",          // common | rare | special | premier
  "xp": 300,
  "image": "/badges/gyeongbok.png",
  "is_polished": true          // false면 locked.png 사용
}
```

**등급별 XP** (12주 plan과 동일):
- Common +50 / Rare +150 / Special +200~400 / Premier +500

**정성 디자인 우선순위 (10개):**
1. ASSIST 강의실 (특별 — 시연 핵심)
2. 경복궁 (특별)
3. N서울타워 (특별)
4. 청와대 (특별)
5. 북한산 (특별)
6. 창덕궁 (희귀)
7. 롯데월드타워 (희귀)
8. 반포 한강 (희귀)
9. 명동 (일반 — 인지도 최상)
10. 광화문 (일반 — 인지도 최상)

나머지 21곳은 `locked.png` 공통 사용.

### `localStorage` 사용자 상태

```ts
type UserState = {
  user: { uid: string; displayName: string; email: string; photoURL: string };
  xp: number;
  level: number;
  title: string;
  obtained: Array<{ badgeId: string; at: string; lat: number; lng: number }>;
  currentLocation: { lat: number; lng: number; isTeleport: boolean } | null;
  realGPS: { lat: number; lng: number } | null;
  lastSeenAt: string;
};
```

키: `voyna_demo_state_v1`. 버전 접미사로 향후 스키마 변경 대응.

### 레벨업 공식 (12주 plan과 동일)

```
필요 XP(Lv n→n+1) = floor(100 × n^1.6)
```

### 칭호 조건 (데모용 단순화 — 5개만)

| 칭호 | 조건 |
|------|------|
| 초보 탐험가 | 기본 (가입 직후) |
| 동네 탐험가 | 배지 5개 |
| 지도 마니아 | 배지 10개 |
| 서울 정복자 | 특별 등급 5개 |
| 전설의 여행자 | Lv10 + 배지 20개 |

---

## 6. 핵심 컴포넌트 명세

### `core/badge-engine.ts`
- `checkProximity(location, currentLocation): boolean` — Haversine 거리 ≤ radius 판정
- `awardBadge(badgeId): { newLevel?, newTitle? }` — 중복 획득 차단, XP 적립, 레벨업·칭호 체크
- `checkAllBadgesNearby(): Badge[]` — 현재 위치 기준 획득 가능한 모든 배지 반환

### `pages/map.ts`
- 카카오맵 인스턴스 + 31개 POI 마커
- "현재 위치" 마커 (real GPS 또는 텔레포트 좌표)
- **텔레포트 패널** (데모 핵심): 31개 명소 드롭다운 → 선택 시 currentLocation 즉시 변경 → 자동 배지 획득 트리거
- 명소 검색 입력란 (카카오 Places API)

### `components/badge-acquired-modal.ts`
- 등급별 색상·효과 (특별=금색 빛, 희귀=보라, 일반=파랑)
- 0.5s 페이드인 → 1.5s 확대 회전 → 사용자 탭하면 닫힘
- XP +N 카운트업 애니메이션 동반

### `components/level-up-modal.ts`
- 배지 획득으로 레벨이 올랐을 때만 트리거 (chained modal)
- "Lv X → Lv Y" 표시 + 폭죽 효과(CSS)

### `auth/firebase.ts`
- Firebase Web SDK v10 (modular)
- Google Provider만 활성화
- 로그인 성공 시 `state.user`에 저장 후 `/home` 라우팅
- 로그아웃 버튼은 더보기 탭에

---

## 7. 데모 시연 동선

```
1. 청중 앞 노트북 화면 (또는 강사 스마트폰 미러링)
2. 구글 로그인 → "환영합니다, [닉네임]님" 홈 진입
3. 맵 탭 진입 → 카카오맵에 31개 POI 핀이 보임
4. ASSIST 강의실 핀이 "내 위치 근처" 표시 (강의실에서 실기기 시연 시 진짜 GPS로 자동 인증)
5. 텔레포트 패널 열기 → "경복궁" 선택
   → 현재 위치 마커가 경복궁으로 이동
   → 자동 배지 획득 팝업 (특별 등급 금색 효과)
   → +300 XP 카운트업
   → 레벨업 모달
6. 연이어 텔레포트로 N서울타워, 북한산 순회
   → 누적 XP, 추가 배지 획득
   → "지도 마니아" 칭호 획득 토스트
7. 배지 탭 진입
   → 획득한 3~5개는 컬러로 빛남
   → 나머지 28개는 회색 자물쇠
   → "이걸 다 모으면 어떤 풍경이?" 기대감 연출
8. 더보기 탭 → 프로필, 데모 리셋 버튼 → 처음부터 다시 시연 가능
```

시연 스크립트 상세 버전은 `docs/DEMO_SCRIPT.md`에 별도 작성.

---

## 8. 환경 변수 & 비밀 키

`.env.local` (커밋 금지):
```
VITE_FB_API_KEY=...
VITE_FB_AUTH_DOMAIN=...
VITE_FB_PROJECT_ID=...
VITE_KAKAO_MAP_KEY=...
```

GitHub Actions 배포용은 리포 Settings → Secrets에 동일 키 등록 후 `deploy.yml`에서 `${{ secrets.VITE_FB_API_KEY }}` 등으로 주입.

**Firebase 인증된 도메인 등록 필수:**
- `localhost`
- `alexsong0674.github.io`

**카카오 개발자 앱 사이트 도메인 등록 필수:**
- `https://alexsong0674.github.io`

---

## 9. GitHub Pages 배포

`.github/workflows/deploy.yml`:
1. Node 20 setup
2. `npm ci`
3. `npm run build` (Vite → `dist/`)
4. `actions/upload-pages-artifact@v3` (`dist/`)
5. `actions/deploy-pages@v4`

**사용자 1회 수동 작업:**
- GitHub 리포 Settings → Pages → Source: "GitHub Actions"

**배포 URL:** `https://alexsong0674.github.io/Voyna-Demo/`
- Vite `base` 설정: `'/Voyna-Demo/'`

---

## 10. 3일 일정

| 일자 | 산출물 | 검증 기준 |
|------|--------|-----------|
| **수 (5/13) Day 1** | 리포 초기화, Vite·Firebase·카카오맵 키 발급, 4탭 라우팅 스켈레톤, `locations.json`(31곳), Google 로그인 동작 | 로그인 후 빈 4탭 화면 진입 가능 |
| **목 (5/14) Day 2** | 맵 페이지(31개 POI + 텔레포트), 배지 엔진(거리·XP·레벨·칭호), localStorage 상태, 핵심 5~10개 배지 AI 생성 | 텔레포트로 배지 획득·XP 적립·레벨업이 동작 |
| **금 (5/15) Day 3** | 배지 컬렉션 그리드(컬러+자물쇠), 레벨업·칭호 애니메이션, 홈 탭, 더보기 탭, GitHub Actions 배포, 모바일 실기기 동작 확인, `DEMO_SCRIPT.md` 완성 | `alexsong0674.github.io/Voyna-Demo`에서 전체 시연 동선 1회 통과 |

**관리 마진:** 일정에 30% 버퍼 없음. 막히면 (a) 핵심 배지 디자인 5개로 축소, (b) 칭호 시스템 일부 생략, (c) 더보기 탭 최소화 순서로 컷.

---

## 11. 본 프로젝트와의 충돌 방지

- **별도 리포지토리** (`Voyna-Demo`) — 코드·CI·이슈 완전 분리
- **별도 GitHub Pages** (`/Voyna-Demo/` 경로) — 기존 `/test/` 경로와 충돌 없음
- **본 12주 plan의 데이터 자산은 참조만**: 서울 명소 좌표는 기획서 리포의 마크다운에서 수동 복사 (직접 import 안 함)
- **데모에서 검증한 UX·데이터 모델은 본 프로젝트로 이식 가능** — 다만 데이터 구조는 본 프로젝트 Supabase 스키마와 일부 다를 수 있음 (의도된 단순화)
- 본 12주 plan 진행 중 데모 결과·교수 피드백을 별도 메모로 본 plan에 반영

---

## 12. 오픈 이슈 / 후속 결정

- [ ] ASSIST 강의실의 정확한 위경도 좌표 확정 (사용자가 알려줘야 함)
- [ ] 핵심 정성 디자인 배지 정확히 몇 개로 갈지(5 vs 7 vs 10) — Day 2에 진행 상황 보고 결정
- [ ] 데모 발표 일자 확정 시 `DEMO_SCRIPT.md`에 슬라이드 타임라인 매핑
- [ ] 발표 후 데모 리포지토리 archive 여부 (즉시 archive vs 본 프로젝트 출시 후 archive)

---

## 13. 다음 단계

이 spec이 승인되면 → **writing-plans 스킬**로 체크박스 단위 구현 계획서를 `docs/superpowers/plans/2026-05-13-voyna-demo-implementation.md`에 작성 → 그 후 **subagent-driven-development** 또는 **executing-plans**로 실제 코드 구현 진행.
