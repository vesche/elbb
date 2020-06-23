"""elbb.playbooks"""

import time
import random

from elbb import engine
from elbb.queue import log
from elbb.resources import Items, UI

HUNGRY = False


def start_auto_fire_essence():
    try:
        while True:
            auto_fire_essence_loop()
    except KeyboardInterrupt:
        pass


def auto_fire_essence_loop():
    # globals needed
    global HUNGRY

    def click_mix_all():
        engine.move_to(UI.Manufacture.MixAll)
        engine.click()
        log('Mixing...', category='good')
        engine.move_to(UI.Logo.Marker)

    # check for any Fire Essence in inventory & move them to storage
    if engine.locate(Items.FireEssence.Inventory):
        engine.move_inventory_to_storage(Items.FireEssence, n=5)

    # check if hungry & eat (taking cooldown into account)
    if HUNGRY:
        if 'Vegetables' in engine.COOLDOWNS:
            seconds = engine.COOLDOWNS['Vegetables']
            log(f'Waiting for cooldown to eat, {seconds} seconds...')
            time.sleep(seconds + 1)
        engine.eat(Items.Vegetables, storage_mode=True)

    HUNGRY = False

    # ensure Red Rose, Red Snapdragons, and Sulfur are in the inventory
    for item in [Items.RedRose, Items.RedSnapdragons, Items.Sulfur]:
        if not engine.locate(item.Inventory):
            engine.move_storage_to_inventory(item, n=4)

    # click "Mix all" button in the Manufacture menu
    click_mix_all()

    while True:
        # check manufacture status every 1/3 of a second
        time.sleep(0.3)
        status = engine.get_manufacture_status()

        if 'hungry' in status:
            log('Food level depleted, re-running automation.')
            HUNGRY = True
            break
        elif 'failed' in status or 'stopped' in status:
            click_mix_all()
        elif 'Nothing' in status:
            log('Inventory empty, re-running automation.')
            break


def auto_read():
    inventory = engine.get_inventory_text()

    while True:
        if engine.locate(UI.Food.NegativeA) or engine.locate(UI.Food.NegativeB):
            engine.eat(Items.Vegetables)

        book_status = engine.get_book_status()

        if 'anything' in book_status:
            log('Book completed!', category='good')
            for i in inventory:
                if 'Book' in i['text']:
                    engine.select_use()
                    engine.move_mouse(*i['location'])
                    engine.click()
                    log(f'Starting to read {i["text"]}.', category='good')
                    inventory.remove(i)
                    break
            else:
                return

        time.sleep(random.randint(45, 75))


def auto_login(username, password):
    # click screen
    engine.move_mouse(258, 147)
    engine.click()

    # enter username
    engine.move_mouse(477+128, 291+128)
    engine.click()
    engine.write(username)

    # enter password
    engine.move_mouse(477+128, 335+128)
    engine.click()
    engine.write(password)

    # hit Log In
    engine.move_mouse(383+128, 384+128)
    engine.click()
