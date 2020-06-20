"""elbb.queue"""

from filelock import FileLock

LOCK_FILE = '/tmp/elbb_queue.lock'
QUEUE_FILE = '/tmp/elbb_queue.log'
CATEGORIES = {
    'alert': '[!]',
    'bad':   '[-]',
    'good':  '[+]',
    'info':  '[~]',
}

# init
open(LOCK_FILE, 'w').close()
open(QUEUE_FILE, 'w').close()


class CategoryNotFound(Exception):
    pass


def _acquire_lock():
    return FileLock(LOCK_FILE)


def get_queue():
    with _acquire_lock():
        return open(QUEUE_FILE, 'r').read()


def clear_queue():
    with _acquire_lock():
        open(QUEUE_FILE, 'w')


def log(message, category='info'):
    message = message.replace('\n', ' ')

    if category not in CATEGORIES:
        raise CategoryNotFound('{category} is not a valid category.')

    with _acquire_lock():
        open(QUEUE_FILE, 'a').write(
            f'{CATEGORIES[category]} {message}\n'
        )
