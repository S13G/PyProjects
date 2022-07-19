def time_conversion(arr):
    split_run = arr.split(":")
    first_num = int(split_run[0])
    second_num = split_run[1]
    third_num = split_run[2][:2]
    weather = split_run[2][2:]

    if weather == 'AM':
        if first_num == 12:
            first_num = '00'
        print(f'{first_num}:{second_num}:{third_num}')
    elif weather == 'PM':
        if first_num != 12:
            first_num += 12
        print(f'{first_num}:{second_num}:{third_num}')


time_conversion("12:00:00AM")
