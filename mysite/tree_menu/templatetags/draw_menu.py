from typing import Dict, Any, List
from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.template import Context
from ..models import MenuItem

register = template.Library()

@register.inclusion_tag('tree_menu/tree_menu.html', takes_context=True)
def draw_menu(context: Context, menu: str) -> Dict[str, Any]:
    """
    Функция, для отрисовки меню
    :return: Словарь, который будет обрабатываться в tree_menu.html шаблоне.
    """

    try:
        # Получаем все элементы меню для данного меню
        items = MenuItem.objects.filter(menu__title=menu)
        items_values = items.values()

        # Получаем вложенные элементы меню без родителя
        root_item = [item for item in items_values.filter(parent=None)]

        # Определяем ID запрашиваемого элемента меню
        selected_item_id = int(context['request'].GET[menu])
        selected_item = items.get(id=selected_item_id)

        # Получаем список IDs для выбранного элемента меню
        selected_item_id_list = get_nested_id_list(selected_item, root_item, selected_item_id)

        # Добавляем вложенные элементы для запрашиваемого элемента меню
        for item in root_item:
            if item['id'] in selected_item_id_list:
                item['child_items'] = get_child_list(items_values, item['id'], selected_item_id_list)

        result_dict = {'items': root_item}

    except (KeyError, ObjectDoesNotExist):
        result_dict = {
            'items': [
                item for item in MenuItem.objects.filter(menu__title=menu, parent=None).values()
            ]
        }

    # Добавляем имя и queryset в словарь
    result_dict['menu'] = menu
    result_dict['other_querystring'] = build_qs(context, menu)

    return result_dict


def build_qs(context: Context, menu: str) -> str:

    items = []

    for key in context['request'].GET:
        if key != menu:
            items.append(f"{key}={context['request'].GET[key]}")

    querystring = '&'.join(items)

    return querystring


def get_child_list(items_values, current_item_id, selected_item_id_list):
    """
    Функция возвращает список вложенных элементов для выбранного элемента меню
    """
    item_list = [item for item in items_values.filter(parent_id=current_item_id)]
    for item in item_list:
        if item['id'] in selected_item_id_list:
            item['child_items'] = get_child_list(items_values, item['id'], selected_item_id_list)
    return item_list


def get_nested_id_list(parent: MenuItem, primary_item: List[MenuItem], selected_item_id: int) -> List[int]:
    """
    Функция возвращает список IDs для выбранного элемента меню, от начального родителя до текущего элемента.
    """
    selected_item_id_list = []

    while parent:
        selected_item_id_list.append(parent.id)
        parent = parent.parent
    if not selected_item_id_list:
        for item in primary_item:
            if item.id == selected_item_id:
                selected_item_id_list.append(selected_item_id)
    return selected_item_id_list
