#!/usr/bin/env python

from pick import pick
from playbooks import start_auto_fire_essence, auto_read


def main():
    options = ['Auto Fire Essence', 'Auto Read']
    selection, _ = pick(options, "Playbooks:", indicator='->')

    if selection == 'Auto Fire Essence':
        start_auto_fire_essence()
    elif selection == 'Auto Read':
        auto_read()


if __name__ == '__main__':
    main()
