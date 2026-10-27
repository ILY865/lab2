from src.main.database.database import init_db
from src.main.ui.auth_ui import login_screen, register_screen
from src.main.ui.menus import client_menu, manager_menu

def main():
    # Подготавливаем базу данных (создастся, если её нет)
    init_db()

    while True:
        print("\n==============================")
        print(" СИСТЕМА УЧЁТА ПУТЁВОК")
        print("==============================")
        print("1. Вход")
        print("2. Регистрация")
        print("0. Выход")
        
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            user = login_screen()
            if user:
                # Проверяем роль: 1 - клиент, 2 - менеджер
                if user.role_id == 2:
                    manager_menu(user)
                else:
                    client_menu(user)
        elif choice == "2":
            register_screen()
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный пункт меню.")

if __name__ == "__main__":
    main()