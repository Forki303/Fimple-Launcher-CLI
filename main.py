import os
import sys
import subprocess
import minecraft_launcher_lib


MINECRAFT_DIR = os.path.join(os.getcwd(), ".minecraft")
CURRENT_USER = "Player"
SELECTED_VERSION = None


def get_version(version_id):
    global SELECTED_VERSION
    print(f"[*] Синхронизация данных для версии {version_id}...")


    def set_status(status):
        print(f"    [Статус]: {status}")

    def set_progress(max_val):
        pass

    def set_max(max_val):
        pass

    callback = {
        "setStatus_text": set_status,
        "setProgress_value": set_progress,
        "setMax_value": set_max
    }

    try:
        minecraft_launcher_lib.install.install_minecraft_version(
            version=version_id,
            minecraft_directory=MINECRAFT_DIR,
            callback=callback
        )
        SELECTED_VERSION = version_id
        print(f"[+] Версия {version_id} успешно установлена и выбрана.")
    except Exception as e:
        print(f"[-] Ошибка при установке версии: {e}")
def set_user(username):
    global CURRENT_USER
    if not username.strip():
        print("[-] Никнейм не может быть пустым.")
        return
    CURRENT_USER = username.strip()
    print(f"[+] Установлен никнейм: {CURRENT_USER}")


def launch_game(version_id):
    version_dir = os.path.join(MINECRAFT_DIR, "versions", version_id)

    if not os.path.isdir(version_dir):
        print(f"[-] Версия {version_id} не найдена локально в {version_dir}.")
        print(f"[-] Сначала выполните /:get-version {version_id}")
        return

    print(f"[*] Подготовка к запуску {version_id} от имени {CURRENT_USER}...")

    options = {
        "username": CURRENT_USER,
        "uuid": "00000000-0000-0000-0000-000000000000",
        "token": "0",
        "launcherName": "CustomPythonLauncher",
        "launcherVersion": "1.0"
    }

    try:
        minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(
            version=version_id,
            minecraft_directory=MINECRAFT_DIR,
            options=options
        )

        print("[+] Запуск процесса игры. Консоль лаунчера временно заблокирована до закрытия игры.")
        subprocess.run(minecraft_command, check=True)
        print("[+] Игра успешно закрыта.")
    except FileNotFoundError:
        print("[-] Ошибка: Java не найдена в PATH вашей системы. Установите Java и добавьте её в переменные среды.")
    except Exception as e:
        print(f"[-] Критическая ошибка при работе игры или генерации команды: {e}")


def list_versions():
    print("[*] Сканирование локальной директории на наличие установленных версий...")
    try:
        installed_versions = minecraft_launcher_lib.utils.get_installed_versions(MINECRAFT_DIR)

        if not installed_versions:
            print("[-] Локально установленные версии не найдены. Используйте /:get-version <версия> для загрузки.")
            return

        print("\nУстановленные локально версии:")
        for v in installed_versions:
            version_id = v.get("id")
            version_type = v.get("type", "unknown")
            print(f"  - {version_id} ({version_type})")
        print(f"Всего обнаружено версий: {len(installed_versions)}\n")

    except Exception as e:
        print(f"[-] Не удалось прочитать список локальных версий: {e}")



def main():
    print("=== Fimple Launcher CLI ===")
    print(f"Директория игры: {MINECRAFT_DIR}")
    print(f"Текущий пользователь: {CURRENT_USER}")
    print("Доступные команды: /:get-version, /:set-user, /:launch, /:list, /:exit\n")

    while True:
        try:
            user_input = input(f"[{CURRENT_USER}] > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nЗавершение работы.")
            break

        if not user_input:
            continue

        parts = user_input.split(maxsplit=1)
        command = parts[0]
        arg = parts[1] if len(parts) > 1 else ""

        if command == "/:get-version":
            if not arg:
                print("[-] Использование: /:get-version <версия>")
            else:
                get_version(arg)

        elif command == "/:set-user":
            if not arg:
                print("[-] Использование: /:set-user <ник>")
            else:
                set_user(arg)

        elif command == "/:launch":
            if not arg:
                if SELECTED_VERSION:
                    launch_game(SELECTED_VERSION)
                else:
                    print("[-] Укажите версию или установите её через /:get-version")
            else:
                launch_game(arg)

        elif command == "/:list":
            list_versions()

        elif command == "/:exit":
            print("[*] Выход из лаунчера.")
            sys.exit(0)

        else:
            print(f"[-] Неизвестная команда: {command}. Доступные: /:get-version, /:set-user, /:launch, /:list")


if __name__ == "__main__":
    main()
