import csv
import pickle
from datetime import datetime
### доп. задания 3, 4 (частично), 6, 7

def typ(x): # своя функция типизирования
    x = str(x)
    if x.isdigit():
        return int(x)
    elif len(x.split('.')) == 2:
        return float(x)
    elif x == 'True' or x == 'False':
        return eval(x)
    else:
        return str(x)

objects = []
def load_table():
    if filename.endswith('.csv'):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            data = [row for row in reader]
            while [] in data:
                data.remove([])
    elif filename.endswith('.pickle'):
        with open(filename, 'rb') as file:
            data = pickle.load(file)
    return data

data = load_table()
# print(data)

def save_table():
    with open('save.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    with open('save.pickle', 'wb') as file:
        pickle.dump(data, file)
    with open('save.txt', 'w') as file:
        for i in data:
            file.write('\t'.join(i) + '\n')

# save_table()
###
###
###
###
###

def get_rows_by_number(start, stop=0, copy_table=False):
    if 0 > start or start >= len(data) or start > stop:
        raise SystemError('Неправильный ввод: некорректные границы')
    if copy_table:
        with open('get_rows_num.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            if stop == 0:
                writer.writerow(data[start])
            else:
                writer.writerows(data[start:stop+1])
        print("Создан файл 'get_rows_num.csv' и в него записаны данные")
    else:
        if stop == 0:
            return data[start]
        else:
            return data[start:stop + 1]

# get_rows_by_number(3, 4, True)
# print(get_rows_by_number(3, 4))


def get_rows_by_index(*vals, copy_table=False):
    if list(map(type, [typ(i) for i in vals]))[0] != int:
        raise SystemError('Неправильный ввод: нецелочисленные аргументы')
    select_rows = [i for i in data if i[0] in vals]
    if copy_table:
        with open('get_rows_ind.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            if len(select_rows) == 1:
                writer.writerow(*select_rows)
            else:
                writer.writerows(select_rows)
        print("Создан файл 'get_rows_ind.csv' и в него записаны данные")
    else:
        return select_rows

# get_rows_by_index('1', '2', copy_table=True)
# print(get_rows_by_index('1', '2'))

dict_ = {}
def get_column_types(by_number=True):
    if by_number not in [True, False]:
        raise SystemError('Неправильный ввод: только True или False')
    elif by_number:
        for i in range(len(data[0])):
            d = data[1]
            if d[i].isdigit():
                dict_[i] = 'int'
            elif len(d[i].split('.')) == 2:
                dict_[i] = 'float'
            elif d[i] == 'True' or d[i] == 'False':
                dict_[i] = 'bool'
            else:
                dict_[i] = 'str'
    else:
        for i in range(len(data[0])):
            d = data[1]
            if d[i].isdigit():
                dict_[f'column_{i+1}'] = 'int'
            elif len(d[i].split('.')) == 2:
                dict_[f'column_{i+1}'] = 'float'
            elif d[i] == 'True' or d[i] == 'False':
                dict_[f'column_{i+1}'] = 'bool'
            else:
                dict_[f'column_{i+1}'] = 'str'
    return dict_

# with open('testik.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     for key, value in get_column_types(False).items():
#         writer.writerow([key, value])
# print(get_column_types())


types_dict_int = {0: int, 1: str, 2: float, 3: str, 4: bool}
types_dict_str = {data[0][0]: int, data[0][1]: str, data[0][2]: float, data[0][3]: str, data[0][4]: bool}
def set_column_types(types_dict, by_number=True):
    if type(types_dict) != dict or types_dict == {}:
        raise SystemError('Неправильный ввод: аргумент функции - непустой словарь')
    try:
        d = data[1:]
        a = []
        if by_number:
            for j in range(len(d[0])):
                if types_dict[j] == bool:
                    types_dict[j] = eval
                a.append(list(map(types_dict[j], [i[j] for i in d])))
        else:
            for j in range(len(d[0])):
                if types_dict[data[0][j]] == bool:
                    types_dict[data[0][j]] = eval
                a.append(list(map(types_dict[data[0][j]], [i[j] for i in d])))
        return a
    except ValueError:
        raise ValueError('Неправильного вида словарь')

# print(set_column_types(types_dict_int, True))
# print(set_column_types(types_dict_str, False))


def get_values(column=0):
    if column not in [i for i in data[0]] and column not in [i for i in range(0, len(data[0]))]:
        raise SystemError('Неправильный ввод: столбца с таким именем или индексом не существует')
    res = []
    if type(column) == int:
        for i in data[1:]:
            res.append(typ(i[column]))
    else:
        column = data[0].index(column)
        for j in data[1:]:
            res.append(typ(j[column]))
    return res

# print(get_values())


def get_value(column=0):
    if column not in [i for i in data[0]] and column not in [i for i in range(0, len(data[0]))]:
        raise SystemError('Неправильный ввод: столбца с таким именем или индексом не существует')
    res = 0
    table = data[1]
    if type(column) == int:
        res = table[column]
    else:
        column = table.index(column)
        res = table[column]
    return typ(res)


# print(get_value())


values = [5, 6, 7, 8]
def set_values(values, column=0):
    if type(values) != list or (column not in [i for i in data[0]] and column not in [i for i in range(0, len(data[0]))]):
        raise SystemError('Неправильный ввод: нужен список или столбца с таким именем или индексом не существует')
    if type(column) == int:
        for row, value in zip(data[1:], values):
            row[column] = value
    else:
        column = data[0].index(column)
        for row, value in zip(data[1:], values):
            row[column] = value
    return data

# print(set_values(values))


value = ['Could be better']
def set_value(value, column=0):
    if type(values) != list or (column not in [i for i in data[0]] and column not in [i for i in range(0, len(data[0]))]):
        raise SystemError('Неправильный ввод: нужен список или столбца с таким именем или индексом не существует')
    table = data[0]
    if type(column) == int:
        table[column] = value[0]
    else:
        column = table.index(column)
        table[column] = value[0]
    return table

# print(set_value(value))


def print_table():
    for i in load_table():
        print('\t'.join(i) + '\n')
# print_table()

######
######
######
######
######

def add(chislo, column):
    if column not in data[0]:
        raise SystemError('Неправильный ввод: столбца с таким именем не существует')
    ind = data[0].index(column)
    if typ(data[1][ind]) == str(data[1][ind]):
        raise SystemError('Неправильный ввод: значения столбца должны быть int, float или bool')
    for i in range(1, len(data)):
        if bool(data[i][ind]):
            data[i][ind] = bool(typ(data[i][ind]) + chislo)
        else:
            data[i][ind] = typ(data[i][ind]) + chislo
    return data

# print(add(2, 'Age'))

def sub(chislo, column):
    if column not in data[0]:
        raise SystemError('Неправильный ввод: столбца с таким именем не существует')
    ind = data[0].index(column)
    if typ(data[1][ind]) == str(data[1][ind]):
        raise SystemError('Неправильный ввод: значения столбца должны быть int, float или bool')
    for i in range(1, len(data)):
        data[i][ind] = typ(data[i][ind]) - chislo
    return data

# print(add(True, 'BoolVal'))

def mul(chislo, column):
    if column not in data[0]:
        raise SystemError('Неправильный ввод: столбца с таким именем не существует')
    ind = data[0].index(column)
    if typ(data[1][ind]) == str(data[1][ind]):
        raise SystemError('Неправильный ввод: значения столбца должны быть int, float или bool')
    for i in range(1, len(data)):
        if bool(data[i][ind]):
            data[i][ind] = bool(typ(data[i][ind]) * chislo)
        else:
            data[i][ind] = typ(data[i][ind]) * chislo
    return data

# print(mul(False, 'BoolVal'))

def div(chislo, column):
    if column not in data[0]:
        raise SystemError('Неправильный ввод: столбца с таким именем не существует')
    if chislo == 0:
        raise SystemError('Неправильный ввод: делить на ноль нельзя')
    ind = data[0].index(column)
    if typ(data[1][ind]) == str(data[1][ind]):
        raise SystemError('Неправильный ввод: значения столбца должны быть int, float или bool')
    for i in range(1, len(data)):
        data[i][ind] = typ(data[i][ind]) / chislo
    return data

# print(div(2, 'id'))


def eq(column, value):
    if column not in data[0]:
        raise SystemError('Неправильный ввод: столбца с таким именем не существует')
    ind = data[0].index(column)
    return [typ(row[ind]) == value for row in data[1:]]
# print(eq('Age', 31.5))

def gr(column, value):
    if column not in data[0]:
        raise SystemError('Неправильный ввод: столбца с таким именем не существует')
    ind = data[0].index(column)
    if typ(data[1][ind]) == str(data[1][ind]):
        raise SystemError('Неправильный ввод: значения столбца должны быть int, float или bool')
    return [typ(row[ind]) > value for row in data[1:]]
# print(gr('Age', 25))

def ls(column, value):
    if column not in data[0]:
        raise SystemError('Неправильный ввод: столбца с таким именем не существует')
    ind = data[0].index(column)
    if typ(data[1][ind]) == str(data[1][ind]):
        raise SystemError('Неправильный ввод: значения столбца должны быть int, float или bool')
    return [typ(row[ind]) < value for row in data[1:]]
# print(ls('Age', 25))

def ge(column, value):
    if column not in data[0]:
        raise SystemError('Неправильный ввод: столбца с таким именем не существует')
    ind = data[0].index(column)
    if typ(data[1][ind]) == str(data[1][ind]):
        raise SystemError('Неправильный ввод: значения столбца должны быть int, float или bool')
    return [typ(row[ind]) >= value for row in data[1:]]
# print(ge('Age', 31.5))

def le(column, value):
    if column not in data[0]:
        raise SystemError('Неправильный ввод: столбца с таким именем не существует')
    ind = data[0].index(column)
    if typ(data[1][ind]) == str(data[1][ind]):
        raise SystemError('Неправильный ввод: значения столбца должны быть int, float или bool')
    return [typ(row[ind]) <= value for row in data[1:]]
# print(le('Age', 28.8))

def ne(column, value):
    if column not in data[0]:
        raise SystemError('Неправильный ввод: столбца с таким именем не существует')
    ind = data[0].index(column)
    return [typ(row[ind]) != value for row in data[1:]]
# print(ne('Age', 28.8))


bool_list = [True, False, False, True, False]
def filter_rows(bool_list, copy_table=False):
    if len(bool_list) != len(data):
        raise SystemError('Неправильный ввод: длина bool_list должна быть равна количеству строк в таблице')
    data1 = data.copy()
    for num, i in enumerate(bool_list):
        if i == False:
            data.remove(data1[num])
            if [] in data:
                data.remove([])
    if copy_table:
        with open('filter_rows.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        print("Создан файл 'filter_rows.csv' и в него записаны данные")
        exit()
    else:
        return data

# print(filter_rows(bool_list, True))


def is_valid_date(value):
    for fmt in ('%d.%m.%Y', '%d-%m-%Y', '%d/%m/%Y', '%m.%d.%Y', '%m-%d-%Y', '%m/%d/%Y', '%Y.%m.%d', '%Y-%m-%d', '%Y/%m/%d'):
        try:
            datetime.strptime(value, fmt)
            return True
        except ValueError:
            continue
    return False

# print(is_valid_date('20-12-2024'))


def opr_column_type(values, column):
    row = values[1]
    if row[column].isdigit():
        return 'int'
    elif len(row[column].split('.')) == 2:
        return 'floal'
    elif row[column] == 'True' or row[column] == 'False':
        return 'bool'
    elif is_valid_date(row[column]):
        return 'datetime'
    return 'str'

# print(opr_column_type(data, column=2))


table1 = [['id', 'Name'], ['1', 'John']]
table2 = [['Age', 'Gender'], ['28.8', 'M']]
table = [['id', 'Name'], ['1', 'John'], ['Age', 'Gender'], ['28.8', 'M']]
def contact(table1, table2):
    res = table1.copy()
    res.extend(table2)
    return res

print(contact(table1, table2))

def split(table, row):
    return table[:row], table[row:]

# print(split(table, row=2))

if __name__ == '__main__':
    pass
