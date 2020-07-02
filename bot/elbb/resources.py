"""elbb.resources"""

import os

from elbb.common import pwd


def resolve(image):
    return os.path.join(pwd, f'images/{image}')


class UI:
    """
    UI Resources
    """

    class Food:
        class NegativeA:
            path = resolve('food_negative_a.png')
        class NegativeB:
            path = resolve('food_negative_b.png')

    class Inventory:
        class Banner:
            path = resolve('inventory_banner.png')

    class Manufacture:
        class Banner:
            path = resolve('manufacture_banner.png')
        class MixAll:
            path = resolve('manufacture_mix_all.png')

    class Storage:
        class Banner:
            path = resolve('storage_banner.png')
        class Flowers:
            path = resolve('storage_flowers.png')
        class Food:
            path = resolve('storage_food.png')
        class Minerals:
            path = resolve('storage_minerals.png')


class Items:
    """
    Item Resources
    """

    class FireEssence:
        storage_menu = None
        class Inventory:
            path = resolve('fire_essence_inventory.png')
        class Storage:
            path = None

    class RedRose:
        storage_menu = UI.Storage.Flowers
        class Inventory:
            path = resolve('red_rose_inventory.png')
        class Storage:
            path = resolve('red_rose_storage.png')

    class RedSnapdragons:
        storage_menu = UI.Storage.Flowers
        class Inventory:
            path = resolve('red_snapdragons_inventory.png')
        class Storage:
            path = resolve('red_snapdragons_storage.png')

    class Sulfur:
        storage_menu = UI.Storage.Minerals
        class Inventory:
            path = resolve('sulfur_inventory.png')
        class Storage:
            path = resolve('sulfur_storage.png')

    class Vegetables:
        cooldown = 50
        storage_menu = UI.Storage.Food
        class Inventory:
            path = resolve('vegetables_inventory.png')
        class Storage:
            path = resolve('vegetables_storage.png')
