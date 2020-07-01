"""elbb.engine"""

import os
import time
import numpy
import scipy
import random
import pyautogui
import threading
import pytesseract

from scipy import interpolate

from elbb.queue import log
from elbb.resources import UI

pyautogui.FAILSAFE = False
COOLDOWNS = dict()


def launch_client():
    game_client = os.environ['GAMECLIENT']
    if not os.popen(f'pgrep -f {game_client}').read():
        os.system(f'{game_client} &')


def locate(image):
    location = pyautogui.locateOnScreen(
        image.path,
        grayscale=True
    )
    return location


def randomize(location):
    x = random.randint(location.left, location.left + location.width)
    y = random.randint(location.top, location.top + location.height)
    return (x, y)


def move_mouse(x_dest, y_dest):
    """
    Semi-natural mouse movement using Bézier curves
    https://stackoverflow.com/a/44666798
    """

    x_curr, y_curr = pyautogui.position()

    control = random.randint(3, 5)
    x = numpy.linspace(x_curr, x_dest, num=control, dtype='int')
    y = numpy.linspace(y_curr, y_dest, num=control, dtype='int')

    R = 10
    x_rand = scipy.random.randint(-R, R, size=control)
    y_rand = scipy.random.randint(-R, R, size=control)

    x_rand[0] = y_rand[0] = x_rand[-1] = y_rand[-1] = 0
    x += x_rand
    y += y_rand

    degree = 3 if control > 3 else control - 1
    tck, u = interpolate.splprep([x, y], k=degree)
    u = numpy.linspace(0, 1, num=1920)

    points = interpolate.splev(u, tck)
    duration = 0.2
    timeout = duration / len(points[0])

    for point in zip(*(i.astype(int) for i in points)):
        pyautogui.platformModule._moveTo(*point)
        time.sleep(timeout)


def get_delta(x, y):
    x_curr, y_curr = pyautogui.position()
    return x_curr + x, y_curr + y


def click(n=1):
    for _ in range(n):
        pyautogui.click()
        time.sleep(random.uniform(0.05, 0.3))


def move_to(image):
    location = locate(image)
    if not location:
        return False
    x, y = randomize(location)
    move_mouse(x, y)
    return True


def click_in_region(x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    rx, ry = random.randint(0, dx), random.randint(0, dy)
    pyautogui.moveTo(x1+rx+128, y1+ry+128)
    click(n=2)


def select_walk():
    click_in_region(1, 737, 29, 766)


def select_sit():
    click_in_region(33, 737, 61, 766)


def select_look():
    click_in_region(65, 737, 93, 766)


def select_use():
    click_in_region(97, 737, 125, 766)


def select_fist():
    click_in_region(129, 737, 157, 766)


def select_trade():
    click_in_region(161, 737, 189, 766)


def select_combat():
    click_in_region(193, 737, 221, 766)


def select_inventory():
    click_in_region(225, 737, 253, 766)


def select_spells():
    click_in_region(257, 737, 285, 766)


def select_manufacture():
    click_in_region(289, 737, 317, 766)


def select_emotes():
    click_in_region(321, 737, 349, 766)


def select_quest_log():
    click_in_region(353, 737, 381, 766)


def select_map():
    click_in_region(385, 737, 413, 766)


def select_notepad():
    click_in_region(417, 737, 445, 766)


def select_buddy():
    click_in_region(449, 737, 477, 766)


def select_map():
    click_in_region(481, 737, 509, 766)


def select_stats():
    click_in_region(513, 737, 541, 766)


def select_console():
    click_in_region(545, 737, 573, 766)


def select_help():
    click_in_region(577, 737, 605, 766)


def select_ranging():
    click_in_region(609, 737, 637, 766)


def select_minimap():
    click_in_region(641, 737, 669, 766)


def select_options():
    click_in_region(673, 737, 701, 766)


def select_book_status():
    click_in_region(963, 605, 1021, 616)


def select_item_1():
    click_in_region(995, 67, 1020, 92)


def select_item_2():
    click_in_region(995, 97, 1020, 122)


def select_item_3():
    click_in_region(995, 127, 1020, 152)


def select_item_4():
    click_in_region(995, 157, 1020, 182)


def select_item_5():
    click_in_region(995, 187, 1020, 212)


def select_item_6():
    click_in_region(995, 217, 1020, 242)


def select_logo():
    click_in_region(968, 4, 1020, 60)


def write(text):
    pyautogui.write(text)


def move_inventory_to_storage(item, n=1):
    log(f'Moving {item.__name__} from inventory to storage...')

    select_walk()

    # click the item in the inventory
    success = move_to(item.Inventory)
    if not success:
        log(f'Could not find {item.__name__} in the inventory!', category='bad')
        return False
    click()

    # move the item to the storage
    storage_location = locate(UI.Storage.Banner)
    x_sto, y_sto = randomize(storage_location)
    rx, ry = random.randint(50, 100), random.randint(50, 100)
    move_mouse(x_sto+rx, y_sto+ry)
    click(n)
    pyautogui.click(button='right')

    log(f'{item.__name__} moved to storage.', category='good')
    return True


def move_storage_to_inventory(item, n=1):
    log(f'Moving {item.__name__} from storage to inventory...')

    select_walk()

    # click the correct storage menu for the item
    success = move_to(item.storage_menu)
    if success:
        click()

    # click the item in the storage
    success = move_to(item.Storage)
    if not success:
        log(f'Could not find {item.__name__} in the storage!', category='bad')
        return False
    # small sleep here to reduce misclicking
    time.sleep(random.uniform(0.1, 0.2))
    click()

    # move the item to the inventory
    inventory_location = locate(UI.Inventory.Banner)
    x_inv, y_inv = randomize(inventory_location)
    rx, ry = random.randint(0, 10), random.randint(50, 100)
    move_mouse(x_inv+rx, y_inv+ry)
    click(n)
    pyautogui.click(button='right')

    log(f'{item.__name__} moved to inventory.', category='good')
    return True


def run_cooldown(name, seconds):
    COOLDOWNS[name] = seconds
    for _ in range(seconds):
        time.sleep(1)
        COOLDOWNS[name] -= 1
    COOLDOWNS.pop(name)


def start_cooldown(name, seconds):
    t = threading.Thread(
        target=run_cooldown,
        kwargs={'name': name, 'seconds': seconds}
    )
    t.daemon = True
    t.start()


def eat(food, storage_mode=False):
    can_eat = False

    if locate(food.Inventory):
        can_eat = True
    elif storage_mode:
        success = move_storage_to_inventory(food, n=1)
        if success:
            can_eat = True
        else:
            return False

    if can_eat:
        select_use()
        move_to(food.Inventory)
        click()
        start_cooldown(food.__name__, food.cooldown)
        log(f'Ate {food.__name__}.', category='good')
    else:
        return False


def toggle_console():
    pyautogui.press('f1')


def ocr(x, y, dx, dy):
    ss = pyautogui.screenshot(region=(x, y, dx, dy))
    return pytesseract.image_to_string(ss)


def get_manufacture_status():
    m_location = locate(UI.Manufacture.Banner)
    m_text = ocr(m_location.left-159, m_location.top+115, 255, 16)
    log(f'Got manufacture status: {m_text}')
    return m_text


def get_inventory_text():
    log('Scanning inventory...')

    select_look()

    inventory = list()
    inventory_location = locate(UI.Inventory.Banner)
    init_x = x = inventory_location.left - 150
    y = inventory_location.top + 45

    for i in range(36):
        move_mouse(x, y)
        click()

        text = ocr(inventory_location.left-175, inventory_location.top+325, 450, 100)
        inventory.append({
            'text': text,
            'location': (x, y)
        })

        # TODO: Fix this later? (breaks on duplicate item)
        if i != 0:
            if inventory[i]['text'] == inventory[i-1]['text']:
                break

        if (i+1) % 6 == 0:
            x = init_x
            y += 50
        else:
            x += 50

    log('Finished scanning inventory.', category='good')
    return inventory


def get_book_status():
    move_mouse(992+128, 610+128)
    click()
    text = ocr(4+128, 24+128, 353, 17)
    log(f'Got book status: {text}')
    return text