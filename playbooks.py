import time
import random
import engine

from resources import Items, UI

HUNGRY = False


def start_auto_fire_essence():
    try:
        while True:
            auto_fire_essence_loop()
    except KeyboardInterrupt:
        pass


def auto_fire_essence_loop():
    # use hungry toggle for mixing
    global HUNGRY

    # check for any Fire Essence in inventory & move them to storage
    if engine.locate(Items.FireEssence.Inventory):
        engine.move_inventory_to_storage(Items.FireEssence.Inventory, n=5)

    # check if hungry & eat (taking cooldown into account)
    if HUNGRY:
        if 'Vegetables' in engine.COOLDOWNS:
            seconds = engine.COOLDOWNS['Vegetables']
            print(f'In cooldown waiting {seconds} sec')
            time.sleep(seconds + 1)
        engine.eat(Items.Vegetables, storage_mode=True)

    HUNGRY = False

    # ensure Red Rose, Red Snapdragons, and Sulfur are in the inventory
    for item in [Items.RedRose, Items.RedSnapdragons, Items.Sulfur]:
        if not engine.locate(item.Inventory):
            engine.move_storage_to_inventory(item, n=4)

    # click "Mix all" button in the Manufacture menu
    engine.move_to(UI.Manufacture.MixAll)
    engine.click()

    while True:
        # check manufacture status every 1/3 of a second
        time.sleep(0.3)
        status = engine.get_manufacture_status()

        if 'hungry' in status:
            HUNGRY = True
            break
        elif 'failed' in status or 'stopped' in status:
            engine.move_to(UI.Manufacture.MixAll)
            engine.click()
        elif 'Nothing' in status:
            break


def auto_read():
    inventory = engine.get_inventory_text()

    while True:
        if engine.locate(UI.Food.NegativeA) or engine.locate(UI.Food.NegativeB):
            engine.eat(Items.Vegetables)

        book_status = engine.get_book_status()
        print(book_status)

        if 'anything' in book_status:
            for i in inventory:
                if 'Book' in i['text']:
                    engine.select_use()
                    engine.move_mouse(*i['location'])
                    engine.click()
                    inventory.remove(i)
                    break
            else:
                return

        time.sleep(random.randint(100, 300))
