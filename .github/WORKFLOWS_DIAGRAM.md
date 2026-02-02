# CI/CD Workflows Diagram

Визуальное представление всех CI/CD пайплайнов и их взаимодействия.

## 🔄 Общий обзор процесса

```mermaid
graph TB
    subgraph "Development"
        A[Local Development] -->|git push| B[Feature Branch]
        B -->|Create PR| C[Pull Request]
    end
    
    subgraph "PR Validation"
        C --> D[pr.yml]
        D --> E{All Checks Pass?}
        E -->|No| F[Fix Issues]
        F --> C
        E -->|Yes| G[Approve & Merge]
    end
    
    subgraph "Main Branch"
        G -->|Merge to main| H[main branch]
        H --> I[ci.yml]
        H --> J[docker.yml]
        H --> K[cd.yml - Staging]
    end
    
    subgraph "Release"
        H -->|Create Tag v*| L[release.yml]
        L --> M[Create GitHub Release]
        M --> N[cd.yml - Production]
    end
    
    subgraph "Scheduled Tasks"
        O[dependency-review.yml]
        P[codeql.yml]
        Q[performance.yml]
    end
    
    style C fill:#e1f5ff
    style G fill:#c8e6c9
    style M fill:#fff9c4
    style N fill:#ffccbc
```

## 📋 Детальная диаграмма workflows

```mermaid
flowchart TD
    Start([Developer Action]) --> CheckAction{What Action?}
    
    CheckAction -->|Push to feature| Feature[Feature Branch Push]
    CheckAction -->|Create PR| PR[Pull Request]
    CheckAction -->|Push to main| Main[Main Branch Push]
    CheckAction -->|Create Tag| Tag[Tag v*.*.*]
    
    Feature -->|No workflows| FeatureEnd([End])
    
    PR --> PRWorkflow[pr.yml Starts]
    PRWorkflow --> Validate[Validate PR Title]
    Validate --> CodeQuality[Code Quality Checks]
    CodeQuality --> Tests[Test Suite]
    Tests --> Security[Security Scan]
    Security --> PRSummary{All Pass?}
    PRSummary -->|Yes| PRSuccess([✅ PR Ready])
    PRSummary -->|No| PRFail([❌ Fix Required])
    
    Main --> CIWorkflow[ci.yml]
    Main --> DockerWorkflow[docker.yml]
    Main --> CDWorkflow[cd.yml]
    
    CIWorkflow --> CILint[Lint & Format]
    CILint --> CITest[Tests & Coverage]
    CITest --> CIArtifact[Upload Coverage]
    
    DockerWorkflow --> DockLint[Dockerfile Lint]
    DockLint --> DockBuild[Build Image]
    DockBuild --> DockTest[Test Container]
    DockTest --> DockScan[Trivy Scan]
    DockScan --> DockPush[Push to GHCR]
    
    CDWorkflow --> CDBuild[Build Docker Image]
    CDBuild --> CDStaging[Deploy to Staging]
    CDStaging --> CDSmoke[Smoke Tests]
    
    Tag --> ReleaseWorkflow[release.yml]
    ReleaseWorkflow --> RelValidate[Validate Version]
    RelValidate --> RelTest[Full Test Suite]
    RelTest --> RelBuild[Build Artifacts]
    RelBuild --> RelChangelog[Generate Changelog]
    RelChangelog --> RelCreate[Create GitHub Release]
    RelCreate --> RelPyPI{Stable Release?}
    RelPyPI -->|Yes| PyPI[Publish to PyPI]
    RelPyPI -->|No| RelEnd([End])
    PyPI --> RelEnd
    
    RelCreate --> CDProd[cd.yml - Production]
    CDProd --> CDApproval{Manual Approval}
    CDApproval -->|Approved| CDDeploy[Deploy to Production]
    CDApproval -->|Rejected| CDCancel([Cancelled])
    CDDeploy --> CDSmokeP[Smoke Tests]
    CDSmokeP --> CDSuccess([✅ Deployed])
    
    style PRSuccess fill:#4caf50,color:#fff
    style PRFail fill:#f44336,color:#fff
    style CDSuccess fill:#4caf50,color:#fff
    style CDCancel fill:#ff9800,color:#fff
```

## 🕐 Scheduled Workflows

```mermaid
gantt
    title Scheduled CI/CD Jobs
    dateFormat HH:mm
    axisFormat %H:%M
    
    section Security
    CodeQL Daily Scan           :codeql, 06:00, 1h
    
    section Dependencies
    Dependency Review Weekly    :dep, 09:00, 1h
    
    section Performance
    Performance Tests Weekly    :perf, 03:00, 2h
```

## 🔀 Workflow Triggers Matrix

| Workflow | Push main | Push tag | PR | Schedule | Manual |
|----------|-----------|----------|-----|----------|--------|
| **ci.yml** | ✅ | ❌ | ✅ | ❌ | ❌ |
| **pr.yml** | ❌ | ❌ | ✅ | ❌ | ❌ |
| **cd.yml** | ✅ | ✅ | ❌ | ❌ | ✅ |
| **release.yml** | ❌ | ✅ | ❌ | ❌ | ✅ |
| **docker.yml** | ✅ | ✅ | ✅ | ❌ | ✅ |
| **dependency-review.yml** | ❌ | ❌ | ✅ | ✅ Mon 09:00 | ✅ |
| **codeql.yml** | ✅ | ❌ | ✅ | ✅ Daily 06:00 | ✅ |
| **performance.yml** | ✅ | ❌ | ✅ | ✅ Sun 03:00 | ✅ |

## 🎯 Jobs Execution Flow

### PR Workflow (pr.yml)
```mermaid
graph LR
    A[validate] --> B[lint-and-format]
    A --> C[test]
    A --> D[security]
    B --> E[summary]
    C --> E
    D --> E
```

### CD Workflow (cd.yml)
```mermaid
graph LR
    A[build] --> B[deploy-staging]
    B --> C{Is Tag?}
    C -->|Yes| D[deploy-production]
    C -->|No| E([End])
    B --> F{Failure?}
    C --> F
    F -->|Yes| G[rollback]
    F -->|No| E
```

### Release Workflow (release.yml)
```mermaid
graph LR
    A[validate] --> B[test]
    A --> C[build-artifacts]
    A --> D[generate-changelog]
    B --> E[create-release]
    C --> E
    D --> E
    E --> F{Stable?}
    F -->|Yes| G[publish-pypi]
    F -->|No| H([End])
    G --> H
    E --> I[notify]
```

### Docker Workflow (docker.yml)
```mermaid
graph LR
    A[docker-lint] --> B[build-and-test]
    B --> C{Is PR?}
    C -->|No| D[push]
    C -->|Yes| E([End])
    D --> E
    B --> F[summary]
    D --> F
```

### Performance Workflow (performance.yml)
```mermaid
graph LR
    A[load-test] --> E[summary]
    B[benchmark] --> E
    C[memory-profiling] --> E
    D[api-performance] --> E
```

## 🔐 Security Scanning Pipeline

```mermaid
graph TB
    subgraph "Code Security"
        A[CodeQL Analysis]
        B[Ruff Security Rules]
    end
    
    subgraph "Dependencies"
        C[Dependency Review]
        D[Safety Scan]
        E[License Check]
    end
    
    subgraph "Container Security"
        F[Trivy Scan]
        G[Dockerfile Lint]
    end
    
    A --> H[GitHub Security Tab]
    B --> H
    C --> H
    D --> I[Artifacts]
    E --> I
    F --> H
    G --> J[Workflow Logs]
    
    style H fill:#ffeb3b
    style I fill:#ff9800
```

## 📦 Artifact Flow

```mermaid
graph TB
    subgraph "CI Artifacts"
        A[Coverage Reports] --> G[GitHub Artifacts]
        B[Test Results] --> G
    end
    
    subgraph "Release Artifacts"
        C[Python Wheel] --> H[GitHub Release]
        D[Source Distribution] --> H
        E[Changelog] --> H
    end
    
    subgraph "Docker Artifacts"
        F[Container Images] --> I[GitHub Container Registry]
    end
    
    subgraph "Performance Artifacts"
        J[Load Test Reports] --> G
        K[Benchmark Results] --> G
        L[Memory Profiles] --> G
    end
    
    style G fill:#2196f3,color:#fff
    style H fill:#4caf50,color:#fff
    style I fill:#00bcd4,color:#fff
```

## 🚀 Deployment Pipeline

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant GH as GitHub
    participant CI as CI/CD
    participant Reg as Container Registry
    participant Stg as Staging
    participant Prd as Production
    
    Dev->>GH: Push to main
    GH->>CI: Trigger workflows
    CI->>CI: Run tests
    CI->>CI: Build Docker image
    CI->>Reg: Push image
    CI->>Stg: Deploy to staging
    Stg-->>CI: Health check
    
    Note over Dev,GH: Create release tag
    Dev->>GH: Push tag v1.0.0
    GH->>CI: Trigger release
    CI->>CI: Full test suite
    CI->>CI: Build artifacts
    CI->>GH: Create GitHub Release
    
    Note over CI,Prd: Manual approval required
    CI->>Prd: Deploy to production
    Prd-->>CI: Health check
    CI->>Dev: Notify success
```

## 🔄 Rollback Strategy

```mermaid
graph TB
    A[Deployment Fails] --> B{Auto Rollback?}
    B -->|Yes| C[rollback job]
    B -->|No| D[Manual Intervention]
    C --> E[Revert to Previous Version]
    D --> E
    E --> F[Health Check]
    F --> G{Healthy?}
    G -->|Yes| H[Notify Success]
    G -->|No| I[Escalate]
```

## 📊 Metrics & Monitoring

```mermaid
graph LR
    subgraph "Workflow Metrics"
        A[Execution Time]
        B[Success Rate]
        C[Failure Rate]
    end
    
    subgraph "Code Metrics"
        D[Test Coverage]
        E[Code Quality]
        F[Security Issues]
    end
    
    subgraph "Deployment Metrics"
        G[Deploy Frequency]
        H[Lead Time]
        I[MTTR]
    end
    
    A --> J[GitHub Actions Insights]
    B --> J
    C --> J
    D --> K[Coverage Reports]
    E --> L[Ruff Reports]
    F --> M[Security Tab]
    G --> J
    H --> J
    I --> J
```

## 🎭 Environment Flow

```mermaid
stateDiagram-v2
    [*] --> Development
    Development --> FeatureBranch: git checkout -b feat/...
    FeatureBranch --> PullRequest: git push & create PR
    PullRequest --> CodeReview: pr.yml passes
    CodeReview --> Main: merge
    Main --> Staging: cd.yml auto-deploy
    Staging --> Testing: smoke tests
    Testing --> TagCreated: create tag v*
    TagCreated --> Production: cd.yml + approval
    Production --> [*]: deployed
    
    Testing --> FixRequired: tests fail
    FixRequired --> Development
    
    Production --> Rollback: deployment fails
    Rollback --> Staging
```

## 📝 Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Enabled/Active |
| ❌ | Disabled/Inactive |
| 🔄 | Automated process |
| 👤 | Manual approval required |
| 🔐 | Security-related |
| 📦 | Artifact generation |
| 🚀 | Deployment step |
| ⚡ | Performance-related |

---

**Last Updated:** 2024  
**Version:** 1.0.0