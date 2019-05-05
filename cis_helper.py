def map_cells_to_dict(cells, dic):

    for c in cells:
        dic[c.id] = c


def get_value(dict, key):

    try:
        value = dict[key]
        return value, True
    except BaseException:
        return None, False
