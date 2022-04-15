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

<<<<<<< HEAD
    raw_data = open('raw_data_file.txt').read()
    converted_volumes = open('converted_volumes.txt', 'a')
    look_up_table = open('lookup_table.txt', 'a')
    total_lines = calculate_total_lines(raw_data)
    line_track = 1

    while line_track <= total_lines:

        info = sort_values(raw_data, total_lines, line_track)

        description = info[1]
        volume = str(covert_units(info[2]))
        mass = int(info[3]) * 1000

        if volume != 'None':
            concentration = float(mass) / float(volume)

            converted_volumes.write(description + '\n')
            converted_volumes.write(str(round(float(volume), 2)) + ' mL\n')
            converted_volumes.write(str(mass) + ' mg\n')

            look_up_table.write(description + '\n')
            look_up_table.write((str(round(concentration, 1))) + ' mg/mL\n')

        line_track += 1
=======
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
>>>>>>> 2f886830f197899ec49099bd8959bf0b3273971f


# --------------------------------------------------

if __name__ == '__main__':
    main()
