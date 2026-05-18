# Brontosys Homepage 작업 내역

> 파일: `brontosys_homepage.html`  
> 위치: `C:\Users\KIMKINAM\Desktop\Brontosys_home\`

---

## 1. 전체 구조

- **Single Page Application (SPA)** — 단일 HTML 파일
- `renderPage(id)` / `goPage(id)` JS 라우팅으로 페이지 전환
- 페이지 목록: `home`, `greeting`, `orgchart`, `location`, `rpa`, `falcon`, `Veeam`, `virtualization`, `sysimpl`, `notice`, `inquiry`

---

## 2. 네비게이션 / 레이아웃

- 상단 nav 공통 적용 (데스크탑 + 모바일 햄버거 메뉴)
- 브라우저 히스토리 연동 (`history.pushState`, `popstate`)
- URL 파라미터 `?page=xxx` 로 직접 접근 가능

---

## 3. Footer (공통)

- `#home` 페이지에 footer HTML 작성 (base64 로고 포함)
- `injectFooters()` JS 함수로 **모든 페이지에 동적 복제 삽입**
  - `.footer` + `.footer-bottom` 을 `cloneNode(true)` 로 복사
  - base64 이미지 중복 저장 없이 메모리 효율적으로 처리
- `DOMContentLoaded` 시점에 자동 실행

---

## 4. Service 페이지 (sysimpl)

### sv-steps 레이아웃 수정
- 요구사항 분석 / 설계 / 구축 / 운영 및 지원 — 4단계 수평 정렬
- `flex-direction: column` + `align-items: flex-start` 로 이름 수평 맞춤
- `›` 화살표 제거, 픽토그램 옆에 텍스트 배치

### CSS 미디어쿼리 정리
- 중복 / 충돌 미디어쿼리 제거

---

## 5. Veeam 페이지

### 5-1. 헤더 섹션
- `.greeting-header` 공통 헤더 적용
- 소개 텍스트 + 아키텍처 다이어그램 (`image/img_sub254.jpg`)
- h3, p, img 에 `reveal` 클래스 추가 (순차 등장 효과)

### 5-2. 주요 5가지 기능 카드 (.vm-func)
| 카드 | 아이콘 이미지 |
|------|-------------|
| 빠른 복구 | `image/recover.png` |
| 완벽한 데이터보호 | `image/lock.png` |
| 자동화 복구검증 | `image/sand clock.png` |
| 데이터활용 | `image/diagram.png` |
| 데이터 가시성 확보 | `image/monitor-heart.png` |

- SVG 픽토그램 → PNG 이미지로 교체
- CSS `filter`로 **`#6db33f`** (Veeam 그린) 색상 적용
- `max-width: 1240px` 로 페이지 너비 확장 (기존 960px)

### 5-3. 도입효과 섹션 (.vm-effect)
- 정성적 효과 3개 카드 (grid 3열)
- 정량적 효과 2개 카드 (grid 2열)
- 각 카드에 이미지 (`1.jpg` ~ `5.jpg`) 삽입
- 폰트 크기 일괄 +2px 조정 (vm-func-inner, vm-effect-card-list 등)

### 5-4. 제품 소개 박스 (.vm-intro)
- vm-effect 하단에 배치
- `Veeam_3d.jpg` (293×238px) + 오른쪽 용도/개요 텍스트
- 얇은 테두리 직사각형 (`border: 1px solid #d0d8e4`)
- `max-width: 1000px`, 내부 패딩 30px

**클래스 정의:**
| 클래스 | 역할 |
|--------|------|
| `.vm-intro` | 외부 섹션 래퍼 |
| `.vm-intro-inner` | 테두리 박스 |
| `.vm-intro-img` | 이미지 영역 |
| `.vm-intro-content` | 오른쪽 텍스트 |
| `.vm-intro-label` | 용도/개요 레이블 (21px bold) |
| `.vm-intro-sub` | 용도 내용 (17px) |
| `.vm-intro-heading` | 개요 레이블 (21px bold) |
| `.vm-intro-items` | 개요 항목 리스트 (17px) |

---

## 6. 이미지 경로

- 로컬 폴더: `image/` (단수, `images/` 아님)
- 배포 시 base64 인코딩 필요 (현재 로컬 경로)

| 파일 | 용도 |
|------|------|
| `img_sub254.jpg` | Veeam 아키텍처 다이어그램 |
| `1.jpg` ~ `5.jpg` | Veeam 도입효과 카드 이미지 |
| `recover.png` | 빠른복구 아이콘 |
| `lock.png` | 완벽한 데이터보호 아이콘 |
| `sand clock.png` | 자동화 복구검증 아이콘 |
| `diagram.png` | 데이터활용 아이콘 |
| `monitor-heart.png` | 데이터 가시성 확보 아이콘 |
| `Veeam_3d.jpg` | 제품 소개 3D 이미지 |
| `Beams.jpg` | 배경 이미지 |
| `Falcon.jpg` | FalconStor 이미지 |
| `RPA.jpg` | RPA 이미지 |

---

## 7. Reveal 스크롤 애니메이션

### 동작 방식
- `IntersectionObserver` 기반 — 요소가 viewport에 들어올 때 `.visible` 추가
- `opacity: 0` + `translateY(32px)` → `opacity: 1` + `translateY(0)`
- **페이지 전환 시마다 재생** (renderPage 호출 시 setupReveal 실행)

### 핵심 수정사항
- viewport 안 요소 애니메이션 스킵 문제 해결
  - `remove('visible')` 후 **60ms setTimeout** 뒤 `observe()` 시작
  - repaint 완료 후 observer 등록으로 정상 애니메이션 보장

### 타이밍
| 항목 | 값 |
|------|-----|
| transition 지속시간 | 0.8s |
| reveal-delay-1 | 0.1s |
| reveal-delay-2 | 0.25s |
| reveal-delay-3 | 0.4s |
| 카드 stagger 간격 | 0.08s |
| 카드 최대 딜레이 | 0.48s |

### 페이지별 적용 요소

| 페이지 | 적용 요소 |
|--------|----------|
| **공통 헤더** | breadcrumb → h2 → sub → 주황선 순차 등장 |
| **회사소개** | greeting-hero-box 내부 h3/h2/divider/p, gsvc-card |
| **조직도** | org2-title-area 내부, org2-ceo, org2-team-card ×4 순차 |
| **오시는 길** | 지도 wrapper, info-card |
| **Veeam** | h3/p/img, vm-func-card, vm-effect-card, vm-intro-inner |
| **Service** | sv-ov-card, sv-sec 텍스트, sv-img-wrap, sv-step, sv-process, sv-cta |
| **공지사항** | notice-list |
| **문의하기** | inquiry-form |

### CSS 충돌 해결
- `.sv-ov-card`의 `transition: box-shadow 0.2s`가 reveal transition 덮어쓰는 문제
- `.sv-ov-card.reveal` 전용 규칙 추가 → opacity/transform/box-shadow 모두 유지

### AUTO_REVEAL 자동 적용 셀렉터
```javascript
'.nh-intro-text', '.nh-intro-sub', '.nh-intro-company', '.nh-solutions-inner',
'.greeting-hero-box', '.gsvc-card',
'.org2-title-area', '.org2-board-card', '.org2-ceo', '.org2-team-card',
'.location-wrap',
'.vm-intro-inner', '.vm-func-card', '.vm-effect-section-title', '.vm-effect-card',
'.sv-ov-card', '.sv-sec-inner', '.sv-step', '.sv-cta-inner', '.sv-process-inner',
'.info-card', '.placeholder-block',
'.notice-list', '.inquiry-form'
```

---

## 8. 기억사항 (Memory)

- 작업 파일: `brontosys_homepage.html`
- 프리뷰 패널 안내 문구 출력 금지
- Veeam 아이콘 색상: `#6db33f` (픽토그램 교체 시 유지)
