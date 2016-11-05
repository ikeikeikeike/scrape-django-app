def fint(i):
    try:
        return int(float(i))
    except ValueError:
        return 0
