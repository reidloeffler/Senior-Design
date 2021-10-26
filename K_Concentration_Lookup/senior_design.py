#!/usr/bin/env python3

import sys

# --------------------------------------------------


def calculate_total_lines(file):

    total_lines = 0

    for char_num in range(len(file)):
        if file[char_num] == '\n':
            total_lines += 1

    total_lines = int(total_lines / 2)

    return total_lines


# --------------------------------------------------


def get_values(file, total_lines, usr_description):

    info = dict(description='', concentration='')
    total_num_line = 0
    num_line = 0
    char_num = 0
    description = ''
    concentration = ''

    while total_num_line <= total_lines:

        if file[char_num] != '\n':

            if num_line == 0:
                description += file[char_num]

            if num_line == 1:
                concentration += file[char_num]

            char_num += 1

        if file[char_num] == '\n':
            num_line += 1
            char_num += 1

        if num_line == 2:
            total_num_line += 1
            num_line = 0

            if usr_description == (description + '\n'):
                info['description'] = description
                info['concentration'] = concentration
                total_num_line = total_lines

                return [info['description'], info['concentration']]

            else:
                description = ''
                concentration= ''

                if total_num_line == total_lines:
                    return ('entry does not exist')


# --------------------------------------------------


def main():

    look_up_table = open('look_up_table.txt').read()
    total_lines = calculate_total_lines(look_up_table)

    print('Please enter and item description to search for:')
    usr_description = sys.stdin.readline()
    info = get_values(look_up_table, total_lines, usr_description)

    if info == 'entry does not exist':
        print('Entry does not exist. Would you like to enter a new item?')

    else:
        print('Description: ' + info[0])
        print('Concentration: ' + info[1])


# --------------------------------------------------

if __name__ == '__main__':
    main()
