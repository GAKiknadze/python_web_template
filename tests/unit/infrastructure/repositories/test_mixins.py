from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from pydantic import ConfigDict, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from src.domain.common.entity import Entity, EntityId, UuidEntityId
from src.infrastructure.database.models.base import Base
from src.infrastructure.database.repositories.mixins import (
    DeleteByIdMethodMixin,
    GetByIdMethodMixin,
    SaveMethodMixin,
    SoftDeleteByIdMethodMixin,
)

# === Вспомогательные типы ===


class IntEntityId(EntityId[int]):
    """EntityId для integer ID."""

    @classmethod
    def _new(cls) -> int:
        import random

        return random.randint(1, 1000000)  # noqa: S311

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: type, handler: GetCoreSchemaHandler) -> CoreSchema:
        from_int_schema = core_schema.chain_schema(
            [
                core_schema.int_schema(),
                core_schema.with_info_after_validator_function(lambda v, i: cls(v), core_schema.any_schema()),
            ]
        )
        instance_schema = core_schema.is_instance_schema(cls)
        return core_schema.union_schema(
            [instance_schema, from_int_schema],
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance.value,
                return_schema=core_schema.int_schema(),
            ),
        )


# === Тестовые модели и сущности ===


class ProductModel(Base):
    """Тестовая модель продукта для SaveMethodMixin и GetByIdMethodMixin."""

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ProductEntity(Entity):
    """Тестовая сущность продукта."""

    id: UuidEntityId
    name: str
    price: int
    created_at: datetime

    model_config = ConfigDict(arbitrary_types_allowed=True)


class CategoryModel(Base):
    """Тестовая модель категории для DeleteByIdMethodMixin."""

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50))


class CategoryEntity(Entity):
    """Тестовая сущность категории."""

    id: IntEntityId
    title: str

    model_config = ConfigDict(arbitrary_types_allowed=True)


class DocumentModel(Base):
    """Тестовая модель документа с soft delete."""

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class DocumentEntity(Entity):
    """Тестовая сущность документа."""

    id: UuidEntityId
    title: str
    is_deleted: bool
    created_at: datetime

    model_config = ConfigDict(arbitrary_types_allowed=True)


# === Тестовые репозитории с миксинами ===


class ProductRepository(
    SaveMethodMixin[ProductEntity],
    GetByIdMethodMixin[ProductEntity, UuidEntityId],
):
    """Репозиторий продуктов с миксинами save и get_by_id."""

    def __init__(self, session: AsyncSession):
        self._session = session
        self._model_cls = ProductModel
        self._entity_cls = ProductEntity

    def model_to_entity(self, model: ProductModel) -> ProductEntity:
        return ProductEntity.model_validate(model, from_attributes=True)

    def entity_to_model(self, entity: ProductEntity) -> ProductModel:
        data = entity.model_dump()
        return ProductModel(**data)


class CategoryRepository(
    DeleteByIdMethodMixin[IntEntityId],
):
    """Репозиторий категорий с миксином delete_by_id."""

    def __init__(self, session: AsyncSession):
        self._session = session
        self._model_cls = CategoryModel
        self._entity_cls = CategoryEntity

    def model_to_entity(self, model: CategoryModel) -> CategoryEntity:
        return CategoryEntity.model_validate(model, from_attributes=True)

    def entity_to_model(self, entity: CategoryEntity) -> CategoryModel:
        data = entity.model_dump()
        return CategoryModel(**data)


class DocumentRepository(
    SoftDeleteByIdMethodMixin[DocumentEntity, UuidEntityId],
):
    """Репозиторий документов с миксином soft delete."""

    def __init__(self, session: AsyncSession):
        self._session = session
        self._model_cls = DocumentModel
        self._entity_cls = DocumentEntity
        self._soft_delete_field = "is_deleted"

    def model_to_entity(self, model: DocumentModel) -> DocumentEntity:
        return DocumentEntity.model_validate(model, from_attributes=True)

    def entity_to_model(self, entity: DocumentEntity) -> DocumentModel:
        data = entity.model_dump()
        return DocumentModel(**data)


# === Фикстуры ===


@pytest.fixture
def mock_session() -> AsyncMock:
    """Создает mock для AsyncSession."""
    session = AsyncMock(spec=AsyncSession)
    session.merge = AsyncMock()
    session.flush = AsyncMock()
    session.refresh = AsyncMock()
    session.get = AsyncMock()
    session.delete = AsyncMock()
    return session


@pytest.fixture
def product_repository(mock_session: AsyncMock) -> ProductRepository:
    """Создает экземпляр ProductRepository."""
    return ProductRepository(session=mock_session)


@pytest.fixture
def category_repository(mock_session: AsyncMock) -> CategoryRepository:
    """Создает экземпляр CategoryRepository."""
    return CategoryRepository(session=mock_session)


@pytest.fixture
def document_repository(mock_session: AsyncMock) -> DocumentRepository:
    """Создает экземпляр DocumentRepository."""
    return DocumentRepository(session=mock_session)


@pytest.fixture
def product_entity() -> ProductEntity:
    """Создает тестовую сущность продукта."""
    return ProductEntity(
        id=UuidEntityId(uuid4()),
        name="Test Product",
        price=1000,
        created_at=datetime.now(UTC),
    )


@pytest.fixture
def product_model() -> ProductModel:
    """Создает тестовую модель продукта."""
    return ProductModel(
        id=uuid4(),
        name="Test Product Model",
        price=2000,
        created_at=datetime.now(UTC),
    )


@pytest.fixture
def category_model() -> CategoryModel:
    """Создает тестовую модель категории."""
    model = CategoryModel(title="Test Category")
    model.id = 1  # Устанавливаем ID вручную для теста
    return model


@pytest.fixture
def document_model() -> DocumentModel:
    """Создает тестовую модель документа."""
    return DocumentModel(
        id=uuid4(),
        title="Test Document",
        is_deleted=False,
        created_at=datetime.now(UTC),
    )


# === Тесты SaveMethodMixin ===


class TestSaveMethodMixin:
    """Тесты для SaveMethodMixin."""

    @pytest.mark.asyncio
    async def test_save_creates_new_entity(
        self, product_repository: ProductRepository, product_entity: ProductEntity, mock_session: AsyncMock
    ) -> None:
        """Проверяет сохранение новой сущности."""
        # Настраиваем mock
        merged_model = ProductModel(
            id=product_entity.id.value,
            name=product_entity.name,
            price=product_entity.price,
            created_at=product_entity.created_at,
        )
        mock_session.merge.return_value = merged_model

        # Вызываем метод
        result = await product_repository.save(product_entity)

        # Проверяем вызовы
        assert mock_session.merge.called
        assert mock_session.flush.called
        assert mock_session.refresh.called

        # Проверяем результат
        assert isinstance(result, ProductEntity)
        assert result.name == product_entity.name
        assert result.price == product_entity.price

    @pytest.mark.asyncio
    async def test_save_updates_existing_entity(
        self, product_repository: ProductRepository, product_entity: ProductEntity, mock_session: AsyncMock
    ) -> None:
        """Проверяет обновление существующей сущности."""
        # Изменяем сущность
        product_entity.name = "Updated Product"
        product_entity.price = 1500

        # Настраиваем mock
        merged_model = ProductModel(
            id=product_entity.id.value,
            name="Updated Product",
            price=1500,
            created_at=product_entity.created_at,
        )
        mock_session.merge.return_value = merged_model

        # Вызываем метод
        result = await product_repository.save(product_entity)

        # Проверяем результат
        assert result.name == "Updated Product"
        assert result.price == 1500

    @pytest.mark.asyncio
    async def test_save_calls_entity_to_model(
        self, product_repository: ProductRepository, product_entity: ProductEntity, mock_session: AsyncMock
    ) -> None:
        """Проверяет, что save вызывает entity_to_model."""
        merged_model = ProductModel(
            id=product_entity.id.value,
            name=product_entity.name,
            price=product_entity.price,
            created_at=product_entity.created_at,
        )
        mock_session.merge.return_value = merged_model

        await product_repository.save(product_entity)

        # Проверяем, что merge был вызван с моделью
        assert mock_session.merge.called
        call_args = mock_session.merge.call_args[0][0]
        assert isinstance(call_args, ProductModel)

    @pytest.mark.asyncio
    async def test_save_calls_model_to_entity(
        self, product_repository: ProductRepository, product_entity: ProductEntity, mock_session: AsyncMock
    ) -> None:
        """Проверяет, что save вызывает model_to_entity для результата."""
        merged_model = ProductModel(
            id=product_entity.id.value,
            name=product_entity.name,
            price=product_entity.price,
            created_at=product_entity.created_at,
        )
        mock_session.merge.return_value = merged_model

        result = await product_repository.save(product_entity)

        # Результат должен быть сущностью
        assert isinstance(result, ProductEntity)

    @pytest.mark.asyncio
    async def test_save_flushes_and_refreshes(
        self, product_repository: ProductRepository, product_entity: ProductEntity, mock_session: AsyncMock
    ) -> None:
        """Проверяет, что save вызывает flush и refresh."""
        merged_model = ProductModel(
            id=product_entity.id.value,
            name=product_entity.name,
            price=product_entity.price,
            created_at=product_entity.created_at,
        )
        mock_session.merge.return_value = merged_model

        await product_repository.save(product_entity)

        # Проверяем порядок вызовов
        mock_session.merge.assert_called_once()
        mock_session.flush.assert_called_once()
        mock_session.refresh.assert_called_once_with(merged_model)


# === Тесты GetByIdMethodMixin ===


class TestGetByIdMethodMixin:
    """Тесты для GetByIdMethodMixin."""

    @pytest.mark.asyncio
    async def test_get_by_id_returns_entity(
        self, product_repository: ProductRepository, product_model: ProductModel, mock_session: AsyncMock
    ) -> None:
        """Проверяет получение сущности по ID."""
        product_id = UuidEntityId(product_model.id)
        mock_session.get.return_value = product_model

        result = await product_repository.get_by_id(product_id)

        # Проверяем вызов
        mock_session.get.assert_called_once_with(ProductModel, product_id)

        # Проверяем результат
        assert result is not None
        assert isinstance(result, ProductEntity)
        assert result.id.value == product_model.id
        assert result.name == product_model.name
        assert result.price == product_model.price

    @pytest.mark.asyncio
    async def test_get_by_id_returns_none_when_not_found(
        self, product_repository: ProductRepository, mock_session: AsyncMock
    ) -> None:
        """Проверяет, что get_by_id возвращает None, если сущность не найдена."""
        product_id = UuidEntityId(uuid4())
        mock_session.get.return_value = None

        result = await product_repository.get_by_id(product_id)

        # Проверяем результат
        assert result is None
        mock_session.get.assert_called_once_with(ProductModel, product_id)

    @pytest.mark.asyncio
    async def test_get_by_id_with_int_id(
        self, category_repository: CategoryRepository, category_model: CategoryModel, mock_session: AsyncMock
    ) -> None:
        """Проверяет работу get_by_id с integer ID."""

        # Добавляем миксин GetByIdMethodMixin к CategoryRepository для теста
        class CategoryRepositoryWithGet(
            CategoryRepository,
            GetByIdMethodMixin[CategoryEntity, IntEntityId],
        ):
            def __init__(self, session: AsyncSession):
                super().__init__(session)

        repo = CategoryRepositoryWithGet(session=mock_session)
        mock_session.get.return_value = category_model

        category_id = IntEntityId(1)
        result = await repo.get_by_id(category_id)

        assert result is not None
        assert isinstance(result, CategoryEntity)
        assert result.id.value == category_model.id
        assert result.title == category_model.title

    @pytest.mark.asyncio
    async def test_get_by_id_calls_model_to_entity(
        self, product_repository: ProductRepository, product_model: ProductModel, mock_session: AsyncMock
    ) -> None:
        """Проверяет, что get_by_id вызывает model_to_entity."""
        product_id = UuidEntityId(product_model.id)
        mock_session.get.return_value = product_model

        result = await product_repository.get_by_id(product_id)

        # Результат должен быть преобразован в сущность
        assert isinstance(result, ProductEntity)


# === Тесты DeleteByIdMethodMixin ===


class TestDeleteByIdMethodMixin:
    """Тесты для DeleteByIdMethodMixin."""

    @pytest.mark.asyncio
    async def test_delete_by_id_deletes_existing_entity(
        self, category_repository: CategoryRepository, category_model: CategoryModel, mock_session: AsyncMock
    ) -> None:
        """Проверяет удаление существующей сущности."""
        mock_session.get.return_value = category_model
        category_id = IntEntityId(1)

        await category_repository.delete_by_id(category_id)

        # Проверяем вызовы
        mock_session.get.assert_called_once_with(CategoryModel, category_id)
        mock_session.delete.assert_called_once_with(category_model)

    @pytest.mark.asyncio
    async def test_delete_by_id_does_nothing_when_not_found(
        self, category_repository: CategoryRepository, mock_session: AsyncMock
    ) -> None:
        """Проверяет, что delete_by_id ничего не делает, если сущность не найдена."""
        mock_session.get.return_value = None
        category_id = IntEntityId(999)

        await category_repository.delete_by_id(category_id)

        # Проверяем, что delete не был вызван
        mock_session.get.assert_called_once_with(CategoryModel, category_id)
        mock_session.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_by_id_with_uuid(
        self, product_repository: ProductRepository, product_model: ProductModel, mock_session: AsyncMock
    ) -> None:
        """Проверяет удаление с UUID ID."""

        class ProductRepositoryWithDelete(
            ProductRepository,
            DeleteByIdMethodMixin[UuidEntityId],
        ):
            def __init__(self, session: AsyncSession):
                super().__init__(session)

        repo = ProductRepositoryWithDelete(session=mock_session)
        product_id = UuidEntityId(product_model.id)
        mock_session.get.return_value = product_model

        await repo.delete_by_id(product_id)

        mock_session.get.assert_called_once_with(ProductModel, product_id)
        mock_session.delete.assert_called_once_with(product_model)

    @pytest.mark.asyncio
    async def test_delete_by_id_returns_none(
        self, category_repository: CategoryRepository, category_model: CategoryModel, mock_session: AsyncMock
    ) -> None:
        """Проверяет, что delete_by_id не возвращает значение."""
        mock_session.get.return_value = category_model
        category_id = IntEntityId(1)

        result = await category_repository.delete_by_id(category_id)

        assert result is None


# === Тесты SoftDeleteByIdMethodMixin ===


class TestSoftDeleteByIdMethodMixin:
    """Тесты для SoftDeleteByIdMethodMixin."""

    @pytest.mark.asyncio
    async def test_soft_delete_by_id_marks_as_deleted(
        self, document_repository: DocumentRepository, document_model: DocumentModel, mock_session: AsyncMock
    ) -> None:
        """Проверяет мягкое удаление сущности."""
        document_id = UuidEntityId(document_model.id)
        mock_session.get.return_value = document_model

        await document_repository.soft_delete_by_id(document_id)

        # Проверяем вызовы
        mock_session.get.assert_called_once_with(DocumentModel, document_id)
        mock_session.flush.assert_called_once()

        # Проверяем, что флаг установлен
        assert document_model.is_deleted is True

    @pytest.mark.asyncio
    async def test_soft_delete_by_id_does_nothing_when_not_found(
        self, document_repository: DocumentRepository, mock_session: AsyncMock
    ) -> None:
        """Проверяет, что soft_delete_by_id ничего не делает, если сущность не найдена."""
        document_id = UuidEntityId(uuid4())
        mock_session.get.return_value = None

        await document_repository.soft_delete_by_id(document_id)

        # Проверяем, что flush не был вызван
        mock_session.get.assert_called_once_with(DocumentModel, document_id)
        mock_session.flush.assert_not_called()

    @pytest.mark.asyncio
    async def test_restore_by_id_restores_deleted_entity(
        self, document_repository: DocumentRepository, document_model: DocumentModel, mock_session: AsyncMock
    ) -> None:
        """Проверяет восстановление удаленной сущности."""
        # Помечаем как удаленную
        document_model.is_deleted = True
        document_id = UuidEntityId(document_model.id)
        mock_session.get.return_value = document_model

        await document_repository.restore_by_id(document_id)

        # Проверяем вызовы
        mock_session.get.assert_called_once_with(DocumentModel, document_id)
        mock_session.flush.assert_called_once()

        # Проверяем, что флаг снят
        assert document_model.is_deleted is False

    @pytest.mark.asyncio
    async def test_restore_by_id_does_nothing_when_not_found(
        self, document_repository: DocumentRepository, mock_session: AsyncMock
    ) -> None:
        """Проверяет, что restore_by_id ничего не делает, если сущность не найдена."""
        document_id = UuidEntityId(uuid4())
        mock_session.get.return_value = None

        await document_repository.restore_by_id(document_id)

        # Проверяем, что flush не был вызван
        mock_session.get.assert_called_once_with(DocumentModel, document_id)
        mock_session.flush.assert_not_called()

    @pytest.mark.asyncio
    async def test_soft_delete_and_restore_cycle(
        self, document_repository: DocumentRepository, document_model: DocumentModel, mock_session: AsyncMock
    ) -> None:
        """Проверяет полный цикл мягкого удаления и восстановления."""
        document_id = UuidEntityId(document_model.id)
        mock_session.get.return_value = document_model

        # Начальное состояние
        assert document_model.is_deleted is False

        # Удаляем
        await document_repository.soft_delete_by_id(document_id)
        assert document_model.is_deleted is True

        # Восстанавливаем
        await document_repository.restore_by_id(document_id)
        assert document_model.is_deleted is False

    @pytest.mark.asyncio
    async def test_soft_delete_uses_correct_field(
        self, document_repository: DocumentRepository, document_model: DocumentModel, mock_session: AsyncMock
    ) -> None:
        """Проверяет, что используется правильное поле для soft delete."""
        assert document_repository._soft_delete_field == "is_deleted"

        document_id = UuidEntityId(document_model.id)
        mock_session.get.return_value = document_model

        await document_repository.soft_delete_by_id(document_id)

        # Проверяем, что изменилось именно поле is_deleted
        assert hasattr(document_model, "is_deleted")
        assert document_model.is_deleted is True


# === Интеграционные тесты для комбинации миксинов ===


class TestMixinsCombination:
    """Тесты для комбинации нескольких миксинов."""

    @pytest.mark.asyncio
    async def test_repository_with_multiple_mixins(
        self, product_repository: ProductRepository, product_entity: ProductEntity, mock_session: AsyncMock
    ) -> None:
        """Проверяет работу репозитория с несколькими миксинами."""
        # Настраиваем mock для save
        merged_model = ProductModel(
            id=product_entity.id.value,
            name=product_entity.name,
            price=product_entity.price,
            created_at=product_entity.created_at,
        )
        mock_session.merge.return_value = merged_model

        # Сохраняем
        saved_entity = await product_repository.save(product_entity)
        assert saved_entity is not None

        # Настраиваем mock для get_by_id
        mock_session.get.return_value = merged_model

        # Получаем
        retrieved_entity = await product_repository.get_by_id(product_entity.id)
        assert retrieved_entity is not None
        assert retrieved_entity.id == product_entity.id

    @pytest.mark.asyncio
    async def test_mixins_share_session(self, product_repository: ProductRepository, mock_session: AsyncMock) -> None:
        """Проверяет, что все миксины используют одну и ту же сессию."""
        assert product_repository._session is mock_session

        # Все миксины должны использовать эту же сессию
        product_id = UuidEntityId(uuid4())
        mock_session.get.return_value = None

        await product_repository.get_by_id(product_id)

        # Проверяем, что использовалась правильная сессия
        assert mock_session.get.called


# === Тесты граничных случаев ===


class TestEdgeCases:
    """Тесты граничных случаев для миксинов."""

    @pytest.mark.asyncio
    async def test_save_with_none_values(self, product_repository: ProductRepository, mock_session: AsyncMock) -> None:
        """Проверяет сохранение с нулевыми значениями."""
        entity = ProductEntity(
            id=UuidEntityId(uuid4()),
            name="Zero Price",
            price=0,
            created_at=datetime.now(UTC),
        )

        merged_model = ProductModel(
            id=entity.id.value,
            name=entity.name,
            price=0,
            created_at=entity.created_at,
        )
        mock_session.merge.return_value = merged_model

        result = await product_repository.save(entity)

        assert result.price == 0

    @pytest.mark.asyncio
    async def test_get_by_id_with_special_characters(
        self, product_repository: ProductRepository, mock_session: AsyncMock
    ) -> None:
        """Проверяет получение сущности со специальными символами в данных."""
        special_name = "Product\n\t'\"Special"
        model = ProductModel(
            id=uuid4(),
            name=special_name,
            price=100,
            created_at=datetime.now(UTC),
        )
        product_id = UuidEntityId(model.id)
        mock_session.get.return_value = model

        result = await product_repository.get_by_id(product_id)

        assert result is not None
        assert result.name == special_name

    @pytest.mark.asyncio
    async def test_soft_delete_idempotent(
        self, document_repository: DocumentRepository, document_model: DocumentModel, mock_session: AsyncMock
    ) -> None:
        """Проверяет, что повторное мягкое удаление идемпотентно."""
        document_id = UuidEntityId(document_model.id)
        mock_session.get.return_value = document_model

        # Удаляем дважды
        await document_repository.soft_delete_by_id(document_id)
        assert document_model.is_deleted is True

        await document_repository.soft_delete_by_id(document_id)
        assert document_model.is_deleted is True

        # flush должен быть вызван дважды
        assert mock_session.flush.call_count == 2

    @pytest.mark.asyncio
    async def test_restore_idempotent(
        self, document_repository: DocumentRepository, document_model: DocumentModel, mock_session: AsyncMock
    ) -> None:
        """Проверяет, что повторное восстановление идемпотентно."""
        document_model.is_deleted = False
        document_id = UuidEntityId(document_model.id)
        mock_session.get.return_value = document_model

        # Восстанавливаем дважды
        await document_repository.restore_by_id(document_id)
        assert document_model.is_deleted is False

        await document_repository.restore_by_id(document_id)
        assert document_model.is_deleted is False

        # flush должен быть вызван дважды
        assert mock_session.flush.call_count == 2
