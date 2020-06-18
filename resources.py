
class UI:
    """
    UI Resources
    """

    class Inventory:
        class Banner:
            path = 'images/inventory_banner.png'

    class Manufacture:
        class Banner:
            path = 'images/manufacture_banner.png'
        class MixAll:
            path = 'images/manufacture_mix_all.png'

    class Storage:
        class Banner:
            path = 'images/storage_banner.png'
        class Flowers:
            path = 'images/storage_flowers.png'
        class Food:
            path = 'images/storage_food.png'
        class Minerals:
            path = 'images/storage_minerals.png'

    class Use:
        class Selected:
            path = None
        class Unselected:
            path = 'images/use_unselected.png'

    class Walk:
        class Selected:
            path = None
        class Unselected:
            path = 'images/walk_unselected.png'


class Items:
    """
    Item Resources
    """

    class FireEssence:
        storage_menu = None
        class Inventory:
            path = 'images/fire_essence_inventory.png'
        class Storage:
            path = None

    class RedRose:
        storage_menu = UI.Storage.Flowers
        class Inventory:
            path = 'images/rose_inventory.png'
        class Storage:
            path = 'images/rose_storage.png'

    class RedSnapdragons:
        storage_menu = UI.Storage.Flowers
        class Inventory:
            path = 'images/snapdragon_inventory.png'
        class Storage:
            path = 'images/snapdragon_storage.png'

    class Sulfur:
        storage_menu = UI.Storage.Minerals
        class Inventory:
            path = 'images/sulfur_inventory.png'
        class Storage:
            path = 'images/sulfur_storage.png'

    class Vegetables:
        cooldown = 50
        storage_menu = UI.Storage.Food
        class Inventory:
            path = 'images/vegetables_inventory.png'
        class Storage:
            path = 'images/vegetables_storage.png'
