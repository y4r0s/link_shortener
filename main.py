import sys
from shortener import URLShortener


def print_menu():
    """Выводит в консоль главное меню приложения."""
    print("\n" + "=" * 35)
    print("🚀 CLI СОКРАЩАТЕЛЬ ССЫЛОК 🚀")
    print("=" * 35)
    print("1. Создать короткую ссылку")
    print("2. Перейти по короткой ссылке")
    print("3. Посмотреть статистику")
    print("4. Выйти из программы")
    print("=" * 35)


def main():
    print("Запуск сервиса...")
    try:
        capacity = int(input("Задайте лимит хранения ссылок (например, 5): "))
        if capacity <= 0:
            raise ValueError
    except ValueError:
        print("Некорректный ввод. Установлен лимит по умолчанию: 5")
        capacity = 5

    app = URLShortener(capacity=capacity)

    while True:
        print_menu()
        choice = input("Ваш выбор (1-4): ").strip()

        if choice == '1':
            url = input("Введите длинный URL: ").strip()
            if url:
                code = app.shorten(url)
                print(f"✅ Успешно! Ваша ссылка: http://cl.ck/{code}")
            else:
                print("❌ Ошибка: URL не может быть пустым.")


        elif choice == '2':

            short = input("Введите короткую ссылку (или ее код): ").strip()

            original = app.get_original(short)

            if original == "URL not found":

                print("❌ Ссылка не найдена (возможно, вытеснена из памяти).")

            else:

                print(f"🔄 Перенаправление на -> {original}")


                import webbrowser

                if original.startswith("http"):

                    webbrowser.open(original)

                else:

                    webbrowser.open(f"https://{original}")



        elif choice == '3':
            print("\n📊 Статистика использования:")
            print(f"Занято в памяти: {len(app.short_to_long)} из {app.capacity}")
            for code, data in app.stats.items():
                print(f" - [http://cl.ck/{code}] переходов: {data['clicks']}")

        elif choice == '4':
            print("Завершение работы. Удачи на экзамене!")
            sys.exit(0)
        else:
            print("❌ Неизвестная команда. Попробуйте снова.")


if __name__ == "__main__":
    main()