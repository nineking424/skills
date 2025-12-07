# Backend Development Skills

백엔드 개발을 위한 Claude Code 스킬 모음입니다. 프롬프트 강화부터 코드 생성, 테스트, 리뷰, 인프라 설계까지 백엔드 개발 전 과정을 지원합니다.

## 스킬 개요

총 18개의 스킬이 5개 플러그인으로 구성되어 있습니다.

### Workflow (개발 워크플로우)

| 스킬 | 설명 |
|------|------|
| [prompt-enhancer](./skills/prompt-enhancer) | 간단한 요청을 아키텍처 인식 상세 요구사항으로 변환 |
| [developer](./skills/developer) | 설계 패턴과 에러 처리가 적용된 프로덕션급 코드 생성 |
| [tester](./skills/tester) | 경계값 분석, 모킹 패턴을 적용한 종합 테스트 스위트 생성 |
| [code-reviewer](./skills/code-reviewer) | 버그, 취약점, 복잡도 탐지 및 클린 코드 기반 개선 제안 |
| [refactorer](./skills/refactorer) | 복잡도 감소, 중복 제거, 디자인 패턴 적용 등 체계적 리팩토링 |
| [document-maintainer](./skills/document-maintainer) | 코드 변경에 따른 문서 자동 업데이트 및 Mermaid 다이어그램 생성 |

### Quality Gate (품질 관리)

| 스킬 | 설명 |
|------|------|
| [security-auditor](./skills/security-auditor) | OWASP 표준 기반 보안 취약점 탐지 및 해결 가이드 제공 |
| [performance-analyzer](./skills/performance-analyzer) | Big-O 복잡도 분석, 병목 탐지 및 최적화 권장사항 제공 |
| [debugger](./skills/debugger) | 스택 트레이스 분석, 5 Whys 방법론을 활용한 근본 원인 분석 |

### Design (설계 도구)

| 스킬 | 설명 |
|------|------|
| [api-designer](./skills/api-designer) | RESTful API 및 gRPC 서비스 설계, OpenAPI 명세 생성 |
| [architecture-advisor](./skills/architecture-advisor) | 아키텍처 가이드, 디자인 패턴 추천, C4 다이어그램, ADR 작성 |
| [cicd-designer](./skills/cicd-designer) | GitHub Actions, Jenkins, ArgoCD 파이프라인 설계 및 배포 전략 |

### Domain (도메인 전문)

| 스킬 | 설명 |
|------|------|
| [kafka-expert](./skills/kafka-expert) | Kafka 토픽/파티션 설계, Producer/Consumer 튜닝, K8s 배포 |
| [k8s-specialist](./skills/k8s-specialist) | Kubernetes 리소스 및 Helm 차트 설계, RBAC, HPA/VPA 설정 |
| [database-optimizer](./skills/database-optimizer) | Oracle/DuckDB 쿼리 최적화, 실행 계획 분석, 인덱스 설계 |
| [airflow-architect](./skills/airflow-architect) | Airflow DAG 설계 및 최적화, 태스크 의존성 관리, 병렬 실행 전략 |
| [etl-pipeline-builder](./skills/etl-pipeline-builder) | ETL/ELT 파이프라인 설계, CDC 패턴, 멱등성 처리 |

### Utility (유틸리티)

| 스킬 | 설명 |
|------|------|
| [skill-packager](./skills/skill-packager) | 스킬 패키징 및 마켓플레이스 배포 준비 |

## 설치 방법

### Claude Code에서 설치

1. 마켓플레이스 등록:
```bash
/plugin marketplace add nineking/skills
```

2. 플러그인 설치:
```bash
# 전체 워크플로우 스킬 설치
/plugin install workflow@nineking-agent-skills

# 품질 관리 스킬 설치
/plugin install quality-gate@nineking-agent-skills

# 설계 도구 스킬 설치
/plugin install design@nineking-agent-skills

# 도메인 전문 스킬 설치
/plugin install domain@nineking-agent-skills

# 유틸리티 스킬 설치
/plugin install utility@nineking-agent-skills
```

### 직접 사용

스킬을 직접 호출하려면 해당 스킬을 언급하면 됩니다:
- "developer 스킬을 사용해서 사용자 인증 API를 만들어줘"
- "code-reviewer 스킬로 이 코드를 리뷰해줘"
- "k8s-specialist 스킬을 사용해서 Deployment를 생성해줘"

## 디렉토리 구조

```
.
├── skills/                  # 스킬 구현
│   ├── airflow-architect/
│   ├── api-designer/
│   ├── architecture-advisor/
│   ├── cicd-designer/
│   ├── code-reviewer/
│   ├── database-optimizer/
│   ├── debugger/
│   ├── developer/
│   ├── document-maintainer/
│   ├── etl-pipeline-builder/
│   ├── k8s-specialist/
│   ├── kafka-expert/
│   ├── performance-analyzer/
│   ├── prompt-enhancer/
│   ├── refactorer/
│   ├── security-auditor/
│   ├── skill-packager/
│   └── tester/
├── spec/                    # Agent Skills 명세
├── template/                # 스킬 템플릿
└── .claude-plugin/          # 플러그인 설정
```

## 스킬 생성하기

새로운 스킬을 만들려면 `template/` 폴더의 템플릿을 참고하세요:

```markdown
---
name: my-skill-name
description: 스킬이 무엇을 하고 언제 사용해야 하는지 명확하게 설명
---

# 스킬 이름

[Claude가 이 스킬이 활성화될 때 따를 지시사항을 여기에 작성]

## 핵심 기능
- 기능 1
- 기능 2

## 사용 예시
- 예시 1
- 예시 2
```

## 참고 자료

- [스킬이란?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Claude에서 스킬 사용하기](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [커스텀 스킬 만들기](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [Agent Skills로 에이전트 강화하기](https://anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

## 라이선스

Apache 2.0
