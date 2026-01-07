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

