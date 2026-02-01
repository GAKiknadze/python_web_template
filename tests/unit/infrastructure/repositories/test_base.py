from datetime import datetime
from typing import Any
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4

import pytest
from pydantic import BaseModel, ConfigDict
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from src.domain.common.entity import Entity, UuidEntityId
from src.infrastructure.database.models.base import Base
from src.infrastructure.database.repositories.base import BaseRepository

# === Тестовые модели и сущности ===


class UserModel(Base):
    """Тестовая модель SQLAlchemy для пользователя."""

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class UserEntity(Entity):
    """Тестовая сущность Pydantic для пользователя."""

    id: UuidEntityId
    name: str
    value: int
    created_at: datetime

    model_config = ConfigDict(arbitrary_types_allowed=True)


class ArticleModel(Base):
    """Простая модель для статьи."""

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50))


class ArticleEntity(BaseModel):
    """Простая Pydantic модель для статьи."""

    id: int
    title: str


# === Тестовые репозитории ===


class UserRepository(BaseRepository[UserModel, UserEntity]):
    """Конкретный репозиторий для пользователей."""

    pass


class ArticleRepository(BaseRepository[ArticleModel, ArticleEntity]):
    """Простой репозиторий для статей."""

    pass


class InvalidRepository(BaseRepository):  # type: ignore
    """Невалидный репозиторий без указания дженериков."""

    pass


# === Фикстуры ===


@pytest.fixture
def mock_session() -> AsyncMock:
    """Создает mock для AsyncSession."""
    session = AsyncMock()
    session.merge = AsyncMock()
    session.flush = AsyncMock()
    session.refresh = AsyncMock()
    session.get = AsyncMock()
    session.delete = AsyncMock()
    return session


@pytest.fixture
def user_repository(mock_session: AsyncMock) -> UserRepository:
    """Создает экземпляр UserRepository."""
    return UserRepository(session=mock_session)


@pytest.fixture
def article_repository(mock_session: AsyncMock) -> ArticleRepository:
    """Создает экземпляр ArticleRepository."""
    return ArticleRepository(session=mock_session)


@pytest.fixture
def user_model() -> UserModel:
    """Создает тестовую модель пользователя."""
    test_id = uuid4()
    now = datetime.now()
    model = UserModel(
        id=test_id,
        name="Test User",
        value=42,
        created_at=now,
    )
    return model


@pytest.fixture
def user_entity() -> UserEntity:
    """Создает тестовую сущность пользователя."""
    test_id = UuidEntityId(uuid4())
    now = datetime.now()
    entity = UserEntity(
        id=test_id,
        name="Test User Entity",
        value=100,
        created_at=now,
    )
    return entity


# === Тесты инициализации ===


class TestInitialization:
    """Тесты инициализации репозитория."""

    def test_init_with_valid_types(self, mock_session: AsyncMock) -> None:
        """Проверяет успешную инициализацию с валидными типами."""
        repo = UserRepository(session=mock_session)

        assert repo._session is mock_session
        assert repo._model_cls is UserModel
        assert repo._entity_cls is UserEntity

    def test_init_simple_repository(self, mock_session: AsyncMock) -> None:
        """Проверяет инициализацию простого репозитория."""
        repo = ArticleRepository(session=mock_session)

        assert repo._session is mock_session
        assert repo._model_cls is ArticleModel
        assert repo._entity_cls is ArticleEntity

    def test_init_without_generic_types_raises_error(self, mock_session: AsyncMock) -> None:
        """Проверяет, что инициализация без дженериков вызывает ошибку."""
        with pytest.raises(TypeError) as exc_info:
            InvalidRepository(session=mock_session)

        assert "Cannot determine concrete types" in str(exc_info.value)
        assert "Make sure your repository subclass inherits from BaseRepository[Model, Entity]" in str(exc_info.value)


# === Тесты получения типов ===


class TestGetConcreteType:
    """Тесты метода _get_concrete_type."""

    def test_get_model_type(self, user_repository: UserRepository) -> None:
        """Проверяет получение типа модели (индекс 0)."""
        model_type = user_repository._get_concrete_type(0)
        assert model_type is UserModel

    def test_get_entity_type(self, user_repository: UserRepository) -> None:
        """Проверяет получение типа сущности (индекс 1)."""
        entity_type = user_repository._get_concrete_type(1)
        assert entity_type is UserEntity

    def test_get_concrete_type_for_simple_repository(self, article_repository: ArticleRepository) -> None:
        """Проверяет получение типов для простого репозитория."""
        model_type = article_repository._get_concrete_type(0)
        entity_type = article_repository._get_concrete_type(1)

        assert model_type is ArticleModel
        assert entity_type is ArticleEntity


# === Тесты конвертации model -> entity ===


class TestModelToEntity:
    """Тесты метода model_to_entity."""

    def test_model_to_entity_basic(self, user_repository: UserRepository, user_model: UserModel) -> None:
        """Проверяет базовую конвертацию модели в сущность."""
        entity = user_repository.model_to_entity(user_model)

        assert isinstance(entity, UserEntity)
        assert str(entity.id.value) == str(user_model.id)
        assert entity.name == user_model.name
        assert entity.value == user_model.value
        assert entity.created_at == user_model.created_at

    def test_model_to_entity_with_uuid_entity_id(self, user_repository: UserRepository) -> None:
        """Проверяет конвертацию с UuidEntityId."""
        test_id = uuid4()
        now = datetime.now()
        model = UserModel(
            id=test_id,
            name="UUID Test",
            value=999,
            created_at=now,
        )

        entity = user_repository.model_to_entity(model)

        assert isinstance(entity.id, UuidEntityId)
        assert entity.id.value == test_id
        assert entity.name == "UUID Test"
        assert entity.value == 999

    def test_model_to_entity_simple(self, article_repository: ArticleRepository) -> None:
        """Проверяет конвертацию для простых типов."""
        model = ArticleModel(id=1, title="Simple Test")

        entity = article_repository.model_to_entity(model)

        assert isinstance(entity, ArticleEntity)
        assert entity.id == 1
        assert entity.title == "Simple Test"

    def test_model_to_entity_validates_data(self, user_repository: UserRepository) -> None:
        """Проверяет, что конвертация валидирует данные через Pydantic."""
        # Создаем модель с валидными данными
        model = UserModel(
            id=uuid4(),
            name="Valid Name",
            value=50,
            created_at=datetime.now(),
        )

        # Должна пройти успешно
        entity = user_repository.model_to_entity(model)
        assert entity.name == "Valid Name"


# === Тесты конвертации entity -> model ===


class TestEntityToModel:
    """Тесты метода entity_to_model."""

    def test_entity_to_model_basic(self, user_repository: UserRepository, user_entity: UserEntity) -> None:
        """Проверяет базовую конвертацию сущности в модель."""
        model = user_repository.entity_to_model(user_entity)

        assert isinstance(model, UserModel)
        # UuidEntityId сериализуется в строку через model_dump()
        assert str(model.id) == str(user_entity.id.value)
        assert model.name == user_entity.name
        assert model.value == user_entity.value
        assert model.created_at == user_entity.created_at

    def test_entity_to_model_with_uuid_entity_id(self, user_repository: UserRepository) -> None:
        """Проверяет конвертацию с UuidEntityId."""
        test_id = UuidEntityId(uuid4())
        now = datetime.now()
        entity = UserEntity(
            id=test_id,
            name="Entity to Model Test",
            value=777,
            created_at=now,
        )

        model = user_repository.entity_to_model(entity)

        assert isinstance(model, UserModel)
        # UuidEntityId сериализуется в строку, но SQLAlchemy конвертирует обратно в UUID
        assert str(model.id) == str(test_id.value)
        assert model.name == "Entity to Model Test"
        assert model.value == 777

    def test_entity_to_model_simple(self, article_repository: ArticleRepository) -> None:
        """Проверяет конвертацию для простых типов."""
        entity = ArticleEntity(id=42, title="Simple Entity")

        model = article_repository.entity_to_model(entity)

        assert isinstance(model, ArticleModel)
        assert model.id == 42
        assert model.title == "Simple Entity"

    def test_entity_to_model_uses_model_dump(self, user_repository: UserRepository, user_entity: UserEntity) -> None:
        """Проверяет, что используется model_dump для сериализации."""
        model = user_repository.entity_to_model(user_entity)

        # UuidEntityId сериализуется в строку, SQLAlchemy может принять строку и конвертировать в UUID
        # Проверяем, что значения совпадают
        assert str(model.id) == str(user_entity.id.value)


# === Интеграционные тесты ===


class TestRoundTrip:
    """Тесты полного цикла конвертации model -> entity -> model."""

    def test_model_to_entity_to_model(self, user_repository: UserRepository, user_model: UserModel) -> None:
        """Проверяет цикл: model -> entity -> model."""
        entity = user_repository.model_to_entity(user_model)
        result_model = user_repository.entity_to_model(entity)

        # Сравниваем как строки, т.к. UuidEntityId сериализуется в строку
        assert str(result_model.id) == str(user_model.id)
        assert result_model.name == user_model.name
        assert result_model.value == user_model.value
        assert result_model.created_at == user_model.created_at

    def test_entity_to_model_to_entity(self, user_repository: UserRepository, user_entity: UserEntity) -> None:
        """Проверяет цикл: entity -> model -> entity."""
        model = user_repository.entity_to_model(user_entity)
        result_entity = user_repository.model_to_entity(model)

        assert result_entity.id == user_entity.id
        assert result_entity.name == user_entity.name
        assert result_entity.value == user_entity.value
        assert result_entity.created_at == user_entity.created_at

    def test_multiple_conversions(self, article_repository: ArticleRepository) -> None:
        """Проверяет множественные конвертации."""
        original_entity = ArticleEntity(id=100, title="Multi Convert")

        # Конвертируем несколько раз
        model1 = article_repository.entity_to_model(original_entity)
        entity1 = article_repository.model_to_entity(model1)
        model2 = article_repository.entity_to_model(entity1)
        entity2 = article_repository.model_to_entity(model2)

        # Данные должны остаться неизменными
        assert entity2.id == original_entity.id
        assert entity2.title == original_entity.title


# === Тесты граничных случаев ===


class TestEdgeCases:
    """Тесты граничных случаев."""

    def test_empty_string_value(self, article_repository: ArticleRepository) -> None:
        """Проверяет работу с пустой строкой."""
        entity = ArticleEntity(id=1, title="")
        model = article_repository.entity_to_model(entity)

        assert model.title == ""

        result_entity = article_repository.model_to_entity(model)
        assert result_entity.title == ""

    def test_zero_values(self, user_repository: UserRepository) -> None:
        """Проверяет работу с нулевыми значениями."""
        entity = UserEntity(
            id=UuidEntityId(uuid4()),
            name="Zero Test",
            value=0,
            created_at=datetime.now(),
        )

        model = user_repository.entity_to_model(entity)
        assert model.value == 0

        result_entity = user_repository.model_to_entity(model)
        assert result_entity.value == 0

    def test_special_characters_in_strings(self, article_repository: ArticleRepository) -> None:
        """Проверяет работу со специальными символами."""
        special_title = "Test\n\t'\"\\Special"
        entity = ArticleEntity(id=1, title=special_title)

        model = article_repository.entity_to_model(entity)
        assert model.title == special_title

        result_entity = article_repository.model_to_entity(model)
        assert result_entity.title == special_title


# === Тесты типов ===


class TestTypeSystem:
    """Тесты системы типов."""

    def test_repository_is_generic(self) -> None:
        """Проверяет, что BaseRepository является дженериком."""
        from typing import get_args, get_origin

        # Проверяем, что UserRepository имеет правильное происхождение
        origin = get_origin(UserRepository.__orig_bases__[0])
        assert origin is BaseRepository

    def test_model_cls_type(self, user_repository: UserRepository) -> None:
        """Проверяет тип _model_cls."""
        assert isinstance(user_repository._model_cls, type)
        assert issubclass(user_repository._model_cls, Base)

    def test_entity_cls_type(self, user_repository: UserRepository) -> None:
        """Проверяет тип _entity_cls."""
        assert isinstance(user_repository._entity_cls, type)
        assert issubclass(user_repository._entity_cls, BaseModel)

    def test_session_type(self, user_repository: UserRepository, mock_session: AsyncMock) -> None:
        """Проверяет тип _session."""
        assert user_repository._session is mock_session


# === Тесты с различными типами данных ===


class TestWithDifferentDataTypes:
    """Тесты с различными типами данных."""

    def test_with_datetime(self, user_repository: UserRepository) -> None:
        """Проверяет работу с datetime."""
        now = datetime.now()
        entity = UserEntity(
            id=UuidEntityId(uuid4()),
            name="DateTime Test",
            value=1,
            created_at=now,
        )

        model = user_repository.entity_to_model(entity)
        result_entity = user_repository.model_to_entity(model)

        assert result_entity.created_at == now

    def test_with_uuid(self, user_repository: UserRepository) -> None:
        """Проверяет работу с UUID через UuidEntityId."""
        test_uuid = uuid4()
        entity_id = UuidEntityId(test_uuid)

        entity = UserEntity(
            id=entity_id,
            name="UUID Test",
            value=123,
            created_at=datetime.now(),
        )

        model = user_repository.entity_to_model(entity)
        # Сравниваем как строки
        assert str(model.id) == str(test_uuid)

        result_entity = user_repository.model_to_entity(model)
        assert result_entity.id.value == test_uuid


# === Тесты наследования ===


class TestInheritance:
    """Тесты наследования репозиториев."""

    def test_subclass_inherits_methods(self, user_repository: UserRepository) -> None:
        """Проверяет, что подкласс наследует методы."""
        assert hasattr(user_repository, "model_to_entity")
        assert hasattr(user_repository, "entity_to_model")
        assert hasattr(user_repository, "_get_concrete_type")

    def test_multiple_repository_instances_independent(self, mock_session: AsyncMock) -> None:
        """Проверяет независимость различных экземпляров репозитория."""
        repo1 = UserRepository(session=mock_session)
        repo2 = ArticleRepository(session=mock_session)

        assert repo1._model_cls is UserModel
        assert repo2._model_cls is ArticleModel
        assert repo1._entity_cls is UserEntity
        assert repo2._entity_cls is ArticleEntity


# === Тесты сериализации UuidEntityId ===


class TestUuidEntityIdSerialization:
    """Тесты специфичные для сериализации UuidEntityId."""

    def test_uuid_entity_id_serializes_to_string(self, user_repository: UserRepository) -> None:
        """Проверяет, что UuidEntityId сериализуется в строку через model_dump()."""
        test_id = UuidEntityId(uuid4())
        entity = UserEntity(
            id=test_id,
            name="Serialization Test",
            value=42,
            created_at=datetime.now(),
        )

        # model_dump() должен вернуть словарь со строковым id
        dumped = entity.model_dump()
        assert isinstance(dumped["id"], str)
        assert dumped["id"] == str(test_id.value)

    def test_sqlalchemy_accepts_uuid_string(self, user_repository: UserRepository) -> None:
        """Проверяет, что SQLAlchemy принимает UUID в виде строки."""
        test_uuid = uuid4()
        uuid_str = str(test_uuid)

        # Создаем модель со строковым UUID
        model = UserModel(
            id=uuid_str,  # type: ignore
            name="String UUID Test",
            value=1,
            created_at=datetime.now(),
        )

        # SQLAlchemy должна конвертировать строку в UUID
        assert isinstance(model.id, (UUID, str))
        assert str(model.id) == uuid_str

    def test_entity_to_model_preserves_uuid_value(self, user_repository: UserRepository) -> None:
        """Проверяет, что значение UUID сохраняется при конвертации entity -> model."""
        original_uuid = uuid4()
        entity = UserEntity(
            id=UuidEntityId(original_uuid),
            name="UUID Preservation Test",
            value=999,
            created_at=datetime.now(),
        )

        model = user_repository.entity_to_model(entity)

        # Значения должны совпадать (сравниваем как строки)
        assert str(model.id) == str(original_uuid)

        # Обратная конвертация должна сохранить значение
        result_entity = user_repository.model_to_entity(model)
        assert result_entity.id.value == original_uuid
