# python_web_template

[![CI](https://github.com/GAKiknadze/python_web_template/actions/workflows/ci.yml/badge.svg)](https://github.com/GAKiknadze/python_web_template/actions/workflows/ci.yml)

Шаблон для создания веб-приложений на Python с архитектурой, основанной на принципах Clean Architecture и Domain-Driven Design (DDD).

## Описание

Этот проект предоставляет структурированный шаблон для разработки масштабируемых Python приложений с четкой разделением ответственности:

- **Domain Layer** (`domain/`) - Бизнес-логика и сущности домена
- **Application Layer** (`application/`) - Сценарии использования и координация бизнес-логики
- **Infrastructure Layer** (`infrastructure/`) - Реализация взаимодействия с внешними системами (БД, репозитории)
- **Interfaces Layer** (`interfaces/`) - API и точки входа приложения
- **DI Layer** (`di/`) - Управление зависимостями

## Особенности

- Clean Architecture структура
- Domain-Driven Design принципы
- Unit of Work паттерн для управления транзакциями
- Repository паттерн для работы с данными
- Dependency Injection для управления зависимостями
- FastAPI интеграция для REST API
- Pre-commit хуки с Ruff для автоматической проверки кода

## Требования

- Python 3.13+
- uv (для управления зависимостями)

## Быстрый старт

1. Установите зависимости:
```bash
uv sync --group dev
```

2. Установите pre-commit хуки:
```bash
uv run pre-commit install
```

3. Запустите проверку кода:
```bash
uv run pre-commit run --all-files
```

## Инструменты разработки

### Pre-commit

Проект настроен на использование pre-commit хуков для автоматической проверки кода перед каждым коммитом:

- **ruff** - линтер и форматтер кода
- Автоматическое исправление проблем (где возможно)
- Проверка форматирования кода

Хуки запускаются автоматически при каждом `git commit`. Для ручной проверки всех файлов:

```bash
uv run pre-commit run --all-files
```

### Ruff

Настройки Ruff находятся в файле `ruff.toml`. Основные проверки:

- pyupgrade
- isort (сортировка импортов)
- flake8 (ошибки, предупреждения, стиль)
- flake8-bugbear
- flake8-bandit (безопасность)
- pytest-style
- и другие

Для запуска линтера вручную:

```bash
uv run ruff check .
uv run ruff format .
```

### CI/CD

Проект настроен с GitHub Actions для автоматической проверки кода и запуска тестов.

#### Workflows

**1. CI Workflow** (`.github/workflows/ci.yml`)
- **Триггеры:** Push и Pull Request в ветку `main`
- **Jobs:**
  - **Lint** - проверка качества кода:
    - `ruff check` - статический анализ кода
    - `ruff format --check` - проверка форматирования
  - **Test** - запуск тестов:
    - Запуск всех тестов с pytest
    - Генерация отчета о покрытии кода
    - Загрузка отчета в артефакты

**2. Pull Request Workflow** (`.github/workflows/pr.yml`)
- **Триггеры:** Pull Request в ветки `main` и `develop`
- **Jobs:**
  - **Validate** - проверка формата PR:
    - Валидация заголовка PR (conventional commits)
  - **Code Quality** - проверка качества кода:
    - Ruff linter и formatter
    - Pre-commit хуки на измененных файлах
  - **Test Suite** - запуск тестов:
    - Тесты с покрытием кода
    - Проверка минимального порога покрытия
  - **Security** - проверка безопасности:
    - Ruff security checks (правила S*)
  - **Summary** - общий статус всех проверок

**3. Dependabot** (`.github/dependabot.yml`)
- Автоматическое обновление зависимостей:
  - Python пакеты (еженедельно по понедельникам)
  - GitHub Actions (еженедельно по понедельникам)
  - Группировка minor и patch обновлений

#### Форматы коммитов для PR

При создании Pull Request заголовок должен следовать conventional commits:

- `feat:` - новая функциональность
- `fix:` - исправление бага
- `docs:` - изменения в документации
- `style:` - форматирование кода
- `refactor:` - рефакторинг кода
- `perf:` - улучшение производительности
- `test:` - добавление тестов
- `build:` - изменения в сборке
- `ci:` - изменения в CI/CD
- `chore:` - рутинные задачи
- `revert:` - откат изменений

#### Локальный запуск тестов

```bash
# Установить тестовые зависимости
uv sync --group test

# Запустить тесты
uv run pytest tests/ -v

# Запустить тесты с покрытием
uv run pytest tests/ --cov=src --cov-report=term --cov-report=html

# Запустить только определенный тест
uv run pytest tests/test_config.py::test_database_settings_defaults -v
```

