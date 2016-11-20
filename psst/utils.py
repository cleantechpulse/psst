def int_else_float_except_string(s):
    try:
        f = float(s)
        i = int(f)
        return i if i==f else f
    except ValueError:
        return s
