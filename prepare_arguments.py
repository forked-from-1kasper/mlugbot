def get_argument(argv, name):
    if name in argv:
        id = argv.index(name)
        return argv[id + 1]
    else:
        return False


def get_bool_argument(argv, name):
    if name in argv:
        return True
    else:
        return False
