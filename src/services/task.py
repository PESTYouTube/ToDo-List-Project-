from sqlalchemy.orm import Session

from src.repositories.task import TaskRepository
from src.schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema


class TaskNotFound(Exception):
    """Задача не найдена в БД"""


class TaskService:
    def __init__(
        self,
        db: Session,
        cache_redis_url: str | None = None,
        cache_ttl_seconds: int = 0,
        cache_tasks_key: str | None = None,
    ):
        self.db = db
        self.task_repositor = TaskRepository(db)
        # self.cache = RedisCacheBackend(cache_redis_url, cache_ttl_seconds)
        # self.cache_tasks_key = cache_tasks_key

    def list_tasks(self) -> list[TaskSchema]:
        # добавить шаг 1: проверить есть ли данные в Redis
        # cached_tasks = self.cache.get(self.cache_tasks_key)
        # if cached_tasks:
        #     return cached_tasks

        tasks = (
            self.task_repositor.get_all()
        )  # данных в к шаг 2 по схеме (если данных в кеше нет идем в бд)
        # TODO: Добавить шаг 3: Сохранить в кеше,еслиеше нет
        task_read = [TaskSchema.model_validate(task) for task in tasks]
        # tasks_for_cache = [task.model_dump() for task in tasks]
        # self.cache.set(self.cache_tasks_key, tasks_for_cache)

        return task_read  # шаг 4

    def create_task(self, task_create: TaskCreateSchema) -> TaskSchema:
        # Инвалидировать кеш
        # self.cache.delete(self.cache_tasks_key)
        task_orm = self.task_repositor.create(title=task_create.title)
        self.db.commit()
        return TaskSchema.model_validate(task_orm)

    def update_task(self, task_id: str, task_update: TaskUpdateSchema) -> TaskSchema:
        # Инвалидировать кеш
        # self.cache.delete(self.cache_tasks_key)
        task_for_update = self.task_repositor.get_by_id(task_id=task_id)
        if not task_for_update:
            raise TaskNotFound(f"Задача c id {task_id} не найдена")
        if task_update.title is not None:
            task_for_update.title = task_update.title
        if task_update.completed is not None:
            task_for_update.completed = task_update.completed
        self.db.commit()
        return TaskSchema.model_validate(task_for_update)

    def delete_task(self, task_id: str) -> TaskSchema:
        # Инвалидировать кеш
        # self.cache.delete(self.cache_tasks_key)
        task_for_delete = self.task_repositor.get_by_id(task_id=task_id)
        if not task_for_delete:
            raise TaskNotFound(f"Задача c id {task_id} не найдена")
        self.task_repositor.delete(task_for_delete)
        self.db.commit()
        return TaskSchema.model_validate(task_for_delete)
