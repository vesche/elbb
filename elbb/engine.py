"""elbb.engine"""

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

COOLDOWNS = dict()


def locate(image):
    location = pyautogui.locateOnScreen(
        image.path,
        region=(1920, 40, 1920, 1040),
        # region=(0, 40, 1920, 1040),
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

    log(f'{item.__name__} moved to storage.', category='good')
    return True


def create_cooldown(name, seconds):
    COOLDOWNS[name] = seconds
    for _ in range(seconds):
        time.sleep(1)
        seconds -= 1
    COOLDOWNS.pop(name)


def start_cooldown(name, seconds):
    t = threading.Thread(
        target=create_cooldown,
        kwargs={'name': name, 'seconds': seconds}
    )
    t.daemon = True
    t.start()


def select_use():
    if locate(UI.Use.Unselected):
        move_to(UI.Use.Unselected)
        click()


def select_walk():
    if locate(UI.Walk.Unselected):
        move_to(UI.Walk.Unselected)
        click()


def select_look():
    if locate(UI.Look.Unselected):
        move_to(UI.Look.Unselected)
        click()


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
    m_text = ocr(m_location.left-245, m_location.top+175, 600, 85)
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
    cd_location = locate(UI.Countdown.Marker)
    move_mouse(cd_location.left + random.randint(20, 80), cd_location.top + 38)
    click()

    toggle_console()
    cm_location = locate(UI.Console.Marker)
    text = ocr(cm_location.left, cm_location.top-72, 1776, 30)
    toggle_console()

    move_to(UI.Logo.Marker)

    log(f'Got book status: {text}')
    return text
