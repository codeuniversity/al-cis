import numpy as np


def map_cells_to_dict(cells, dic):

    for c in cells:
        dic[c.id] = c


def get_value(dict, key):

    try:
        value = dict[key]
        return value, True
    except BaseException:
        return None, False


def random_vector_of_length(l):

    vec = np.random.uniform(1 / 10 * 6, 2, [3]) - 1
    dist = np.sqrt(vec.dot(vec))
    factor = l / dist

    return factor * vec


def group_connected_cells(group, cell, cell_dict):

    for conn in cell.connections:
        other_cell, exists = get_value(cell_dict, conn.connected_to)
        if exists:
            if other_cell not in group:
                group.append(other_cell)
                group_connected_cells(group, other_cell, cell_dict)

    return group
