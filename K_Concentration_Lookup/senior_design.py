#!/usr/bin/env python3

import sys


# --------------------------------------------------


def select_1():
    ''' Searches through the lookup table '''

    search_matches = {}
    description = ''

    print('\nEnter a serch term:')
    search_term = sys.stdin.readline().strip().lower()
    # Obtains seach term from user

    for line_num, line in enumerate(open('lookup_table.txt', 'rt')):
        if line_num % 2 == 0 and search_term in line.lower():
            description = line
            search_matches[description] = 0
        elif (line_num + 1) % 2 == 0 and description in search_matches.keys():
            search_matches[description] = line
            description = ''

    if len(search_matches) > 0:
        print('\nSearch Results:')

        for line_num, line in enumerate(search_matches, start=1):
            print(str(line_num) + ': ' + line, end='')

        print('\nPlease enter the corresponding number:')
        description_num = float(sys.stdin.readline().strip())

        if (description_num in range(1, len(search_matches) + 1)):

            for line_num, line in enumerate(search_matches, start=1):
                if line_num == description_num:
                    print('\nItem Description:', line, end='')
                    print('Potassium Concentration:',
                          search_matches.get(line).strip(), 'mg/L', '\n')
                    return()

        else:
            print('Not a valid selection. Please try again')
            return()

    else:
        print('No match results. Please try again.')
        return()


# --------------------------------------------------


def select_2():
    ''' Adds a new entry to the lookup table '''

    print('\nEnter a description:')
    new_description = sys.stdin.readline()

    for line_num, line in enumerate(open('lookup_table.txt', 'rt')):
        if line_num % 2 == 0 and line.lower().strip() == new_description.lower().strip():
            print('Description all ready exist in the look up table. Please try again.')
            return()

    print('Enter the corresponding concentration (mg/L):')
    new_concentration = sys.stdin.readline()

    try:
        new_concentration = float(new_concentration.strip())

        if new_concentration > 0:
            print(new_description.strip(),
                    file=open('lookup_table.txt', 'at'))
            print(new_concentration, file=open('lookup_table.txt', 'at'))
            print('\nNew concentration has been added.')
        else: 
            print('Concentration must be greater than 0. Please try again')

        return()
    
    except ValueError:
        print('Not a valid concentration. Please try again.')
        return()


# --------------------------------------------------


def main():

    user_selection = '0'

    while user_selection != '1' or user_selection != '2':
        print('\nPlease make a selection:')
        print('1: Search lookup table')
        print('2: Add a new entry')
        print('3: Quit')

        user_selection = sys.stdin.readline().strip()

        if user_selection == '1':
            select_1()
        elif user_selection == '2':
            select_2()
        elif user_selection == '3':
            print('\nBye!')
            break
        else:
            print('\nInvalid entry, please try again\n')


# --------------------------------------------------

if __name__ == '__main__':
    main()