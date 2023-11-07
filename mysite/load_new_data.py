import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tree.settings')

import django

django.setup()

from tree_menu.models import Menu, MenuItem


def load_data():
    # Удаляем существующее меню "main_menu"
    Menu.objects.filter(title="main_menu").delete()

    # Создаем меню "main_menu"
    main_menu = Menu.objects.create(title="main_menu", slug="main_menu")

    # Создаем корневой объект "Склад"
    store = MenuItem.objects.create(title="Склад", slug="store", menu=main_menu)

    # Создаем объекты 2-го уровня
    candies = MenuItem.objects.create(title="Конфеты", slug="candies", menu=main_menu, parent=store)
    cookies = MenuItem.objects.create(title="Печенье", slug="cookies", menu=main_menu, parent=store)
    caramel = MenuItem.objects.create(title="Карамель", slug="caramel", menu=main_menu, parent=store)


    # Списки названий
    candies_list = ["Белочка", "Кара-кум", "Красная шапочка", "Трюфель", "Ассорти", "Особый"]
    cookies_list = ["Шоколадное", "Овсяное", "Сливочное", "Калорийное"]
    caramel_list = ["Апельсиновая", "Лимонная", "Мятная", "Барбарис", "Дюшес"]

    # Создаем объекты 3-го уровня
    for item in candies_list:
        MenuItem.objects.create(title=item, slug=item.lower(), parent=candies, menu=main_menu)

    for item in cookies_list:
        MenuItem.objects.create(title=item, slug=item.lower(), parent=cookies, menu=main_menu)

    for item in caramel_list:
        MenuItem.objects.create(title=item, slug=item.lower(), parent=caramel, menu=main_menu)

    # Создаем объекты 4-го уровня
    weight = [1, 5, 10]
    for item in candies_list + cookies_list + caramel_list:
        p_item = MenuItem.objects.get(title=item)

        for w in weight:
            timeframe_item = MenuItem.objects.create(title=f"{item}_{w}", slug=f"{item.lower()}_{w}",
                                                     parent=p_item, menu=main_menu)

if __name__ == "__main__":
    print("Loading data...")
    load_data()
    print("Store menu successfully loaded")
