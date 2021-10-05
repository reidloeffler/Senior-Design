#!/usr/bin/env python3

import sys

# --------------------------------------------------


def calculate_total_lines(file):

    total_lines = 0

    for char_num in range(len(file) - 1):
        if file[char_num] == '\t':
            total_lines += 1

    total_lines = int(total_lines / 3)

    return total_lines


# --------------------------------------------------


def get_values(file, total_lines, usr_description):

    info = dict(line_num=0, description='', volume='', mass=0)
    total_num_line = 0
    num_line = 0
    char_num = 0
    description = ''
    volume = ''
    mass = ''

    while total_num_line < total_lines:

        if file[char_num] != '\n' and file[char_num] != '\t':

            if num_line == 0:
                description += file[char_num]

            if num_line == 1:
                volume += file[char_num]

            if num_line == 2:
                mass += file[char_num]

            char_num += 1

        if file[char_num] == '\n':
            num_line += 1
            char_num += 1

        if file[char_num] == '\t':
            char_num += 1

        if num_line == 3:
            total_num_line += 1
            num_line = 0
            info['description'] = description
            info['volume'] = volume
            info['mass'] = mass

            if usr_description == (info['description'] + '\n'):
                info['line_num'] = total_num_line
                info['volume'] = volume
                info['mass'] = mass
                total_num_line = total_lines

            description = ''
            volume = ''
            mass = ''

    return [
        info['line_num'], info['description'], info['volume'], info['mass']
    ]


# --------------------------------------------------


def main():

    look_up_table = open('Look_Up_Table.txt').read()

    total_lines = calculate_total_lines(look_up_table)

    usr_description = sys.stdin.readline()

    info = get_values(look_up_table, total_lines, usr_description)

    print('Line Number: ' + str(info[0]))
    print('Descroption: ' + info[1])
    print('Volume: ' + info[2])
    print('Mass: ' + info[3])


# --------------------------------------------------

if __name__ == '__main__':
    main()
