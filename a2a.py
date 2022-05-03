from sys import argv as args
from os.path import exists
import json


def download_settings():
    pass


def migrate(from_path: str, to_path: str, cmds: list[str]) -> None:
    """Переносим вкладку в другой файл"""
    # Проверяем на наличие конфигов по указаным путям
    if not exists(from_path) or not exists(to_path):
        print(f"[E] Проверьте пути к конфигам: {from_path}/{to_path}")
        return

    # Проверяем на наличие файла конфигурации
    if not exists("settings.json"):
        print("[W] Скачиваю конфигурацию по умолчанию...")
        download_settings()

    # Получаем сведенья из джсон файлов
    settings: dict = json.load(open("settings.json", "r"))
    from_cfg: dict = json.load(open(from_path))
    to_cfg: dict = json.load(open(to_path))

    # Создаем резервную копию конфига
    if settings["global"]["make-backup"]:
        json.dump(to_cfg, open(to_path + "b", "w"), indent=2)

    # Определяем что нужно сделать
    for cmd in cmds:
        cmd = cmd.lower()
        if cmd == "binds":
            # Переносим все бинды
            for feature in from_cfg["features"]:
                to_cfg["features"][feature]["hotkey"] = from_cfg["features"][feature]["hotkey"]
            print("[I] Все бинды успешно перенесены")
        elif cmd == "macros":
            # Переносим все макросы
            to_cfg["macros"] = from_cfg["macros"]

            print("[I] Все макросы успешно перенесены")
        else:
            # Проверяем на наличие категории
            if not (cmd in settings["features"]):
                print(f"[W] Аргумент {cmd} неизвестен")
                continue

            # Переносим настройки для n категории
            for feature in from_cfg["features"]:
                if not (feature in settings["features"][cmd]):
                    continue

                # Оставляем хоткей
                if settings["global"]["save-binds"]:
                    from_cfg["features"][feature]["hotkey"] = to_cfg["features"][feature]["hotkey"]
                    
                # Устанавливаем настройки
                to_cfg["features"][feature] = from_cfg["features"][feature]
            print(f"[I] Все функции для категории {cmd} перенесены")

    # Сохраняем наш кфг новыми настройками
    json.dump(to_cfg, open(to_path, "w"), indent=2)
    
    print(f"[I] Конфиг {to_path} сохранен")


if __name__ == "__main__":
    if len(args) == 1:
        migrate(input("Исходный кфг: "), input("Новый кфг: "), input("Флаги: ").split(" "))
    elif len(args) < 4:
        print("[E] Нужны аргументы: <путь/до/исходного_кфг.akr> <путь/до/нового_кфг.akr> <флаги>")
    else:
        migrate(args[1], args[2], args[3:])
