"""elbb.resources"""

import os

pwd = os.path.abspath(os.path.dirname(__file__))

def resolve(image):
    return os.path.join(pwd, f'images/{image}')


class UI:
    """
    UI Resources
    """

    class Console:
        class Marker:
            path = resolve('console_marker.png')

    class Countdown:
        class Marker:
            path = resolve('countdown_marker.png')

    class Food:
        class NegativeA:
            path = resolve('food_negative_a.png')
        class NegativeB:
            path = resolve('food_negative_b.png')

    class Inventory:
        class Banner:
            path = resolve('inventory_banner.png')

    class Logo:
        class Marker:
            path = resolve('logo_marker.png')

    class Look:
        class Unselected:
            path = resolve('look_unselected.png')

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

    class Use:
        class Selected:
            path = None
        class Unselected:
            path = resolve('use_unselected.png')

    class Walk:
        class Selected:
            path = None
        class Unselected:
            path = resolve('walk_unselected.png')


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
            path = resolve('rose_inventory.png')
        class Storage:
            path = resolve('rose_storage.png')

    class RedSnapdragons:
        storage_menu = UI.Storage.Flowers
        class Inventory:
            path = resolve('snapdragon_inventory.png')
        class Storage:
            path = resolve('snapdragon_storage.png')

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
