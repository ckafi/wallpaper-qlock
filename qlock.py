#!/usr/bin/env python3

import os
from PIL import Image
from datetime import datetime
from time import sleep

interval = 60
res_before = 2
cache_path = os.path.expanduser('~/.cache/qlock/')

def fuzzy_hour(time):
    translate = {
        1 : 'one',
        2 : 'two',
        3 : 'three',
        4 : 'four',
        5 : 'five_(h)',
        6 : 'six',
        7 : 'seven',
        8 : 'eight',
        9 : 'nine',
        10 : 'ten_(h)',
        11 : 'eleven',
        0 : 'twelve',
    }
    hour = time.hour
    if time.minute + res_before >= 25:
        hour += 1
    hour %= 12
    return translate[hour]


def fuzzy_minute(time):
    minute = time.minute - res_before
    if minute <= 0:
        return ['oclock']
    elif minute <= 5:
        return ['five_(m)', 'past']
    elif minute <= 10:
        return ['ten_(m)', 'past']
    elif minute <= 15:
        return ['quarter', 'past']
    elif minute <= 20:
        return ['twenty', 'past']
    elif minute <= 25:
        return ['five_(m)', 'to','half']
    elif minute <= 30:
        return ['half']
    elif minute <= 35:
        return ['five_(m)','past','half']
    elif minute <= 40:
        return ['twenty', 'to']
    elif minute <= 45:
        return ['quarter', 'to']
    elif minute <= 50:
        return ['ten_(m)', 'to']
    elif minute <= 55:
        return ['five_(m)', 'to']
    else:
        return ['oclock']


def assemble_clock(hour, minute):
    base = Image.open('images/base.png')

    it_is = Image.open('images/it_is.png')
    base.paste(it_is, (0,0), it_is)
    it_is.close()

    hour_fname = 'images/' + hour + '.png'
    hour_image = Image.open(hour_fname)
    base.paste(hour_image, (0,0), hour_image)
    hour_image.close()

    for word in minute:
        fname = 'images/' + word + '.png'
        image = Image.open(fname)
        base.paste(image, (0,0), image)
        image.close()

    base.save(cache_path + '/qlock.png')
    base.close()

def main():
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    if not os.path.exists(cache_path):
        os.makedirs(cache_path)
    old_minute = []
    while True:
        now = datetime.today().time()
        hour = fuzzy_hour(now)
        minute = fuzzy_minute(now)
        if minute != old_minute:
            assemble_clock(hour, minute)
            os.system('setroot --bg-color black ' + cache_path + '/qlock.png')
            old_minute = minute
        sleep(interval)

if __name__ == "__main__":
    main()
