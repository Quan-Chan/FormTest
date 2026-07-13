# FormTest - AI 구조화된 형식 분석 능력 테스트 프레임워크

> **포함된 테스트 세트는 모두 AI가 생성한 가상 데이터이며, 실제 데이터가 아닙니다. 우연히 일치할 경우 순수한 우연입니다.**
>
> **이 프로젝트는 충분한 프로그램 구축 및 테스트 계획을 거치지 않았으며, 코드 구조와 테스트 커버리지가 아직 완벽하지 않습니다. 참고 및 학습용으로만 사용하십시오.**

LLM(대규모 언어 모델)의 구조화된 데이터 형식 이해 및 분석 능력을 평가하기 위한 자동화된 테스트 프레임워크입니다. 사전 정의된 테스트 케이스를 통해 AI API를 자동으로 호출하고 반환 결과를 예상 답변과 비교하여 모델의 형식 이해 성능을 정량화합니다.

## 빠른 시작

### 1. 의존성 설치

```bash
pip install -r APPs/requirements.txt
```

### 2. 실행

```bash
cd APPs
python app.py
# 또는 run.bat 더블 클릭
```

브라우저에서 [http://localhost:5000](http://localhost:5000) 열기

### 3. 설정

실행 후 웹 인터페이스 우측 상단의 **설정** 버튼을 클릭하여 API 주소, 모델, 매개변수 등을 구성합니다. `APPs/config.example.json`을 참조하여 설정 파일을 생성할 수도 있습니다.

주요 설정 항목:
- `base_url` — API 주소 (`/v1` 자동 추가 지원)
- `model` — 기본 모델명
- `model_thinking_config` — 모델별 추론/사고 모드 설정
- `streaming` — SSE 스트리밍 출력 스위치
- `concurrency` — 동시 스레드 수
- `disabled_params` — 프론트엔드에서 숨기거나 비활성화할 매개변수

### 4. 테스트 실행

1. **캔버스**에서 노드 편집기를 통해 프롬프트 × 질문 × 모델 조합
2. **테스트 시작**을 클릭하여 실시간 스트리밍 결과 확인
3. 테스트 완료 후 **이력 결과**에서 확인/필터링

## 프로젝트 구조

```
FormTest/
├── APPs/                          # 메인 프로그램
│   ├── app.py                     # Flask 백엔드 (API + 테스트 실행 엔진 + SSE 스트리밍)
│   ├── requirements.txt           # Python 의존성
│   ├── run.bat                    # Windows 실행 스크립트
│   ├── config.example.json        # 설정 템플릿
│   ├── flow.json                  # 플로우차트 정의
│   └── static/
│       └── index.html             # 프론트엔드 SPA (네이티브 HTML/CSS/JS, 약 7300줄)
├── Benches/                       # 테스트 데이터셋
│   ├── AI嘉豪测试/                # AI 리터러시 객관식 문제 (NAGI STUDIO 각색)
│   ├── Python测试/                # Python 고급 지식 테스트
│   ├── 企业信息测试/              # 가상 기업工商 정보
│   ├── 教学视频测试/              # Python 입문 교육 비디오 콘텐츠
│   └── 运行日志测试/              # 시스템 운영 로그 분석
├── skills/                        # 사용자가 직접 사용할 수 있는 도구 스크립트
│   ├── New-TestSet-新建测试集.ps1 # PowerShell 새 테스트 세트 스켈레톤 생성
│   └── QA-Extract-问答提取.md     # 소스 파일에서 QA 쌍 추출 가이드
├── .opencode/
│   └── skills/                    # opencode AI 스킬 (AI Agent 지원용)
│       ├── new-test-set/          # 테스트 세트 스켈레톤 생성
│       └── qa-extract/            # QA 쌍 추출
├── .gitignore
├── LICENSE                        # Apache License 2.0
└── README.md                      # 본 파일
```

## 테스트 세트

### 구조

각 테스트 세트는 `.test-set-part` 마커 파일을 통해 하위 디렉터리 역할을 식별합니다. 디렉터리명은 자유롭게 지정할 수 있으며, 시스템은 마커 파일의 내용을 인식합니다:

```
Benches/<이름>/
├── <질문 디렉터리>/               # .test-set-part 포함 → "questions"
│   ├── .test-set-part
│   ├── 基础问题.json              # 10문제
│   └── 进阶问题.json              # 10문제 (일부 테스트 세트는 기초 문제만 있음)
├── <프롬프트 디렉터리>/           # .test-set-part 포함 → "prompts"
│   ├── .test-set-part
│   ├── <이름>原版.json            # 일반 텍스트 서사 형식
│   ├── <이름>列表.json            # 번호 목록 형식
│   ├── <이름>JSON.json            # JSON 구조화 형식
│   ├── <이름>YAML.json            # YAML 형식
│   ├── <이름>XML.json             # XML 형식
│   ├── <이름>Markdown.json        # Markdown 테이블 형식
│   ├── <이름>MarkdownKV.json      # Markdown 키-값 쌍 형식
│   └── <이름>DSL.json             # 사용자 정의 DSL 형식
└── <결과 디렉터리>/               # .test-set-part 포함 → "results" (런타임 생성)
    └── .test-set-part
```

### 테스트 형식

| 형식 | 설명 |
|------|------|
| 원본 (Plain Text) | 일반 텍스트 서사, 기준 비교용 |
| 목록 (List) | 번호/기호 목록 |
| JSON | 표준 JSON 객체 |
| YAML | YAML 구조화 데이터 |
| XML | XML 태그 계층 표현 |
| Markdown | Markdown 테이블 |
| MarkdownKV | Markdown 키-값 쌍 |
| DSL | 사용자 정의 도메인 특화 언어 |

### 테스트 도메인

| 테스트 세트 | 내용 도메인 | 문제 수 | 출처 |
|--------|----------|------|------|
| 교육 비디오 테스트 | Python 프로그래밍 강의 전사록 | 20 | AI 가상 |
| 기업 정보 테스트 | 가상 기업工商 정보 | 20 | AI 가상 |
| 운영 로그 테스트 | 시스템 운영 로그 항목 | 20 | AI 가상 |
| Python 테스트 | Python 데코레이터/제너레이터/컨텍스트 관리자 | 20 | AI 가상 |
| AI 리터러시 테스트 | AI 리터러시 객관식 문제 (기초/고급/오해/인문) | 30 | [NAGI STUDIO](https://github.com/nagi-studio/ai-jiahao) 각색 (MIT) |

## 핵심 기능

- **시각적 캔버스 편집기** — SVG 노드 캔버스, 드래그 앤 드롭으로 프롬프트 × 질문 × 모델 조합, 연결선 그리기 지원
- **실행 취소/다시 실행** — 전체 히스토리 기록 시스템, Ctrl+Z / Ctrl+Shift+Z 지원
- **다중 형식 비교 테스트** — 동일한 내용을 8가지 형식으로 표현, 각 형식에 대한 모델 이해 차이 평가
- **배치 자동화 테스트** — 프롬프트 × 질문 × 모델의 데카르트 곱 조합, 자동 동시 실행
- **다중 모델 관리** — 모델 팝업 관리, 추가/삭제/정렬 지원
- **추론 설정** — 모델별로 thinking/reasoning_effort 매개변수 독립 구성
- **매개변수 비활성화 토글** — 각 매개변수를 dot-toggle으로 개별 활성화/비활성화
- **스트리밍 실시간 출력** — SSE 기반 스트리밍 결과 푸시, 테스트 진행 상황 실시간 확인
- **이력 결과 조회** — 상태/모델/텍스트 검색으로 과거 실행 결과 필터링
- **보관/복원** — 테스트 설정 스냅샷 저장/로드 (캔버스 상태 + 모델 추론 설정 포함)
- **_notFound 모델 감지** — 캔버스가 사용 불가능한 모델을 자동 감지하여 ⚠ 경고 표시
- **자동 /v1 추가** — 토글 스위치로 API 주소 뒤에 자동으로 `/v1` 추가
- **다크/라이트 테마** — 완전한 CSS 변수 시스템으로 테마 전환 지원
- **Anthropic API 지원** — Anthropic 메시지 형식 + 전용 SSE 추론 파싱 지원
- **다회 테스트** — 단일 문제를 여러 번 반복하여 응답 안정성 측정
- **동시성 제어** — 설정 가능한 동시 스레드 수 및 재시도 전략
- **증분 저장** — 테스트 중 정기적으로 결과를 증분 저장하여 예기치 않은 손실 방지
- **경로 보안 검증** — 경로 탐색 공격 방지, Windows 예약 이름 검사, 파일 이름 화이트리스트

## API 인터페이스

| 엔드포인트 | 메서드 | 설명 |
|------|------|------|
| `/` | GET | 프론트엔드 SPA 제공 |
| `/api/v1/config` | GET/POST | 설정 읽기/저장 |
| `/api/v1/models` | GET/POST | 사용 가능한 모델 목록 가져오기/저장 |
| `/api/v1/test-set/scan` | GET | 테스트 세트 스캔 |
| `/api/v1/test-set/prompts` | GET | 테스트 세트 시스템 프롬프트 가져오기 |
| `/api/v1/test-set/questions` | GET | 테스트 세트 질문 가져오기 |
| `/api/v1/test-set/results` | GET | 과거 테스트 결과 가져오기 |
| `/api/v1/test-job/hub` | POST | 통합 작업 스케줄링 (action: start/status/stop) |
| `/api/v1/test-job/stream/<job_id>` | GET | SSE 스트리밍 실시간 결과 푸시 |
| `/api/v1/canvas-state` | GET/POST | 캔버스 상태 저장/읽기 |
| `/api/v1/archives` | GET/POST/DELETE | 보관 관리 |
| `/api/v1/tags` | GET | 모든 태그 가져오기 |

오류 응답: `404` → `{"error": "Not found"}`, `500` → `{"error": "서버 내부 오류"}`

## 설정 항목

| 키 | 타입 | 설명 |
|-----|------|------|
| `api_key` | string | API 키 |
| `base_url` | string | API 주소 |
| `model` | string | 기본 모델명 |
| `models` | string[] | 추가 모델 목록 |
| `temperature` | float | 온도 (0-2) |
| `top_p` | float | Top-P (0-1) |
| `top_k` | int | Top-K |
| `min_p` | float | Min-P |
| `context_size` | int | 컨텍스트 크기 |
| `concurrency` | int | 동시 스레드 수 (1-50) |
| `test_count` | int | 문제당 반복 테스트 횟수 |
| `max_retries` | int | 최대 재시도 횟수 |
| `streaming` | bool | SSE 스트리밍 스위치 |
| `timeout` | int | 요청 제한 시간 (초) |
| `model_thinking_config` | object | 모델별 추론 설정 (예: `{"model-a": {"thinking": {"type": "enabled"}, "reasoning_effort": "medium"}}`) |
| `anthropic_mode` | bool | 강제 Anthropic 메시지 형식 사용 |
| `force_openai_endpoint` | bool | 강제 OpenAI 호환 엔드포인트 사용 |
| `disabled_params` | string[] | 프론트엔드에서 숨기거나 비활성화할 매개변수명 목록 |

## OpenCode Skills

이 프로젝트에는 테스트 세트를 빠르게 생성하고 관리하는 데 도움이 되는 두 가지 도구 스킬이 포함되어 있습니다:

### 사용자 도구 (`skills/`)

개발자가 직접 실행할 수 있는 스크립트와 문서:

| 파일 | 설명 |
|------|------|
| `skills/New-TestSet-新建测试集.ps1` | PowerShell 스크립트, 번호가 있는 테스트 세트 스켈레톤 디렉터리와 .test-set-part 마커 파일 자동 생성 |
| `skills/QA-Extract-问答提取.md` | 상세 가이드, 소스 파일에서 QA 쌍을 추출하고 호환되는 JSON 파일을 생성하는 방법 설명 |

### AI Agent 스킬 (`.opencode/skills/`)

[opencode](https://opencode.ai) 또는 호환되는 AI 코딩 도구를 사용하는 경우, `.opencode/skills/`의 스킬이 AI Agent에 의해 자동으로 발견되고 로드될 수 있습니다:

| 스킬 | 설명 |
|------|------|
| `new-test-set` | AI가 테스트 세트 스켈레톤(디렉터리 + 마커 파일)을 생성하도록 안내, 자동 번호 부여로 충돌 방지 |
| `qa-extract` | AI가 소스 파일에서 QA 쌍을 추출하여 FormTest 테스트 세트와 호환되는 JSON 형식으로 출력하도록 안내 |

## 기술 스택

- **백엔드**: Python Flask + Flask-CORS
- **프론트엔드**: 네이티브 HTML / CSS (사용자 정의 변수 시스템, 다크/라이트 테마) / JavaScript
- **AI 호출**: `requests` 라이브러리 (SSE 스트리밍 및 일반 JSON 두 가지 모드 지원, OpenAI / Anthropic API 호환)
- **동시성**: `ThreadPoolExecutor` 스레드 풀 + 지수 백오프 재시도
- **출력**: Server-Sent Events (`text/event-stream`)

## 중요 고지

**이 프로젝트의 테스트 세트 내용은 모두 AI가 생성한 가상의 예제 데이터이며, 실제 데이터가 아닙니다. 우연히 일치할 경우 순수한 우연입니다.** 모든 데이터는 AI 모델의 구조화된 형식 이해 및 분석 능력을 평가하기 위해서만 사용되며, 어떠한 실제 비즈니스 시나리오나 개체도 대표하지 않습니다.

- `Benches/AI嘉豪测试/`는 [NAGI STUDIO의 AI 리터러시 테스트](https://github.com/nagi-studio/ai-jiahao)를 각색한 것으로, MIT 라이선스에 따라 배포됩니다
- 나머지 테스트 세트는 모두 AI가 생성한 가상 데이터입니다

## 라이선스

Apache License 2.0 — 자세한 내용은 [LICENSE](LICENSE) 파일 참조

---

**이것은 AI가 가짜 술을 마시고 써낸 결과물일 수 있습니다. 저는 주로 AI를 혼내주기 위해 이걸 만들었습니다.**
