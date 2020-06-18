#!/usr/bin/env python

from pick import pick
from playbooks import start_auto_fire_essence


def main():
    options = ['Auto Fire Essence']
    selection, _ = pick(options, "Playbooks:", indicator='->')

    if selection == 'Auto Fire Essence':
        start_auto_fire_essence()


if __name__ == '__main__':
    main()
