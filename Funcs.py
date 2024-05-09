def get_path():
    config_path = "config.txt"
    try:
        with open(config_path, "r") as config_file:
            for line in config_file:
                if line.startswith("catalog="):
                    folder_path = line.split("catalog=")[1].strip()
                    return folder_path
    except FileNotFoundError:
        print("Файл конфигурации не найден")
        return None
