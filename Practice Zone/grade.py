def grading_students(grades):
    next_multiple = []

    new_grades = filter(lambda grade: grade >= 38, grades)

    new_grades = list(new_grades)
    print(new_grades)

    for i in new_grades:
        if i % 5 == 4:
            next_multiple.append(i + 1)
        elif i % 5 == 3:
            next_multiple.append(i + 2)
        elif i % 5 == 2:
            next_multiple.append(i + 3)
        elif i % 5 == 1:
            next_multiple.append(i + 4)
    print(next_multiple)

    rounded = []

    zip_list = zip(new_grades, next_multiple)
    for i, j in zip_list:
        rounded.append(j - i)

    print(rounded)


grading_students([73, 67, 38, 33])
