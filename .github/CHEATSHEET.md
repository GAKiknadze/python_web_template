# CI/CD Cheatsheet

Быстрая справка по всем командам и workflows.

## 🚀 Quick Commands

### Локальная разработка
```bash
# Полная настройка окружения
make setup

# Установить зависимости
make dev

# Запустить приложение
make run

# Быстрая проверка перед commit
make check
```

### Тестирование
```bash
# Запустить тесты
make test

# Тесты с покрытием
make test-cov

# Тесты в watch mode
make test-watch
```

### Качество кода
```bash
# Lint
make lint

# Lint с автофиксом
make lint-fix

# Форматирование
make format

# Проверка форматирования
make format-check

# Pre-commit хуки
make pre-commit
```

### База данных
```bash
# Применить миграции
make db-upgrade

# Откатить миграцию
make db-downgrade

# Создать новую миграцию
make db-revision

# История миграций
make db-history

# Текущая версия
make db-current

# Полный сброс БД
make db-reset
```

### Docker
```bash
# Собрать образ
make docker-build

# Собрать dev образ
make docker-build-dev

# Запустить все сервисы
make docker-up

# Собрать и запустить
make docker-up-build

# Остановить сервисы
make docker-down

# Логи
make docker-logs

# Shell в контейнере
make docker-shell

# Очистить всё
make docker-clean
```

### CI/CD
```bash
# Локальный CI
make ci

# Полный CI с pre-commit
make ci-full

# Тесты производительности
make performance

# Бенчмарки
make benchmark

# Проверка безопасности
make security

# Аудит зависимостей
make security-audit
```

### Релизы
```bash
# Patch релиз (0.0.X)
make release-patch

# Minor релиз (0.X.0)
make release-minor

# Major релиз (X.0.0)
make release-major

# Показать версию
make version
```

### Очистка
```bash
# Очистить кеш
make clean

# Очистить всё (включая Docker)
make clean-all
```

---

## 📋 Git Workflow

### Feature разработка
```bash
# 1. Создать ветку
git checkout -b feat/my-feature

# 2. Внести изменения
git add .
git commit -m "feat: add new feature"

# 3. Запушить и создать PR
git push origin feat/my-feature

# 4. После merge - удалить ветку
git branch -d feat/my-feature
```

### Conventional Commits
```bash
feat:     # Новая функциональность
fix:      # Исправление бага
docs:     # Документация
style:    # Форматирование
refactor: # Рефакторинг
perf:     # Производительность
test:     # Тесты
build:    # Сборка
ci:       # CI/CD
chore:    # Рутина
revert:   # Откат
```

### Примеры коммитов
```bash
git commit -m "feat: add user authentication"
git commit -m "fix: resolve database connection timeout"
git commit -m "docs: update API documentation"
git commit -m "refactor: simplify user service logic"
git commit -m "perf: optimize database queries"
git commit -m "test: add integration tests for auth"
```

---

## 🏷️ Release Process

### Автоматический (рекомендуется)
```bash
# Patch: 1.0.0 → 1.0.1
make release-patch

# Minor: 1.0.0 → 1.1.0
make release-minor

# Major: 1.0.0 → 2.0.0
make release-major
```

### Ручной
```bash
# 1. Обновить версию
vim pyproject.toml  # version = "1.0.0"

# 2. Commit
git add pyproject.toml
git commit -m "chore: bump version to 1.0.0"

# 3. Тег
git tag -a v1.0.0 -m "Release 1.0.0"

# 4. Push
git push origin main
git push origin v1.0.0
```

### Prerelease
```bash
git tag -a v1.0.0-alpha.1 -m "Alpha release"
git tag -a v1.0.0-beta.1 -m "Beta release"
git tag -a v1.0.0-rc.1 -m "Release candidate"
```

---

## 🐳 Docker Commands

### Образы
```bash
# Pull из registry
docker pull ghcr.io/username/python-web-template:latest

# Run контейнер
docker run -d -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  ghcr.io/username/python-web-template:latest

# Build локально
docker build -t my-app .

# Build dev версию
docker build --target development -t my-app:dev .

# Логи
docker logs -f <container-id>

# Shell
docker exec -it <container-id> /bin/sh
```

### Docker Compose
```bash
# Запуск
docker-compose up -d

# С пересборкой
docker-compose up -d --build

# Только определенные сервисы
docker-compose up -d app db

# С профилями (tools)
docker-compose --profile tools up -d

# Логи
docker-compose logs -f
docker-compose logs -f app

# Остановка
docker-compose down

# С удалением volumes
docker-compose down -v

# Рестарт сервиса
docker-compose restart app

# Запуск команды
docker-compose exec app /bin/sh
docker-compose exec db psql -U postgres
```

---

## 🔍 Workflows Triggers

### ci.yml
- ✅ Push → main
- ✅ PR → main

### pr.yml
- ✅ PR opened/updated → main/develop

### cd.yml
- ✅ Push → main (staging)
- ✅ Tag v*.*.* (production)
- ✅ Manual dispatch

### release.yml
- ✅ Tag v*.*.*
- ✅ Manual dispatch

### docker.yml
- ✅ Push → main/develop
- ✅ PR → main
- ✅ Tag v*.*.*
- ✅ Manual dispatch

### dependency-review.yml
- ✅ PR → main/develop
- ✅ Schedule: Mon 09:00 UTC
- ✅ Manual dispatch

### codeql.yml
- ✅ Push → main/develop
- ✅ PR → main/develop
- ✅ Schedule: Daily 06:00 UTC
- ✅ Manual dispatch

### performance.yml
- ✅ PR → main/develop
- ✅ Push → main
- ✅ Schedule: Sun 03:00 UTC
- ✅ Manual dispatch

---

## 🔐 Секреты (Settings → Secrets)

### Обязательные
```
GITHUB_TOKEN  # Автоматически доступен
```

### Опциональные (для деплоя)
```
DEPLOY_SSH_KEY         # SSH ключ для деплоя
DEPLOY_HOST            # Хост для деплоя
DEPLOY_USER            # Пользователь для деплоя
KUBE_CONFIG            # Kubernetes config (base64)
PYPI_API_TOKEN         # PyPI token для публикации
SLACK_WEBHOOK_URL      # Slack уведомления
DISCORD_WEBHOOK_URL    # Discord уведомления
```

---

## 🌍 Environments

### staging
- Auto-deploy: ✅ (main branch)
- Approval: ❌
- URL: https://staging.example.com

### production
- Auto-deploy: ❌
- Approval: ✅ (required)
- Branches: tags v*.*.*
- URL: https://example.com

### pypi (optional)
- Approval: ✅ (recommended)
- Только stable releases

---

## 📊 Где смотреть результаты

```
Actions tab        → Все запуски workflows
Security tab       → CodeQL, Dependabot, Trivy
Packages tab       → Docker образы
Releases tab       → История релизов
Environments       → История деплоев
Pull Requests      → Статус проверок
Insights           → Dependency graph
```

---

## 🚨 Troubleshooting

### Workflow не запускается
```bash
# Проверить синтаксис
cat .github/workflows/ci.yml | yq .

# Проверить permissions
# Settings → Actions → General → Workflow permissions
```

### Тесты падают в CI
```bash
# Проверить локально
make ci

# Сравнить окружение
python --version
uv --version

# Проверить зависимости
cat uv.lock
```

### Docker build fails
```bash
# Lint Dockerfile
docker run --rm -i hadolint/hadolint < Dockerfile

# Build локально
docker build -t test .

# Проверить .dockerignore
cat .dockerignore
```

### Deploy fails
```bash
# Проверить секреты
# Settings → Secrets → Actions

# Проверить логи
# Actions → Workflow run → Job → Step

# Тест подключения (если SSH)
ssh $DEPLOY_USER@$DEPLOY_HOST
```

---

## 🔗 Quick Links

- [CI/CD Documentation](./.github/CICD.md)
- [Quick Start Guide](./.github/QUICKSTART_CICD.md)
- [Workflows Diagram](./.github/WORKFLOWS_DIAGRAM.md)
- [Main README](../README.md)

---

## 💡 Pro Tips

1. **Используйте `make` для всех команд** - это быстрее и удобнее
2. **Запускайте `make check` перед commit** - сэкономит время в CI
3. **Используйте `make release-*` для релизов** - автоматизация исключает ошибки
4. **Настройте pre-commit хуки** - `make pre-commit-install`
5. **Мониторьте Security tab** - проверяйте уязвимости регулярно
6. **Используйте Conventional Commits** - для автоматического changelog
7. **Тестируйте Docker образы локально** - перед push в registry
8. **Настройте уведомления** - для критичных workflows
9. **Используйте environments** - для защиты production
10. **Документируйте изменения** - в commit messages и PR

---

**Version:** 1.0.0  
**Last Updated:** 2024