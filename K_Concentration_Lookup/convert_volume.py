#!/usr/bin/env python3

import sys

# --------------------------------------------------

def convert_volume(volume_string):

    units = ['fl oz', 'oz', 'tsp', 'tbsp', 'tablespoon', 'cups']
    nums = ['0', '1', '2', '3', '4', '5', '6,' '7', '8', '9', '.']
    volume = ''

    for unit in units:
        if unit in volume_string:
            for char in volume_string:
                if char in nums:
                    volume += char
                if (volume + ' ' + unit) in volume_string:
                    if unit == 'fl oz' or unit == 'oz':
                        volume = float(volume) * 0.0295735
                    if unit == 'tsp':
                        volume = float(volume) * 0.00492892
                    if unit == 'tbsp' or unit == 'tablespoon':
                        volume = float(volume) * 0.0147868
                    if unit == 'cups':
                        volume = float(volume) * 0.24
                    return volume


# --------------------------------------------------


def main():

    lookup_table = open('lookup_table.txt', 'wt')
    description = ''
    volume_string = ''
    potassium_mass = 0
    concentration = 0
    volume = 0.0

    for line_num, line in enumerate(open('raw_data_file.txt', 'rt')):

        if (line_num % 3) == 0:
            description = line
        elif (line_num + 2) % 3 == 0:
            volume_string = line
            volume = convert_volume(volume_string)
        else:
            potassium_mass = line.strip()

            if volume != None and volume != 0:
                concentration = (float(potassium_mass) / float(volume))
                print(description, end='', file=lookup_table)
                print(round(concentration, 2), file=lookup_table)


# --------------------------------------------------

if __name__ == '__main__':
    main()