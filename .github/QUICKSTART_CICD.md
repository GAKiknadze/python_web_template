# CI/CD Quick Start Guide

Быстрый старт для настройки CI/CD пайплайнов в вашем проекте.

## 🚀 Минимальная настройка (5 минут)

### 1. Включите GitHub Actions

GitHub Actions должны быть включены по умолчанию, но проверьте:

1. Перейдите в **Settings** → **Actions** → **General**
2. Убедитесь, что выбрано **"Allow all actions and reusable workflows"**
3. В разделе **Workflow permissions** выберите:
   - ✅ **"Read and write permissions"**
   - ✅ **"Allow GitHub Actions to create and approve pull requests"**

### 2. Проверьте работу базовых workflows

После первого push в `main` ветку автоматически запустятся:
- ✅ **CI** - линтинг и тесты
- ✅ **Docker** - сборка образов

Проверьте статус в разделе **Actions** вашего репозитория.

### 3. Создайте тестовый Pull Request

```bash
git checkout -b feat/test-cicd
echo "# Test" >> TEST.md
git add TEST.md
git commit -m "feat: test CI/CD workflows"
git push origin feat/test-cicd
```

Создайте PR в GitHub и убедитесь, что все проверки проходят:
- ✅ Validate PR title
- ✅ Code quality checks
- ✅ Test suite
- ✅ Security scan

## 🔧 Расширенная настройка (15 минут)

### 1. Настройте Environments для деплоя

#### Staging Environment

1. **Settings** → **Environments** → **New environment**
2. Имя: `staging`
3. **Deployment protection rules**:
   - Reviewers: не требуются
   - Wait timer: 0 минут
4. **Environment variables**:
   ```
   DEPLOY_URL = https://staging.yourdomain.com
   ENVIRONMENT_NAME = staging
   ```

#### Production Environment

1. **Settings** → **Environments** → **New environment**
2. Имя: `production`
3. **Deployment protection rules**:
   - ✅ Required reviewers: 1-2 человека
   - ✅ Wait timer: 5 минут (опционально)
   - ✅ Deployment branches: только теги `v*.*.*`
4. **Environment variables**:
   ```
   DEPLOY_URL = https://yourdomain.com
   ENVIRONMENT_NAME = production
   ```

### 2. Добавьте секреты для деплоя

**Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Минимальные секреты:

```
# Для деплоя через SSH
DEPLOY_SSH_KEY = <ваш приватный SSH ключ>
DEPLOY_HOST = your-server.com
DEPLOY_USER = deploy

# Для Kubernetes (если используете)
KUBE_CONFIG = <base64 encoded kubeconfig>

# Для уведомлений (опционально)
SLACK_WEBHOOK_URL = https://hooks.slack.com/...
```

### 3. Настройте Container Registry

GitHub Container Registry (ghcr.io) работает автоматически с `GITHUB_TOKEN`.

Для доступа извне:

```bash
# 1. Создайте Personal Access Token
# Settings → Developer settings → Personal access tokens → Generate new token
# Scopes: write:packages, delete:packages

# 2. Логин
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# 3. Pull образы
docker pull ghcr.io/username/python-web-template:latest
```

### 4. Настройте PyPI (опционально)

Для автоматической публикации в PyPI при релизе:

1. Создайте API token на https://pypi.org/manage/account/token/
2. Добавьте секрет `PYPI_API_TOKEN`
3. Создайте environment `pypi` с required reviewers (опционально)

## 📋 Workflow Reference

### Основные workflows

| Workflow | Триггер | Описание |
|----------|---------|----------|
| **ci.yml** | Push/PR → main | Lint + Tests |
| **pr.yml** | PR открыт/обновлен | Полные проверки PR |
| **cd.yml** | Push main / Tag | Деплой staging/production |
| **docker.yml** | Push/PR/Tag | Build & Push образов |
| **release.yml** | Tag `v*.*.*` | Создание релиза |
| **dependency-review.yml** | PR / Еженедельно | Проверка зависимостей |
| **codeql.yml** | Push/PR / Ежедневно | Анализ безопасности |
| **performance.yml** | PR / Еженедельно | Тесты производительности |

### Когда запускаются workflows

```
┌─────────────┐
│ Push to     │
│ feature/*   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Create PR   │──────┐
└─────────────┘      │
                     ▼
              ┌──────────────┐
              │ pr.yml       │ ← Валидация + Тесты + Security
              └──────────────┘
                     │
                     ▼
              ┌──────────────┐
              │ Merge to     │
              │ main         │
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │ ci.yml       │ ← Lint + Tests
              │ docker.yml   │ ← Build образов
              │ cd.yml       │ ← Deploy to staging
              └──────────────┘
                     │
                     ▼
              ┌──────────────┐
              │ Create Tag   │
              │ v1.0.0       │
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │ release.yml  │ ← Создание релиза
              │ cd.yml       │ ← Deploy to production
              └──────────────┘
```

## 🎯 Первый релиз

### Вариант 1: Автоматический (рекомендуется)

```bash
# Используйте Makefile
make release-patch    # 0.1.0 → 0.1.1
make release-minor    # 0.1.0 → 0.2.0
make release-major    # 0.1.0 → 1.0.0

# Или напрямую через скрипт
./scripts/release.sh patch "Описание релиза"
```

Скрипт автоматически:
- ✅ Проверит git статус
- ✅ Обновит версию в `pyproject.toml`
- ✅ Запустит тесты
- ✅ Создаст коммит и тег
- ✅ Отправит изменения на GitHub

### Вариант 2: Ручной

```bash
# 1. Обновите версию в pyproject.toml
version = "1.0.0"

# 2. Закоммитьте изменения
git add pyproject.toml
git commit -m "chore: bump version to 1.0.0"

# 3. Создайте тег
git tag -a v1.0.0 -m "Release version 1.0.0"

# 4. Отправьте на GitHub
git push origin main
git push origin v1.0.0
```

### После создания релиза

1. GitHub Actions автоматически:
   - Запустит тесты
   - Соберет пакеты
   - Сгенерирует changelog
   - Создаст GitHub Release
   - Опубликует в PyPI (если настроено)

2. Deployment workflow:
   - Деплой на production (требует approval)
   - Smoke tests
   - Уведомления

## 🐳 Docker Quick Start

### Локальная разработка

```bash
# Build образ
make docker-build-dev

# Запустить все сервисы
make docker-up

# Просмотр логов
make docker-logs

# Остановить
make docker-down
```

### Использование опубликованных образов

```bash
# Pull latest
docker pull ghcr.io/username/python-web-template:latest

# Run
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  ghcr.io/username/python-web-template:latest
```

## 🔍 Мониторинг CI/CD

### Где смотреть статус

1. **Actions tab** - все запуски workflows
2. **Pull Request checks** - статус проверок PR
3. **Environments** - история деплоев
4. **Security tab** - результаты CodeQL и Dependabot
5. **Packages** - опубликованные Docker образы

### Полезные бейджи для README

```markdown
[![CI](https://github.com/username/repo/actions/workflows/ci.yml/badge.svg)](https://github.com/username/repo/actions/workflows/ci.yml)
[![CD](https://github.com/username/repo/actions/workflows/cd.yml/badge.svg)](https://github.com/username/repo/actions/workflows/cd.yml)
[![Docker](https://github.com/username/repo/actions/workflows/docker.yml/badge.svg)](https://github.com/username/repo/actions/workflows/docker.yml)
[![CodeQL](https://github.com/username/repo/actions/workflows/codeql.yml/badge.svg)](https://github.com/username/repo/actions/workflows/codeql.yml)
```

## 🛠️ Кастомизация workflows

### Изменение расписания

```yaml
# В .github/workflows/dependency-review.yml
on:
  schedule:
    - cron: '0 9 * * 1'  # Каждый понедельник в 09:00 UTC
```

### Добавление уведомлений

```yaml
- name: Notify Slack
  if: always()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### Настройка деплоя

Замените placeholder команды в `.github/workflows/cd.yml`:

```yaml
# Для Docker Compose
- name: Deploy
  run: |
    ssh ${{ secrets.DEPLOY_USER }}@${{ secrets.DEPLOY_HOST }} "
      cd /app
      docker-compose pull
      docker-compose up -d
    "

# Для Kubernetes
- name: Deploy
  run: |
    kubectl set image deployment/app \
      app=${{ needs.build.outputs.image-tag }}
    kubectl rollout status deployment/app
```

## 📚 Дополнительные команды

### Локальная проверка CI

```bash
# Запустить все CI проверки локально
make ci

# Только тесты с покрытием
make test-cov

# Только lint
make lint

# Форматирование
make format

# Pre-commit хуки
make pre-commit
```

### Проверка workflow файлов

```bash
# Установите act для локального запуска workflows
# https://github.com/nektos/act

# Запустить CI локально
act -j lint
act -j test

# Запустить с конкретным событием
act push
act pull_request
```

## ❓ Troubleshooting

### Workflow не запускается

1. Проверьте Actions permissions в Settings
2. Убедитесь что workflow файл правильно отформатирован
3. Проверьте что branch/tag соответствует условиям триггера

### Тесты падают в CI

1. Проверьте environment variables
2. Сравните Python версии (локальная vs CI)
3. Убедитесь что `uv.lock` закоммичен

### Deployment fails

1. Проверьте секреты (DEPLOY_SSH_KEY, etc.)
2. Проверьте доступность целевого сервера
3. Проверьте логи в Actions tab

### Docker build fails

1. Запустите hadolint локально:
   ```bash
   docker run --rm -i hadolint/hadolint < Dockerfile
   ```
2. Проверьте .dockerignore
3. Очистите build cache

## 🎓 Best Practices

1. **Всегда используйте Conventional Commits** для автоматической генерации changelog
2. **Настройте required reviewers** для production environment
3. **Регулярно проверяйте Security alerts** в Security tab
4. **Мониторьте производительность** workflows (время выполнения)
5. **Используйте caching** для ускорения CI (включено по умолчанию)
6. **Тестируйте локально** перед push (используйте `make ci`)
7. **Документируйте изменения** в commits и PR descriptions

## 📖 Дополнительная документация

- [Полная CI/CD документация](./.github/CICD.md)
- [GitHub Actions документация](https://docs.github.com/en/actions)
- [Docker лучшие практики](https://docs.docker.com/develop/dev-best-practices/)
- [Conventional Commits](https://www.conventionalcommits.org/)

## 🆘 Получить помощь

- Создайте Issue с лейблом `ci/cd`
- Проверьте существующие Issues
- Обратитесь к команде DevOps

---

**Готово!** Ваш CI/CD пайплайн настроен и готов к использованию. 🎉