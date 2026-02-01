# python_web_template

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

