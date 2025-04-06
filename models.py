"""
Модуль models.py
----------------
Содержит определение класса Task, представляющего модель данных для задачи.
"""

class Task:
    """
    Класс Task представляет задачу в трекере.

    Атрибуты:
        id (int): Уникальный идентификатор задачи.
        title (str): Заголовок задачи.
        description (str): Описание задачи.
        status (str): Статус задачи, возможные значения:
                      "todo" - задача еще не выполнена (по умолчанию),
                      "in_progress" - задача в процессе выполнения,
                      "done" - задача выполнена.
    """

    def __init__(self, task_id, title, description, status="todo"):
        # Инициализация задачи с заданными параметрами
        self.id = task_id                # Уникальный идентификатор задачи
        self.title = title               # Заголовок задачи
        self.description = description   # Описание задачи
        self.status = status             # Статус задачи (по умолчанию "todo")

    def to_dict(self):
        """
        Преобразует объект Task в словарь для дальнейшей сериализации в JSON.

        Returns:
            dict: Словарь, содержащий данные задачи.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, task_dict):
        """
        Создает объект Task из словаря.

        Args:
            task_dict (dict): Словарь с данными задачи.

        Returns:
            Task: Объект Task, созданный на основе данных словаря.
        """
        return cls(
            task_id=task_dict.get("id"),
            title=task_dict.get("title"),
            description=task_dict.get("description"),
            status=task_dict.get("status", "todo")
        )

    def __str__(self):
        """
        Возвращает строковое представление задачи для удобного отображения в консоли.

        Returns:
            str: Форматированная строка с информацией о задаче.
        """
        return f"ID: {self.id} | Заголовок: {self.title} | Описание: {self.description} | Статус: {self.status}"
