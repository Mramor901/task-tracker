"""
Модуль main.py
--------------
Точка входа в приложение. Если программа запущена без аргументов – запускается интерактивный режим,
где пользователь через меню может добавлять, обновлять, удалять, изменять статус задач и просматривать списки.
Если же переданы аргументы командной строки, то используется стандартный CLI через argparse.
"""

import sys
import argparse
from operations import add_task, update_task, delete_task, mark_task, list_tasks


def interactive_mode():
    """
    Интерактивный режим работы Task Tracker. Пользователю показывается меню с возможными действиями.
    Программа ждёт ввода команды и выполняет соответствующие функции.
    """
    print("Запускается интерактивный режим Task Tracker CLI")
    print("-------------------------------------------------")
    while True:
        print("\nВыберите действие:")
        print("1. Добавить задачу")
        print("2. Обновить задачу")
        print("3. Удалить задачу")
        print("4. Изменить статус задачи")
        print("5. Показать список задач")
        print("6. Выход")

        choice = input("Введите номер действия: ").strip()

        if choice == "6":
            print("До свидания!")
            break

        elif choice == "1":
            # Добавление новой задачи
            title = input("Введите заголовок задачи: ").strip()
            description = input("Введите описание задачи (можно оставить пустым): ").strip()
            task = add_task(title, description)
            print("Задача добавлена:")
            print(task)

        elif choice == "2":
            # Обновление задачи
            try:
                task_id = int(input("Введите ID задачи для обновления: "))
            except ValueError:
                print("Некорректный ID!")
                continue
            title = input("Введите новый заголовок задачи: ").strip()
            description = input("Введите новое описание задачи (можно оставить пустым): ").strip()
            success = update_task(task_id, title, description)
            if success:
                print("Задача успешно обновлена!")
            else:
                print("Задача с таким ID не найдена.")

        elif choice == "3":
            # Удаление задачи
            try:
                task_id = int(input("Введите ID задачи для удаления: "))
            except ValueError:
                print("Некорректный ID!")
                continue
            success = delete_task(task_id)
            if success:
                print("Задача успешно удалена!")
            else:
                print("Задача с таким ID не найдена.")

        elif choice == "4":
            # Изменение статуса задачи
            try:
                task_id = int(input("Введите ID задачи для изменения статуса: "))
            except ValueError:
                print("Некорректный ID!")
                continue
            print("Выберите новый статус:")
            print("1. todo")
            print("2. in_progress")
            print("3. done")
            status_choice = input("Введите номер статуса: ").strip()
            if status_choice == "1":
                new_status = "todo"
            elif status_choice == "2":
                new_status = "in_progress"
            elif status_choice == "3":
                new_status = "done"
            else:
                print("Некорректный выбор статуса!")
                continue
            success = mark_task(task_id, new_status)
            if success:
                print(f"Статус задачи с ID {task_id} изменён на '{new_status}'.")
            else:
                print("Задача с таким ID не найдена.")

        elif choice == "5":
            # Отображение списка задач с выбором фильтра
            print("Выберите фильтр:")
            print("1. Все задачи")
            print("2. Выполненные задачи (done)")
            print("3. Задачи, не выполненные (not_done)")
            print("4. Задачи в процессе (in_progress)")
            filter_choice = input("Введите номер фильтра: ").strip()
            if filter_choice == "1":
                tasks = list_tasks("all")
            elif filter_choice == "2":
                tasks = list_tasks("done")
            elif filter_choice == "3":
                tasks = list_tasks("not_done")
            elif filter_choice == "4":
                tasks = list_tasks("in_progress")
            else:
                print("Некорректный выбор фильтра!")
                continue

            if tasks:
                print("\nСписок задач:")
                for task in tasks:
                    print(task)
            else:
                print("Нет задач для выбранного фильтра.")

        else:
            print("Некорректный выбор, попробуйте снова.")


def main():
    """
    Основная функция, запускающая программу. Если переданы аргументы командной строки,
    используется режим CLI с argparse. Иначе запускается интерактивный режим.
    """
    if len(sys.argv) == 1:
        # Если аргументы командной строки не указаны, запускаем интерактивный режим.
        interactive_mode()
    else:
        # Режим работы с аргументами командной строки.
        parser = argparse.ArgumentParser(
            description="Task Tracker CLI - приложение для управления задачами через командную строку"
        )

        # Определяем субкоманды для различных операций.
        subparsers = parser.add_subparsers(dest="command", help="Действия, которые можно выполнить")

        # Субкоманда для добавления задачи
        parser_add = subparsers.add_parser("add", help="Добавить новую задачу")
        parser_add.add_argument("title", type=str, help="Заголовок задачи")
        parser_add.add_argument("--description", type=str, default="", help="Описание задачи (опционально)")

        # Субкоманда для обновления задачи
        parser_update = subparsers.add_parser("update", help="Обновить задачу")
        parser_update.add_argument("id", type=int, help="ID задачи для обновления")
        parser_update.add_argument("title", type=str, help="Новый заголовок задачи")
        parser_update.add_argument("--description", type=str, default="", help="Новое описание задачи (опционально)")

        # Субкоманда для удаления задачи
        parser_delete = subparsers.add_parser("delete", help="Удалить задачу")
        parser_delete.add_argument("id", type=int, help="ID задачи для удаления")

        # Субкоманда для изменения статуса задачи
        parser_mark = subparsers.add_parser("mark", help="Изменить статус задачи")
        parser_mark.add_argument("id", type=int, help="ID задачи")
        parser_mark.add_argument("status", type=str, choices=["todo", "in_progress", "done"],
                                 help="Новый статус задачи")

        # Субкоманда для отображения списка задач
        parser_list = subparsers.add_parser("list", help="Показать список задач")
        parser_list.add_argument("--filter", type=str, choices=["all", "done", "not_done", "in_progress"],
                                 default="all",
                                 help="Фильтр для отображения задач: all, done, not_done, in_progress")

        args = parser.parse_args()

        if args.command == "add":
            new_task = add_task(args.title, args.description)
            print("Добавлена задача:")
            print(new_task)

        elif args.command == "update":
            success = update_task(args.id, args.title, args.description)
            if success:
                print(f"Задача с ID {args.id} успешно обновлена.")
            else:
                print(f"Задача с ID {args.id} не найдена.")

        elif args.command == "delete":
            success = delete_task(args.id)
            if success:
                print(f"Задача с ID {args.id} успешно удалена.")
            else:
                print(f"Задача с ID {args.id} не найдена.")

        elif args.command == "mark":
            success = mark_task(args.id, args.status)
            if success:
                print(f"Статус задачи с ID {args.id} изменён на '{args.status}'.")
            else:
                print(f"Задача с ID {args.id} не найдена.")

        elif args.command == "list":
            tasks = list_tasks(filter_by=args.filter)
            if tasks:
                print("Список задач:")
                for task in tasks:
                    print(task)
            else:
                print("Задачи не найдены для заданного фильтра.")
        else:
            parser.print_help()


if __name__ == "__main__":
    main()
