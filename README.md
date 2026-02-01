# python_web_template

[![CI](https://github.com/GAKiknadze/python_web_template/actions/workflows/ci.yml/badge.svg)](https://github.com/GAKiknadze/python_web_template/actions/workflows/ci.yml)
[![PR Checks](https://github.com/GAKiknadze/python_web_template/actions/workflows/pr.yml/badge.svg)](https://github.com/GAKiknadze/python_web_template/actions/workflows/pr.yml)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3130/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Шаблон для создания веб-приложений на Python с архитектурой, основанной на принципах Clean Architecture и Domain-Driven Design (DDD).

## 📋 Описание

Этот проект предоставляет структурированный шаблон для разработки масштабируемых Python приложений с четким разделением ответственности:

- **Domain Layer** (`src/domain/`) - Бизнес-логика и сущности домена
- **Application Layer** (`src/application/`) - Сценарии использования (use cases) и интерфейсы
- **Infrastructure Layer** (`src/infrastructure/`) - Реализация взаимодействия с внешними системами (БД, конфигурация)
- **Interfaces Layer** (`src/interfaces/`) - API endpoints и точки входа приложения
- **DI Layer** (`src/di/`) - Управление зависимостями через Dishka

## ✨ Особенности

### Архитектура
- ✅ Clean Architecture структура с четким разделением слоев
- ✅ Domain-Driven Design принципы
- ✅ Unit of Work паттерн для управления транзакциями
- ✅ Repository паттерн для работы с данными
- ✅ Outbox Pattern для событийно-ориентированной архитектуры

### Технологический стек
- 🚀 **FastAPI** - современный, быстрый веб-фреймворк
- 🔌 **Dishka** - мощная система Dependency Injection
- 🗄️ **SQLAlchemy 2.0** - асинхронный ORM для работы с БД
- 🔄 **Alembic** - миграции базы данных
- ⚙️ **Pydantic Settings** - управление конфигурацией через переменные окружения
- 📝 **Loguru** - удобное и гибкое логирование
- 🔍 **Ruff** - быстрый линтер и форматтер
- ✅ **Pytest** - тестирование с поддержкой async

### Инструменты разработки
- 🔧 Pre-commit хуки для автоматической проверки кода
- 🤖 GitHub Actions CI/CD с автоматическими проверками
- 📦 UV для быстрого управления зависимостями
- 🔐 Встроенные проверки безопасности (Bandit rules)

## 📦 Требования

- **Python** 3.13+
- **uv** (для управления зависимостями)

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
# Установить все зависимости (включая dev)
uv sync --group dev

# Установить только production зависимости
uv sync

# Установить с тестовыми зависимостями
uv sync --group test
```

### 2. Настройка окружения

Создайте файл `.env` на основе `.env.example` и настройте переменные окружения:

```bash
cp .env.example .env
```

Основные настройки:

```env
# Application
APP_NAME="Python Web Template"
APP_VERSION="0.1.0"
APP_ENVIRONMENT="development"
APP_DEBUG=true
APP_HOST="0.0.0.0"
APP_PORT=8000

# Database
DB_HOST="localhost"
DB_PORT=5432
DB_USER="postgres"
DB_PASSWORD="postgres"
DB_NAME="app_db"

# Logging
LOG_LEVEL="INFO"
LOG_SERIALIZE=false

# API
API_PREFIX="/api/v1"
API_DOCS_URL="/docs"
API_REDOC_URL="/redoc"

# CORS
CORS_ENABLED=true
CORS_ALLOW_ORIGINS="*"
```

### 3. Миграции базы данных

```bash
# Создать новую миграцию
uv run alembic revision --autogenerate -m "Initial migration"

# Применить миграции
uv run alembic upgrade head

# Откатить последнюю миграцию
uv run alembic downgrade -1
```

### 4. Запуск приложения

```bash
# Запуск в режиме разработки
uv run python main.py

# Или через uvicorn напрямую с hot-reload
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Приложение будет доступно по адресу:
- API: http://localhost:8000/api/v1
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🏗️ Структура проекта

```
python_web_template/
├── src/
│   ├── application/         # Application Layer - Use Cases
│   │   └── common/          # Общие интерфейсы (IUnitOfWork, etc.)
│   ├── domain/              # Domain Layer - Бизнес-логика
│   │   └── common/          # Общие базовые классы
│   ├── infrastructure/      # Infrastructure Layer
│   │   ├── config/          # Конфигурация приложения (Pydantic Settings)
│   │   ├── database/        # БД: модели, репозитории, типы
│   │   │   ├── models/      # SQLAlchemy модели
│   │   │   └── repositories/# Реализации репозиториев
│   │   └── unit_of_work.py  # Реализация Unit of Work
│   ├── interfaces/          # Interfaces Layer - API
│   │   └── api/             # REST API
│   │       ├── v1/          # API версии 1
│   │       ├── depends.py   # FastAPI dependencies
│   │       └── exception_handlers.py
│   └── di/                  # Dependency Injection
│       └── database.py      # Dishka providers для БД
├── alembic/                 # Миграции базы данных
│   ├── versions/            # Файлы миграций
│   └── env.py               # Настройка Alembic
├── tests/                   # Тесты
│   ├── unit/                # Unit тесты
│   └── test_config.py       # Тесты конфигурации
├── .github/                 # GitHub Actions и шаблоны
│   ├── workflows/           # CI/CD workflows
│   ├── ISSUE_TEMPLATE/      # Шаблоны Issues
│   ├── SETUP.md             # Инструкция по настройке CI/CD
│   └── COMMANDS.md          # Полезные команды
├── main.py                  # Точка входа приложения
├── pyproject.toml           # Зависимости проекта (UV)
├── ruff.toml                # Настройки Ruff
├── alembic.ini              # Настройки Alembic
└── .pre-commit-config.yaml  # Pre-commit хуки
```

## 🛠️ Инструменты разработки

### Pre-commit хуки

Проект использует pre-commit для автоматической проверки кода перед коммитом:

```bash
# Установить хуки
uv run pre-commit install

# Запустить проверку вручную на всех файлах
uv run pre-commit run --all-files

# Обновить хуки до последних версий
uv run pre-commit autoupdate
```

Настроенные хуки:
- **Ruff** - линтинг и форматирование
- Проверка конца файлов
- Проверка YAML/TOML синтаксиса
- Удаление trailing whitespace

### Ruff - Линтер и Форматтер

Настройки находятся в `ruff.toml`. Включенные проверки:

- ✅ **UP** - pyupgrade (модернизация синтаксиса Python)
- ✅ **I** - isort (сортировка импортов)
- ✅ **E/W** - flake8 errors/warnings
- ✅ **F** - pyflakes
- ✅ **B** - flake8-bugbear (обнаружение багов)
- ✅ **S** - flake8-bandit (проверки безопасности)
- ✅ **PT** - pytest-style
- ✅ **FURB** - refurb (современные идиомы Python)
- ✅ **RUF** - Ruff-специфичные правила

```bash
# Проверить код
uv run ruff check .

# Автоматически исправить проблемы
uv run ruff check . --fix

# Форматировать код
uv run ruff format .

# Проверить форматирование без изменений
uv run ruff format . --check
```

### Тестирование

```bash
# Запустить все тесты
uv run pytest tests/ -v

# Запустить тесты с покрытием
uv run pytest tests/ --cov=src --cov-report=term-missing --cov-report=html

# Запустить конкретный тест
uv run pytest tests/test_config.py::test_database_settings_defaults -v

# Запустить тесты с подробным выводом
uv run pytest tests/ -vv -s
```

HTML отчет о покрытии будет доступен в `htmlcov/index.html`.

## 🤖 CI/CD

### GitHub Actions Workflows

#### 1. CI Workflow (`.github/workflows/ci.yml`)

Запускается при push и pull request в `main`:

- **Lint** - проверка качества кода
  - `ruff check` - статический анализ
  - `ruff format --check` - проверка форматирования
- **Test** - запуск тестов
  - Выполнение pytest
  - Генерация отчета о покрытии кода
  - Сохранение артефактов

#### 2. PR Workflow (`.github/workflows/pr.yml`)

Запускается при создании PR в `main` или `develop`:

- **Validate** - валидация заголовка PR (Conventional Commits)
- **Code Quality** - Ruff проверки + pre-commit
- **Test Suite** - запуск тестов с проверкой покрытия
- **Security** - проверка безопасности (Bandit rules)
- **Summary** - итоговый статус всех проверок

#### 3. Dependabot (`.github/dependabot.yml`)

Автоматическое обновление зависимостей:
- Python пакеты (еженедельно, понедельник)
- GitHub Actions (еженедельно, понедельник)
- Группировка minor/patch обновлений

### Форматы коммитов

При создании PR заголовок должен следовать [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - новая функциональность
- `fix:` - исправление бага
- `docs:` - изменения в документации
- `style:` - форматирование кода (без изменения логики)
- `refactor:` - рефакторинг кода
- `perf:` - улучшение производительности
- `test:` - добавление/изменение тестов
- `build:` - изменения в сборке/зависимостях
- `ci:` - изменения в CI/CD
- `chore:` - рутинные задачи
- `revert:` - откат изменений

Примеры:
```
feat: add user authentication endpoint
fix: resolve database connection timeout
docs: update README with deployment instructions
```

## 📖 Конфигурация

Приложение использует **Pydantic Settings** для управления конфигурацией. Все настройки можно задать через переменные окружения или файл `.env`.

### Группы настроек

#### AppSettings (`APP_*`)
- `APP_NAME` - название приложения
- `APP_VERSION` - версия
- `APP_ENVIRONMENT` - окружение (development/staging/production)
- `APP_DEBUG` - режим отладки
- `APP_HOST` / `APP_PORT` - хост и порт
- `APP_RELOAD` - hot-reload
- `APP_WORKERS` - количество worker процессов

#### DatabaseSettings (`DB_*`)
- `DB_HOST` / `DB_PORT` - хост и порт БД
- `DB_USER` / `DB_PASSWORD` - учетные данные
- `DB_NAME` - имя базы данных
- `DB_ECHO` - вывод SQL запросов
- `DB_POOL_SIZE` / `DB_MAX_OVERFLOW` - настройки пула соединений

#### LoggingSettings (`LOG_*`)
- `LOG_LEVEL` - уровень логирования (TRACE/DEBUG/INFO/WARNING/ERROR/CRITICAL)
- `LOG_FORMAT` - формат сообщений
- `LOG_SERIALIZE` - JSON формат логов
- `LOG_DIAGNOSE` / `LOG_BACKTRACE` - диагностика

#### CORSSettings (`CORS_*`)
- `CORS_ENABLED` - включить CORS
- `CORS_ALLOW_ORIGINS` - разрешенные origins (через запятую или `*`)
- `CORS_ALLOW_CREDENTIALS` - credentials
- `CORS_ALLOW_METHODS` / `CORS_ALLOW_HEADERS` - методы и заголовки

#### APISettings (`API_*`)
- `API_PREFIX` - префикс API (по умолчанию `/api/v1`)
- `API_DOCS_URL` - URL для Swagger UI
- `API_REDOC_URL` - URL для ReDoc
- `API_OPENAPI_URL` - URL для OpenAPI схемы

## 🏛️ Архитектурные паттерны

### Dependency Injection (Dishka)

Проект использует [Dishka](https://github.com/reagento/dishka) для управления зависимостями:

```python
# src/di/database.py
class DBProvider(Provider):
    @provide(scope=Scope.APP)
    def get_engine(self) -> AsyncEngine:
        return create_async_engine(self._config.url)
    
    @provide(scope=Scope.REQUEST)
    async def get_session(self, engine: AsyncEngine) -> AsyncSession:
        async with AsyncSession(engine) as session:
            yield session
    
    @provide(scope=Scope.REQUEST)
    async def get_unit_of_work(self, session: AsyncSession) -> IUnitOfWork:
        async with UnitOfWork(session=session) as uow:
            yield uow
```

### Unit of Work Pattern

Управление транзакциями через Unit of Work:

```python
from src.application.common.unit_of_work import IUnitOfWork

async def my_use_case(uow: IUnitOfWork):
    # Выполнение операций
    await uow.register_event(event)
    # Коммит транзакции
    await uow.commit()
```

### Repository Pattern

Абстракция доступа к данным через репозитории (см. `src/infrastructure/database/repositories/`).

## 📚 Дополнительные ресурсы

### Документация проекта

- [📋 Шаблон Pull Request](.github/pull_request_template.md)
- [🐛 Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md)
- [✨ Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md)
- [🔧 CI/CD Setup Guide](.github/SETUP.md)
- [💻 Useful Commands](.github/COMMANDS.md)

### Внешние ресурсы

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Dishka Documentation](https://dishka.readthedocs.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Loguru Documentation](https://loguru.readthedocs.io/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [pytest Documentation](https://docs.pytest.org/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

## 🤝 Contributing

Приветствуются любые вклады в проект! При создании Pull Request:

1. ✅ Заголовок PR должен следовать [Conventional Commits](https://www.conventionalcommits.org/)
2. ✅ Все тесты должны проходить
3. ✅ Код должен проходить проверки Ruff
4. ✅ Добавьте тесты для новой функциональности
5. ✅ Обновите документацию при необходимости
6. ✅ Опишите изменения в теле PR

Подробнее см.:
- [Шаблон PR](.github/pull_request_template.md)
- [CI/CD Setup Guide](.github/SETUP.md)

## 📝 Лицензия

См. файл [LICENSE](LICENSE) для подробной информации.

---

**Made with ❤️ using Python 3.13, FastAPI, and Clean Architecture principles**