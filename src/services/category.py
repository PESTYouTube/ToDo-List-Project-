from sqlalchemy.orm import Session

from src.repositories.category import CategoryRepository
from src.schemas.category import (
    CategorySchema,
    CategoryUpdateSchema,
    CreateCategorySchema,
)


class CategoryNotFound(Exception):
    """Категория не найдена в БД"""


class CategoryService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.category_repositor = CategoryRepository(db)

    def list_category(self) -> list[CategorySchema]:
        tasks_orm = self.category_repositor.get_all()
        return [CategorySchema.model_validate(task) for task in tasks_orm]

    def create_category(self, category_create: CreateCategorySchema) -> CategorySchema:
        category_orm = self.category_repositor.create(name=category_create.name)
        self.db.commit()
        return CategorySchema.model_validate(category_orm)

    def update_category(
        self, category_id: str, category_update: CategoryUpdateSchema
    ) -> CategorySchema:
        category_for_update = self.category_repositor.get_by_id(category_id=category_id)
        if not category_for_update:
            raise CategoryNotFound(f"Задача c id {category_id} не найдена")
        if category_update.name is not None:
            category_update.name = category_update.name

        self.db.commit()
        return CategorySchema.model_validate(category_for_update)

    def delete_category(self, category_id: str):
        category_for_delete = self.category_repositor.get_by_id(category_id=category_id)
        if not category_for_delete:
            raise CategoryNotFound(f"Задача c id {category_id} не найдена")
        self.category_repositor.delete(category_for_delete)
        self.db.commit()
