"""
Модуль operations.py
--------------------
Содержит функции для выполнения основных операций с задачами:
- загрузка и сохранение задач в JSON файл,
- добавление, обновление, удаление задач,
- изменение статуса задачи,
- фильтрация и получение списка задач.
"""

import json
import os
from models import Task

# Определяем имя файла, в котором будут храниться задачи
TASKS_FILE = "tasks.json"

def load_tasks():
    """
    Загружает список задач из файла TASKS_FILE.

    Если файл не существует или поврежден, возвращает пустой список.

    Returns:
        list[Task]: Список объектов Task.
    """
    if not os.path.exists(TASKS_FILE):
        # Если файл не существует, возвращаем пустой список
        return []
    with open(TASKS_FILE, "r", encoding="utf-8") as file:
        try:
            # Считываем данные и создаем список задач из словарей
            tasks_data = json.load(file)
            tasks = [Task.from_dict(td) for td in tasks_data]
            return tasks
        except json.JSONDecodeError:
            # Если файл не удается декодировать, возвращаем пустой список
            return []

def save_tasks(tasks):
    """
    Сохраняет список задач в файл TASKS_FILE в формате JSON.

    Args:
        tasks (list[Task]): Список объектов Task, который необходимо сохранить.
    """
    # Преобразуем каждый объект Task в словарь
    tasks_data = [task.to_dict() for task in tasks]
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        # Записываем данные с отступами для удобочитаемости и с отключенной ASCII-кодировкой
        json.dump(tasks_data, file, indent=4, ensure_ascii=False)

def get_new_task_id(tasks):
    """
    Генерирует новый уникальный идентификатор для новой задачи.

    Args:
        tasks (list[Task]): Список существующих задач.

    Returns:
        int: Новый уникальный идентификатор.
    """
    if not tasks:
        return 1
    else:
        # Находим максимальный id в существующих задачах и увеличиваем его на 1
        max_id = max(task.id for task in tasks)
        return max_id + 1

def add_task(title, description):
    """
    Добавляет новую задачу с заданными заголовком и описанием.
    Новый объект Task создается со статусом "todo".

    Args:
        title (str): Заголовок новой задачи.
        description (str): Описание новой задачи.

    Returns:
        Task: Объект добавленной задачи.
    """
    # Загружаем текущий список задач
    tasks = load_tasks()
    # Генерируем новый уникальный идентификатор для задачи
    new_id = get_new_task_id(tasks)
    # Создаем новый объект Task
    new_task = Task(new_id, title, description, status="todo")
    # Добавляем задачу в список
    tasks.append(new_task)
    # Сохраняем обновленный список задач
    save_tasks(tasks)
    return new_task

def update_task(task_id, title, description):
    """
    Обновляет заголовок и описание существующей задачи по заданному id.

    Args:
        task_id (int): Идентификатор задачи, которую необходимо обновить.
        title (str): Новый заголовок.
        description (str): Новое описание.

    Returns:
        bool: True, если задача обновлена успешно, иначе False.
    """
    tasks = load_tasks()
    updated = False
    # Перебираем список задач для поиска нужной по id
    for task in tasks:
        if task.id == task_id:
            task.title = title            # Обновляем заголовок
            task.description = description  # Обновляем описание
            updated = True
            break  # Прерываем цикл, т.к. задача найдена
    if updated:
        # Сохраняем изменения в файл
        save_tasks(tasks)
        return True
    else:
        return False

def delete_task(task_id):
    """
    Удаляет задачу по заданному id.

    Args:
        task_id (int): Идентификатор удаляемой задачи.

    Returns:
        bool: True, если задача найдена и удалена, иначе False.
    """
    tasks = load_tasks()
    # Фильтруем список, исключая задачу с указанным id
    updated_tasks = [task for task in tasks if task.id != task_id]
    if len(updated_tasks) == len(tasks):
        # Если ни одна задача не удалена, то задача не найдена
        return False
    else:
        # Сохраняем новый список задач
        save_tasks(updated_tasks)
        return True

def mark_task(task_id, new_status):
    """
    Изменяет статус задачи на новый.

    Args:
        task_id (int): Идентификатор задачи.
        new_status (str): Новый статус. Должен быть одним из "todo", "in_progress", "done".

    Returns:
        bool: True, если задача найдена и статус изменен, иначе False.
    """
    tasks = load_tasks()
    updated = False
    # Ищем задачу по id и меняем ее статус
    for task in tasks:
        if task.id == task_id:
            task.status = new_status  # Изменяем статус
            updated = True
            break
    if updated:
        # Сохраняем изменения после обновления статуса
        save_tasks(tasks)
        return True
    else:
        return False

def list_tasks(filter_by="all"):
    """
    Возвращает список задач на основе указанного фильтра.

    Args:
        filter_by (str): Фильтр для задач.
                         "all" - все задачи,
                         "done" - только выполненные задачи (status == "done"),
                         "not_done" - задачи, которые не выполнены (status != "done"),
                         "in_progress" - задачи, находящиеся в процессе выполнения (status == "in_progress").

    Returns:
        list[Task]: Отфильтрованный список задач.
    """
    tasks = load_tasks()
    if filter_by == "all":
        return tasks
    elif filter_by == "done":
        return [task for task in tasks if task.status == "done"]
    elif filter_by == "not_done":
        # Возвращаем задачи, у которых статус не равен "done"
        return [task for task in tasks if task.status != "done"]
    elif filter_by == "in_progress":
        return [task for task in tasks if task.status == "in_progress"]
    else:
        # Если указан неизвестный фильтр – возвращаем все задачи
        return tasks
