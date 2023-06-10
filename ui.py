import re


def ui_print(in_output, end='\n'):
    print(in_output, end=end)


def ui_get_binary_answer(question=None):
    if question:
        ui_print(question + ' | ', end='')
    yes_pattern = r'^(yes|y|1)$'
    no_pattern = r'^(no|n|0)$'
    while True:
        ui_print('Please type ["Yes", "Y", or "1"] OR ["No", "N", or "0"]: ', end='')
        in_input = input().lower().strip()
        if re.match(yes_pattern, in_input):
            return 1
        elif re.match(no_pattern, in_input):
            return 0
        else:
            ui_print('Invalid option! ', end='')


def ui_get_range_answer(question, range_size):
    if question:
        ui_print(question + ' | ', end='')
    while True:
        ui_print(f'Please enter a number between [0 - {range_size}]: ', end='')
        try:
            in_input = int(input().lower().strip())
            if in_input not in range(0, range_size + 1):
                raise ValueError
            return in_input
        except ValueError:
            ui_print('Invalid option! ', end='')