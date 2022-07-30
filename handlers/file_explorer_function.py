import os
import json


def file_explorer_function(way, user_id):
    if way == "@back":
        with open("data.json", "w") as new_data:
            json.dump({user_id: "C:/"}, new_data)
        return "Бекап зроблений!"
    elif way == "@view":
        try:
            with open("data.json", "r") as data:
                data = json.load(data)
            files = '\n'.join(os.listdir(data[user_id]))
            message = f"<{data[user_id]}>\n" \
                      f"{files}"
        except:
            message = "Сталась помилка"
        finally:
            return message
    else:
        with open("data.json", "r") as data:
            data = json.load(data)
        way += "/"
        data[user_id] += way
        try:
            files = os.listdir(data[user_id])
            files = "\n".join(files)
            with open("data.json", "w") as new_data:
                json.dump(data, new_data)
            message = f"<{data[user_id]}>\n" \
                      f"{files}"
            return message
        except:
            return f'Сталась помилка!\n<{data[user_id]}>'
