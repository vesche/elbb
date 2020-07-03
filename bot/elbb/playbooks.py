"""elbb.playbooks"""

import time
import random

from elbb import engine
from elbb.queue import log
from elbb.resources import Items, UI

HUNGRY = False


def start_auto_fire_essence():
    """
    Automatic fire essence creation in any storage.
    """

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
        engine.select_logo()

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
    """
    Automatic book reading in the secret library.
    """

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
    """
    Automatic login from client launch.
    """

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


def auto_sulfur():
    # TODO: go to VotD storage & equip leather gloves first

    while True:
        engine.close_everything()
        log('Heading to crystal cavern!')
        engine.go_to_crystal_cave_sulfur()

        # setup camera to harvest sulfur
        engine.zoom_in(n=30)
        engine.pan_up(n=10)
        engine.zoom_out(n=2)
        engine.point_south()
        engine.point_north()

        while True:
            # reset harvesting
            engine.select_use()
            engine.move_mouse(150, 150)
            engine.click()

            # engine.click_sulfur()
            # TODO: do rando
            engine.select_walk()
            engine.move_mouse(818, 618)

            # click strats
            engine.click()
            time.sleep(.5)
            engine.click()

            # pause to harvest
            log('Harvesting...')
            time.sleep(90)

            # ensure we didn't teleport
            engine.click_on_map(524, 172)
            # wait to move back to harvest spot
            time.sleep(3)

            # sit down if moved
            if not engine.locate(UI.Generic.Stand):
                engine.select_sit()

            # break if overweighted
            if engine.get_load_status() < 4:
                break

        log('Overweighted... Going to storage!')
        engine.go_to_valley_of_the_dwarves_storage()
        engine.sto_items([Items.Sulfur])
        log('Stored sulfur!')


def noop():
    pass


manifest = {
    'noop': noop,
    'auto_fire_essence': start_auto_fire_essence,
    'auto_login': auto_login,
    'auto_read': auto_read,
    'auto_sulfur': auto_sulfur
}
