"""Функція для провідника"""
import os
import json


def file_explorer_function(way, user_id):
    """
    Файловий провідник

    :param way: Шлях у файловій системі
    :param user_id: ID користувача
    :return: Повідомлення яке має надіслати бот
    """
    global message
    if way == "back":
        with open("data.json", "w") as new_data:
            json.dump({user_id: "C:/"}, new_data)
        return "Бекап зроблений!"
    elif way == "view":
        try:
            with open("data.json", "r") as data:
                data = json.load(data)
            files = '\n'.join(os.listdir(data[user_id]))
            message = f'<{data[user_id]}>\n' \
                      f'{files}'
        except FileNotFoundError:
            message = "Файл data.json не знайдений"
        finally:
            return message
    else:
        try:
            with open("data.json", "r") as data:
                data = json.load(data)
            way += "/"
            data[user_id] += way
        except FileNotFoundError:
            return "Файл data.json не знайдений"
        try:
            files = os.listdir(data[user_id])
            files = "\n".join(files)
            with open("data.json", "w") as new_data:
                json.dump(data, new_data)
            message = f"<{data[user_id]}>\n" \
                      f"{files}"
            return message
        except FileNotFoundError:
            return f'Сталась помилка!\n<{data[user_id]}>'
