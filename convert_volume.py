#!/usr/bin/env python3

# --------------------------------------------------


def calculate_total_lines(file):

    total_lines = 0

    for char_num in range(len(file)):
        if file[char_num] == '\n':
            total_lines += 1

    total_lines = int(total_lines / 3)

    return total_lines


# --------------------------------------------------


def sort_values(file, total_lines, line_track):

    info = dict(line_num=0, description='', volume='', mass=0)
    total_num_line = 0
    num_line = 0
    char_num = 0
    description = ''
    volume = ''
    mass = ''

    while total_num_line < total_lines:

        if file[char_num] != '\n':

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

        if num_line == 3:
            total_num_line += 1
            num_line = 0

            if line_track == total_num_line:
                info['description'] = description
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


def covert_units(volume_string):

    nums = ['.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    units = ['cups', 'fl oz', 'tsp', 'tbsp']
    volume = ''
    x = 0

    while x in range(len(volume_string)):

        if volume_string[x] in nums:
            volume += volume_string[x]
        x += 1

    if (units[0] in volume_string and volume in volume_string):
        volume = float(volume) * 240
        return volume

    if (units[1] in volume_string and volume in volume_string):
        volume = float(volume) * 29.5735
        return volume

    if (units[2] in volume_string and volume in volume_string):
        volume = float(volume) * 4.92892
        return volume

    if (units[3] in volume_string and volume in volume_string):
        volume = float(volume) * 14.7868
        return volume


# --------------------------------------------------


def main():

    raw_data = open('raw_data_file.txt').read()
    converted_volumes = open('converted_volumes.txt', 'a')
    look_up_table = open('look_up_table.txt', 'a')
    total_lines = calculate_total_lines(raw_data)
    line_track = 1

    while line_track <= total_lines:

        info = sort_values(raw_data, total_lines, line_track)

        description = info[1]
        volume = str(covert_units(info[2]))
        mass = info[3]

        if volume != 'None':
            concentration = float(mass) / float(volume)

            converted_volumes.write(description + '\n')
            converted_volumes.write(volume + '\n')
            converted_volumes.write(mass + '\n')

            look_up_table.write(description + '\n')
            look_up_table.write((str(concentration)) + '\n')

        line_track += 1


# --------------------------------------------------

if __name__ == '__main__':
    main()
