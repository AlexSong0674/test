# Voyna Demo App Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 3일 안에(2026-05-13 수 ~ 2026-05-15 금) Voyna 데모용 웹 앱을 `AlexSong0674/Voyna-Demo` 리포에 구축하고 GitHub Pages로 배포한다.

**Architecture:** Vite + Vanilla TypeScript SPA. Firebase Google 인증 + 카카오맵 JS SDK + 정적 JSON 카탈로그 + localStorage 사용자 상태. 4탭 라우팅(홈/맵/배지/더보기). 모든 비즈니스 로직 클라이언트 측. GitHub Actions로 main push 시 Pages 자동 배포.

**Tech Stack:** Vite 5, TypeScript 5, Firebase Web SDK 10 (Google Auth), 카카오맵 JS SDK v3, Vitest(단위 테스트), GitHub Actions, GitHub Pages.

**Spec Reference:** [`docs/superpowers/specs/2026-05-13-voyna-demo-design.md`](../specs/2026-05-13-voyna-demo-design.md)

---

## 사전 준비 (코드 시작 전 30분~1시간)

이 plan은 다음이 준비된 상태로 시작한다고 가정한다. 누락 시 Phase 0에서 처리:
- GitHub 리포 `AlexSong0674/Voyna-Demo` 생성됨 (빈 리포, README 없음)
- Node.js 20+ 설치됨
- Git 사용자 설정(`user.name`, `user.email`)
- 카카오 개발자 계정 (https://developers.kakao.com)
- Firebase 콘솔 접근 (https://console.firebase.google.com)

**작업 디렉터리(권장):** `C:\Users\송 하 준\Documents\알토대학원\수업과제\벤처 스타트업\Voyna-Demo`
(이하 모든 경로는 이 리포 루트 기준)

---

## File / Component Structure

| 위치 | 역할 |
|------|------|
| `package.json`, `tsconfig.json`, `vite.config.ts` | 빌드 설정 |
| `index.html` | SPA 엔트리 |
| `.env.example` / `.env.local` | 환경변수 템플릿(커밋) / 실제값(미커밋) |
| `.gitignore` | node_modules, dist, .env.local 제외 |
| `.github/workflows/deploy.yml` | main push → Pages 자동 배포 |
| `src/main.ts` | 부트스트랩 + 라우터 진입 |
| `src/core/router.ts` | 4탭 + 로그인 라우팅 |
| `src/core/state.ts` | localStorage 래퍼 (사용자 상태) |
| `src/core/geo.ts` | Haversine 거리 + GPS 획득 |
| `src/core/catalog.ts` | locations.json / badges.json 로더 |
| `src/core/badge-engine.ts` | 거리 판정·XP·레벨·칭호 체크 |
| `src/core/titles.ts` | 칭호 조건표 + 평가 함수 |
| `src/core/levels.ts` | 레벨업 XP 공식 |
| `src/auth/firebase.ts` | Firebase init |
| `src/auth/login-page.ts` | 구글 로그인 화면 |
| `src/pages/home.ts` | 홈 탭 렌더 |
| `src/pages/map.ts` | 카카오맵 + 텔레포트 |
| `src/pages/badges.ts` | 컬렉션 그리드 |
| `src/pages/more.ts` | 프로필·리셋 |
| `src/components/tab-bar.ts` | 하단 4탭 |
| `src/components/badge-card.ts` | 배지 카드 (잠금/획득) |
| `src/components/badge-acquired-modal.ts` | 배지 획득 팝업 |
| `src/components/level-up-modal.ts` | 레벨업 모달 |
| `src/components/title-toast.ts` | 칭호 토스트 |
| `src/data/locations.json` | 31곳 명소 데이터 |
| `src/data/badges.json` | 31종 배지 메타데이터 |
| `src/styles/main.css` | 브랜드 컬러 + 공통 스타일 |
| `public/badges/*.png` | 핵심 5~10 배지 이미지 + locked.png |
| `tests/core/*.test.ts` | 단위 테스트 (engine/geo/state/levels) |
| `docs/DEMO_SCRIPT.md` | 시연 진행 시나리오 |
| `docs/KAKAO_FIREBASE_SETUP.md` | 키 발급 가이드 |

---

## 일정 매핑

| 단계 | 작업 | 권장 일자 |
|------|------|----------|
| Phase 0 | 계정·키 발급, 리포 클론·초기화 | 수 오전 |
| Phase 1 | Vite 프로젝트 셋업 + 환경변수 | 수 오전 |
| Phase 2 | 핵심 도메인 모듈 (TDD) | 수 오후 |
| Phase 3 | 데이터 카탈로그 (locations/badges JSON) | 수 오후 |
| Phase 4 | Firebase Google 로그인 | 수 저녁 |
| Phase 5 | 4탭 라우터 + 스켈레톤 페이지 | 목 오전 |
| Phase 6 | 카카오맵 + POI + 텔레포트 | 목 오후 |
| Phase 7 | 배지 획득 모달 + 레벨업/칭호 애니메이션 | 목 저녁 |
| Phase 8 | 홈/배지/더보기 탭 완성 | 금 오전 |
| Phase 9 | 핵심 배지 이미지 AI 생성·배치 | 금 오전(병행) |
| Phase 10 | GitHub Actions Pages 배포 | 금 오후 |
| Phase 11 | DEMO_SCRIPT 작성 + 모바일 실기기 리허설 | 금 저녁 |

---

## Phase 0: 계정·키·리포 준비

### Task 0.1: GitHub 리포 초기화 및 로컬 클론

- [ ] **Step 1: 사용자에게 리포 생성 확인**

확인: `https://github.com/AlexSong0674/Voyna-Demo` 가 존재하고 빈 상태인지. 없으면 https://github.com/new 에서 이름 `Voyna-Demo`, Public, 초기화 옵션 모두 해제로 생성.

- [ ] **Step 2: 로컬 디렉터리 생성 후 git init**

```bash
mkdir -p "/c/Users/송 하 준/Documents/알토대학원/수업과제/벤처 스타트업/Voyna-Demo"
cd "/c/Users/송 하 준/Documents/알토대학원/수업과제/벤처 스타트업/Voyna-Demo"
git init
git branch -M main
git remote add origin https://github.com/AlexSong0674/Voyna-Demo.git
```

- [ ] **Step 3: 초기 README + .gitignore 생성**

`README.md`:
```markdown
# Voyna Demo

알토대학원 벤처 스타트업 수업 발표 데모용 웹 앱.

본 프로젝트의 12주 네이티브 앱 출시 일정과는 별개의 시연용 MVP이다.

- 라이브 데모: https://alexsong0674.github.io/Voyna-Demo/
- 설계 명세: [기획서 리포의 spec](https://github.com/AlexSong0674/test/blob/main/docs/superpowers/specs/2026-05-13-voyna-demo-design.md)

## 개발

```bash
npm install
cp .env.example .env.local   # 키 채우기
npm run dev
```
```

`.gitignore`:
```
node_modules
dist
.env.local
.env.*.local
.DS_Store
.vite
coverage
*.log
```

- [ ] **Step 4: 초기 커밋·푸시**

```bash
git add README.md .gitignore
git commit -m "chore: 리포 초기화"
git push -u origin main
```

### Task 0.2: 카카오 JavaScript 키 발급

- [ ] **Step 1: 카카오 개발자 콘솔에서 앱 생성**

`https://developers.kakao.com/console/app` → "애플리케이션 추가" → 앱 이름 `Voyna-Demo` → 저장.

- [ ] **Step 2: 플랫폼·도메인 등록**

생성된 앱 → "플랫폼" → Web 플랫폼 등록 → 사이트 도메인:
- `http://localhost:5173`
- `https://alexsong0674.github.io`

- [ ] **Step 3: JavaScript 키 복사**

"앱 키" → "JavaScript 키" 값 복사. `.env.local`에 `VITE_KAKAO_MAP_KEY=...`로 저장 예정.

### Task 0.3: Firebase 프로젝트 + Google 인증 활성화

- [ ] **Step 1: Firebase 프로젝트 생성**

`https://console.firebase.google.com` → 프로젝트 추가 → 이름 `voyna-demo` → Google Analytics 비활성화 → 생성.

- [ ] **Step 2: 웹 앱 등록**

프로젝트 개요 → 웹 아이콘(</>) → 앱 별칭 `Voyna-Demo Web` → 호스팅 설정 없음 → 등록. 표시되는 `firebaseConfig` 6개 값(apiKey, authDomain, projectId, storageBucket, messagingSenderId, appId) 메모.

- [ ] **Step 3: Google 인증 공급자 활성화**

좌측 메뉴 Authentication → "시작하기" → Sign-in method → Google → 사용 설정 → 프로젝트 지원 이메일 선택 → 저장.

- [ ] **Step 4: 인증 도메인 등록**

Authentication → Settings → 승인된 도메인 → `localhost`는 기본 포함. `alexsong0674.github.io` 추가.

- [ ] **Step 5: 키 메모 보관**

이 6개 값은 Task 1.3에서 `.env.local`에 작성한다. 일단 안전한 곳에 임시 메모.

---

## Phase 1: Vite 프로젝트 셋업

### Task 1.1: Vite + TypeScript 초기화

- [ ] **Step 1: npm init + 의존성 설치**

```bash
npm init -y
npm install -D vite@^5 typescript@^5 @types/node vitest@^1
npm install firebase@^10
```

- [ ] **Step 2: `package.json` 스크립트 수정**

`package.json`의 `scripts` 섹션을 다음으로 교체:
```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc --noEmit && vite build",
    "preview": "vite preview",
    "test": "vitest run",
    "test:watch": "vitest"
  }
}
```
`"type": "module"`도 추가:
```json
{
  "name": "voyna-demo",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  ...
}
```

- [ ] **Step 3: `tsconfig.json` 작성**

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "types": ["vite/client"],
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src", "tests"]
}
```

- [ ] **Step 4: `vite.config.ts` 작성**

```ts
import { defineConfig } from 'vite';
import path from 'node:path';

export default defineConfig({
  base: '/Voyna-Demo/',
  resolve: {
    alias: { '@': path.resolve(__dirname, 'src') }
  },
  server: { port: 5173 },
  build: { outDir: 'dist', sourcemap: true }
});
```

### Task 1.2: 엔트리 파일 + 기본 HTML/CSS

- [ ] **Step 1: `index.html` 작성**

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
    <meta name="theme-color" content="#2a5cdc" />
    <title>Voyna — 보이나</title>
    <link rel="icon" href="/Voyna-Demo/favicon.ico" />
  </head>
  <body>
    <div id="app"></div>
    <script
      src="https://dapi.kakao.com/v2/maps/sdk.js?appkey=KAKAO_KEY_PLACEHOLDER&autoload=false&libraries=services"
      id="kakao-map-sdk"
    ></script>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
```

(SDK src의 `KAKAO_KEY_PLACEHOLDER`는 Task 5.1에서 환경변수로 동적 치환)

- [ ] **Step 2: `src/styles/main.css` 작성**

```css
:root {
  --voyna-primary: #2a5cdc;
  --voyna-special: #d4a017;
  --voyna-rare: #8e44ad;
  --voyna-common: #3498db;
  --voyna-bg: #f7f9fc;
  --voyna-card: #ffffff;
  --voyna-text: #1f2937;
  --voyna-muted: #6b7280;
  --voyna-locked: #d1d5db;
  --tabbar-h: 64px;
}

* { box-sizing: border-box; }
html, body { margin: 0; height: 100%; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Apple SD Gothic Neo', sans-serif;
  background: var(--voyna-bg);
  color: var(--voyna-text);
}
#app { min-height: 100vh; padding-bottom: var(--tabbar-h); }

.page { padding: 16px; }
button { font-family: inherit; cursor: pointer; }

/* Modal base */
.modal-backdrop {
  position: fixed; inset: 0; background: rgba(0,0,0,0.5);
  display: flex; align-items: center; justify-content: center; z-index: 100;
}
.modal {
  background: var(--voyna-card); padding: 24px; border-radius: 16px;
  max-width: 90vw; text-align: center;
  animation: pop 0.4s ease-out;
}
@keyframes pop {
  from { transform: scale(0.5); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

/* Toast */
.toast {
  position: fixed; top: 24px; left: 50%; transform: translateX(-50%);
  background: var(--voyna-primary); color: white; padding: 12px 20px;
  border-radius: 999px; z-index: 200; animation: slidedown 0.3s ease-out;
}
@keyframes slidedown {
  from { transform: translate(-50%, -100px); opacity: 0; }
  to { transform: translate(-50%, 0); opacity: 1; }
}
```

- [ ] **Step 3: `src/main.ts` 부트스트랩 골격**

```ts
import './styles/main.css';
import { startRouter } from './core/router';

window.addEventListener('DOMContentLoaded', () => {
  const root = document.getElementById('app')!;
  startRouter(root);
});
```

(`router`는 Task 5.1에서 구현, 그 전엔 빌드 오류 → Task 1.4에서 임시 stub)

- [ ] **Step 4: `src/core/router.ts` 임시 stub**

```ts
export function startRouter(root: HTMLElement): void {
  root.innerHTML = '<div style="padding:24px">Voyna Demo — bootstrap OK</div>';
}
```

### Task 1.3: 환경변수 셋업

- [ ] **Step 1: `.env.example` 작성**

```
VITE_FB_API_KEY=
VITE_FB_AUTH_DOMAIN=
VITE_FB_PROJECT_ID=
VITE_FB_STORAGE_BUCKET=
VITE_FB_MESSAGING_SENDER_ID=
VITE_FB_APP_ID=
VITE_KAKAO_MAP_KEY=
```

- [ ] **Step 2: `.env.local` 작성 (커밋 금지)**

Task 0.2·0.3에서 메모한 실제 값으로 채움. 키 형식만 예시:
```
VITE_FB_API_KEY=AIzaSy...
VITE_FB_AUTH_DOMAIN=voyna-demo.firebaseapp.com
VITE_FB_PROJECT_ID=voyna-demo
VITE_FB_STORAGE_BUCKET=voyna-demo.appspot.com
VITE_FB_MESSAGING_SENDER_ID=123456789012
VITE_FB_APP_ID=1:123456789012:web:abc...
VITE_KAKAO_MAP_KEY=...
```

- [ ] **Step 3: `src/env.d.ts` 타입 선언**

```ts
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_FB_API_KEY: string;
  readonly VITE_FB_AUTH_DOMAIN: string;
  readonly VITE_FB_PROJECT_ID: string;
  readonly VITE_FB_STORAGE_BUCKET: string;
  readonly VITE_FB_MESSAGING_SENDER_ID: string;
  readonly VITE_FB_APP_ID: string;
  readonly VITE_KAKAO_MAP_KEY: string;
}
interface ImportMeta { readonly env: ImportMetaEnv; }

declare global {
  interface Window { kakao: any; }
}
export {};
```

- [ ] **Step 4: 부트 확인**

```bash
npm run dev
```
브라우저에서 `http://localhost:5173/Voyna-Demo/` 접속 → "Voyna Demo — bootstrap OK" 표시되면 통과.

- [ ] **Step 5: 커밋**

```bash
git add package.json package-lock.json tsconfig.json vite.config.ts index.html src .env.example .gitignore
git commit -m "feat: Vite + TypeScript 스캐폴딩"
git push
```

---

## Phase 2: 핵심 도메인 모듈 (TDD)

> 이 단계는 단위 테스트로 검증한다. UI 통합은 후속 Phase에서.

### Task 2.1: 레벨업 공식 모듈

**Files:**
- Create: `src/core/levels.ts`
- Test: `tests/core/levels.test.ts`

- [ ] **Step 1: 테스트 작성**

`tests/core/levels.test.ts`:
```ts
import { describe, it, expect } from 'vitest';
import { xpForLevel, levelForXp } from '@/core/levels';

describe('levels', () => {
  it('xpForLevel: Lv1→2 누적 100xp', () => {
    expect(xpForLevel(2)).toBe(100);
  });
  it('xpForLevel: Lv2→3 누적 = 100 + floor(100*2^1.6)', () => {
    expect(xpForLevel(3)).toBe(100 + Math.floor(100 * Math.pow(2, 1.6)));
  });
  it('levelForXp: 0 xp → Lv1', () => {
    expect(levelForXp(0)).toBe(1);
  });
  it('levelForXp: 99 xp → Lv1', () => {
    expect(levelForXp(99)).toBe(1);
  });
  it('levelForXp: 100 xp → Lv2', () => {
    expect(levelForXp(100)).toBe(2);
  });
  it('levelForXp: 누적 xp 한 단계 부족하면 그 전 레벨', () => {
    const xp = xpForLevel(5) - 1;
    expect(levelForXp(xp)).toBe(4);
  });
});
```

- [ ] **Step 2: 테스트 실패 확인**

```bash
npm test -- tests/core/levels.test.ts
```
Expected: FAIL ("Cannot find module").

- [ ] **Step 3: 구현 작성**

`src/core/levels.ts`:
```ts
/**
 * 누적 XP for reaching level n (n>=1).
 * Lv1 = 0xp 시작. Lv2 도달 = 100xp. Lv n 도달 = sum_{k=1..n-1} floor(100 * k^1.6).
 */
export function xpForLevel(n: number): number {
  if (n <= 1) return 0;
  let total = 0;
  for (let k = 1; k < n; k++) {
    total += Math.floor(100 * Math.pow(k, 1.6));
  }
  return total;
}

export function levelForXp(xp: number): number {
  let level = 1;
  while (xpForLevel(level + 1) <= xp) {
    level++;
    if (level > 200) break; // 안전망
  }
  return level;
}

export function xpToNextLevel(xp: number): { current: number; nextThreshold: number; progress: number } {
  const lv = levelForXp(xp);
  const cur = xpForLevel(lv);
  const next = xpForLevel(lv + 1);
  return { current: xp - cur, nextThreshold: next - cur, progress: (xp - cur) / (next - cur) };
}
```

- [ ] **Step 4: 테스트 통과 확인**

```bash
npm test -- tests/core/levels.test.ts
```
Expected: PASS (6 tests).

- [ ] **Step 5: 커밋**

```bash
git add src/core/levels.ts tests/core/levels.test.ts
git commit -m "feat(core): 레벨업 XP 공식 + 단위 테스트"
```

### Task 2.2: Haversine 거리 모듈

**Files:**
- Create: `src/core/geo.ts`
- Test: `tests/core/geo.test.ts`

- [ ] **Step 1: 테스트 작성**

`tests/core/geo.test.ts`:
```ts
import { describe, it, expect } from 'vitest';
import { haversineMeters, withinRadius } from '@/core/geo';

describe('geo', () => {
  it('같은 좌표는 0m', () => {
    expect(haversineMeters(37.5573, 126.9485, 37.5573, 126.9485)).toBe(0);
  });
  it('ASSIST와 경복궁 사이 거리 약 2.6~3.5km 범위', () => {
    const d = haversineMeters(37.5573, 126.9485, 37.5796, 126.9770);
    expect(d).toBeGreaterThan(2500);
    expect(d).toBeLessThan(3700);
  });
  it('withinRadius: 반경 안이면 true', () => {
    expect(withinRadius(37.5573, 126.9485, 37.5573, 126.9485, 50)).toBe(true);
  });
  it('withinRadius: 반경 밖이면 false', () => {
    expect(withinRadius(37.5573, 126.9485, 37.5796, 126.9770, 200)).toBe(false);
  });
});
```

- [ ] **Step 2: 테스트 실패 확인**

```bash
npm test -- tests/core/geo.test.ts
```
Expected: FAIL.

- [ ] **Step 3: 구현 작성**

`src/core/geo.ts`:
```ts
const R = 6371000; // 지구 반지름 (m)

export function haversineMeters(lat1: number, lng1: number, lat2: number, lng2: number): number {
  const toRad = (d: number) => (d * Math.PI) / 180;
  const φ1 = toRad(lat1);
  const φ2 = toRad(lat2);
  const Δφ = toRad(lat2 - lat1);
  const Δλ = toRad(lng2 - lng1);
  const a = Math.sin(Δφ / 2) ** 2 + Math.cos(φ1) * Math.cos(φ2) * Math.sin(Δλ / 2) ** 2;
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

export function withinRadius(
  lat1: number, lng1: number, lat2: number, lng2: number, radiusM: number
): boolean {
  return haversineMeters(lat1, lng1, lat2, lng2) <= radiusM;
}

export type Coords = { lat: number; lng: number };

export function getBrowserGPS(): Promise<Coords> {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error('Geolocation API 미지원'));
      return;
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => resolve({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
      (err) => reject(err),
      { enableHighAccuracy: true, timeout: 8000, maximumAge: 10000 }
    );
  });
}
```

- [ ] **Step 4: 테스트 통과 확인**

```bash
npm test -- tests/core/geo.test.ts
```
Expected: PASS (4 tests).

- [ ] **Step 5: 커밋**

```bash
git add src/core/geo.ts tests/core/geo.test.ts
git commit -m "feat(core): Haversine 거리 + GPS 획득"
```

### Task 2.3: localStorage 상태 모듈

**Files:**
- Create: `src/core/state.ts`
- Test: `tests/core/state.test.ts`

- [ ] **Step 1: 테스트 작성**

`tests/core/state.test.ts`:
```ts
import { describe, it, expect, beforeEach } from 'vitest';
import { loadState, saveState, resetState, defaultState, type UserState } from '@/core/state';

beforeEach(() => {
  localStorage.clear();
});

describe('state', () => {
  it('loadState: 없으면 defaultState', () => {
    expect(loadState()).toEqual(defaultState());
  });
  it('saveState → loadState 왕복', () => {
    const s = defaultState();
    s.xp = 250;
    s.level = 2;
    saveState(s);
    const loaded = loadState();
    expect(loaded.xp).toBe(250);
    expect(loaded.level).toBe(2);
  });
  it('resetState: localStorage 초기화', () => {
    const s = defaultState();
    s.xp = 999;
    saveState(s);
    resetState();
    expect(loadState().xp).toBe(0);
  });
  it('손상된 JSON은 defaultState 반환', () => {
    localStorage.setItem('voyna_demo_state_v1', '{ broken');
    expect(loadState()).toEqual(defaultState());
  });
});
```

- [ ] **Step 2: 테스트 실패 확인**

```bash
npm test -- tests/core/state.test.ts
```
Expected: FAIL.

- [ ] **Step 3: vitest jsdom 환경 활성화**

`package.json`에 추가:
```json
{
  ...
  "vitest": {
    "environment": "jsdom"
  }
}
```

`jsdom` 의존성 설치:
```bash
npm install -D jsdom @vitest/coverage-v8
```

`vitest.config.ts` 생성:
```ts
import { defineConfig } from 'vitest/config';
import path from 'node:path';

export default defineConfig({
  test: { environment: 'jsdom' },
  resolve: { alias: { '@': path.resolve(__dirname, 'src') } }
});
```

- [ ] **Step 4: 구현 작성**

`src/core/state.ts`:
```ts
const KEY = 'voyna_demo_state_v1';

export type ObtainedBadge = {
  badgeId: string;
  at: string;        // ISO timestamp
  lat: number;
  lng: number;
};

export type FirebaseUser = {
  uid: string;
  displayName: string;
  email: string;
  photoURL: string;
};

export type UserState = {
  user: FirebaseUser | null;
  xp: number;
  level: number;
  title: string;
  obtained: ObtainedBadge[];
  currentLocation: { lat: number; lng: number; isTeleport: boolean } | null;
  realGPS: { lat: number; lng: number } | null;
  lastSeenAt: string;
};

export function defaultState(): UserState {
  return {
    user: null,
    xp: 0,
    level: 1,
    title: '초보 탐험가',
    obtained: [],
    currentLocation: null,
    realGPS: null,
    lastSeenAt: new Date().toISOString(),
  };
}

export function loadState(): UserState {
  const raw = localStorage.getItem(KEY);
  if (!raw) return defaultState();
  try {
    const parsed = JSON.parse(raw) as UserState;
    return { ...defaultState(), ...parsed };
  } catch {
    return defaultState();
  }
}

export function saveState(s: UserState): void {
  s.lastSeenAt = new Date().toISOString();
  localStorage.setItem(KEY, JSON.stringify(s));
}

export function resetState(): void {
  localStorage.removeItem(KEY);
}
```

- [ ] **Step 5: 테스트 통과 확인**

```bash
npm test -- tests/core/state.test.ts
```
Expected: PASS (4 tests).

- [ ] **Step 6: 커밋**

```bash
git add src/core/state.ts tests/core/state.test.ts vitest.config.ts package.json package-lock.json
git commit -m "feat(core): localStorage 상태 모듈 + jsdom 셋업"
```

### Task 2.4: 칭호 평가 모듈

**Files:**
- Create: `src/core/titles.ts`
- Test: `tests/core/titles.test.ts`

- [ ] **Step 1: 테스트 작성**

`tests/core/titles.test.ts`:
```ts
import { describe, it, expect } from 'vitest';
import { evaluateTitle, TITLES } from '@/core/titles';
import type { UserState } from '@/core/state';

function mkState(over: Partial<UserState>): UserState {
  return {
    user: null, xp: 0, level: 1, title: '초보 탐험가',
    obtained: [], currentLocation: null, realGPS: null,
    lastSeenAt: '', ...over,
  };
}

describe('titles', () => {
  it('기본: 초보 탐험가', () => {
    expect(evaluateTitle(mkState({})).id).toBe('beginner');
  });
  it('배지 5개 → 동네 탐험가', () => {
    const obtained = Array.from({ length: 5 }, (_, i) => ({
      badgeId: `b${i}`, at: '', lat: 0, lng: 0,
    }));
    expect(evaluateTitle(mkState({ obtained })).id).toBe('neighborhood');
  });
  it('배지 10개 → 지도 마니아', () => {
    const obtained = Array.from({ length: 10 }, (_, i) => ({
      badgeId: `b${i}`, at: '', lat: 0, lng: 0,
    }));
    expect(evaluateTitle(mkState({ obtained })).id).toBe('mania');
  });
  it('Lv10 + 배지 20개 → 전설의 여행자', () => {
    const obtained = Array.from({ length: 20 }, (_, i) => ({
      badgeId: `b${i}`, at: '', lat: 0, lng: 0,
    }));
    expect(evaluateTitle(mkState({ level: 10, obtained })).id).toBe('legend');
  });
});
```

- [ ] **Step 2: 테스트 실패 확인**

```bash
npm test -- tests/core/titles.test.ts
```
Expected: FAIL.

- [ ] **Step 3: 구현 작성**

`src/core/titles.ts`:
```ts
import type { UserState } from './state';

export type Title = {
  id: string;
  name: string;
  description: string;
  predicate: (s: UserState, specialCount: number) => boolean;
};

export const TITLES: Title[] = [
  // 우선순위 높은 순으로 평가 (위가 우선)
  {
    id: 'legend',
    name: '전설의 여행자',
    description: 'Lv10 + 배지 20개',
    predicate: (s) => s.level >= 10 && s.obtained.length >= 20,
  },
  {
    id: 'seoul-conqueror',
    name: '서울 정복자',
    description: '특별 등급 배지 5개',
    predicate: (_, special) => special >= 5,
  },
  {
    id: 'mania',
    name: '지도 마니아',
    description: '배지 10개',
    predicate: (s) => s.obtained.length >= 10,
  },
  {
    id: 'neighborhood',
    name: '동네 탐험가',
    description: '배지 5개',
    predicate: (s) => s.obtained.length >= 5,
  },
  {
    id: 'beginner',
    name: '초보 탐험가',
    description: '시작 칭호',
    predicate: () => true,
  },
];

export function evaluateTitle(s: UserState, specialCount: number = 0): Title {
  for (const t of TITLES) {
    if (t.predicate(s, specialCount)) return t;
  }
  return TITLES[TITLES.length - 1]!;
}
```

- [ ] **Step 4: 테스트 통과 확인**

```bash
npm test -- tests/core/titles.test.ts
```
Expected: PASS (4 tests).

- [ ] **Step 5: 커밋**

```bash
git add src/core/titles.ts tests/core/titles.test.ts
git commit -m "feat(core): 칭호 평가 시스템"
```

---

## Phase 3: 데이터 카탈로그

### Task 3.1: 명소 데이터 작성 (locations.json)

**Files:**
- Create: `src/data/locations.json`

- [ ] **Step 1: 31개 명소 JSON 작성**

기획서 리포의 `data/seoul_50_locations.md`에서 선별. 12주 plan의 30곳 + ASSIST. `src/data/locations.json`:

```json
[
  { "id": "assist", "name": "ASSIST 강의실", "lat": 37.5573, "lng": 126.9485, "radius": 50, "category": "교육", "grade": "special" },
  { "id": "gyeongbok", "name": "경복궁", "lat": 37.5796, "lng": 126.9770, "radius": 200, "category": "고궁", "grade": "special" },
  { "id": "n-seoul-tower", "name": "N서울타워", "lat": 37.5512, "lng": 126.9882, "radius": 150, "category": "랜드마크", "grade": "special" },
  { "id": "cheongwadae", "name": "청와대", "lat": 37.5866, "lng": 126.9748, "radius": 200, "category": "역사", "grade": "special" },
  { "id": "bukhansan", "name": "북한산", "lat": 37.6588, "lng": 126.9772, "radius": 500, "category": "국립공원", "grade": "special" },
  { "id": "changdeok", "name": "창덕궁", "lat": 37.5794, "lng": 126.9910, "radius": 150, "category": "고궁", "grade": "rare" },
  { "id": "deoksu", "name": "덕수궁", "lat": 37.5658, "lng": 126.9751, "radius": 120, "category": "고궁", "grade": "rare" },
  { "id": "jongmyo", "name": "종묘", "lat": 37.5746, "lng": 126.9941, "radius": 150, "category": "고궁", "grade": "rare" },
  { "id": "bukchon", "name": "북촌 한옥마을", "lat": 37.5826, "lng": 126.9836, "radius": 200, "category": "마을", "grade": "rare" },
  { "id": "lotte-tower", "name": "롯데월드타워", "lat": 37.5126, "lng": 127.1025, "radius": 150, "category": "랜드마크", "grade": "rare" },
  { "id": "banpo-hangang", "name": "반포 한강공원", "lat": 37.5108, "lng": 126.9959, "radius": 300, "category": "공원", "grade": "rare" },
  { "id": "inwangsan", "name": "인왕산", "lat": 37.5790, "lng": 126.9595, "radius": 400, "category": "산", "grade": "rare" },
  { "id": "cheonggyesan", "name": "청계산", "lat": 37.4286, "lng": 127.0467, "radius": 400, "category": "산", "grade": "rare" },
  { "id": "national-museum", "name": "국립중앙박물관", "lat": 37.5240, "lng": 126.9803, "radius": 200, "category": "박물관", "grade": "rare" },
  { "id": "leeum", "name": "리움미술관", "lat": 37.5384, "lng": 126.9991, "radius": 100, "category": "미술관", "grade": "rare" },
  { "id": "changgyeong", "name": "창경궁", "lat": 37.5786, "lng": 126.9947, "radius": 150, "category": "고궁", "grade": "common" },
  { "id": "gwanghwamun", "name": "광화문", "lat": 37.5759, "lng": 126.9769, "radius": 100, "category": "랜드마크", "grade": "common" },
  { "id": "sungnyemun", "name": "숭례문", "lat": 37.5610, "lng": 126.9753, "radius": 80, "category": "문화재", "grade": "common" },
  { "id": "insadong", "name": "인사동", "lat": 37.5717, "lng": 126.9858, "radius": 200, "category": "거리", "grade": "common" },
  { "id": "myeongdong", "name": "명동", "lat": 37.5636, "lng": 126.9826, "radius": 200, "category": "거리", "grade": "common" },
  { "id": "hongdae", "name": "홍대 거리", "lat": 37.5563, "lng": 126.9237, "radius": 250, "category": "거리", "grade": "common" },
  { "id": "garosu-gil", "name": "가로수길", "lat": 37.5208, "lng": 127.0227, "radius": 200, "category": "거리", "grade": "common" },
  { "id": "gangnam-station", "name": "강남역", "lat": 37.4979, "lng": 127.0276, "radius": 150, "category": "도심", "grade": "common" },
  { "id": "itaewon", "name": "이태원", "lat": 37.5347, "lng": 126.9947, "radius": 200, "category": "거리", "grade": "common" },
  { "id": "yeouido-hangang", "name": "여의도 한강공원", "lat": 37.5283, "lng": 126.9341, "radius": 300, "category": "공원", "grade": "common" },
  { "id": "jamsil-hangang", "name": "잠실 한강공원", "lat": 37.5180, "lng": 127.0820, "radius": 300, "category": "공원", "grade": "common" },
  { "id": "namsan-park", "name": "남산공원", "lat": 37.5519, "lng": 126.9908, "radius": 300, "category": "공원", "grade": "common" },
  { "id": "seoul-forest", "name": "서울숲", "lat": 37.5443, "lng": 127.0374, "radius": 300, "category": "공원", "grade": "common" },
  { "id": "gwangjang-market", "name": "광장시장", "lat": 37.5701, "lng": 126.9999, "radius": 100, "category": "시장", "grade": "common" },
  { "id": "ddp", "name": "DDP 동대문디자인플라자", "lat": 37.5663, "lng": 127.0091, "radius": 150, "category": "건축", "grade": "common" },
  { "id": "coex-byeolmadang", "name": "코엑스 별마당도서관", "lat": 37.5126, "lng": 127.0590, "radius": 100, "category": "도서관", "grade": "common" }
]
```

- [ ] **Step 2: 카운트 확인**

```bash
node -e "console.log(JSON.parse(require('fs').readFileSync('src/data/locations.json')).length)"
```
Expected: `31`

### Task 3.2: 배지 데이터 작성 (badges.json)

**Files:**
- Create: `src/data/badges.json`

- [ ] **Step 1: 31종 배지 JSON 작성**

`src/data/badges.json`. 정성 디자인 우선순위 10개(spec 섹션 5)는 `is_polished: true` + 전용 이미지 경로, 나머지 21개는 `locked.png` 공통:

```json
[
  { "id": "assist", "name": "지식의 전당", "description": "ASSIST 강의실에서 첫 발걸음", "grade": "special", "xp": 300, "image": "/Voyna-Demo/badges/assist.png", "is_polished": true },
  { "id": "gyeongbok", "name": "조선의 정궁", "description": "경복궁에서 조선의 역사를 마주하다", "grade": "special", "xp": 400, "image": "/Voyna-Demo/badges/gyeongbok.png", "is_polished": true },
  { "id": "n-seoul-tower", "name": "서울의 별", "description": "N서울타워에서 도시를 내려다보다", "grade": "special", "xp": 400, "image": "/Voyna-Demo/badges/n-seoul-tower.png", "is_polished": true },
  { "id": "cheongwadae", "name": "푸른 기와", "description": "청와대 앞을 지나다", "grade": "special", "xp": 300, "image": "/Voyna-Demo/badges/cheongwadae.png", "is_polished": true },
  { "id": "bukhansan", "name": "산악인", "description": "북한산 정상을 향하다", "grade": "special", "xp": 400, "image": "/Voyna-Demo/badges/bukhansan.png", "is_polished": true },
  { "id": "changdeok", "name": "비원의 사색", "description": "창덕궁의 후원을 거닐다", "grade": "rare", "xp": 150, "image": "/Voyna-Demo/badges/changdeok.png", "is_polished": true },
  { "id": "lotte-tower", "name": "마천루", "description": "롯데월드타워에 닿다", "grade": "rare", "xp": 150, "image": "/Voyna-Demo/badges/lotte-tower.png", "is_polished": true },
  { "id": "banpo-hangang", "name": "한강의 노을", "description": "반포 한강에서 노을을 만나다", "grade": "rare", "xp": 150, "image": "/Voyna-Demo/badges/banpo-hangang.png", "is_polished": true },
  { "id": "myeongdong", "name": "명동의 활기", "description": "명동 거리를 누비다", "grade": "common", "xp": 50, "image": "/Voyna-Demo/badges/myeongdong.png", "is_polished": true },
  { "id": "gwanghwamun", "name": "광화문 앞에서", "description": "광화문 광장에 서다", "grade": "common", "xp": 50, "image": "/Voyna-Demo/badges/gwanghwamun.png", "is_polished": true },

  { "id": "deoksu", "name": "덕수궁 산책", "description": "덕수궁을 걷다", "grade": "rare", "xp": 150, "image": "/Voyna-Demo/badges/locked.png", "is_polished": false },
  { "id": "jongmyo", "name": "종묘 제례", "description": "종묘를 방문하다", "grade": "rare", "xp": 150, "image": "/Voyna-Demo/badges/locked.png", "is_polished": false },
  { "id": "bukchon", "name": "한옥의 풍경", "description": "북촌 한옥마을을 거닐다", "grade": "rare", "xp": 150, "image": "/Voyna-Demo/badges/locked.png", "is_polished": false },
  { "id": "inwangsan", "name": "인왕산 등반", "description": "인왕산을 오르다", "grade": "rare", "xp": 150, "image": "/Voyna-Demo/badges/locked.png", "is_polished": false },
  { "id": "cheonggyesan", "name": "청계산 등반", "description": "청계산을 오르다", "grade": "rare", "xp": 150, "image": "/Voyna-Demo/badges/locked.png", "is_polished": false },
  { "id": "national-museum", "name": "박물관 산책자", "description": "국립중앙박물관을 방문하다", "grade": "rare", "xp": 150, "image": "/Voyna-Demo/badges/locked.png", "is_polished": false },
  { "id": "leeum", "name": "현대미술의 시선", "description": "리움미술관을 방문하다", "grade": "rare", "xp": 150, "image": "/Voyna-Demo/badges/locked.png", "is_polished": false },
  { "id": "changgyeong", "name": "창경궁 산책", "description": "창경궁을 거닐다", "grade": "common", "xp": 50, "image": "/Voyna-Demo/badges/locked.png", "is_polished": false },
  { "id": "sungnyemun", "name": "숭례문 앞에서", "description": "숭례문을 마주하다", "grade": "common", "xp": 50, "image": "/Voyna-Demo/badges/locked.png", "is_polished": false },
  { "id": "insadong", "name": "전통의 거리", "description": "인사동을 거닐다", "grade": "common", "xp": 50, "image": "/Voyna-Demo/badges/locked.png", "is_polished": false },
  { "id": "hongdae", "name": "젊음의 거리", "description": "홍대 거리를 누비다", "grade": "common", "xp": 50, "image": "/Voyna-Demo/badges/locked.png", "is_polished": false },
  { "id": "garosu-gil", "name": "가로수길 산책", "description": "가로수길을 거닐다", "grade": "common", "xp": 50, "image": "/Voyna-Demo/badges/locked.png", "is_polished": false },
  { "id": "gangnam-station", "name": "강남의 한복판", "description": "강남역에 다다르다", "grade": "common", "xp": 50, "image": "/Voyna-Demo/badges/locked.png", "is_polished": false },
  { "id": "itaewon", "name": "다국적 거리", "description": "이태원을 누비다", "grade": "common", "xp": 50, "image": "/Voyna-Demo/badges/locked.png", "is_polished": false },
  { "id": "yeouido-hangang", "name": "여의도 한강", "description": "여의도 한강공원을 걷다", "grade": "common", "xp": 50, "image": "/Voyna-Demo/badges/locked.png", "is_polished": false },
  { "id": "jamsil-hangang", "name": "잠실 한강", "description": "잠실 한강공원을 걷다", "grade": "common", "xp": 50, "image": "/Voyna-Demo/badges/locked.png", "is_polished": false },
  { "id": "namsan-park", "name": "남산 산책", "description": "남산공원을 거닐다", "grade": "common", "xp": 50, "image": "/Voyna-Demo/badges/locked.png", "is_polished": false },
  { "id": "seoul-forest", "name": "도심의 숲", "description": "서울숲을 거닐다", "grade": "common", "xp": 50, "image": "/Voyna-Demo/badges/locked.png", "is_polished": false },
  { "id": "gwangjang-market", "name": "광장시장의 맛", "description": "광장시장을 방문하다", "grade": "common", "xp": 50, "image": "/Voyna-Demo/badges/locked.png", "is_polished": false },
  { "id": "ddp", "name": "DDP의 곡선", "description": "동대문디자인플라자에 가다", "grade": "common", "xp": 50, "image": "/Voyna-Demo/badges/locked.png", "is_polished": false },
  { "id": "coex-byeolmadang", "name": "별마당의 향기", "description": "코엑스 별마당도서관을 방문하다", "grade": "common", "xp": 50, "image": "/Voyna-Demo/badges/locked.png", "is_polished": false }
]
```

- [ ] **Step 2: 정합성 검증 스크립트 실행**

```bash
node -e "
const locs = require('./src/data/locations.json');
const badges = require('./src/data/badges.json');
console.log('locations:', locs.length, 'badges:', badges.length);
const locIds = new Set(locs.map(l => l.id));
const badIds = new Set(badges.map(b => b.id));
const missing = [...locIds].filter(id => !badIds.has(id));
const extra = [...badIds].filter(id => !locIds.has(id));
if (missing.length || extra.length) {
  console.error('MISMATCH', { missing, extra });
  process.exit(1);
}
console.log('OK: 1:1 매칭');
"
```
Expected: `locations: 31 badges: 31\nOK: 1:1 매칭`

### Task 3.3: 카탈로그 로더 모듈

**Files:**
- Create: `src/core/catalog.ts`
- Test: `tests/core/catalog.test.ts`

- [ ] **Step 1: 테스트 작성**

`tests/core/catalog.test.ts`:
```ts
import { describe, it, expect } from 'vitest';
import { getLocations, getBadges, getLocation, getBadge } from '@/core/catalog';

describe('catalog', () => {
  it('locations 31개', () => {
    expect(getLocations()).toHaveLength(31);
  });
  it('badges 31개', () => {
    expect(getBadges()).toHaveLength(31);
  });
  it('ASSIST 좌표 정확', () => {
    const loc = getLocation('assist');
    expect(loc?.lat).toBe(37.5573);
    expect(loc?.lng).toBe(126.9485);
  });
  it('badge id가 location id와 1:1 대응', () => {
    const locIds = new Set(getLocations().map((l) => l.id));
    for (const b of getBadges()) {
      expect(locIds.has(b.id)).toBe(true);
    }
  });
  it('정성 디자인 배지 10개', () => {
    expect(getBadges().filter((b) => b.is_polished)).toHaveLength(10);
  });
  it('getBadge 존재하지 않으면 undefined', () => {
    expect(getBadge('nonexistent')).toBeUndefined();
  });
});
```

- [ ] **Step 2: 테스트 실패 확인**

```bash
npm test -- tests/core/catalog.test.ts
```
Expected: FAIL.

- [ ] **Step 3: 구현 작성**

`src/core/catalog.ts`:
```ts
import locationsData from '@/data/locations.json';
import badgesData from '@/data/badges.json';

export type Grade = 'common' | 'rare' | 'special' | 'premier';

export type Location = {
  id: string;
  name: string;
  lat: number;
  lng: number;
  radius: number;
  category: string;
  grade: Grade;
};

export type Badge = {
  id: string;
  name: string;
  description: string;
  grade: Grade;
  xp: number;
  image: string;
  is_polished: boolean;
};

const LOCATIONS = locationsData as Location[];
const BADGES = badgesData as Badge[];
const LOC_MAP = new Map(LOCATIONS.map((l) => [l.id, l]));
const BADGE_MAP = new Map(BADGES.map((b) => [b.id, b]));

export const getLocations = (): Location[] => LOCATIONS;
export const getBadges = (): Badge[] => BADGES;
export const getLocation = (id: string): Location | undefined => LOC_MAP.get(id);
export const getBadge = (id: string): Badge | undefined => BADGE_MAP.get(id);
```

- [ ] **Step 4: 테스트 통과 확인**

```bash
npm test -- tests/core/catalog.test.ts
```
Expected: PASS (6 tests).

- [ ] **Step 5: 커밋**

```bash
git add src/data src/core/catalog.ts tests/core/catalog.test.ts
git commit -m "feat(data): 31곳 명소·배지 카탈로그 + 로더"
```

### Task 3.4: 배지 엔진 (도메인 통합)

**Files:**
- Create: `src/core/badge-engine.ts`
- Test: `tests/core/badge-engine.test.ts`

- [ ] **Step 1: 테스트 작성**

`tests/core/badge-engine.test.ts`:
```ts
import { describe, it, expect, beforeEach } from 'vitest';
import { resetState, loadState, defaultState, saveState } from '@/core/state';
import { findNearbyBadges, awardBadge } from '@/core/badge-engine';
import { getLocation } from '@/core/catalog';

beforeEach(() => {
  resetState();
  const s = defaultState();
  s.user = { uid: 'test', displayName: 'Tester', email: 't@t.com', photoURL: '' };
  saveState(s);
});

describe('badge-engine', () => {
  it('findNearbyBadges: 경복궁 좌표면 경복궁 후보 반환', () => {
    const loc = getLocation('gyeongbok')!;
    const found = findNearbyBadges({ lat: loc.lat, lng: loc.lng });
    expect(found.some((c) => c.location.id === 'gyeongbok')).toBe(true);
  });

  it('findNearbyBadges: 이미 획득한 배지는 제외', () => {
    const loc = getLocation('gyeongbok')!;
    awardBadge('gyeongbok', loc.lat, loc.lng);
    const found = findNearbyBadges({ lat: loc.lat, lng: loc.lng });
    expect(found.some((c) => c.location.id === 'gyeongbok')).toBe(false);
  });

  it('awardBadge: XP 적립', () => {
    const before = loadState().xp;
    const r = awardBadge('myeongdong', 37.5636, 126.9826);
    expect(r.success).toBe(true);
    expect(loadState().xp).toBe(before + 50);
  });

  it('awardBadge: 중복 획득 거부', () => {
    awardBadge('gyeongbok', 37.5796, 126.9770);
    const r = awardBadge('gyeongbok', 37.5796, 126.9770);
    expect(r.success).toBe(false);
    expect(r.reason).toBe('already_obtained');
  });

  it('awardBadge: 누적 xp가 임계 넘으면 leveledUp=true', () => {
    // 경복궁(400) + 북한산(400) + N서울타워(400) = 1200 → Lv1→2(100)→3(이상)
    awardBadge('gyeongbok', 37.5796, 126.9770);
    const r = awardBadge('bukhansan', 37.6588, 126.9772);
    expect(r.success).toBe(true);
    expect(r.leveledUp).toBe(true);
    expect(r.newLevel).toBeGreaterThan(1);
  });

  it('awardBadge: 칭호 변경 시 newTitle 반환', () => {
    // 5개 채우면 동네 탐험가
    for (const id of ['myeongdong', 'gwanghwamun', 'insadong', 'hongdae', 'itaewon']) {
      awardBadge(id, 0, 0);
    }
    expect(loadState().title).toBe('동네 탐험가');
  });
});
```

- [ ] **Step 2: 테스트 실패 확인**

```bash
npm test -- tests/core/badge-engine.test.ts
```
Expected: FAIL.

- [ ] **Step 3: 구현 작성**

`src/core/badge-engine.ts`:
```ts
import { loadState, saveState } from './state';
import { getBadges, getBadge, getLocation, getLocations, type Location, type Badge } from './catalog';
import { haversineMeters } from './geo';
import { levelForXp } from './levels';
import { evaluateTitle } from './titles';

export type NearbyCandidate = {
  location: Location;
  badge: Badge;
  distance: number;
};

export type AwardResult =
  | {
      success: true;
      badge: Badge;
      xpGained: number;
      newXp: number;
      newLevel: number;
      previousLevel: number;
      leveledUp: boolean;
      newTitle?: string;
      previousTitle: string;
    }
  | { success: false; reason: 'already_obtained' | 'unknown_badge' };

export function findNearbyBadges(
  current: { lat: number; lng: number },
  maxResults: number = 20
): NearbyCandidate[] {
  const state = loadState();
  const obtained = new Set(state.obtained.map((o) => o.badgeId));
  const out: NearbyCandidate[] = [];
  for (const loc of getLocations()) {
    if (obtained.has(loc.id)) continue;
    const d = haversineMeters(current.lat, current.lng, loc.lat, loc.lng);
    if (d <= loc.radius) {
      const badge = getBadge(loc.id);
      if (badge) out.push({ location: loc, badge, distance: d });
    }
  }
  return out.sort((a, b) => a.distance - b.distance).slice(0, maxResults);
}

function countSpecialObtained(obtainedIds: string[]): number {
  let n = 0;
  for (const id of obtainedIds) {
    const b = getBadge(id);
    if (b?.grade === 'special') n++;
  }
  return n;
}

export function awardBadge(badgeId: string, lat: number, lng: number): AwardResult {
  const badge = getBadge(badgeId);
  if (!badge) return { success: false, reason: 'unknown_badge' };

  const state = loadState();
  if (state.obtained.some((o) => o.badgeId === badgeId)) {
    return { success: false, reason: 'already_obtained' };
  }

  const previousLevel = state.level;
  const previousTitle = state.title;
  state.obtained.push({ badgeId, at: new Date().toISOString(), lat, lng });
  state.xp += badge.xp;
  state.level = levelForXp(state.xp);

  const specialCount = countSpecialObtained(state.obtained.map((o) => o.badgeId));
  const title = evaluateTitle(state, specialCount);
  state.title = title.name;
  saveState(state);

  const leveledUp = state.level > previousLevel;
  const titleChanged = title.name !== previousTitle;

  return {
    success: true,
    badge,
    xpGained: badge.xp,
    newXp: state.xp,
    newLevel: state.level,
    previousLevel,
    leveledUp,
    newTitle: titleChanged ? title.name : undefined,
    previousTitle,
  };
}

export function getObtainedCount(): number {
  return loadState().obtained.length;
}
```

- [ ] **Step 4: 테스트 통과 확인**

```bash
npm test
```
Expected: 전체 PASS (engine 6개 + 기존 테스트).

- [ ] **Step 5: 커밋**

```bash
git add src/core/badge-engine.ts tests/core/badge-engine.test.ts
git commit -m "feat(core): 배지 엔진 (획득·XP·레벨·칭호 통합)"
git push
```

---

## Phase 4: Firebase Google 로그인

### Task 4.1: Firebase 초기화

**Files:**
- Create: `src/auth/firebase.ts`

- [ ] **Step 1: 작성**

`src/auth/firebase.ts`:
```ts
import { initializeApp } from 'firebase/app';
import {
  getAuth, GoogleAuthProvider, signInWithPopup, signOut,
  onAuthStateChanged, type User,
} from 'firebase/auth';
import { loadState, saveState } from '@/core/state';

const config = {
  apiKey: import.meta.env.VITE_FB_API_KEY,
  authDomain: import.meta.env.VITE_FB_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FB_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FB_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FB_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FB_APP_ID,
};

const app = initializeApp(config);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

export async function loginWithGoogle(): Promise<User> {
  const result = await signInWithPopup(auth, provider);
  const u = result.user;
  const state = loadState();
  state.user = {
    uid: u.uid,
    displayName: u.displayName ?? '여행자',
    email: u.email ?? '',
    photoURL: u.photoURL ?? '',
  };
  saveState(state);
  return u;
}

export async function logout(): Promise<void> {
  await signOut(auth);
  const state = loadState();
  state.user = null;
  saveState(state);
}

export function onAuth(cb: (u: User | null) => void): () => void {
  return onAuthStateChanged(auth, cb);
}

export function currentUser(): User | null {
  return auth.currentUser;
}
```

### Task 4.2: 로그인 페이지

**Files:**
- Create: `src/auth/login-page.ts`

- [ ] **Step 1: 작성**

`src/auth/login-page.ts`:
```ts
import { loginWithGoogle } from './firebase';

export function renderLoginPage(root: HTMLElement, onSuccess: () => void): void {
  root.innerHTML = `
    <div class="login-page">
      <div class="login-card">
        <h1 class="brand">Voyna</h1>
        <p class="tagline">발걸음이 기록이 되고,<br/>기록이 추억이 된다</p>
        <button id="google-login" class="google-btn">
          <span class="g-icon">G</span> Google로 시작하기
        </button>
        <p class="hint">데모용 빌드입니다.</p>
      </div>
    </div>
    <style>
      .login-page {
        min-height: 100vh; display: flex; align-items: center; justify-content: center;
        background: linear-gradient(160deg, #2a5cdc 0%, #1a3a8c 100%);
      }
      .login-card {
        background: white; padding: 40px 32px; border-radius: 20px; text-align: center;
        box-shadow: 0 12px 40px rgba(0,0,0,0.2); max-width: 360px; width: 90%;
      }
      .brand { font-size: 48px; margin: 0 0 12px; color: var(--voyna-primary); letter-spacing: -1px; }
      .tagline { color: var(--voyna-muted); margin: 0 0 32px; line-height: 1.5; }
      .google-btn {
        background: white; border: 1px solid #dadce0; border-radius: 8px;
        padding: 12px 20px; font-size: 16px; width: 100%;
        display: flex; align-items: center; justify-content: center; gap: 12px;
      }
      .google-btn:hover { background: #f8f9fa; }
      .g-icon {
        width: 22px; height: 22px; display: inline-flex; align-items: center; justify-content: center;
        background: linear-gradient(135deg, #4285f4, #34a853, #fbbc04, #ea4335);
        color: white; border-radius: 50%; font-weight: bold; font-size: 14px;
      }
      .hint { margin-top: 16px; font-size: 12px; color: var(--voyna-muted); }
    </style>
  `;

  document.getElementById('google-login')!.addEventListener('click', async () => {
    try {
      await loginWithGoogle();
      onSuccess();
    } catch (e) {
      alert('로그인 실패: ' + (e as Error).message);
    }
  });
}
```

- [ ] **Step 2: 커밋**

```bash
git add src/auth
git commit -m "feat(auth): Firebase Google 로그인 화면"
```

---

## Phase 5: 4탭 라우터 + 스켈레톤 페이지

### Task 5.1: 카카오맵 SDK 동적 로더

**Files:**
- Create: `src/core/kakao-loader.ts`
- Modify: `index.html` (SDK script 태그 제거)

- [ ] **Step 1: `index.html` 수정**

`<script src="https://dapi.kakao.com/v2/maps/sdk.js?..."></script>` 라인 삭제. (동적으로 로드)

- [ ] **Step 2: 로더 작성**

`src/core/kakao-loader.ts`:
```ts
let loaded: Promise<void> | null = null;

export function loadKakaoMaps(): Promise<void> {
  if (loaded) return loaded;
  loaded = new Promise((resolve, reject) => {
    const key = import.meta.env.VITE_KAKAO_MAP_KEY;
    if (!key) { reject(new Error('VITE_KAKAO_MAP_KEY 미설정')); return; }
    const script = document.createElement('script');
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${key}&autoload=false&libraries=services`;
    script.onload = () => {
      window.kakao.maps.load(() => resolve());
    };
    script.onerror = () => reject(new Error('카카오맵 SDK 로드 실패'));
    document.head.appendChild(script);
  });
  return loaded;
}
```

### Task 5.2: 라우터 + 탭바

**Files:**
- Rewrite: `src/core/router.ts`
- Create: `src/components/tab-bar.ts`

- [ ] **Step 1: 탭바 컴포넌트 작성**

`src/components/tab-bar.ts`:
```ts
export type Tab = 'home' | 'map' | 'badges' | 'more';

export function renderTabBar(active: Tab, onChange: (t: Tab) => void): HTMLElement {
  const bar = document.createElement('nav');
  bar.className = 'tabbar';
  bar.innerHTML = `
    <button data-tab="home" class="${active === 'home' ? 'active' : ''}">🏠<span>홈</span></button>
    <button data-tab="map" class="${active === 'map' ? 'active' : ''}">🗺️<span>탐험</span></button>
    <button data-tab="badges" class="${active === 'badges' ? 'active' : ''}">🏅<span>배지</span></button>
    <button data-tab="more" class="${active === 'more' ? 'active' : ''}">⚙️<span>더보기</span></button>
  `;
  bar.querySelectorAll<HTMLButtonElement>('button').forEach((btn) => {
    btn.addEventListener('click', () => onChange(btn.dataset.tab as Tab));
  });
  return bar;
}
```

탭바 스타일을 `src/styles/main.css`에 추가:
```css
.tabbar {
  position: fixed; bottom: 0; left: 0; right: 0; height: var(--tabbar-h);
  background: white; border-top: 1px solid #e5e7eb;
  display: flex; z-index: 50;
}
.tabbar button {
  flex: 1; border: none; background: transparent; font-size: 22px;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  color: var(--voyna-muted); gap: 2px; padding: 6px;
}
.tabbar button span { font-size: 11px; }
.tabbar button.active { color: var(--voyna-primary); }
```

- [ ] **Step 2: 라우터 본 구현**

`src/core/router.ts` 전체 교체:
```ts
import { renderTabBar, type Tab } from '@/components/tab-bar';
import { renderLoginPage } from '@/auth/login-page';
import { renderHome } from '@/pages/home';
import { renderMap } from '@/pages/map';
import { renderBadges } from '@/pages/badges';
import { renderMore } from '@/pages/more';
import { loadState } from '@/core/state';

let appRoot: HTMLElement;
let currentTab: Tab = 'home';

export function startRouter(root: HTMLElement): void {
  appRoot = root;
  const state = loadState();
  if (!state.user) {
    renderLoginPage(appRoot, () => navigate('home'));
  } else {
    navigate(currentTab);
  }
}

export function navigate(tab: Tab): void {
  currentTab = tab;
  const state = loadState();
  if (!state.user) {
    renderLoginPage(appRoot, () => navigate('home'));
    return;
  }

  appRoot.innerHTML = '';
  const pageContainer = document.createElement('main');
  pageContainer.className = 'page';
  appRoot.appendChild(pageContainer);

  switch (tab) {
    case 'home':   renderHome(pageContainer); break;
    case 'map':    renderMap(pageContainer); break;
    case 'badges': renderBadges(pageContainer); break;
    case 'more':   renderMore(pageContainer); break;
  }

  appRoot.appendChild(renderTabBar(tab, navigate));
}

export function logoutAndReset(): void {
  currentTab = 'home';
  startRouter(appRoot);
}
```

### Task 5.3: 페이지 스켈레톤 4개

- [ ] **Step 1: 빈 페이지 4개 생성**

`src/pages/home.ts`:
```ts
export function renderHome(root: HTMLElement): void {
  root.innerHTML = '<h1>홈</h1><p>구현 예정</p>';
}
```

`src/pages/map.ts`:
```ts
export function renderMap(root: HTMLElement): void {
  root.innerHTML = '<h1>탐험 맵</h1><p>구현 예정</p>';
}
```

`src/pages/badges.ts`:
```ts
export function renderBadges(root: HTMLElement): void {
  root.innerHTML = '<h1>배지 컬렉션</h1><p>구현 예정</p>';
}
```

`src/pages/more.ts`:
```ts
export function renderMore(root: HTMLElement): void {
  root.innerHTML = '<h1>더보기</h1><p>구현 예정</p>';
}
```

- [ ] **Step 2: 동작 확인**

```bash
npm run dev
```
브라우저에서 로그인 화면 → 구글 로그인 → 4탭 네비게이션 동작 확인.

- [ ] **Step 3: 커밋**

```bash
git add src
git commit -m "feat(ui): 4탭 라우터 + 스켈레톤 페이지"
git push
```

---

## Phase 6: 카카오맵 + POI + 텔레포트

### Task 6.1: 맵 페이지 본 구현

**Files:**
- Rewrite: `src/pages/map.ts`

- [ ] **Step 1: 작성**

`src/pages/map.ts`:
```ts
import { loadKakaoMaps } from '@/core/kakao-loader';
import { getLocations, getBadge, type Location } from '@/core/catalog';
import { loadState, saveState } from '@/core/state';
import { findNearbyBadges, awardBadge } from '@/core/badge-engine';
import { showBadgeAcquired } from '@/components/badge-acquired-modal';
import { showLevelUp } from '@/components/level-up-modal';
import { showTitleToast } from '@/components/title-toast';
import { getBrowserGPS } from '@/core/geo';

let mapInstance: any = null;
let userMarker: any = null;

const GRADE_COLOR: Record<string, string> = {
  special: '#d4a017', rare: '#8e44ad', common: '#3498db', premier: '#ff5252',
};

export async function renderMap(root: HTMLElement): Promise<void> {
  root.innerHTML = `
    <div class="map-wrap">
      <div id="kakao-map" class="kakao-map"></div>
      <div class="map-actions">
        <button id="gps-btn">📍 내 GPS</button>
        <button id="teleport-btn">✈️ 텔레포트</button>
      </div>
      <div id="teleport-panel" class="teleport-panel hidden"></div>
    </div>
    <style>
      .map-wrap { position: relative; height: calc(100vh - var(--tabbar-h) - 32px); }
      .kakao-map { width: 100%; height: 100%; border-radius: 12px; overflow: hidden; }
      .map-actions {
        position: absolute; bottom: 16px; left: 16px; right: 16px;
        display: flex; gap: 8px; z-index: 10;
      }
      .map-actions button {
        flex: 1; padding: 12px; border: none; border-radius: 24px;
        background: white; box-shadow: 0 4px 12px rgba(0,0,0,0.15); font-weight: 600;
      }
      .teleport-panel {
        position: absolute; bottom: 80px; left: 16px; right: 16px;
        background: white; border-radius: 12px; padding: 16px;
        max-height: 50%; overflow-y: auto; box-shadow: 0 8px 24px rgba(0,0,0,0.2); z-index: 11;
      }
      .teleport-panel.hidden { display: none; }
      .teleport-panel h3 { margin: 0 0 12px; font-size: 16px; }
      .tp-item {
        padding: 10px 12px; border-radius: 8px; display: flex;
        justify-content: space-between; align-items: center; cursor: pointer;
      }
      .tp-item:hover { background: #f3f4f6; }
      .tp-item.obtained { opacity: 0.5; }
      .tp-grade {
        font-size: 11px; padding: 2px 8px; border-radius: 999px; color: white;
      }
    </style>
  `;

  await loadKakaoMaps();
  const container = document.getElementById('kakao-map')!;
  const center = new window.kakao.maps.LatLng(37.5573, 126.9485); // ASSIST 기본
  mapInstance = new window.kakao.maps.Map(container, { center, level: 8 });

  // POI 마커 31개
  for (const loc of getLocations()) {
    const pos = new window.kakao.maps.LatLng(loc.lat, loc.lng);
    const marker = new window.kakao.maps.Marker({ position: pos, map: mapInstance, title: loc.name });
    const iw = new window.kakao.maps.InfoWindow({
      content: `<div style="padding:6px 10px;font-size:12px">${loc.name}<br/><span style="color:${GRADE_COLOR[loc.grade]}">${loc.grade}</span></div>`,
    });
    window.kakao.maps.event.addListener(marker, 'click', () => {
      iw.open(mapInstance, marker);
      tryAcquireBadgeAt({ lat: loc.lat, lng: loc.lng });
    });
  }

  // 현재 위치 마커
  const state = loadState();
  const cur = state.currentLocation ?? state.realGPS ?? { lat: 37.5573, lng: 126.9485 };
  setUserMarker(cur.lat, cur.lng);

  document.getElementById('gps-btn')!.addEventListener('click', useRealGPS);
  document.getElementById('teleport-btn')!.addEventListener('click', toggleTeleport);
}

function setUserMarker(lat: number, lng: number): void {
  const pos = new window.kakao.maps.LatLng(lat, lng);
  if (userMarker) userMarker.setMap(null);
  userMarker = new window.kakao.maps.Marker({
    position: pos,
    map: mapInstance,
    image: new window.kakao.maps.MarkerImage(
      'data:image/svg+xml;utf8,' + encodeURIComponent(
        `<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28">
           <circle cx="14" cy="14" r="10" fill="#2a5cdc" stroke="white" stroke-width="3"/>
         </svg>`
      ),
      new window.kakao.maps.Size(28, 28),
      { offset: new window.kakao.maps.Point(14, 14) }
    ),
  });
  mapInstance.panTo(pos);
}

async function useRealGPS(): Promise<void> {
  try {
    const gps = await getBrowserGPS();
    const state = loadState();
    state.realGPS = gps;
    state.currentLocation = { ...gps, isTeleport: false };
    saveState(state);
    setUserMarker(gps.lat, gps.lng);
    tryAcquireBadgeAt(gps);
  } catch (e) {
    alert('GPS 획득 실패: ' + (e as Error).message);
  }
}

function toggleTeleport(): void {
  const panel = document.getElementById('teleport-panel')!;
  if (!panel.classList.contains('hidden')) { panel.classList.add('hidden'); return; }

  const state = loadState();
  const obtained = new Set(state.obtained.map((o) => o.badgeId));
  const items = getLocations().map((loc) => {
    const isObtained = obtained.has(loc.id);
    return `
      <div class="tp-item ${isObtained ? 'obtained' : ''}" data-id="${loc.id}">
        <span>${loc.name}</span>
        <span class="tp-grade" style="background:${GRADE_COLOR[loc.grade]}">${loc.grade}</span>
      </div>`;
  }).join('');
  panel.innerHTML = `<h3>텔레포트 (데모용)</h3>${items}`;
  panel.classList.remove('hidden');

  panel.querySelectorAll<HTMLElement>('.tp-item').forEach((el) => {
    el.addEventListener('click', () => {
      const id = el.dataset.id!;
      const loc = getLocations().find((l) => l.id === id)!;
      teleportTo(loc);
      panel.classList.add('hidden');
    });
  });
}

function teleportTo(loc: Location): void {
  const state = loadState();
  state.currentLocation = { lat: loc.lat, lng: loc.lng, isTeleport: true };
  saveState(state);
  setUserMarker(loc.lat, loc.lng);
  tryAcquireBadgeAt({ lat: loc.lat, lng: loc.lng });
}

async function tryAcquireBadgeAt(coords: { lat: number; lng: number }): Promise<void> {
  const nearby = findNearbyBadges(coords);
  if (nearby.length === 0) return;
  const top = nearby[0]!;
  const result = awardBadge(top.location.id, coords.lat, coords.lng);
  if (!result.success) return;
  await showBadgeAcquired(result.badge);
  if (result.leveledUp) await showLevelUp(result.previousLevel, result.newLevel);
  if (result.newTitle) showTitleToast(result.newTitle);
}
```

- [ ] **Step 2: 의존하는 컴포넌트 stub 작성**

(Task 7에서 본 구현. 일단 빌드 통과용 stub)

`src/components/badge-acquired-modal.ts`:
```ts
import type { Badge } from '@/core/catalog';
export async function showBadgeAcquired(_b: Badge): Promise<void> { /* Task 7 */ }
```

`src/components/level-up-modal.ts`:
```ts
export async function showLevelUp(_prev: number, _next: number): Promise<void> { /* Task 7 */ }
```

`src/components/title-toast.ts`:
```ts
export function showTitleToast(_title: string): void { /* Task 7 */ }
```

- [ ] **Step 3: 동작 확인**

```bash
npm run dev
```
- 로그인 → 맵 탭 진입 → 31개 마커 표시
- 텔레포트 버튼 → 명소 리스트 → 경복궁 선택 → 마커 이동
- (모달은 아직 비어있음, 다음 Phase에서)

- [ ] **Step 4: 커밋**

```bash
git add src
git commit -m "feat(map): 카카오맵 + 31 POI + 텔레포트 + 자동 배지 획득 트리거"
git push
```

---

## Phase 7: 모달 + 애니메이션 컴포넌트

### Task 7.1: 배지 획득 모달

**Files:**
- Rewrite: `src/components/badge-acquired-modal.ts`

- [ ] **Step 1: 작성**

`src/components/badge-acquired-modal.ts`:
```ts
import type { Badge } from '@/core/catalog';

const GRADE_STYLE: Record<string, { color: string; label: string; glow: string }> = {
  special: { color: '#d4a017', label: '특별', glow: '0 0 60px rgba(212,160,23,0.7)' },
  rare:    { color: '#8e44ad', label: '희귀', glow: '0 0 50px rgba(142,68,173,0.6)' },
  common:  { color: '#3498db', label: '일반', glow: '0 0 40px rgba(52,152,219,0.5)' },
  premier: { color: '#ff5252', label: '프리미어', glow: '0 0 80px rgba(255,82,82,0.8)' },
};

export function showBadgeAcquired(badge: Badge): Promise<void> {
  return new Promise((resolve) => {
    const style = GRADE_STYLE[badge.grade] ?? GRADE_STYLE.common!;
    const backdrop = document.createElement('div');
    backdrop.className = 'modal-backdrop';
    backdrop.innerHTML = `
      <div class="modal badge-acquired" style="border:3px solid ${style.color}; box-shadow: ${style.glow}, 0 12px 40px rgba(0,0,0,0.3);">
        <div class="ba-grade" style="color:${style.color}">✨ ${style.label} 배지 획득 ✨</div>
        <img src="${badge.image}" alt="${badge.name}" class="ba-img"
             onerror="this.src='/Voyna-Demo/badges/locked.png'"/>
        <h2 class="ba-name">${badge.name}</h2>
        <p class="ba-desc">${badge.description}</p>
        <div class="ba-xp">+${badge.xp} XP</div>
        <button class="ba-close">확인</button>
      </div>
      <style>
        .badge-acquired { padding: 32px 28px; max-width: 320px; }
        .ba-grade { font-size: 14px; font-weight: 700; letter-spacing: 1px; margin-bottom: 12px; }
        .ba-img {
          width: 140px; height: 140px; border-radius: 50%; margin: 16px 0;
          animation: rotate-in 0.8s ease-out;
        }
        .ba-name { margin: 8px 0; font-size: 22px; }
        .ba-desc { color: var(--voyna-muted); margin: 4px 0 16px; font-size: 14px; }
        .ba-xp {
          font-weight: 700; color: var(--voyna-primary); font-size: 20px;
          margin-bottom: 20px; animation: pulse 0.6s ease-out;
        }
        .ba-close {
          background: var(--voyna-primary); color: white; border: none;
          padding: 12px 28px; border-radius: 999px; font-weight: 600;
        }
        @keyframes rotate-in {
          from { transform: scale(0.3) rotate(-180deg); opacity: 0; }
          to { transform: scale(1) rotate(0deg); opacity: 1; }
        }
        @keyframes pulse {
          0% { transform: scale(0.8); } 50% { transform: scale(1.2); } 100% { transform: scale(1); }
        }
      </style>
    `;
    document.body.appendChild(backdrop);
    const close = () => { backdrop.remove(); resolve(); };
    backdrop.querySelector('.ba-close')!.addEventListener('click', close);
    backdrop.addEventListener('click', (e) => { if (e.target === backdrop) close(); });
  });
}
```

### Task 7.2: 레벨업 모달

**Files:**
- Rewrite: `src/components/level-up-modal.ts`

- [ ] **Step 1: 작성**

`src/components/level-up-modal.ts`:
```ts
export function showLevelUp(prev: number, next: number): Promise<void> {
  return new Promise((resolve) => {
    const backdrop = document.createElement('div');
    backdrop.className = 'modal-backdrop';
    backdrop.innerHTML = `
      <div class="modal level-up">
        <div class="lu-confetti">🎉</div>
        <div class="lu-label">LEVEL UP!</div>
        <div class="lu-numbers">
          <span class="lu-prev">Lv ${prev}</span>
          <span class="lu-arrow">→</span>
          <span class="lu-next">Lv ${next}</span>
        </div>
        <button class="lu-close">계속</button>
      </div>
      <style>
        .level-up { padding: 32px; min-width: 280px; }
        .lu-confetti { font-size: 48px; margin-bottom: 12px; animation: bounce 1s infinite; }
        .lu-label {
          font-size: 14px; font-weight: 800; color: var(--voyna-primary);
          letter-spacing: 3px; margin-bottom: 16px;
        }
        .lu-numbers { font-size: 32px; font-weight: 700; margin-bottom: 24px; }
        .lu-prev { color: var(--voyna-muted); }
        .lu-arrow { margin: 0 12px; color: var(--voyna-primary); }
        .lu-next { color: var(--voyna-primary); animation: glow 1s ease-out; }
        .lu-close {
          background: var(--voyna-primary); color: white; border: none;
          padding: 12px 32px; border-radius: 999px; font-weight: 600;
        }
        @keyframes bounce { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
        @keyframes glow {
          from { text-shadow: 0 0 30px var(--voyna-primary); transform: scale(1.4); }
          to { text-shadow: none; transform: scale(1); }
        }
      </style>
    `;
    document.body.appendChild(backdrop);
    const close = () => { backdrop.remove(); resolve(); };
    backdrop.querySelector('.lu-close')!.addEventListener('click', close);
  });
}
```

### Task 7.3: 칭호 토스트

**Files:**
- Rewrite: `src/components/title-toast.ts`

- [ ] **Step 1: 작성**

`src/components/title-toast.ts`:
```ts
export function showTitleToast(title: string): void {
  const t = document.createElement('div');
  t.className = 'toast';
  t.innerHTML = `🏆 새 칭호 획득: <strong>${title}</strong>`;
  document.body.appendChild(t);
  setTimeout(() => {
    t.style.transition = 'opacity 0.4s';
    t.style.opacity = '0';
    setTimeout(() => t.remove(), 400);
  }, 3000);
}
```

- [ ] **Step 2: 동작 확인 + 커밋**

```bash
npm run dev
```
- 텔레포트 → 경복궁 → 배지 획득 모달(특별 등급 금색) → 확인 → 레벨업 모달 → 계속
- 텔레포트 5곳 누적 → 칭호 토스트 "동네 탐험가"

```bash
git add src/components
git commit -m "feat(ui): 배지 획득·레벨업 모달 + 칭호 토스트"
git push
```

---

## Phase 8: 홈 · 배지 · 더보기 탭

### Task 8.1: 홈 탭

**Files:**
- Rewrite: `src/pages/home.ts`

- [ ] **Step 1: 작성**

`src/pages/home.ts`:
```ts
import { loadState } from '@/core/state';
import { xpToNextLevel } from '@/core/levels';
import { getBadge } from '@/core/catalog';
import { navigate } from '@/core/router';

export function renderHome(root: HTMLElement): void {
  const state = loadState();
  const xpInfo = xpToNextLevel(state.xp);
  const recent = [...state.obtained].slice(-3).reverse();

  root.innerHTML = `
    <header class="home-hero">
      <img class="avatar" src="${state.user?.photoURL || ''}" onerror="this.style.display='none'"/>
      <div>
        <div class="hello">안녕하세요, ${state.user?.displayName ?? '여행자'}님</div>
        <div class="title-line">🏆 ${state.title}</div>
      </div>
    </header>

    <section class="lv-card">
      <div class="lv-top">
        <span class="lv-num">Lv ${state.level}</span>
        <span class="lv-xp">${state.xp} XP</span>
      </div>
      <div class="lv-bar">
        <div class="lv-bar-fill" style="width:${Math.min(100, xpInfo.progress * 100).toFixed(1)}%"></div>
      </div>
      <div class="lv-bar-text">다음 레벨까지 ${xpInfo.nextThreshold - xpInfo.current} XP</div>
    </section>

    <section class="recent">
      <h2>최근 획득 배지</h2>
      <div class="recent-list">
        ${recent.length === 0
          ? '<p class="empty">아직 획득한 배지가 없어요. 맵 탭에서 탐험을 시작해보세요!</p>'
          : recent.map((o) => {
            const b = getBadge(o.badgeId);
            return `
              <div class="recent-item">
                <img src="${b?.image ?? ''}" onerror="this.src='/Voyna-Demo/badges/locked.png'"/>
                <div>
                  <div class="r-name">${b?.name ?? o.badgeId}</div>
                  <div class="r-grade">${b?.grade}</div>
                </div>
              </div>`;
          }).join('')}
      </div>
      <button class="cta" id="go-map">탐험 맵으로 이동</button>
    </section>

    <style>
      .home-hero { display:flex; align-items:center; gap:14px; margin-bottom:20px; }
      .avatar { width:56px; height:56px; border-radius:50%; }
      .hello { font-weight: 700; font-size: 18px; }
      .title-line { color: var(--voyna-muted); font-size: 13px; margin-top: 2px; }

      .lv-card {
        background: white; padding: 18px; border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 20px;
      }
      .lv-top { display: flex; justify-content: space-between; margin-bottom: 10px; }
      .lv-num { font-size: 22px; font-weight: 800; color: var(--voyna-primary); }
      .lv-xp { color: var(--voyna-muted); }
      .lv-bar { background: #e5e7eb; border-radius: 99px; height: 10px; overflow: hidden; }
      .lv-bar-fill { background: var(--voyna-primary); height: 100%; transition: width 0.4s; }
      .lv-bar-text { font-size: 12px; color: var(--voyna-muted); margin-top: 6px; }

      .recent h2 { font-size: 16px; margin-bottom: 12px; }
      .recent-list { display: flex; flex-direction: column; gap: 10px; margin-bottom: 16px; }
      .recent-item {
        background: white; border-radius: 10px; padding: 10px;
        display: flex; gap: 12px; align-items: center;
      }
      .recent-item img { width: 48px; height: 48px; border-radius: 50%; }
      .r-name { font-weight: 600; }
      .r-grade { font-size: 12px; color: var(--voyna-muted); }
      .empty { color: var(--voyna-muted); font-size: 14px; }
      .cta {
        background: var(--voyna-primary); color: white; border: none;
        padding: 14px; width: 100%; border-radius: 10px; font-weight: 600; font-size: 16px;
      }
    </style>
  `;
  document.getElementById('go-map')!.addEventListener('click', () => navigate('map'));
}
```

### Task 8.2: 배지 컬렉션 탭

**Files:**
- Rewrite: `src/pages/badges.ts`

- [ ] **Step 1: 작성**

`src/pages/badges.ts`:
```ts
import { getBadges } from '@/core/catalog';
import { loadState } from '@/core/state';

const GRADE_ORDER = { special: 0, premier: 1, rare: 2, common: 3 } as const;
const GRADE_COLOR: Record<string, string> = {
  special: '#d4a017', rare: '#8e44ad', common: '#3498db', premier: '#ff5252',
};

export function renderBadges(root: HTMLElement): void {
  const state = loadState();
  const obtained = new Set(state.obtained.map((o) => o.badgeId));
  const badges = [...getBadges()].sort((a, b) =>
    GRADE_ORDER[a.grade] - GRADE_ORDER[b.grade] || a.name.localeCompare(b.name)
  );
  const collected = badges.filter((b) => obtained.has(b.id)).length;

  root.innerHTML = `
    <header class="bg-header">
      <h1>배지 컬렉션</h1>
      <div class="bg-progress">${collected} / ${badges.length}</div>
    </header>
    <div class="bg-grid">
      ${badges.map((b) => {
        const got = obtained.has(b.id);
        return `
          <div class="bg-card ${got ? 'got' : 'locked'}">
            <img src="${got ? b.image : '/Voyna-Demo/badges/locked.png'}"
                 onerror="this.src='/Voyna-Demo/badges/locked.png'"/>
            <div class="bg-name">${got ? b.name : '???'}</div>
            <div class="bg-grade" style="color:${got ? GRADE_COLOR[b.grade] : '#9ca3af'}">${b.grade}</div>
          </div>`;
      }).join('')}
    </div>
    <style>
      .bg-header { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 14px; }
      .bg-header h1 { margin: 0; font-size: 20px; }
      .bg-progress { color: var(--voyna-primary); font-weight: 700; }
      .bg-grid {
        display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;
      }
      .bg-card {
        background: white; border-radius: 12px; padding: 12px;
        text-align: center; box-shadow: 0 2px 6px rgba(0,0,0,0.05);
      }
      .bg-card img { width: 64px; height: 64px; border-radius: 50%; margin-bottom: 6px; }
      .bg-card.locked img { filter: grayscale(1) opacity(0.4); }
      .bg-card.locked { opacity: 0.7; }
      .bg-name { font-size: 12px; font-weight: 600; line-height: 1.2; min-height: 28px; }
      .bg-grade { font-size: 10px; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.5px; }
    </style>
  `;
}
```

### Task 8.3: 더보기 탭

**Files:**
- Rewrite: `src/pages/more.ts`

- [ ] **Step 1: 작성**

`src/pages/more.ts`:
```ts
import { loadState, resetState } from '@/core/state';
import { logout } from '@/auth/firebase';
import { logoutAndReset } from '@/core/router';

export function renderMore(root: HTMLElement): void {
  const state = loadState();
  root.innerHTML = `
    <h1>더보기</h1>

    <section class="profile">
      <img src="${state.user?.photoURL || ''}" onerror="this.style.display='none'" class="profile-img"/>
      <div>
        <div class="profile-name">${state.user?.displayName ?? ''}</div>
        <div class="profile-email">${state.user?.email ?? ''}</div>
      </div>
    </section>

    <section class="settings">
      <button class="setting-btn" id="reset-demo">🔄 데모 리셋 (배지/XP 초기화)</button>
      <button class="setting-btn danger" id="logout">🚪 로그아웃</button>
    </section>

    <section class="about">
      <h3>Voyna 데모 v0.1</h3>
      <p>이 빌드는 알토대학원 벤처 스타트업 수업 발표 데모용입니다.</p>
      <p>본 서비스는 12주 일정으로 별도 개발 중입니다.</p>
    </section>

    <style>
      .profile { display: flex; gap: 14px; align-items: center; padding: 16px;
                 background: white; border-radius: 12px; margin-bottom: 16px; }
      .profile-img { width: 60px; height: 60px; border-radius: 50%; }
      .profile-name { font-weight: 700; font-size: 16px; }
      .profile-email { color: var(--voyna-muted); font-size: 13px; }
      .settings { display: flex; flex-direction: column; gap: 8px; margin-bottom: 24px; }
      .setting-btn {
        background: white; border: none; padding: 14px; text-align: left;
        border-radius: 10px; font-size: 14px; font-weight: 500;
      }
      .setting-btn.danger { color: #dc2626; }
      .about { background: white; padding: 16px; border-radius: 12px; }
      .about h3 { margin: 0 0 8px; font-size: 14px; }
      .about p { margin: 4px 0; font-size: 12px; color: var(--voyna-muted); }
    </style>
  `;

  document.getElementById('reset-demo')!.addEventListener('click', () => {
    if (!confirm('정말 모든 배지/XP를 초기화하시겠어요? (계정 정보는 유지됩니다)')) return;
    const u = loadState().user;
    resetState();
    if (u) {
      const s = loadState();
      s.user = u;
      // 직접 saveState 불러 user만 보존
      localStorage.setItem('voyna_demo_state_v1', JSON.stringify(s));
    }
    location.reload();
  });

  document.getElementById('logout')!.addEventListener('click', async () => {
    await logout();
    resetState();
    logoutAndReset();
  });
}
```

- [ ] **Step 2: 동작 확인**

```bash
npm run dev
```
- 홈 탭: 닉네임·레벨·XP바·최근 배지 표시
- 배지 탭: 31칸 그리드, 미획득은 회색 자물쇠
- 더보기 탭: 프로필, 리셋, 로그아웃 동작

- [ ] **Step 3: 커밋**

```bash
git add src
git commit -m "feat(ui): 홈/배지/더보기 탭 완성"
git push
```

---

## Phase 9: 배지 이미지 자산

### Task 9.1: 핵심 10개 배지 AI 생성

> 사용자(인간)가 수행. Claude는 프롬프트와 파일명 가이드만 제공.

- [ ] **Step 1: AI 도구 선택**

권장: Microsoft Designer (https://designer.microsoft.com) 또는 Ideogram (https://ideogram.ai). 무료 사용량으로 10개 충분.

- [ ] **Step 2: 공통 프롬프트 템플릿**

각 배지별로 다음 템플릿을 사용 (이미지 사이즈 1024×1024, 정사각형, 원형 배지 디자인):
```
A circular travel achievement badge for "{명소명}", clean flat design, 
{등급} grade with {색상} metallic border, single iconic symbol 
representing {특징}, no text, vector illustration style, 
white background, 1024x1024 px
```

- [ ] **Step 3: 10개 생성 (등급별 색상)**

- 특별(5): 금색 테두리. ASSIST(책+학사모), 경복궁(전각 지붕), N서울타워(타워 실루엣), 청와대(푸른 기와), 북한산(산봉우리)
- 희귀(3): 보라 테두리. 창덕궁(전각+나무), 롯데월드타워(고층 빌딩), 반포 한강(다리+노을)
- 일반(2): 파랑 테두리. 명동(쇼핑백), 광화문(누각)

- [ ] **Step 4: 파일명 규칙대로 저장**

`public/badges/` 디렉터리에 다음 파일명으로 저장:
- `assist.png`
- `gyeongbok.png`
- `n-seoul-tower.png`
- `cheongwadae.png`
- `bukhansan.png`
- `changdeok.png`
- `lotte-tower.png`
- `banpo-hangang.png`
- `myeongdong.png`
- `gwanghwamun.png`

### Task 9.2: `locked.png` 자물쇠 이미지

- [ ] **Step 1: 디자인 또는 SVG로 생성**

빠른 옵션: SVG를 PNG로 변환. 일단 SVG로 임시 생성하고 후속에 PNG 교체.

`public/badges/locked.png`:
회색 원 배경 + 흰색 자물쇠 아이콘. 사이즈 256×256 충분.

Designer/Ideogram에 다음 프롬프트:
```
A simple circular locked badge icon, gray gradient background, 
white padlock symbol in center, flat design, no text, 256x256
```

- [ ] **Step 2: 11개 파일 존재 확인**

```bash
ls public/badges/
```
Expected: `assist.png  banpo-hangang.png  bukhansan.png  changdeok.png  cheongwadae.png  gwanghwamun.png  gyeongbok.png  locked.png  lotte-tower.png  myeongdong.png  n-seoul-tower.png`

- [ ] **Step 3: 동작 확인**

```bash
npm run dev
```
- 배지 탭에서 잠긴 배지들은 회색 자물쇠
- 텔레포트로 경복궁 획득 → 모달에 진짜 경복궁 배지 이미지 표시 → 배지 탭에서도 컬러로 빛남

- [ ] **Step 4: 커밋**

```bash
git add public/badges
git commit -m "assets: 핵심 10개 배지 + locked 이미지"
git push
```

---

## Phase 10: GitHub Actions Pages 배포

### Task 10.1: 워크플로 작성

**Files:**
- Create: `.github/workflows/deploy.yml`

- [ ] **Step 1: 작성**

`.github/workflows/deploy.yml`:
```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: npm }
      - run: npm ci
      - name: Build
        env:
          VITE_FB_API_KEY: ${{ secrets.VITE_FB_API_KEY }}
          VITE_FB_AUTH_DOMAIN: ${{ secrets.VITE_FB_AUTH_DOMAIN }}
          VITE_FB_PROJECT_ID: ${{ secrets.VITE_FB_PROJECT_ID }}
          VITE_FB_STORAGE_BUCKET: ${{ secrets.VITE_FB_STORAGE_BUCKET }}
          VITE_FB_MESSAGING_SENDER_ID: ${{ secrets.VITE_FB_MESSAGING_SENDER_ID }}
          VITE_FB_APP_ID: ${{ secrets.VITE_FB_APP_ID }}
          VITE_KAKAO_MAP_KEY: ${{ secrets.VITE_KAKAO_MAP_KEY }}
        run: npm run build
      - uses: actions/upload-pages-artifact@v3
        with: { path: dist }

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

### Task 10.2: GitHub Secrets 등록

> 사용자가 수행.

- [ ] **Step 1: 리포 Secrets 페이지 진입**

`https://github.com/AlexSong0674/Voyna-Demo/settings/secrets/actions`

- [ ] **Step 2: 7개 Secret 추가**

"New repository secret"으로 다음 7개 등록:
- `VITE_FB_API_KEY`
- `VITE_FB_AUTH_DOMAIN`
- `VITE_FB_PROJECT_ID`
- `VITE_FB_STORAGE_BUCKET`
- `VITE_FB_MESSAGING_SENDER_ID`
- `VITE_FB_APP_ID`
- `VITE_KAKAO_MAP_KEY`

값은 `.env.local`과 동일하게 입력.

### Task 10.3: Pages 활성화

> 사용자가 수행.

- [ ] **Step 1: Settings → Pages**

`https://github.com/AlexSong0674/Voyna-Demo/settings/pages`

- [ ] **Step 2: Source 선택**

"Source" → "GitHub Actions" 선택.

### Task 10.4: 첫 배포

- [ ] **Step 1: 워크플로 푸시**

```bash
git add .github/workflows/deploy.yml
git commit -m "ci: GitHub Actions Pages 배포 워크플로"
git push
```

- [ ] **Step 2: Actions 탭에서 빌드 모니터링**

`https://github.com/AlexSong0674/Voyna-Demo/actions` → "Deploy to GitHub Pages" 워크플로 → green ✅ 확인.

- [ ] **Step 3: 라이브 URL 동작 확인**

`https://alexsong0674.github.io/Voyna-Demo/` 접속 → 로그인 → 맵 → 텔레포트 → 배지 획득까지 전체 동선 확인.

Firebase 인증 도메인에 `alexsong0674.github.io` 등록되어 있는지 재확인 (Task 0.3 Step 4).

---

## Phase 11: 데모 스크립트 + 모바일 리허설

### Task 11.1: DEMO_SCRIPT.md 작성

**Files:**
- Create: `docs/DEMO_SCRIPT.md`

- [ ] **Step 1: 작성**

`docs/DEMO_SCRIPT.md`:
```markdown
# Voyna 데모 시연 스크립트

> 대상: 알토대학원 벤처 스타트업 수업 / 발표 시간 5~7분

## 준비물

- 발표자 스마트폰(또는 노트북) — Chrome/Safari 최신
- 노트북 빔프로젝터 미러링
- 라이브 URL: https://alexsong0674.github.io/Voyna-Demo/
- (옵션) 사전 로그아웃 + 데모 리셋 완료된 상태

## 시나리오 (5분 30초)

### 0:00–0:30 오프닝
"여행이 게임이 된다면 어떨까요. Voyna는 GPS 기반으로 명소를 방문하면 자동으로 배지를 모으는 앱입니다."

### 0:30–1:30 로그인 + 첫 화면
1. URL 접속 → 로그인 화면 (브랜드 + 슬로건 노출)
2. Google 로그인 → 즉시 홈 진입
3. "Lv 1, XP 0, 초보 탐험가" 상태 보여주기
4. "아직 배지가 없죠? 탐험해볼까요?"

### 1:30–3:30 탐험 맵 + 텔레포트
1. 맵 탭 진입 → 31개 명소 마커 노출
2. "사용자가 직접 가야 받는 건데, 강의실이라 텔레포트 데모 모드를 켤게요"
3. 텔레포트 → ASSIST 강의실 선택 (특별 등급 자기 강의실 — 청중 반응 유도)
4. ✨ 특별 배지 획득 모달 (금빛, +300 XP) → 레벨업 모달 → 확인
5. 연이어 텔레포트 → 경복궁, 북한산, N서울타워 순회 (각 +400)
6. 누적되면 "동네 탐험가" 칭호 토스트 등장

### 3:30–4:30 배지 컬렉션
1. 배지 탭 진입 → 컬러로 빛나는 5개 + 회색 자물쇠 26개
2. "이 잠긴 배지들을 채우는 게 다음 동기부여입니다"

### 4:30–5:00 본 프로젝트 안내
1. 더보기 탭 → "이 빌드는 데모용입니다. 12주 일정으로 실제 iOS 앱 출시 준비 중"

### 5:00–5:30 클로징
"여행은 추억이 되지만, Voyna에서는 기록도 됩니다. 발걸음이 자산이 되는 새로운 여행 방식, Voyna."

## 비상 시나리오

- **GPS 실패 / 카카오맵 미로드:** 텔레포트로만 진행
- **로그인 안됨:** 미리 로그인된 다른 탭 사용
- **배지 이미지 깨짐:** 회색 자물쇠 fallback이 자동 적용되므로 그대로 진행
- **네트워크 끊김:** 캐시된 상태로 계속 동작 (Service Worker는 없으나 localStorage 유지)

## 사전 점검 체크리스트 (발표 30분 전)

- [ ] 라이브 URL 접속 가능
- [ ] Google 로그인 동작
- [ ] 카카오맵 타일 로드 성공
- [ ] 텔레포트 → 배지 획득 모달 정상
- [ ] 배지 이미지 10개 표시
- [ ] 데모 리셋 후 처음부터 시연 가능
- [ ] 빔프로젝터 미러링 화면 비율 OK
- [ ] 폰트 깨짐 없는지(한글)
```

### Task 11.2: 모바일 실기기 리허설

- [ ] **Step 1: 폰에서 라이브 URL 접속**

스마트폰 Chrome/Safari → `https://alexsong0674.github.io/Voyna-Demo/`

- [ ] **Step 2: 전체 동선 시연**

로그인 → 홈 → 맵 → 텔레포트 → 배지 획득 → 레벨업 → 배지 탭 → 더보기 → 데모 리셋 까지 한 번 통과.

- [ ] **Step 3: 발견된 버그 핫픽스**

발견 시 별도 커밋. 일반적인 모바일 이슈:
- 텔레포트 패널 스크롤 안 됨 → `overflow-y: auto` 확인
- 모달 너무 크거나 작음 → `max-width: 90vw` 확인
- 카카오맵 키 도메인 미등록 → Task 0.2 Step 2 재확인

### Task 11.3: 최종 커밋·푸시

- [ ] **Step 1: 커밋**

```bash
git add docs/DEMO_SCRIPT.md
git commit -m "docs: 데모 시연 스크립트"
git push
```

- [ ] **Step 2: 라이브 재배포 확인**

GitHub Actions가 자동 빌드·배포 → 5분 내 라이브 URL 갱신.

---

## 컷오프 우선순위 (시간 부족 시 자르는 순서)

1. **Phase 9 정성 디자인 10개 → 5개로 축소** (ASSIST + 경복궁 + N서울타워 + 북한산 + 명동만 정성, 나머지는 자물쇠)
2. **Phase 8.3 더보기 탭 최소화** (로그아웃 버튼만)
3. **Phase 11.1 DEMO_SCRIPT 짧게** (시나리오 한 단락만)
4. **칭호 시스템 단순화** (1~2개만 유지)
5. **레벨업 모달 폭죽 애니메이션 생략**

핵심 시연 동선(로그인 → 텔레포트 → 배지 획득 모달 → 배지 탭 컬렉션)은 절대 컷하지 않는다.

---

## 다음 단계

이 plan을 **`superpowers:subagent-driven-development`** 또는 **`superpowers:executing-plans`**로 task-by-task 실행. Task 0(준비)은 사용자 수동 작업이 일부 섞여 있으니 그 단계만 사용자 확인 후 진행.
