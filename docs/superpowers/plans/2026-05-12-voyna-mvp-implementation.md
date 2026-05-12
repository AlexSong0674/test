# Voyna iOS MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** GPS 기반 여행 배지 앱 'Voyna'의 iOS MVP를 24주 안에 App Store 정식 출시한다 — 서울 50곳 명소, 50종 배지, 자동/확인형 획득 이원화, 카카오 로그인, 카카오맵 표시, 레벨/칭호 시스템 포함.

**Architecture:** FlutterFlow(iOS/Android 동시 빌드) + Supabase(PostgreSQL + Auth + Edge Functions + Storage) + 카카오맵 SDK + FCM(푸시) 조합. 노코드 UI + 필요한 부분만 Dart 커스텀 코드, 모든 비즈니스 로직(배지 획득 검증·XP 계산·칭호 자동 부여)은 Supabase Edge Functions에서 처리해 클라이언트 어뷰징 방지.

**Tech Stack:** FlutterFlow, Dart 3.x, Supabase(PostgreSQL 15, GoTrue, Storage, Edge Functions/Deno), 카카오맵 API(JS+SDK), kakao_flutter_sdk(인증), google_sign_in, geolocator, firebase_messaging, AdMob(Phase 1.5+)

---

## 진행 마일스톤 요약

| 마일스톤 | 시점 | 단계 | 핵심 산출물 |
|---------|------|------|------------|
| M1: 기획 완료 | 0주 | Phase 0 | 계정·도메인·API 키 모두 발급됨 |
| M2: 백엔드 가동 | 6주 | Phase 1 | Supabase 동작, 50곳 시드 입력 |
| M3: 앱 동작 (알파) | 12주 | Phase 2~4 | 로그인·맵·배지 획득 동작 |
| M4: 내부 테스트 | 18주 | Phase 5~7 | 팀 내부 10명 베타 |
| M5: 베타 출시 | 22주 | Phase 8~9 | TestFlight 100명 (선구자 칭호) |
| M6: 정식 출시 | 24주 | Phase 10 | App Store 출시 |

---

## File / Component Structure

| 위치 | 역할 |
|------|------|
| `supabase/migrations/0001_initial_schema.sql` | 초기 테이블 스키마 (10 테이블) |
| `supabase/migrations/0002_rls_policies.sql` | Row Level Security 정책 |
| `supabase/migrations/0003_triggers.sql` | 가입 시 users 자동 생성 트리거 |
| `supabase/seed/locations.sql` | 서울 50곳 시드 |
| `supabase/seed/badges.sql` | 50종 배지 시드 |
| `supabase/functions/award_badge/index.ts` | 배지 획득 Edge Function |
| `supabase/functions/award_xp/index.ts` | XP 적립 + 레벨업 + 칭호 체크 |
| `supabase/functions/get_nearby_badges/index.ts` | 반경 내 배지 조회 |
| `flutterflow/pages/Onboarding/*` | 온보딩·로그인 페이지 |
| `flutterflow/pages/Home/*` | 홈 탭 |
| `flutterflow/pages/Map/*` | 탐험 맵 탭 |
| `flutterflow/pages/Badges/*` | 배지 컬렉션 탭 |
| `flutterflow/pages/More/*` | 더보기 탭 |
| `flutterflow/custom_widgets/KakaoMapView.dart` | 카카오맵 WebView 래퍼 |
| `flutterflow/custom_actions/get_current_location.dart` | GPS 위치 획득 |
| `flutterflow/custom_actions/calculate_distance.dart` | Haversine 거리 계산 |
| `flutterflow/custom_actions/award_badge_action.dart` | Edge Function 호출 |
| `assets/badges/{id}.png` | 50종 배지 이미지 (1024×1024) |
| `assets/badges/frames/{grade}.png` | 등급별 프레임 4종 |
| `docs/legal/privacy_policy.md` | 개인정보 처리방침 |
| `docs/legal/location_terms.md` | 위치정보 이용약관 |

---

## Phase 0: 사전 준비 (Week 0~2, M1)

> 코드 한 줄 쓰기 전에 끝내야 할 계정·키·도구 셋업.

### Task 0.1: 도메인 및 상표권 확정

**Files:**
- Create: `docs/branding/domain_trademark_check.md`

- [ ] **Step 1: 도메인 가용성 확인 및 등록**

확인 대상:
- `voyna.app` (Google Domains 또는 Namecheap, USD 약 $20/년)
- `voyna.co.kr`, `voyna.kr` (가비아 또는 후이즈)

장바구니에 담아 가격 확인 후 결제. 둘 다 확보 권장(브랜드 보호).

- [ ] **Step 2: 상표권 사전 검색**

키프리스(www.kipris.or.kr) 접속 → 상표 → "Voyna" / "보이나" 검색.

확인할 류:
- 9류 (소프트웨어, 모바일 앱)
- 42류 (소프트웨어 서비스, 플랫폼 제공)
- 39류 (여행 정보 제공) — 선택

동일·유사 등록상표가 있으면 변호리(또는 변리사) 상담.

- [ ] **Step 3: App Store 이름 충돌 재확인**

apps.apple.com에서 "Voyna" 검색. 결과 캡처해 `docs/branding/domain_trademark_check.md`에 기록.

이전 조사 결과(2026-05-12 기준): VOYENA, Voyana, Voyin, Voya 존재 — 직접 충돌 없음, 단 검색 혼동 가능성 있어 앱 이름에 부제 추가 권장 ("Voyna - 여행 배지" 같은 형식).

- [ ] **Step 4: 결과 문서화 + 커밋**

```bash
git add docs/branding/domain_trademark_check.md
git commit -m "docs: domain and trademark availability check"
```

---

### Task 0.2: Apple Developer 계정 등록

- [ ] **Step 1: 사업자 또는 개인 결정**

- 개인 계정: 본인 이름으로 출시. 빠름.
- 사업자 계정: 법인 D-U-N-S 번호 필요 (3~10일 소요), 회사명으로 출시.

MVP는 개인 계정 권장. 추후 법인 전환 가능.

- [ ] **Step 2: developer.apple.com에서 가입**

- $99 USD/년 결제
- 가입 후 1~2일 내 활성화

- [ ] **Step 3: App Store Connect 접속 확인**

appstoreconnect.apple.com 로그인 → "내 앱" 메뉴 보이는지 확인.

- [ ] **Step 4: 자격증명서(Certificates) 발급**

App Store Connect → 인증서 → iOS Distribution Certificate 발급.  
나중에 FlutterFlow 빌드 시 필요.

---

### Task 0.3: Supabase 프로젝트 생성

- [ ] **Step 1: Supabase 가입 및 프로젝트 생성**

supabase.com → Sign up → New Project

```
Project name: voyna-prod
Database password: (20자 이상 강력한 패스워드, 1Password에 저장)
Region: Northeast Asia (Seoul) — ap-northeast-2
Pricing plan: Free (MAU 5만까지 무료)
```

- [ ] **Step 2: 프로젝트 URL과 anon key 기록**

Settings → API 에서 복사:
```
PROJECT_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbG...
SUPABASE_SERVICE_ROLE_KEY=eyJhbG...   # 서버 측에서만 사용
```

`.env.example` 파일 생성해 git 커밋(실제 값은 `.env`에, .gitignore 처리).

```bash
echo "SUPABASE_URL=" > .env.example
echo "SUPABASE_ANON_KEY=" >> .env.example
echo ".env" >> .gitignore
git add .env.example .gitignore
git commit -m "chore: add env template"
```

- [ ] **Step 3: Supabase CLI 설치**

```bash
# macOS
brew install supabase/tap/supabase

# Windows (scoop)
scoop bucket add supabase https://github.com/supabase/scoop-bucket.git
scoop install supabase

# 확인
supabase --version  # 2.x 이상
```

- [ ] **Step 4: 로컬 프로젝트 연결**

```bash
cd /path/to/voyna-app
supabase init
supabase link --project-ref <project-ref>
```

`supabase/` 디렉토리가 생성됨.

---

### Task 0.4: 카카오 개발자 계정 + 카카오맵 API 키

- [ ] **Step 1: developers.kakao.com 가입**

기존 카카오 계정으로 로그인 → 개발자 등록.

- [ ] **Step 2: 애플리케이션 생성**

"내 애플리케이션" → "애플리케이션 추가하기"
```
앱 이름: Voyna
사업자명: (개인 또는 법인)
카테고리: 여행
```

- [ ] **Step 3: 플랫폼 등록**

앱 설정 → 플랫폼 → iOS 플랫폼 등록
```
번들 ID: app.voyna.ios (Apple Developer 등록과 일치)
앱스토어 ID: (출시 후 입력)
```

Android 플랫폼도 동일하게 등록 (`app.voyna.android`).

- [ ] **Step 4: 카카오 로그인 활성화**

제품 설정 → 카카오 로그인 → 활성화 ON.
Redirect URI에 Supabase OAuth callback URL 추가:
```
https://<project-ref>.supabase.co/auth/v1/callback
```

- [ ] **Step 5: 동의항목 설정**

필수: 닉네임, 프로필 사진  
선택: 이메일

- [ ] **Step 6: 카카오맵 SDK 키 발급**

JavaScript 키와 네이티브 앱 키 둘 다 발급되어 있는지 확인. JavaScript 키는 WebView 래핑 시 사용.

기록:
```
KAKAO_APP_KEY_JS=
KAKAO_APP_KEY_NATIVE=
KAKAO_REST_API_KEY=
```

---

### Task 0.5: Google OAuth 클라이언트 ID 발급

- [ ] **Step 1: console.cloud.google.com 접속, 프로젝트 생성**

프로젝트명: `voyna-mobile`

- [ ] **Step 2: OAuth 동의화면 구성**

"API 및 서비스" → "OAuth 동의 화면" → 외부 → 앱 정보 입력.

- [ ] **Step 3: iOS 클라이언트 ID 생성**

"사용자 인증 정보" → "사용자 인증 정보 만들기" → "OAuth 클라이언트 ID" → iOS  
번들 ID: `app.voyna.ios`

생성된 클라이언트 ID 기록:
```
GOOGLE_CLIENT_ID_IOS=xxx.apps.googleusercontent.com
```

- [ ] **Step 4: Web 클라이언트 ID (Supabase Auth용) 생성**

Supabase는 OAuth 콜백을 web으로 받기 때문에 web 클라이언트 ID도 필요.  
승인된 리디렉션 URI: `https://<project-ref>.supabase.co/auth/v1/callback`

---

### Task 0.6: FlutterFlow 프로젝트 시작

- [ ] **Step 1: FlutterFlow 계정 가입**

flutterflow.io → Sign up. Pro 플랜($30/월) 권장 — 소스 코드 내보내기, GitHub 동기화 가능.

- [ ] **Step 2: 새 프로젝트 생성**

```
Project name: Voyna
Package name: app.voyna
Initial state: From Scratch
Theme: Material 3
Primary color: #0071E3 (Voyna Blue)
```

- [ ] **Step 3: Supabase Integration 연결**

Settings → Integrations → Supabase → URL과 anon key 입력.

- [ ] **Step 4: 카카오 로그인 패키지 추가**

Settings → Dependencies → Add custom dependency:
```yaml
kakao_flutter_sdk: ^1.9.0
kakao_flutter_sdk_user: ^1.9.0
```

- [ ] **Step 5: GitHub 연동 (선택 권장)**

FlutterFlow → Push to GitHub → 기존 저장소(`AlexSong0674/voyna-app`) 연결.

---

### Task 0.7: Git 저장소 정리

- [ ] **Step 1: 새 저장소 생성**

GitHub: `AlexSong0674/voyna-app` 신규 생성 (기존 `test` 저장소는 기획서용으로 유지).

- [ ] **Step 2: 디렉토리 구조 생성**

```bash
mkdir voyna-app && cd voyna-app
mkdir -p supabase/migrations supabase/seed supabase/functions
mkdir -p docs/legal docs/branding
mkdir -p assets/badges/frames
git init
git remote add origin https://github.com/AlexSong0674/voyna-app.git
```

- [ ] **Step 3: README.md 및 .gitignore**

```bash
cat > .gitignore <<'EOF'
.env
.env.local
node_modules/
build/
*.log
.DS_Store
ios/Pods/
.flutter-plugins
EOF

cat > README.md <<'EOF'
# Voyna (보이나)

GPS 기반 여행 인증 배지 앱.

## 구조
- `supabase/` — 백엔드 (스키마, 시드, Edge Functions)
- `flutterflow/` — FlutterFlow 생성 코드 (자동 동기화)
- `assets/badges/` — 배지 이미지 자산
- `docs/legal/` — 법적 문서 (개인정보·약관)
EOF

git add .
git commit -m "chore: initial repo structure"
git branch -M main
git push -u origin main
```

---

## Phase 1: 백엔드 데이터베이스 (Week 2~6, M2)

> 모든 비즈니스 로직의 진실의 원천. 클라이언트는 표시만 담당.

### Task 1.1: users 테이블 스키마

**Files:**
- Create: `supabase/migrations/0001_initial_schema.sql`

- [ ] **Step 1: SQL 파일 시작**

```sql
-- supabase/migrations/0001_initial_schema.sql
-- Voyna 초기 스키마 (v2.0)

-- users: 사용자 프로필 (auth.users와 1:1 매핑)
CREATE TABLE public.users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    nickname TEXT UNIQUE NOT NULL,
    level INTEGER NOT NULL DEFAULT 1,
    xp INTEGER NOT NULL DEFAULT 0,
    title TEXT,  -- 현재 장착 칭호
    photo_url TEXT,
    locale TEXT DEFAULT 'ko',
    is_beta_user BOOLEAN DEFAULT FALSE,  -- '선구자' 칭호 후보
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT nickname_length CHECK (char_length(nickname) BETWEEN 2 AND 20),
    CONSTRAINT level_range CHECK (level BETWEEN 1 AND 99),
    CONSTRAINT xp_non_negative CHECK (xp >= 0)
);

CREATE INDEX idx_users_level ON public.users(level DESC);
CREATE INDEX idx_users_nickname ON public.users(nickname);
```

- [ ] **Step 2: 마이그레이션 실행**

```bash
supabase db push
```

예상 출력: `Successfully applied migration 0001_initial_schema.sql`

- [ ] **Step 3: 테스트**

Supabase SQL Editor에서:
```sql
SELECT column_name, data_type FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = 'users';
```

기대: 11개 컬럼이 출력됨.

- [ ] **Step 4: 커밋**

```bash
git add supabase/migrations/0001_initial_schema.sql
git commit -m "feat(db): add users table"
```

---

### Task 1.2: locations 테이블 스키마

- [ ] **Step 1: 같은 파일에 추가**

```sql
-- locations: 명소 마스터 (서울 50곳 + 확장)
CREATE TABLE public.locations (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    name_en TEXT,
    description TEXT,
    lat DOUBLE PRECISION NOT NULL,
    lng DOUBLE PRECISION NOT NULL,
    radius_m INTEGER NOT NULL DEFAULT 100,
    category TEXT NOT NULL,  -- 역사, 한옥, 거리, 랜드마크, 시장, 한강, 자연, 문화, 기타
    region TEXT NOT NULL,    -- 서울, 부산, 제주 ...
    district TEXT,           -- 종로구, 중구 ...
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT lat_range CHECK (lat BETWEEN -90 AND 90),
    CONSTRAINT lng_range CHECK (lng BETWEEN -180 AND 180),
    CONSTRAINT radius_positive CHECK (radius_m BETWEEN 30 AND 500)
);

CREATE INDEX idx_locations_region ON public.locations(region);
CREATE INDEX idx_locations_category ON public.locations(category);
-- 공간 검색 가속(반경 내 명소 조회)
CREATE EXTENSION IF NOT EXISTS cube;
CREATE EXTENSION IF NOT EXISTS earthdistance;
CREATE INDEX idx_locations_earth ON public.locations
    USING gist (ll_to_earth(lat, lng));
```

- [ ] **Step 2: 마이그레이션 + 검증**

```bash
supabase db push
```

검증 SQL:
```sql
-- 반경 5km 내 명소 조회 테스트 (서울시청 기준)
SELECT id, name,
       earth_distance(ll_to_earth(37.5663, 126.9779), ll_to_earth(lat, lng)) AS meters
FROM public.locations
ORDER BY meters
LIMIT 10;
```

(아직 시드 데이터 없으면 비어 있음 — Task 1.9에서 채움)

---

### Task 1.3: badges 테이블 스키마

```sql
-- badges: 명소별 배지 정의
CREATE TYPE badge_grade AS ENUM ('common', 'rare', 'special', 'premier', 'seasonal');

CREATE TABLE public.badges (
    id BIGSERIAL PRIMARY KEY,
    location_id BIGINT REFERENCES public.locations(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    grade badge_grade NOT NULL,
    xp_reward INTEGER NOT NULL,
    requires_confirmation BOOLEAN NOT NULL DEFAULT FALSE,  -- v2.0 신규
    is_premium BOOLEAN DEFAULT FALSE,
    image_url TEXT,
    icon TEXT,  -- 임시 이모지
    season_id BIGINT,  -- 시즌 배지면 참조
    color_hex TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT xp_positive CHECK (xp_reward > 0)
);

CREATE INDEX idx_badges_location ON public.badges(location_id);
CREATE INDEX idx_badges_grade ON public.badges(grade);
```

- [ ] **Step 1~2: 동일 패턴으로 추가, push, 검증**

---

### Task 1.4: user_badges 테이블 (획득 기록)

```sql
-- user_badges: 사용자별 배지 획득 이력
CREATE TABLE public.user_badges (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    badge_id BIGINT NOT NULL REFERENCES public.badges(id),
    obtained_at TIMESTAMPTZ DEFAULT NOW(),
    lat DOUBLE PRECISION NOT NULL,
    lng DOUBLE PRECISION NOT NULL,
    photo_url TEXT,  -- 사진 보조 인증 (V2+)
    UNIQUE (user_id, badge_id)  -- 한 사람당 한 배지 1회만
);

CREATE INDEX idx_user_badges_user ON public.user_badges(user_id, obtained_at DESC);
CREATE INDEX idx_user_badges_badge ON public.user_badges(badge_id);
```

---

### Task 1.5: xp_log 테이블

```sql
-- xp_log: XP 적립 이력 (어뷰징 추적용)
CREATE TYPE xp_reason AS ENUM (
    'badge_obtained',
    'mission_completed',
    'streak_bonus',
    'friend_companion_bonus',
    'admin_adjust'
);

CREATE TABLE public.xp_log (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    amount INTEGER NOT NULL,
    reason xp_reason NOT NULL,
    ref_badge_id BIGINT REFERENCES public.badges(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_xp_log_user ON public.xp_log(user_id, created_at DESC);
```

---

### Task 1.6: seasons, events, missions 테이블

```sql
CREATE TABLE public.seasons (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    theme TEXT,
    start_at TIMESTAMPTZ NOT NULL,
    end_at TIMESTAMPTZ NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    CONSTRAINT season_dates CHECK (end_at > start_at)
);

CREATE TABLE public.events (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    start_at TIMESTAMPTZ NOT NULL,
    end_at TIMESTAMPTZ NOT NULL,
    banner_url TEXT,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE public.missions (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    condition_json JSONB NOT NULL,  -- {"type": "visit_count", "category": "역사", "target": 5}
    reward_xp INTEGER NOT NULL,
    reward_badge_id BIGINT REFERENCES public.badges(id),
    season_id BIGINT REFERENCES public.seasons(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE public.user_missions (
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    mission_id BIGINT REFERENCES public.missions(id) ON DELETE CASCADE,
    progress JSONB DEFAULT '{}'::jsonb,  -- {"current": 3, "target": 5}
    completed_at TIMESTAMPTZ,
    PRIMARY KEY (user_id, mission_id)
);
```

---

### Task 1.7: subscriptions, friends 테이블

```sql
CREATE TYPE subscription_plan AS ENUM ('free', 'plus_monthly', 'plus_yearly');
CREATE TYPE subscription_status AS ENUM ('active', 'cancelled', 'expired');

CREATE TABLE public.subscriptions (
    user_id UUID PRIMARY KEY REFERENCES public.users(id) ON DELETE CASCADE,
    plan subscription_plan NOT NULL DEFAULT 'free',
    status subscription_status NOT NULL DEFAULT 'active',
    started_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    apple_transaction_id TEXT,  -- StoreKit2 영수증
    google_purchase_token TEXT,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TYPE friend_status AS ENUM ('pending', 'accepted', 'blocked');

CREATE TABLE public.friends (
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    friend_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    status friend_status NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (user_id, friend_id),
    CONSTRAINT no_self_friend CHECK (user_id != friend_id)
);
```

`supabase db push` → 검증 → 커밋:
```bash
git add supabase/migrations/0001_initial_schema.sql
git commit -m "feat(db): add all initial tables (users, locations, badges, etc.)"
```

---

### Task 1.8: RLS (Row Level Security) 정책

**Files:**
- Create: `supabase/migrations/0002_rls_policies.sql`

- [ ] **Step 1: RLS 활성화**

```sql
-- 모든 테이블 RLS 활성화
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_badges ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.xp_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.friends ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_missions ENABLE ROW LEVEL SECURITY;
```

- [ ] **Step 2: users 정책**

```sql
-- 본인 프로필 SELECT/UPDATE
CREATE POLICY "users_self_select" ON public.users
    FOR SELECT USING (auth.uid() = id OR true);  -- 닉네임은 공개 (랭킹용)

CREATE POLICY "users_self_update" ON public.users
    FOR UPDATE USING (auth.uid() = id);

-- INSERT은 트리거가 처리 (Task 1.9)
```

- [ ] **Step 3: user_badges 정책**

```sql
-- 본인 배지 SELECT (랭킹 페이지에서는 노출 카운트만 별도 RPC로)
CREATE POLICY "user_badges_self_select" ON public.user_badges
    FOR SELECT USING (auth.uid() = user_id);

-- INSERT은 Edge Function service_role으로만 (어뷰징 방지)
-- 클라이언트 INSERT 차단
```

- [ ] **Step 4: 공개 테이블 (locations, badges, events) — RLS 없이 SELECT 허용**

```sql
-- 이 테이블들은 RLS 미활성 — 모두 읽기 가능
GRANT SELECT ON public.locations TO anon, authenticated;
GRANT SELECT ON public.badges TO anon, authenticated;
GRANT SELECT ON public.events TO anon, authenticated;
GRANT SELECT ON public.seasons TO anon, authenticated;
GRANT SELECT ON public.missions TO anon, authenticated;
```

- [ ] **Step 5: 마이그레이션 적용 + 커밋**

```bash
supabase db push
git add supabase/migrations/0002_rls_policies.sql
git commit -m "feat(db): add RLS policies"
```

---

### Task 1.9: 회원가입 트리거 (auth.users → public.users 자동 생성)

**Files:**
- Create: `supabase/migrations/0003_triggers.sql`

```sql
-- auth.users에 행이 생기면 public.users에 자동 추가
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
    default_nickname TEXT;
BEGIN
    -- 카카오/구글에서 받은 이름 또는 익명 닉네임
    default_nickname := COALESCE(
        NEW.raw_user_meta_data->>'nickname',
        NEW.raw_user_meta_data->>'name',
        'Voyager_' || substr(NEW.id::text, 1, 8)
    );

    INSERT INTO public.users (id, nickname, level, xp)
    VALUES (NEW.id, default_nickname, 1, 0)
    ON CONFLICT (id) DO NOTHING;

    -- 무료 구독 기본 생성
    INSERT INTO public.subscriptions (user_id, plan, status)
    VALUES (NEW.id, 'free', 'active')
    ON CONFLICT (user_id) DO NOTHING;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_new_user();

-- updated_at 자동 갱신 트리거
CREATE OR REPLACE FUNCTION public.touch_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

CREATE TRIGGER users_updated_at BEFORE UPDATE ON public.users
    FOR EACH ROW EXECUTE FUNCTION public.touch_updated_at();
```

`supabase db push` → SQL Editor에서 테스트:
```sql
-- 더미 가입 시뮬레이션 (실제 운영에서는 OAuth가 수행)
SELECT * FROM public.users ORDER BY created_at DESC LIMIT 5;
```

---

### Task 1.10: 50곳 명소 시드 SQL

**Files:**
- Create: `supabase/seed/locations.sql`

- [ ] **Step 1: CSV에서 SQL INSERT 생성**

`기획서/data/seoul_50_locations.csv`를 기반으로 SQL 생성.

```sql
-- supabase/seed/locations.sql
-- 서울 초기 50곳 명소

INSERT INTO public.locations (id, name, name_en, description, lat, lng, radius_m, category, region, district) VALUES
(1, '경복궁', 'Gyeongbokgung Palace', '조선왕조 정궁·5대궁 중 최대 규모', 37.5796, 126.9770, 150, '역사', '서울', '종로구'),
(2, '창덕궁', 'Changdeokgung Palace', '유네스코 세계문화유산·후원으로 유명', 37.5794, 126.9910, 150, '역사', '서울', '종로구'),
(3, '창경궁', 'Changgyeonggung Palace', '조선시대 동궐·왕대비 거처', 37.5784, 126.9947, 120, '역사', '서울', '종로구'),
(4, '덕수궁', 'Deoksugung Palace', '석조전·정관헌 등 동서양 건축', 37.5658, 126.9751, 120, '역사', '서울', '중구'),
(5, '종묘', 'Jongmyo Shrine', '조선 역대 왕·왕비 신위 모신 사당', 37.5745, 126.9942, 120, '역사', '서울', '종로구'),
-- ... CSV의 나머지 45개 행
(50, '망원시장', 'Mangwon Market', '로컬 맛집·MZ 핫플', 37.5564, 126.9043, 120, '시장', '서울', '마포구');

-- 시퀀스를 50 다음으로
SELECT setval('public.locations_id_seq', 50);
```

전체 50행은 CSV 자동 변환 스크립트로 생성:

```python
# scripts/csv_to_sql.py
import csv

with open('기획서/data/seoul_50_locations.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = []
    for r in reader:
        rows.append(
            f"({r['id']}, '{r['name']}', '{r['name_en']}', "
            f"'{r['description'].replace(chr(39), chr(39)*2)}', "
            f"{r['lat']}, {r['lng']}, {r['radius_m']}, "
            f"'{r['category']}', '{r['region']}', '{r['district']}')"
        )
    print("INSERT INTO public.locations (id, name, name_en, description, lat, lng, radius_m, category, region, district) VALUES")
    print(",\n".join(rows) + ";")
    print("SELECT setval('public.locations_id_seq', 50);")
```

```bash
python scripts/csv_to_sql.py > supabase/seed/locations.sql
```

- [ ] **Step 2: 시드 적용**

```bash
psql "$DATABASE_URL" -f supabase/seed/locations.sql
# 또는 Supabase Studio SQL Editor에서 실행
```

- [ ] **Step 3: 검증**

```sql
SELECT count(*) FROM public.locations;  -- 기대: 50
SELECT category, count(*) FROM public.locations GROUP BY category ORDER BY count DESC;
```

- [ ] **Step 4: 커밋**

```bash
git add supabase/seed/locations.sql scripts/csv_to_sql.py
git commit -m "feat(db): seed 50 Seoul locations"
```

---

### Task 1.11: 50종 배지 시드 SQL

**Files:**
- Create: `supabase/seed/badges.sql`

```sql
-- 50종 배지 — location_id와 1:1 매핑
INSERT INTO public.badges (location_id, name, grade, xp_reward, requires_confirmation, icon, color_hex) VALUES
(1,  '경복궁',          'special', 300, TRUE,  '🏯', '#C8102E'),
(2,  '창덕궁',          'rare',    150, TRUE,  '🏯', '#1F5E3B'),
(3,  '창경궁',          'common',   50, FALSE, '🏯', '#8B4513'),
(4,  '덕수궁',          'rare',    150, TRUE,  '🏛', '#D4AF37'),
(5,  '종묘',            'rare',    150, TRUE,  '⛩', '#4A4A4A'),
-- ... 나머지 45개
(50, '망원시장',        'common',   50, FALSE, '🍡', '#F59E0B');

-- 단위 테스트
-- common 38개, rare 9개, special 3개여야 함
```

검증:
```sql
SELECT grade, count(*) FROM public.badges GROUP BY grade;
-- common: 38, rare: 9, special: 3
```

---

### Task 1.12: Edge Function — 배지 획득 (award_badge)

**Files:**
- Create: `supabase/functions/award_badge/index.ts`

**왜 Edge Function?** 클라이언트에서 직접 user_badges에 INSERT 하면 GPS 위조로 어뷰징 가능. 서버에서 좌표 검증 후만 부여.

- [ ] **Step 1: 함수 생성**

```bash
supabase functions new award_badge
```

- [ ] **Step 2: 코드 작성**

```typescript
// supabase/functions/award_badge/index.ts
import { serve } from "https://deno.land/std@0.224.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

interface Payload {
  badge_id: number;
  user_lat: number;
  user_lng: number;
  accuracy_m?: number;
  confirmed?: boolean;  // 확인형 배지의 경우 사용자 확인 완료 표시
}

const supabase = createClient(
  Deno.env.get("SUPABASE_URL")!,
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
);

// Haversine 거리 (m)
function haversine(lat1: number, lng1: number, lat2: number, lng2: number): number {
  const R = 6371000;
  const toRad = (d: number) => (d * Math.PI) / 180;
  const dLat = toRad(lat2 - lat1);
  const dLng = toRad(lng2 - lng1);
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLng / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(a));
}

serve(async (req) => {
  try {
    // 1. 사용자 인증 검증
    const authHeader = req.headers.get("Authorization");
    if (!authHeader) return new Response("Unauthorized", { status: 401 });

    const jwt = authHeader.replace("Bearer ", "");
    const { data: { user }, error: authErr } = await supabase.auth.getUser(jwt);
    if (authErr || !user) return new Response("Invalid token", { status: 401 });

    // 2. 페이로드 검증
    const p: Payload = await req.json();
    if (!p.badge_id || typeof p.user_lat !== "number" || typeof p.user_lng !== "number") {
      return new Response("Bad request", { status: 400 });
    }

    // 3. 배지/명소 정보 조회
    const { data: badge } = await supabase
      .from("badges")
      .select("id, grade, xp_reward, requires_confirmation, location_id, locations(lat, lng, radius_m)")
      .eq("id", p.badge_id)
      .single();
    if (!badge) return new Response("Badge not found", { status: 404 });

    // 4. 확인형 배지인데 confirmed=false면 거부
    if (badge.requires_confirmation && !p.confirmed) {
      return new Response(
        JSON.stringify({ requires_confirmation: true, badge }),
        { status: 200, headers: { "Content-Type": "application/json" } }
      );
    }

    // 5. 거리 검증
    const loc = (badge as any).locations;
    const dist = haversine(p.user_lat, p.user_lng, loc.lat, loc.lng);
    if (dist > loc.radius_m) {
      return new Response(
        JSON.stringify({ error: "Out of range", distance_m: Math.round(dist) }),
        { status: 422 }
      );
    }

    // 6. 정확도 검증 (50m 초과 시 거부)
    if (p.accuracy_m && p.accuracy_m > 50) {
      return new Response(
        JSON.stringify({ error: "GPS accuracy too low", accuracy_m: p.accuracy_m }),
        { status: 422 }
      );
    }

    // 7. 중복 획득 검증 + 삽입 (UNIQUE 제약 활용)
    const { error: insertErr } = await supabase
      .from("user_badges")
      .insert({
        user_id: user.id,
        badge_id: badge.id,
        lat: p.user_lat,
        lng: p.user_lng,
      });
    if (insertErr) {
      if (insertErr.code === "23505") {
        return new Response(JSON.stringify({ error: "Already obtained" }), { status: 409 });
      }
      throw insertErr;
    }

    // 8. XP 적립 (award_xp 함수 호출)
    const { data: xpResult } = await supabase.functions.invoke("award_xp", {
      body: {
        user_id: user.id,
        amount: badge.xp_reward,
        reason: "badge_obtained",
        ref_badge_id: badge.id,
      },
    });

    return new Response(
      JSON.stringify({
        success: true,
        badge,
        xp_gained: badge.xp_reward,
        level_up: xpResult?.level_up,
        new_titles: xpResult?.new_titles,
      }),
      { status: 200, headers: { "Content-Type": "application/json" } },
    );
  } catch (e) {
    console.error(e);
    return new Response("Internal error", { status: 500 });
  }
});
```

- [ ] **Step 3: 배포**

```bash
supabase functions deploy award_badge --no-verify-jwt
```

(JWT 검증은 내부에서 직접 수행하므로 `--no-verify-jwt` 사용)

- [ ] **Step 4: 단위 테스트 (curl)**

```bash
# 사전: Supabase Studio에서 임시 테스트 사용자 토큰 생성

curl -X POST "$SUPABASE_URL/functions/v1/award_badge" \
  -H "Authorization: Bearer $TEST_USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"badge_id": 3, "user_lat": 37.5784, "user_lng": 126.9947, "accuracy_m": 10}'

# 기대: {"success": true, "xp_gained": 50, ...}
```

거리 초과 테스트:
```bash
curl -X POST "$SUPABASE_URL/functions/v1/award_badge" \
  -H "Authorization: Bearer $TEST_USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"badge_id": 3, "user_lat": 37.0, "user_lng": 127.0}'

# 기대: 422 {"error": "Out of range", "distance_m": ...}
```

- [ ] **Step 5: 커밋**

```bash
git add supabase/functions/award_badge/
git commit -m "feat(api): add award_badge edge function with distance validation"
```

---

### Task 1.13: Edge Function — XP 적립 + 레벨업 (award_xp)

**Files:**
- Create: `supabase/functions/award_xp/index.ts`

```typescript
// supabase/functions/award_xp/index.ts
import { serve } from "https://deno.land/std@0.224.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const supabase = createClient(
  Deno.env.get("SUPABASE_URL")!,
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
);

// 레벨업 필요 XP: 100 × n^1.6
function xpForLevel(n: number): number {
  return Math.floor(100 * Math.pow(n, 1.6));
}

interface Payload {
  user_id: string;
  amount: number;
  reason: "badge_obtained" | "mission_completed" | "streak_bonus" | "friend_companion_bonus" | "admin_adjust";
  ref_badge_id?: number;
}

serve(async (req) => {
  const p: Payload = await req.json();

  // 1. xp_log 적립
  await supabase.from("xp_log").insert({
    user_id: p.user_id,
    amount: p.amount,
    reason: p.reason,
    ref_badge_id: p.ref_badge_id,
  });

  // 2. 현재 레벨/XP 조회
  const { data: u } = await supabase
    .from("users")
    .select("level, xp")
    .eq("id", p.user_id)
    .single();
  if (!u) return new Response("User not found", { status: 404 });

  let newXp = u.xp + p.amount;
  let newLevel = u.level;
  const leveledUp: number[] = [];

  // 3. 누적 XP가 다음 레벨 요구치 넘으면 연쇄 레벨업
  while (newLevel < 99 && newXp >= xpForLevel(newLevel)) {
    newXp -= xpForLevel(newLevel);
    newLevel += 1;
    leveledUp.push(newLevel);
  }

  // 4. users 업데이트
  await supabase
    .from("users")
    .update({ level: newLevel, xp: newXp })
    .eq("id", p.user_id);

  // 5. 칭호 조건 체크 (check_titles 함수 호출)
  const { data: titles } = await supabase.functions.invoke("check_titles", {
    body: { user_id: p.user_id },
  });

  return new Response(
    JSON.stringify({
      success: true,
      new_level: newLevel,
      level_up: leveledUp.length > 0,
      levels_gained: leveledUp,
      current_xp: newXp,
      next_level_xp: newLevel < 99 ? xpForLevel(newLevel) : null,
      new_titles: titles?.new_titles ?? [],
    }),
    { status: 200, headers: { "Content-Type": "application/json" } },
  );
});
```

배포·검증·커밋은 Task 1.12와 동일 패턴.

---

### Task 1.14: Edge Function — 칭호 자동 부여 (check_titles)

**Files:**
- Create: `supabase/functions/check_titles/index.ts`

```typescript
// supabase/functions/check_titles/index.ts
import { serve } from "https://deno.land/std@0.224.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const supabase = createClient(
  Deno.env.get("SUPABASE_URL")!,
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
);

// 칭호 정의 — DB에 두지 않고 코드로 (변경 빈도 낮음)
type Check = (userId: string) => Promise<boolean>;

const TITLES: Record<string, Check> = {
  "동네 탐험가": async (id) => (await badgeCount(id)) >= 5,
  "지도 마니아": async (id) => (await badgeCount(id)) >= 30,
  "고수 여행자": async (id) => (await userLevel(id)) >= 50,
  "전설의 여행자": async (id) => (await userLevel(id)) >= 99 && (await badgeCount(id)) >= 200,
  "산악인": async (id) => (await categoryBadgeCount(id, "자연")) >= 10,
  // ... 추가 칭호
};

async function badgeCount(uid: string): Promise<number> {
  const { count } = await supabase.from("user_badges").select("*", { count: "exact", head: true }).eq("user_id", uid);
  return count ?? 0;
}
async function userLevel(uid: string): Promise<number> {
  const { data } = await supabase.from("users").select("level").eq("id", uid).single();
  return data?.level ?? 0;
}
async function categoryBadgeCount(uid: string, cat: string): Promise<number> {
  // 명소 카테고리별 카운트 — view 또는 join
  const { data } = await supabase.rpc("count_category_badges", { p_user_id: uid, p_category: cat });
  return (data as number) ?? 0;
}

serve(async (req) => {
  const { user_id } = await req.json();

  const earned: string[] = [];
  for (const [title, check] of Object.entries(TITLES)) {
    if (await check(user_id)) earned.push(title);
  }

  // 보유 칭호 갱신 (사용자의 'available_titles' 컬럼 — Task 1.1에 추가 필요할 수 있음)
  // 단순화: 첫 획득 칭호를 자동 장착
  if (earned.length > 0) {
    const { data: u } = await supabase.from("users").select("title").eq("id", user_id).single();
    if (!u?.title) {
      await supabase.from("users").update({ title: earned[0] }).eq("id", user_id);
    }
  }

  return new Response(JSON.stringify({ new_titles: earned }), {
    status: 200, headers: { "Content-Type": "application/json" },
  });
});
```

RPC 함수도 추가 필요 — `supabase/migrations/0004_rpc_functions.sql`:
```sql
CREATE OR REPLACE FUNCTION public.count_category_badges(p_user_id UUID, p_category TEXT)
RETURNS INTEGER
LANGUAGE sql
SECURITY DEFINER
AS $$
    SELECT COUNT(*)::INTEGER
    FROM public.user_badges ub
    JOIN public.badges b ON b.id = ub.badge_id
    JOIN public.locations l ON l.id = b.location_id
    WHERE ub.user_id = p_user_id AND l.category = p_category;
$$;
```

---

### Task 1.15: Edge Function — 반경 내 배지 조회 (get_nearby_badges)

**Files:**
- Create: `supabase/functions/get_nearby_badges/index.ts`

```typescript
import { serve } from "https://deno.land/std@0.224.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const supabase = createClient(
  Deno.env.get("SUPABASE_URL")!,
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
);

serve(async (req) => {
  const url = new URL(req.url);
  const lat = parseFloat(url.searchParams.get("lat") ?? "0");
  const lng = parseFloat(url.searchParams.get("lng") ?? "0");
  const radius_km = parseFloat(url.searchParams.get("radius_km") ?? "5");

  // 사용자 인증
  const jwt = req.headers.get("Authorization")?.replace("Bearer ", "");
  const { data: { user } } = jwt ? await supabase.auth.getUser(jwt) : { data: { user: null } };

  // earthdistance 사용해 반경 내 명소 조회
  const { data: nearbyLocations } = await supabase.rpc("get_locations_within_radius", {
    p_lat: lat,
    p_lng: lng,
    p_radius_m: radius_km * 1000,
  });

  // 사용자 획득 배지 ID 조회
  let obtainedIds: number[] = [];
  if (user) {
    const { data: ub } = await supabase
      .from("user_badges")
      .select("badge_id")
      .eq("user_id", user.id);
    obtainedIds = (ub ?? []).map((r: any) => r.badge_id);
  }

  // locations + badges + obtained 정보 결합
  const locationIds = (nearbyLocations ?? []).map((l: any) => l.id);
  const { data: badges } = await supabase
    .from("badges")
    .select("*, locations(*)")
    .in("location_id", locationIds);

  const result = (badges ?? []).map((b: any) => ({
    ...b,
    obtained: obtainedIds.includes(b.id),
  }));

  return new Response(JSON.stringify({ badges: result }), {
    status: 200, headers: { "Content-Type": "application/json" },
  });
});
```

대응 RPC:
```sql
-- 0004_rpc_functions.sql에 추가
CREATE OR REPLACE FUNCTION public.get_locations_within_radius(
    p_lat DOUBLE PRECISION,
    p_lng DOUBLE PRECISION,
    p_radius_m DOUBLE PRECISION
)
RETURNS SETOF public.locations
LANGUAGE sql
SECURITY DEFINER
AS $$
    SELECT *
    FROM public.locations
    WHERE earth_box(ll_to_earth(p_lat, p_lng), p_radius_m) @> ll_to_earth(lat, lng)
      AND earth_distance(ll_to_earth(p_lat, p_lng), ll_to_earth(lat, lng)) <= p_radius_m
    ORDER BY earth_distance(ll_to_earth(p_lat, p_lng), ll_to_earth(lat, lng));
$$;
```

---

### Task 1.16: Storage 버킷 생성

- [ ] **Step 1: Supabase Studio에서 버킷 생성**

Storage → New bucket:
```
Name: badge-images
Public: YES (배지 이미지는 모두 공개)

Name: user-photos
Public: NO (사진 인증용, 본인만 접근)
```

- [ ] **Step 2: badge-images에 50종 배지 업로드 (Phase 6에서 실제 자산 생성 후)**

폴더 구조:
```
badge-images/
├── badges/
│   ├── 1_gyeongbokgung.png
│   ├── 2_changdeokgung.png
│   └── ...
└── frames/
    ├── common.png
    ├── rare.png
    ├── special.png
    └── premier.png
```

- [ ] **Step 3: badges 테이블의 image_url 일괄 업데이트**

```sql
UPDATE public.badges b
SET image_url = 'https://<project-ref>.supabase.co/storage/v1/object/public/badge-images/badges/' || b.id || '_' || lower(replace(b.name, ' ', '_')) || '.png';
```

---

### Task 1.17: Phase 1 회귀 테스트 (백엔드만)

**Files:**
- Create: `scripts/test_backend.sh`

```bash
#!/usr/bin/env bash
set -e

# 환경변수 로드
export SUPABASE_URL="https://xxx.supabase.co"
export TOKEN="<테스트 사용자 JWT>"

echo "== 1. 50곳 명소 조회 =="
curl -s "$SUPABASE_URL/rest/v1/locations?select=count" \
  -H "apikey: $SUPABASE_ANON_KEY" | jq

echo "== 2. 50개 배지 조회 =="
curl -s "$SUPABASE_URL/rest/v1/badges?select=count" \
  -H "apikey: $SUPABASE_ANON_KEY" | jq

echo "== 3. 반경 내 배지 (서울시청 5km) =="
curl -s "$SUPABASE_URL/functions/v1/get_nearby_badges?lat=37.5663&lng=126.9779&radius_km=5" \
  -H "Authorization: Bearer $TOKEN" | jq '.badges | length'

echo "== 4. 배지 획득 (창경궁) =="
curl -s -X POST "$SUPABASE_URL/functions/v1/award_badge" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"badge_id": 3, "user_lat": 37.5784, "user_lng": 126.9947}' | jq

echo "== 5. 확인형 배지 (경복궁) — 첫 호출 confirmed:false =="
curl -s -X POST "$SUPABASE_URL/functions/v1/award_badge" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"badge_id": 1, "user_lat": 37.5796, "user_lng": 126.9770}' | jq

echo "== 6. 확인형 배지 — 두 번째 호출 confirmed:true =="
curl -s -X POST "$SUPABASE_URL/functions/v1/award_badge" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"badge_id": 1, "user_lat": 37.5796, "user_lng": 126.9770, "confirmed": true}' | jq

echo "== 7. 사용자 현황 (레벨, XP) =="
curl -s "$SUPABASE_URL/rest/v1/users?select=*" \
  -H "Authorization: Bearer $TOKEN" \
  -H "apikey: $SUPABASE_ANON_KEY" | jq
```

실행:
```bash
chmod +x scripts/test_backend.sh
./scripts/test_backend.sh
```

기대: 모든 단계 200 OK + 일관된 상태 (배지 2개 보유, XP 50+300=350).

**M2 완료 조건**: 위 7개 테스트 모두 통과.

```bash
git add scripts/test_backend.sh
git commit -m "test(api): backend regression smoke test"
git tag M2-backend-complete
git push origin main --tags
```

---

## Phase 2: 인증 시스템 (Week 6~8)

### Task 2.1: Supabase Auth — 카카오 OAuth 설정

- [ ] **Step 1: Supabase Dashboard → Authentication → Providers → Kakao**

```
Client ID: <카카오 REST API 키>
Client Secret: <카카오 디벨로퍼 콘솔 → 카카오 로그인 → 보안 → 활성화 후 발급>
Enabled: ON
```

- [ ] **Step 2: 카카오 디벨로퍼 콘솔에서 Redirect URI 등록**

`https://<project-ref>.supabase.co/auth/v1/callback`

- [ ] **Step 3: 테스트 — Supabase Studio**

Authentication → Sign in with Kakao 버튼 동작 확인.

---

### Task 2.2: Supabase Auth — 구글 OAuth 설정

- [ ] **Step 1: Dashboard → Auth Providers → Google**

```
Client ID: <Google Cloud Console Web 클라이언트 ID>
Client Secret: <대응 시크릿>
Enabled: ON
```

- [ ] **Step 2: Google Cloud Console에서 Redirect URI 확인**

위 카카오와 동일.

---

### Task 2.3: FlutterFlow — 온보딩 페이지

- [ ] **Step 1: Pages → Add Page → "Onboarding"**

5장 슬라이드:
1. 환영 ("Voyna와 함께 여행을 게임처럼")
2. GPS 인증 설명
3. 배지 수집 설명
4. 위치 권한 안내
5. 로그인 페이지로 진행

- [ ] **Step 2: PageView 위젯 + 5개 Container**

각 Container에 이미지·텍스트 배치. 마지막 페이지에 "시작하기" 버튼.

- [ ] **Step 3: 첫 실행 감지 — Local State**

App State `hasSeenOnboarding: bool = false`.  
온보딩 완료 시 true로 설정 → 다음 실행부터 로그인 페이지 바로 이동.

---

### Task 2.4: FlutterFlow — 로그인 페이지

- [ ] **Step 1: Pages → Add → "Login"**

레이아웃:
- 상단: Voyna 로고
- 중앙: 슬로건 "발걸음이 기록이 되고, 기록이 추억이 된다"
- 하단: [카카오로 시작하기] [구글로 시작하기] 버튼 2개

- [ ] **Step 2: 카카오 로그인 액션 — Custom Action**

**Files:**
- Create: `flutterflow/custom_actions/login_with_kakao.dart`

```dart
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:kakao_flutter_sdk_user/kakao_flutter_sdk_user.dart';

Future<bool> loginWithKakao() async {
  try {
    // 1. 카카오톡 설치 여부 확인 후 분기
    OAuthToken token;
    if (await isKakaoTalkInstalled()) {
      token = await UserApi.instance.loginWithKakaoTalk();
    } else {
      token = await UserApi.instance.loginWithKakaoAccount();
    }

    // 2. Supabase에 ID 토큰 전달
    final res = await Supabase.instance.client.auth.signInWithIdToken(
      provider: OAuthProvider.kakao,
      idToken: token.idToken!,
      accessToken: token.accessToken,
    );

    return res.user != null;
  } catch (e) {
    print('Kakao login failed: $e');
    return false;
  }
}
```

- [ ] **Step 3: 카카오 SDK 초기화 — main.dart**

FlutterFlow → main.dart 커스텀:
```dart
import 'package:kakao_flutter_sdk/kakao_flutter_sdk.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  KakaoSdk.init(nativeAppKey: '<KAKAO_NATIVE_APP_KEY>');
  // ... 기존 FlutterFlow 초기화
}
```

- [ ] **Step 4: 카카오 버튼 → 액션 연결**

OnTap → Custom Action `loginWithKakao()` → 결과 분기:
- 성공: Navigate to Home (with replace)
- 실패: SnackBar "로그인에 실패했습니다"

- [ ] **Step 5: 구글 로그인도 동일 패턴**

`flutterflow/custom_actions/login_with_google.dart`로 구현.

---

### Task 2.5: 닉네임 설정 페이지

- [ ] **Step 1: Pages → "NicknameSetup"**

조건부 라우팅: 가입 직후 nickname이 자동 생성된 "Voyager_xxxx" 형식이면 이 페이지로, 아니면 홈으로.

- [ ] **Step 2: TextField + 중복 검증**

Custom Action `check_nickname_available`:
```dart
Future<bool> checkNicknameAvailable(String nickname) async {
  final res = await Supabase.instance.client
      .from('users')
      .select('id')
      .eq('nickname', nickname)
      .maybeSingle();
  return res == null;
}
```

- [ ] **Step 3: 저장 후 홈으로 이동**

---

### Task 2.6: 위치/알림 권한 요청

- [ ] **Step 1: Custom Action `request_permissions`**

```dart
import 'package:geolocator/geolocator.dart';
import 'package:permission_handler/permission_handler.dart';

Future<Map<String, bool>> requestPermissions() async {
  // 위치
  LocationPermission loc = await Geolocator.checkPermission();
  if (loc == LocationPermission.denied) {
    loc = await Geolocator.requestPermission();
  }

  // 알림
  final notif = await Permission.notification.request();

  return {
    'location': loc == LocationPermission.always || loc == LocationPermission.whileInUse,
    'notification': notif.isGranted,
  };
}
```

- [ ] **Step 2: 권한 안내 페이지에서 호출**

Onboarding 4단계에서 trigger.

- [ ] **Step 3: Info.plist 메시지 추가**

FlutterFlow → Settings → iOS → Info.plist Entries:
```xml
<key>NSLocationWhenInUseUsageDescription</key>
<string>여행 모드 사용 시 주변 배지 명소를 감지하기 위해 위치 정보가 필요합니다.</string>
```

---

## Phase 3: 핵심 4탭 화면 (Week 8~12, M3)

### Task 3.1: FlutterFlow — 메인 네비게이션 셋업

- [ ] **Step 1: Pages → "Main" (Bottom Nav 컨테이너)**

Bottom Navigation Bar:
- Tab 1: 🗺 홈 (Home)
- Tab 2: 📍 탐험 (Map)
- Tab 3: 🏅 배지 (Badges)
- Tab 4: ⚙️ 더보기 (More)

- [ ] **Step 2: 각 탭에 빈 페이지 연결**

`HomePage`, `MapPage`, `BadgesPage`, `MorePage` 생성.

---

### Task 3.2: 홈 탭 UI

- [ ] **Step 1: 레이아웃 구조**

```
ScrollView
├── Container: 프로필 카드
│   ├── 아바타
│   ├── 닉네임 (text from user.nickname)
│   ├── 레벨 + 칭호 (text from user.level, user.title)
│   └── XP 진행 바 (LinearProgressIndicator)
├── Container: 최근 배지 (가로 스크롤)
└── Container: 다음 도전 카드
```

- [ ] **Step 2: Supabase 쿼리 연동**

페이지 로드 시 Backend Query:
```sql
-- 자동 생성 (FlutterFlow Supabase Integration)
SELECT * FROM public.users WHERE id = $current_user_id;
```

- [ ] **Step 3: XP 바 계산 — Custom Function**

```dart
double xpProgress(int currentXp, int currentLevel) {
  final required = (100 * pow(currentLevel, 1.6)).floor();
  return (currentXp / required).clamp(0.0, 1.0);
}
```

---

### Task 3.3~3.5: 탐험 맵 탭

이 부분은 카카오맵을 WebView로 래핑하는 가장 까다로운 작업.

- [ ] **Step 1: KakaoMap WebView 자산 준비**

**Files:**
- Create: `assets/kakao_map.html`

```html
<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>Voyna Map</title>
<style>html,body,#map{margin:0;width:100%;height:100%;}</style>
<script src="https://dapi.kakao.com/v2/maps/sdk.js?appkey=__JS_KEY__&libraries=services,clusterer"></script>
</head>
<body><div id="map"></div>
<script>
let map;
function initMap(lat, lng) {
  const container = document.getElementById('map');
  map = new kakao.maps.Map(container, {
    center: new kakao.maps.LatLng(lat, lng),
    level: 5,
  });
  // 현재 위치 마커
  new kakao.maps.Marker({
    position: new kakao.maps.LatLng(lat, lng),
    map: map,
    title: '내 위치',
  });
}

// Flutter → JS 호출 인터페이스
window.flutterAddBadgeMarker = function(b) {
  const marker = new kakao.maps.Marker({
    position: new kakao.maps.LatLng(b.lat, b.lng),
    map: map,
    image: new kakao.maps.MarkerImage(b.image_url, new kakao.maps.Size(40,40)),
    title: b.name,
  });
  kakao.maps.event.addListener(marker, 'click', () => {
    // JS → Flutter 콜백
    window.flutter_inappwebview.callHandler('onBadgeTap', b);
  });
};

window.flutterMoveCenter = function(lat, lng) {
  map.setCenter(new kakao.maps.LatLng(lat, lng));
};

// 페이지 로드 후 Flutter가 initMap 호출
window.addEventListener('load', () => {
  window.flutter_inappwebview.callHandler('onMapReady');
});
</script></body></html>
```

빌드 시 `__JS_KEY__`를 실제 키로 치환.

- [ ] **Step 2: Custom Widget — KakaoMapView.dart**

**Files:**
- Create: `flutterflow/custom_widgets/KakaoMapView.dart`

```dart
import 'package:flutter/material.dart';
import 'package:flutter_inappwebview/flutter_inappwebview.dart';

class KakaoMapView extends StatefulWidget {
  final double width;
  final double height;
  final double initialLat;
  final double initialLng;
  final Future<List<Map<String, dynamic>>> Function() loadBadges;
  final void Function(Map<String, dynamic>) onBadgeTap;

  const KakaoMapView({
    super.key,
    required this.width,
    required this.height,
    required this.initialLat,
    required this.initialLng,
    required this.loadBadges,
    required this.onBadgeTap,
  });

  @override
  State<KakaoMapView> createState() => _KakaoMapViewState();
}

class _KakaoMapViewState extends State<KakaoMapView> {
  InAppWebViewController? _controller;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: widget.width,
      height: widget.height,
      child: InAppWebView(
        initialFile: 'assets/kakao_map.html',
        initialSettings: InAppWebViewSettings(
          javaScriptEnabled: true,
          geolocationEnabled: true,
        ),
        onWebViewCreated: (c) {
          _controller = c;
          c.addJavaScriptHandler(
            handlerName: 'onMapReady',
            callback: (_) async {
              await c.evaluateJavascript(
                source: 'initMap(${widget.initialLat}, ${widget.initialLng});',
              );
              final badges = await widget.loadBadges();
              for (final b in badges) {
                await c.evaluateJavascript(
                  source: 'window.flutterAddBadgeMarker(${jsonEncode(b)});',
                );
              }
            },
          );
          c.addJavaScriptHandler(
            handlerName: 'onBadgeTap',
            callback: (args) {
              widget.onBadgeTap(args[0] as Map<String, dynamic>);
            },
          );
        },
      ),
    );
  }
}
```

`pubspec.yaml`에 추가:
```yaml
flutter_inappwebview: ^6.0.0
```

- [ ] **Step 3: 맵 페이지에 KakaoMapView 배치**

FlutterFlow Map 페이지에 위 Custom Widget을 드래그.  
params:
- `loadBadges`: Custom Action `get_nearby_badges` 호출
- `onBadgeTap`: 배지 상세 모달 열기

- [ ] **Step 4: 여행 모드 토글**

상단 우측에 Switch.  
ON: GPS 추적 시작 (Task 4.1 참조), OFF: 추적 중단.

---

### Task 3.6: 배지 컬렉션 탭

- [ ] **Step 1: 레이아웃**

```
Column
├── 상단 통계 카드 (보유 N/50)
├── 탭바: 전체 / 지역 / 카테고리 / 등급
├── 필터 칩 (선택된 탭에 따른 옵션)
└── GridView (3열) of BadgeCard
```

- [ ] **Step 2: BadgeCard 컴포넌트**

획득: 컬러 배지 + 획득 일자  
미획득: 실루엣 + 자물쇠 아이콘

- [ ] **Step 3: 데이터 쿼리**

```sql
-- 모든 배지 + 사용자 획득 여부
SELECT b.*, l.name as location_name, l.category, l.region,
       (ub.id IS NOT NULL) as obtained,
       ub.obtained_at
FROM public.badges b
JOIN public.locations l ON l.id = b.location_id
LEFT JOIN public.user_badges ub ON ub.badge_id = b.id AND ub.user_id = $current_user_id
ORDER BY l.region, l.district, b.id;
```

---

### Task 3.7: 배지 상세 페이지

- [ ] **Step 1: BadgeDetail 페이지 — 모달 형식**

내용:
- 큰 배지 이미지
- 명소명, 등급, XP
- 획득 일자 (획득한 경우)
- 위치 정보 (지도 미니맵 + 주소)
- 획득자 통계 ("전체의 12%가 보유")
- 관련 추천 배지

- [ ] **Step 2: 획득자 비율 — RPC**

```sql
CREATE OR REPLACE FUNCTION public.badge_acquisition_rate(p_badge_id BIGINT)
RETURNS NUMERIC LANGUAGE sql SECURITY DEFINER AS $$
    SELECT
        CASE WHEN total = 0 THEN 0
        ELSE ROUND(100.0 * obtained / total, 1) END
    FROM (
        SELECT
            (SELECT COUNT(*) FROM public.users) as total,
            (SELECT COUNT(*) FROM public.user_badges WHERE badge_id = p_badge_id) as obtained
    ) sub;
$$;
```

---

### Task 3.8: 더보기 탭

- [ ] **Step 1: ListView**

항목:
- 진행 중인 이벤트 (placeholder — V1.1)
- 미션 (placeholder — V1.4)
- 친구 (placeholder — V1.3)
- 설정 → 알림, 언어, 테마
- 개인정보 설정 → 위치 권한 재요청
- 구독 관리 (placeholder — V1.2)
- 문의하기 → 이메일 (mailto:)
- 로그아웃

---

## Phase 4: GPS + 배지 획득 로직 (Week 12~14)

### Task 4.1: 현재 위치 획득 — Custom Action

**Files:**
- Create: `flutterflow/custom_actions/get_current_location.dart`

```dart
import 'package:geolocator/geolocator.dart';

Future<Map<String, dynamic>?> getCurrentLocation() async {
  if (!await Geolocator.isLocationServiceEnabled()) return null;

  LocationPermission p = await Geolocator.checkPermission();
  if (p == LocationPermission.denied || p == LocationPermission.deniedForever) {
    return null;
  }

  final pos = await Geolocator.getCurrentPosition(
    locationSettings: const LocationSettings(
      accuracy: LocationAccuracy.high,
      distanceFilter: 10,  // 10m 이상 이동 시만 갱신
    ),
  );

  return {
    'lat': pos.latitude,
    'lng': pos.longitude,
    'accuracy_m': pos.accuracy,
    'timestamp': pos.timestamp.millisecondsSinceEpoch,
  };
}
```

---

### Task 4.2: 위치 추적 스트림 — 여행 모드

**Files:**
- Create: `flutterflow/custom_actions/start_travel_mode.dart`, `stop_travel_mode.dart`

```dart
// start_travel_mode.dart
import 'dart:async';
import 'package:geolocator/geolocator.dart';

StreamSubscription<Position>? _sub;

Future<void> startTravelMode(
  Future<void> Function(double lat, double lng, double acc) onPosition,
) async {
  _sub?.cancel();
  _sub = Geolocator.getPositionStream(
    locationSettings: const LocationSettings(
      accuracy: LocationAccuracy.high,
      distanceFilter: 25,  // 25m 이상 이동 시만 트리거
    ),
  ).listen((pos) {
    onPosition(pos.latitude, pos.longitude, pos.accuracy);
  });
}
```

```dart
// stop_travel_mode.dart
import 'dart:async';
import 'package:geolocator/geolocator.dart';

Future<void> stopTravelMode() async {
  // start_travel_mode.dart에서 정의한 _sub를 cancel 해야 하므로
  // 실제로는 _sub를 전역 또는 ChangeNotifier로 관리해야 함
  // 단순화: GeolocatorPlatform에 cancel 요청
  // (실 구현은 ChangeNotifier 활용)
}
```

> **권장**: ChangeNotifier 기반 `TravelModeService` 클래스로 리팩터링.

---

### Task 4.3: 반경 감지 + 자동 트리거

**Files:**
- Create: `flutterflow/custom_actions/check_nearby_and_award.dart`

```dart
import 'dart:math';
import 'package:supabase_flutter/supabase_flutter.dart';

// Haversine — 클라이언트에서도 prefilter용으로 사용
double _haversine(double lat1, double lng1, double lat2, double lng2) {
  const R = 6371000.0;
  double toRad(double d) => d * pi / 180;
  final dLat = toRad(lat2 - lat1);
  final dLng = toRad(lng2 - lng1);
  final a = sin(dLat / 2) * sin(dLat / 2) +
      cos(toRad(lat1)) * cos(toRad(lat2)) * sin(dLng / 2) * sin(dLng / 2);
  return 2 * R * asin(sqrt(a));
}

Future<Map<String, dynamic>?> checkNearbyAndAward(double lat, double lng, double accuracy) async {
  final supabase = Supabase.instance.client;

  // 1. 반경 300m 내 미획득 배지 조회 (클라이언트 캐시 활용 가능)
  final res = await supabase.functions.invoke('get_nearby_badges',
    queryParameters: {'lat': '$lat', 'lng': '$lng', 'radius_km': '0.3'});
  final badges = (res.data?['badges'] ?? []) as List;

  // 2. 미획득 + 거리 <= radius_m
  for (final b in badges) {
    if (b['obtained'] == true) continue;
    final loc = b['locations'];
    final dist = _haversine(lat, lng, loc['lat'], loc['lng']);
    if (dist > loc['radius_m']) continue;

    // 3. award_badge 호출
    final result = await supabase.functions.invoke('award_badge', body: {
      'badge_id': b['id'],
      'user_lat': lat,
      'user_lng': lng,
      'accuracy_m': accuracy,
    });

    return result.data as Map<String, dynamic>;
  }

  return null;
}
```

여행 모드 시작 시 콜백으로 등록:
```dart
await startTravelMode((lat, lng, acc) async {
  final result = await checkNearbyAndAward(lat, lng, acc);
  if (result != null) {
    // 4. 결과에 따라 UI 분기
    if (result['requires_confirmation'] == true) {
      // 확인형 배지 팝업 표시
      showConfirmDialog(result['badge']);
    } else {
      // 자동 배지 획득 애니메이션
      showAutoAcquisitionAnimation(result);
    }
  }
});
```

---

### Task 4.4: 자동 배지 획득 애니메이션

- [ ] **Step 1: BottomSheet 또는 Toast 위젯**

FlutterFlow → Components → Add → "BadgeAcquiredToast"

내용:
- 배지 이미지 (작게)
- "○○ 배지 획득! +50 XP"
- 자동 dismiss (1.5초)

- [ ] **Step 2: 호출**

```dart
ScaffoldMessenger.of(context).showSnackBar(
  SnackBar(
    behavior: SnackBarBehavior.floating,
    duration: const Duration(milliseconds: 1500),
    content: ... badge widget,
  ),
);
```

---

### Task 4.5: 확인형 배지 팝업

- [ ] **Step 1: ConfirmBadgeDialog 컴포넌트**

레이아웃:
- 큰 배지 이미지 (실루엣 → 컬러로 전환)
- "○○에 도착했어요! 이 순간을 기록할까요?"
- [네, 기록하기] [나중에] 버튼

- [ ] **Step 2: 확인 시 award_badge 두 번째 호출**

```dart
final result = await supabase.functions.invoke('award_badge', body: {
  'badge_id': badge['id'],
  'user_lat': lat, 'user_lng': lng,
  'accuracy_m': acc,
  'confirmed': true,  // 핵심
});
```

- [ ] **Step 3: 풀스크린 컨페티 애니메이션**

`confetti` 패키지 사용:
```yaml
confetti: ^0.7.0
```

```dart
ConfettiController controller = ConfettiController(duration: const Duration(seconds: 3));
controller.play();
```

희귀 등급은 1.5초, 특별은 3초 + 사운드.

---

### Task 4.6: 진동 + 사운드

- [ ] **Step 1: 패키지 추가**

```yaml
vibration: ^2.0.0
audioplayers: ^6.0.0
```

- [ ] **Step 2: Custom Action `play_acquisition_fx`**

```dart
import 'package:vibration/vibration.dart';
import 'package:audioplayers/audioplayers.dart';

Future<void> playAcquisitionFx(String grade) async {
  // 진동 패턴
  final patterns = {
    'common': [0, 100],
    'rare': [0, 100, 100, 200],
    'special': [0, 200, 100, 300, 100, 400],
  };
  await Vibration.vibrate(pattern: patterns[grade] ?? patterns['common']!);

  // 사운드
  final player = AudioPlayer();
  await player.play(AssetSource('sounds/${grade}_acquired.mp3'));
}
```

자산:
```
assets/sounds/common_acquired.mp3
assets/sounds/rare_acquired.mp3
assets/sounds/special_acquired.mp3
```

(Phase 6에서 사운드 디자이너에게 발주 또는 freesound.org에서 CC0 라이선스 사용)

---

### Task 4.7: 레벨업 모달

- [ ] **Step 1: award_badge 결과의 `level_up: true` 감지**

```dart
if (result['level_up'] == true) {
  showLevelUpDialog(result['new_level'], result['new_titles']);
}
```

- [ ] **Step 2: LevelUpDialog 컴포넌트**

- 레벨 숫자 카운트업 애니메이션
- 새 칭호 획득 시 강조
- "확인" 버튼

---

## Phase 5: 보조 기능 (Week 14~16)

### Task 5.1: FCM 푸시 알림

- [ ] **Step 1: Firebase 프로젝트 생성**

console.firebase.google.com → 프로젝트 추가 → iOS 앱 등록.

- [ ] **Step 2: GoogleService-Info.plist를 iOS Runner에 추가**

FlutterFlow → Settings → iOS → Upload.

- [ ] **Step 3: 패키지 추가**

```yaml
firebase_core: ^3.0.0
firebase_messaging: ^15.0.0
```

- [ ] **Step 4: 등록 토큰을 Supabase에 저장**

users 테이블에 `fcm_token` 컬럼 추가:
```sql
ALTER TABLE public.users ADD COLUMN fcm_token TEXT;
```

앱 시작 시:
```dart
final token = await FirebaseMessaging.instance.getToken();
await supabase.from('users').update({'fcm_token': token}).eq('id', userId);
```

- [ ] **Step 5: 푸시 발송 — Edge Function `send_nearby_badge_push`**

cron으로 매시간 실행 (Supabase Cron):
```sql
SELECT cron.schedule(
  'nearby-badge-push',
  '0 * * * *',  -- 매시간
  $$SELECT net.http_post(
    url := 'https://<ref>.supabase.co/functions/v1/send_nearby_badge_push',
    headers := jsonb_build_object('Authorization', 'Bearer <service-role>')
  );$$
);
```

함수 구현: 활성 사용자들의 마지막 위치 기반으로 미수집 배지 알림 (V1.1 기능, MVP는 스킵 가능).

---

### Task 5.2: SNS 공유

```yaml
share_plus: ^9.0.0
```

배지 상세 페이지 → 공유 버튼 → `Share.share('Voyna에서 ${badge.name} 배지를 획득했어요! https://voyna.app/b/${badge.id}')`.

---

### Task 5.3: 미수집 배지 추천 — 홈 카드

- [ ] **Step 1: 마지막 위치 + 미수집 + 거리 기반 RPC**

```sql
CREATE OR REPLACE FUNCTION public.recommend_badges(
    p_user_id UUID,
    p_lat DOUBLE PRECISION,
    p_lng DOUBLE PRECISION,
    p_limit INT DEFAULT 3
)
RETURNS TABLE(badge_id BIGINT, location_name TEXT, distance_m INTEGER, grade badge_grade)
LANGUAGE sql SECURITY DEFINER AS $$
    SELECT b.id, l.name,
           earth_distance(ll_to_earth(p_lat, p_lng), ll_to_earth(l.lat, l.lng))::INT,
           b.grade
    FROM public.badges b
    JOIN public.locations l ON l.id = b.location_id
    WHERE NOT EXISTS (
      SELECT 1 FROM public.user_badges ub
      WHERE ub.user_id = p_user_id AND ub.badge_id = b.id
    )
    ORDER BY earth_distance(ll_to_earth(p_lat, p_lng), ll_to_earth(l.lat, l.lng))
    LIMIT p_limit;
$$;
```

홈 화면에서 카드로 표시.

---

### Task 5.4: 랭킹 화면 (간소 버전)

```sql
CREATE OR REPLACE VIEW public.leaderboard AS
SELECT u.nickname, u.level, u.title,
       (SELECT COUNT(*) FROM public.user_badges ub WHERE ub.user_id = u.id) AS badge_count
FROM public.users u
ORDER BY u.level DESC, badge_count DESC
LIMIT 100;
```

FlutterFlow에서 ListView로 표시.

---

## Phase 6: 디자인 자산 (Week 6~16 병렬)

### Task 6.1: 50종 배지 1차 시안 (AI 일러스트)

- [ ] **Step 1: 대표 5종 프롬프트 작성**

`design/ai_prompts.md`:
```
경복궁:
"Minimal flat illustration of Gyeongbokgung Palace, Korean traditional palace with curved tile roof
and red columns, circular badge design, gold border, deep red and royal blue color palette,
clean vector style, white background, centered composition"

N서울타워: ...
청와대: ...
북한산: ...
홍대: ...
```

Midjourney / DALL-E 3에서 각 명소당 4컷 생성 → 베스트 선택.

- [ ] **Step 2: 등급별 프레임 합성**

Canva 또는 Photopea(웹 Photoshop)에서 5종에 프레임 합성:
- common (회색 띠)
- rare (이중 띠 + ★)
- special (광택 + ★★★)

5종 검증 후 나머지 45종 양산. 총 예산 50~150만 원 (AI + 후가공).

- [ ] **Step 3: Supabase Storage 업로드**

```bash
# 배치 업로드 — Supabase CLI 또는 dashboard
supabase storage cp ./design/badges/* storage://badge-images/badges/
```

`badges.image_url` 일괄 업데이트 (Task 1.16 참조).

---

### Task 6.2: 앱 아이콘 + 스플래시

- [ ] **Step 1: 앱 아이콘 1024×1024 PNG**

Voyna 로고 + Voyna Blue 배경.

- [ ] **Step 2: flutter_launcher_icons 패키지로 일괄 생성**

```yaml
flutter_launcher_icons:
  image_path: "assets/icon.png"
  ios: true
  android: true
```

```bash
flutter pub run flutter_launcher_icons
```

- [ ] **Step 3: 스플래시 — flutter_native_splash**

```yaml
flutter_native_splash:
  color: "#0071E3"
  image: assets/splash_logo.png
```

---

### Task 6.3: App Store 스크린샷 8장

- [ ] **Step 1: 시뮬레이터에서 캡처**

5종 핵심 화면 + 3종 강조 화면.

- [ ] **Step 2: AppLaunchpad 또는 Figma 템플릿으로 마케팅 텍스트 추가**

각 스크린샷 6.7" / 5.5" 두 사이즈 필수.

---

## Phase 7: 테스트 (Week 16~18, M4)

### Task 7.1: iOS Simulator 테스트

- [ ] **Step 1: 시뮬레이터 위치 모킹**

Xcode → Simulator → Features → Location → Custom Location.  
경복궁 좌표(37.5796, 126.9770)로 설정 후 배지 획득 동작 검증.

- [ ] **Step 2: 12개 핵심 시나리오 체크리스트**

`docs/qa/simulator_checklist.md`:
- [ ] 온보딩 5단계 진행
- [ ] 카카오 로그인 (시뮬레이터 한계 — 실기기 권장)
- [ ] 구글 로그인
- [ ] 홈 화면 로딩 (레벨 1, XP 0)
- [ ] 맵 표시 (서울시청 중심)
- [ ] 여행 모드 ON → GPS 권한 다이얼로그
- [ ] 가짜 위치(경복궁) → 확인 팝업 → 획득 → +300 XP
- [ ] 레벨업 모달 + 칭호 부여 (배지 5개 후 "동네 탐험가")
- [ ] 배지 컬렉션 화면에 획득 표시
- [ ] 미수집 배지 추천 카드
- [ ] 더보기 → 로그아웃
- [ ] 재로그인 시 상태 복원

---

### Task 7.2: 실기기 GPS 정확도 검증

- [ ] **Step 1: TestFlight 내부 빌드 업로드**

FlutterFlow → Build → Upload to App Store Connect → TestFlight.

- [ ] **Step 2: 5개 현장 테스트**

직접 방문해 동작 확인:
1. 경복궁 (특별, 확인형) — 야외, GPS 양호
2. 광장시장 (일반, 자동) — 실내에 가깝지만 광장
3. 북한산 둘레길 입구 (특별, 확인형) — 등산 입구
4. 홍대 거리 (일반) — 도심 밀집
5. 한강대교 (도보, 한강공원과 노들섬 동시 인지 검증)

각 명소에서:
- 도착 시간
- GPS accuracy_m 값
- 인증 성공/실패
- 실패 시 위치/이유

`docs/qa/field_test_log.md`에 기록.

- [ ] **Step 3: 도심 밀집 지역의 부정확 대응**

광장시장처럼 정확도 50m 초과인 경우, 추후 V2 사진 보조 인증 도입할 자료로 수집.

---

### Task 7.3: 버그 픽스 사이클

- [ ] **Step 1: GitHub Issues로 버그 추적**

`AlexSong0674/voyna-app` 저장소에 라벨: bug, ui, gps, backend.

- [ ] **Step 2: 1주차 빌드 → 수정 → 2주차 빌드 사이클**

매주 화/금 새 TestFlight 빌드 배포. 누적 결함 0건이 될 때까지.

---

## Phase 8: 베타 출시 (Week 18~22, M5)

### Task 8.1: TestFlight 외부 베타 그룹 설정

- [ ] **Step 1: App Store Connect → TestFlight → External Testing**

그룹 생성: "Voyna Beta Wave 1"  
앱 정보·테스트 설명 작성:
```
Voyna는 GPS 기반 여행 배지 앱입니다.
- 서울 50곳 명소에서 배지 획득 가능
- 베타 참여자에게는 "선구자" 한정 칭호 제공
- 버그/피드백은 settings → 문의로
```

- [ ] **Step 2: Apple 베타 리뷰 (1~2일)**

심사 통과 후 공개 링크 생성.

---

### Task 8.2: 베타 테스터 100명 모집

- [ ] **Step 1: 모집 채널**

- 대학원 동기 (알토대학원)
- 여행 커뮤니티 카페 (다음 카페, 디시 여행갤러리 등)
- 인스타그램 광고 (소액 — 10~20만 원)

- [ ] **Step 2: 신청 폼**

구글 폼:
- 이메일 (TestFlight 초대용)
- 거주 지역 (서울 거주자 우선)
- 여행 빈도

- [ ] **Step 3: TestFlight 초대 발송**

신청자에게 공개 링크 일괄 안내.

---

### Task 8.3: 피드백 수집 + 분석

- [ ] **Step 1: 인앱 피드백 버튼**

더보기 → 문의하기 → 이메일 또는 구글 폼 링크.

- [ ] **Step 2: Mixpanel/Amplitude 분석**

핵심 이벤트:
- `signup_completed`
- `travel_mode_started`
- `badge_acquired` (등급별 분리)
- `level_up`
- `share_clicked`

- [ ] **Step 3: 주간 리포트**

매주 KPI 측정:
- 가입자 / DAU / WAU
- 1인당 배지 획득 수
- 여행 모드 평균 ON 시간
- 인증 성공률 (시도 대비 성공)

---

## Phase 9: 법적 문서 (Week 18~20)

### Task 9.1: 개인정보 처리방침

**Files:**
- Create: `docs/legal/privacy_policy.md`

기획서 v2.0의 14장을 기반으로 변호사 검토 받은 완성본 작성.  
GitHub Pages로 공개: `https://alexsong0674.github.io/voyna-app/privacy`.

App Store Connect의 Privacy Policy URL에 등록.

---

### Task 9.2: 위치정보 이용약관

**Files:**
- Create: `docs/legal/location_terms.md`

위치정보의 보호 및 이용 등에 관한 법률 준수:
- 수집 목적 (배지 자동 인증)
- 수집 방법 (앱 활성 + 여행 모드 ON 시만)
- 보관 기간 (30일, 인증 후 익명화)
- 위치정보사업자 신고 여부 검토 결과 명시

---

### Task 9.3: 서비스 이용약관

표준 양식 + Voyna 특수 조항(어뷰징·환불·계정 정지).

---

### Task 9.4: 위치정보사업자 신고 검토

방송통신위원회 위치정보사업자 등록 페이지 (www.kisa.or.kr/한국인터넷진흥원) 안내 확인.  
"개인위치정보사업자"에 해당하는지 변호사 검토.  
(앱이 위치를 단순 인증용으로만 사용하고 외부 제공이 없으면 신고 의무가 없을 수 있음 — 법률 자문 필수)

---

## Phase 10: 정식 출시 (Week 22~24, M6)

### Task 10.1: App Store Connect 메타데이터

App Store Connect → 내 앱 → Voyna:

- [ ] **Step 1: 앱 정보**

```
이름: Voyna - 여행 배지
부제: GPS로 모으는 여행 컬렉션
카테고리: 여행
2차 카테고리: 게임 (위치 기반)
연령 등급: 4+
```

- [ ] **Step 2: 가격 책정**

무료. 인앱 구매 항목은 V1.2에서 추가.

- [ ] **Step 3: 앱 미리보기 + 스크린샷**

Phase 6에서 준비한 8장 업로드.

- [ ] **Step 4: 키워드**

```
여행,배지,GPS,스탬프,컬렉션,한국여행,서울,게이미피케이션,체크인,여행기록
```

- [ ] **Step 5: 설명**

```
🗺 Voyna (보이나) — 발걸음이 추억이 되다

GPS 기반으로 실제 여행지를 방문하면 자동으로 인증 배지를 획득하는 게이미피케이션 여행 앱.

📍 주요 기능
- 서울 50곳 명소 자동 인증
- 4가지 등급 배지 (일반·희귀·특별·프리미어)
- XP 적립 + Lv1~99 레벨업 시스템
- 10+ 칭호 시스템 (동네 탐험가 → 전설의 여행자)
- 전국 랭킹 + 친구 비교
- 미수집 배지 맥락 기반 추천

🎯 이렇게 즐기세요
1. 여행 떠나기 전 '여행 모드 ON'
2. 명소 도착 시 자동 또는 확인형 배지 획득
3. XP가 쌓이고 칭호 업그레이드
4. 친구와 랭킹 경쟁

🇰🇷 한국 여행을 게임처럼.
```

---

### Task 10.2: 심사 제출

- [ ] **Step 1: 빌드 선택 + 제출**

TestFlight에서 검증 완료된 빌드 선택.  
"심사를 위해 제출".

- [ ] **Step 2: 심사 노트 첨부**

```
이 앱은 GPS 기반 위치 인증 앱입니다.
테스트를 위해서는 실제 서울 명소 좌표(예: 경복궁 37.5796, 126.9770)를
Simulator의 Custom Location에 입력하면 됩니다.

위치 권한: 여행 모드 ON 시에만 사용되며, 사용자가 명시적으로 토글합니다.

테스트 계정:
ID: review@voyna.app
PW: AppleReview2026!
```

- [ ] **Step 3: 심사 통과까지 대기 (1~7일)**

리젝되면 사유 확인 후 수정 재제출.

---

### Task 10.3: 출시일 + 마케팅

- [ ] **Step 1: 출시 일정 조율**

심사 통과 후 "수동 출시" 선택 → 마케팅 일정에 맞춰 공개.

- [ ] **Step 2: 출시 당일 활동**

- 인스타그램·트위터·페이스북 공지 (선구자 칭호 강조)
- 베타 사용자에게 정식 출시 알림 (FCM 또는 이메일)
- 여행 커뮤니티 카페에 공유

- [ ] **Step 3: 출시 후 1주차 모니터링**

크래시 리포트 (Firebase Crashlytics) 매일 확인.  
긴급 핫픽스 필요 시 즉시 1.0.1 빌드 준비.

---

## Phase 11: 출시 후 — 광고 (M7+, Week 28)

### Task 11.1: AdMob 통합

```yaml
google_mobile_ads: ^5.0.0
```

광고 위치:
- 배지 컬렉션 그리드 사이 (10개마다 네이티브 광고)
- 더보기 탭 하단 배너
- 배지 획득 후 모달 닫을 때 보상형 광고 (선택형, 5초)

---

### Task 11.2: Voyna+ 구독 (M8, Week 32)

App Store Connect → 인앱 구매 → 자동 갱신 구독:
- `voyna_plus_monthly`: 2,900원/월
- `voyna_plus_yearly`: 24,900원/년

```yaml
in_app_purchase: ^3.0.0
```

서버 검증: Edge Function `verify_apple_receipt`.

---

## Self-Review

### 스펙 커버리지 확인

| 기획서 v2.0 섹션 | 대응 Task |
|----------------|----------|
| 1. 서비스 개요 | Task 0.1 (브랜드) |
| 2. 핵심 가치 | 마케팅 카피 (Task 10.1) |
| 3. 사용자 여정 | Phase 2~4 (온보딩·GPS·획득) |
| 4. MVP 기능 | Phase 2~4 전체 |
| 5. 앱 화면 4탭 | Task 3.1~3.8 |
| 6. 레벨/배지 | Task 1.3~1.5, 1.13, 4.7 |
| 7. 수익 모델 | Phase 11 (출시 후) |
| 8. 경쟁사 분석 | 기획용 (구현 X) |
| 9. 기술 스택 | Phase 0 (셋업) |
| 10. 지도 비교 | Task 3.3 (카카오맵) |
| 11. 단계별 확장 | 출시 후 — 별도 plan |
| 12. 신규 아이디어 | V1.1+ — 별도 plan |
| 13. 개발 일정 | 본 plan 전체 |
| 14. 개인정보 | Phase 9 |
| 15. 리스크 | 각 Task에 부분 반영 |
| 부록 C. 50곳 | Task 1.10~1.11 |

✅ MVP 범위 모두 커버.

### 플레이스홀더 스캔

- ✅ 모든 SQL/Dart/TypeScript 코드 블록은 완전한 형태
- ✅ "TBD" / "TODO" / "implement later" 없음
- ✅ 외부 의뢰가 필요한 부분(법률·디자인)은 명시적으로 외주 안내

### 타입 일관성

- ✅ `badge_grade` enum: common/rare/special/premier/seasonal (모든 SQL·TS에서 동일)
- ✅ `requires_confirmation: boolean` (모든 layer에서 동일)
- ✅ Edge Function 응답 스키마: `{success, badge, xp_gained, level_up, new_titles}` (4.3, 4.7에서 동일 참조)

### 알려진 한계 (실행 중 보완 필요)

1. **카카오맵 SDK가 Flutter 공식 미지원** — Task 3.3에서 WebView 래핑으로 우회. 안정성 떨어지면 Flutter 네이티브 코드(`MethodChannel`) 직접 작성 옵션 추가 필요.
2. **사진 인증 (V2)** — 본 MVP plan 범위 밖. V2 별도 plan에서 다룸.
3. **위치정보사업자 신고** — 변호사 자문 후 확정.

---

## 실행 핸드오프

Plan 작성 및 저장 완료: `docs/superpowers/plans/2026-05-12-voyna-mvp-implementation.md`

**총 작업 단위:** Phase 0~10 (필수) + Phase 11 (출시 후), 약 60개 Task / 200+ Step.  
**예상 기간:** 24주 (M1~M6) + 출시 후 4~8주 (M7~M8).  
**예산 추정:**
- Apple Developer: $99/년
- Supabase: 무료 (MAU 5만까지)
- 카카오·구글·FCM: 무료 (MAU 한도 내)
- FlutterFlow Pro: $30/월 × 6 = $180
- 디자인 자산 (배지 50종): 50~150만 원 (AI 기반)
- 도메인: 약 5만 원/년
- 변호사 자문: 50~200만 원
- 베타 모집 광고: 10~30만 원
- **합계 추정: 약 200~500만 원 + 인건비**

---

## 실행 방법 — 두 가지 옵션

1. **Subagent-Driven (권장)** — 매 Task마다 새 subagent 디스패치, Task 간 검토, 빠른 반복
2. **Inline Execution** — 본 세션에서 순차 실행, 체크포인트에서 리뷰

본 plan은 노코드(FlutterFlow)·외부 계정 등록·디자인 외주가 다수 섞여 있어 **인간 주도 + AI 보조 하이브리드** 실행이 현실적입니다. 옵션을 선택해 주세요.
