# 🚀 Quick Reference Commands

Шпаргалка с командами для быстрой работы с проектом.

## 📦 Установка и настройка

```bash
# Клонировать репозиторий
git clone https://github.com/GAKiknadze/python_web_template.git
cd python_web_template

# Установить все зависимости (dev + test)
uv sync --group dev --group test

# Установить pre-commit хуки
uv run pre-commit install
```

## 🔍 Проверка кода

```bash
# Запустить Ruff линтер
uv run ruff check .

# Автоматически исправить проблемы
uv run ruff check . --fix

# Проверить форматирование
uv run ruff format --check .

# Отформатировать код
uv run ruff format .

# Запустить pre-commit на всех файлах
uv run pre-commit run --all-files

# Запустить pre-commit на конкретных файлах
uv run pre-commit run --files src/main.py tests/test_config.py
```

## 🧪 Тестирование

```bash
# Запустить все тесты
uv run pytest

# Запустить тесты с подробным выводом
uv run pytest -v

# Запустить конкретный файл тестов
uv run pytest tests/test_config.py

# Запустить конкретный тест
uv run pytest tests/test_config.py::test_database_settings_defaults

# Запустить тесты с покрытием
uv run pytest --cov=src --cov-report=term

# Генерировать HTML отчет о покрытии
uv run pytest --cov=src --cov-report=html
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux

# Запустить тесты с покрытием и минимальным порогом
uv run pytest --cov=src --cov-fail-under=80

# Запустить только упавшие тесты
uv run pytest --lf

# Остановиться на первом упавшем тесте
uv run pytest -x

# Показать медленные тесты
uv run pytest --durations=10
```

## 🗃️ База данных (Alembic)

```bash
# Создать новую миграцию
uv run alembic revision --autogenerate -m "description"

# Применить все миграции
uv run alembic upgrade head

# Откатить последнюю миграцию
uv run alembic downgrade -1

# Посмотреть историю миграций
uv run alembic history

# Посмотреть текущую версию БД
uv run alembic current

# Откатить все миграции
uv run alembic downgrade base
```

## 🚀 Запуск приложения

```bash
# Запустить приложение
uv run python main.py

# Запустить с uvicorn напрямую
uv run uvicorn main:app --reload

# Запустить на другом порту
uv run uvicorn main:app --reload --port 8080

# Запустить с доступом извне
uv run uvicorn main:app --reload --host 0.0.0.0
```

## 📝 Git и коммиты

```bash
# Создать ветку для новой фичи
git checkout -b feat/my-feature

# Создать ветку для исправления
git checkout -b fix/bug-description

# Проверить статус
git status

# Добавить файлы
git add .

# Коммит (pre-commit запустится автоматически)
git commit -m "feat: add new feature"

# Пропустить pre-commit хуки (не рекомендуется!)
git commit -m "feat: add new feature" --no-verify

# Изменить последний коммит
git commit --amend

# Запушить ветку
git push origin feat/my-feature

# Создать Pull Request
gh pr create --base main --head feat/my-feature
```

## 🔄 Форматы коммитов (Conventional Commits)

```bash
# Новая функциональность
git commit -m "feat: add user authentication"
git commit -m "feat(api): add endpoint for user registration"

# Исправление бага
git commit -m "fix: resolve database connection timeout"
git commit -m "fix(auth): correct token validation logic"

# Документация
git commit -m "docs: update README with installation steps"
git commit -m "docs(api): add swagger documentation"

# Рефакторинг
git commit -m "refactor: simplify user service logic"
git commit -m "refactor(db): optimize query performance"

# Тесты
git commit -m "test: add tests for user service"
git commit -m "test(auth): add integration tests"

# CI/CD
git commit -m "ci: add GitHub Actions workflow"
git commit -m "ci: update pytest configuration"

# Стиль кода
git commit -m "style: format code with ruff"

# Рутинные задачи
git commit -m "chore: update dependencies"
git commit -m "chore(deps): bump fastapi to 0.110.0"

# Breaking changes
git commit -m "feat!: change API response format"
git commit -m "refactor!: rename User model to Account"
```

## 📦 Управление зависимостями

```bash
# Добавить производственную зависимость
uv add package-name

# Добавить зависимость для разработки
uv add --dev package-name

# Добавить зависимость в группу test
uv add --group test package-name

# Удалить зависимость
uv remove package-name

# Обновить все зависимости
uv sync --upgrade

# Обновить конкретную зависимость
uv add package-name --upgrade

# Показать установленные пакеты
uv pip list

# Показать устаревшие пакеты
uv pip list --outdated

# Экспортировать зависимости в requirements.txt
uv pip freeze > requirements.txt
```

## 🔧 Pre-commit

```bash
# Установить хуки
uv run pre-commit install

# Удалить хуки
uv run pre-commit uninstall

# Запустить на всех файлах
uv run pre-commit run --all-files

# Запустить на staged файлах
uv run pre-commit run

# Обновить версии хуков
uv run pre-commit autoupdate

# Очистить кеш
uv run pre-commit clean

# Запустить конкретный хук
uv run pre-commit run ruff --all-files
uv run pre-commit run ruff-format --all-files
```

## 🐛 Отладка

```bash
# Запустить с отладочной информацией
DEBUG=1 uv run python main.py

# Запустить pytest с отладкой
uv run pytest -vv --tb=long

# Запустить pytest с pdb при ошибке
uv run pytest --pdb

# Запустить pytest с логами
uv run pytest --log-cli-level=DEBUG

# Проверить импорты
uv run python -c "import src; print(src.__file__)"

# Проверить версии пакетов
uv run python -c "import fastapi; print(fastapi.__version__)"
```

## 📊 CI/CD (GitHub Actions)

```bash
# Посмотреть статус workflows локально (требует gh cli)
gh workflow list
gh workflow view ci.yml
gh run list
gh run watch

# Запустить workflow вручную (если настроен workflow_dispatch)
gh workflow run ci.yml

# Посмотреть логи последнего запуска
gh run view --log

# Скачать артефакты
gh run download <run-id>
```

## 🔍 Полезные однострочники

```bash
# Найти все TODO комментарии
grep -r "TODO" src/ tests/

# Найти все print statements
grep -rn "print(" src/

# Посчитать строки кода
find src/ -name "*.py" | xargs wc -l

# Найти большие файлы
find . -type f -size +100k -not -path "./.venv/*" -not -path "./.git/*"

# Очистить __pycache__
find . -type d -name "__pycache__" -exec rm -r {} +

# Очистить .pyc файлы
find . -type f -name "*.pyc" -delete

# Показать размер виртуального окружения
du -sh .venv

# Проверить синтаксис всех Python файлов
find src/ tests/ -name "*.py" -exec python -m py_compile {} \;
```

## 🎯 Быстрые комбинации

```bash
# Полная проверка перед коммитом
uv run ruff check . --fix && \
uv run ruff format . && \
uv run pytest tests/ -v && \
echo "✅ Готово к коммиту!"

# Полная очистка проекта
find . -type d -name "__pycache__" -exec rm -r {} + && \
find . -type f -name "*.pyc" -delete && \
rm -rf .pytest_cache .ruff_cache htmlcov .coverage && \
echo "✅ Проект очищен!"

# Быстрый тест + coverage
uv run pytest --cov=src --cov-report=term-missing -v

# Проверить все + запустить тесты
uv run pre-commit run --all-files && \
uv run pytest tests/ -v && \
echo "✅ Все проверки пройдены!"
```

## 📱 GitHub CLI (gh) полезные команды

```bash
# Создать PR
gh pr create --title "feat: new feature" --body "Description"

# Посмотреть открытые PR
gh pr list

# Checkout PR локально
gh pr checkout <number>

# Просмотреть PR в браузере
gh pr view --web

# Смержить PR
gh pr merge <number> --squash

# Создать issue
gh issue create --title "Bug report" --body "Description"

# Посмотреть issues
gh issue list

# Посмотреть статус CI
gh pr checks
```

## 💡 Подсказки

- Всегда запускайте тесты перед коммитом
- Используйте `--fix` с ruff для автоматического исправления
- Pre-commit хуки помогут поймать ошибки до push
- Conventional commits делают историю читаемой
- Используйте `pytest -k "pattern"` для запуска конкретных тестов по имени
- Добавьте `DEBUG=1` перед командой для детального логирования
- Используйте `uv run` для гарантии использования правильного окружения

## 📚 Дополнительно

- Полная документация по CI/CD: `.github/SETUP.md`
- Шаблон PR: `.github/pull_request_template.md`
- Сообщить о баге: `.github/ISSUE_TEMPLATE/bug_report.md`
- Предложить фичу: `.github/ISSUE_TEMPLATE/feature_request.md`
