def int_else_float_except_string(s):
    try:
        f = float(s)
        i = int(f)
        return i if i==f else f
    except ValueError:
        return s


def has_number(string):
    return any(c.isdigit() for c in string)
