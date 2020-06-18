import time
import numpy
import scipy
import random
import pyautogui
import threading
import pytesseract

from scipy import interpolate
from resources import Items, UI

COOLDOWNS = dict()


def locate(image):
    location = pyautogui.locateOnScreen(
        image.path,
        region=(1920, 40, 1920, 1040),
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
    select_walk()

    # click the item in the inventory
    success = move_to(item)
    if not success:
        return False
    click()

    # move the item to the storage
    storage_location = locate(UI.Storage.Banner)
    x_sto, y_sto = randomize(storage_location)
    rx, ry = random.randint(50, 100), random.randint(50, 100)
    move_mouse(x_sto+rx, y_sto+ry)
    click(n)
    pyautogui.click(button='right')
    return True


def move_storage_to_inventory(item, n=1):
    select_walk()

    # click the correct storage menu for the item
    success = move_to(item.storage_menu)
    if success:
        click()

    # click the item in the storage
    success = move_to(item.Storage)
    if not success:
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
    return True


def create_cooldown(name, seconds):
    COOLDOWNS[name] = seconds
    for _ in range(50):
        time.sleep(1)
        COOLDOWNS[name] -= 1
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
        start_cooldown(type(food).__name__, food.cooldown)
    else:
        return False


def get_manufacture_status():
    m_location = locate(UI.Manufacture.Banner)
    x = m_location.left - 245
    y = m_location.top + 175
    ss = numpy.array(pyautogui.screenshot(region=(x, y, 600, 85)))
    return pytesseract.image_to_string(ss)
