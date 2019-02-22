import cis_config as conf
import random
import numpy as np
# from cis_dna import


class Curl():
    def __init__(self, coor_origin, vec_len):
        self.coor_origin = coor_origin
        self.vec_len = vec_len

    def _P(self, x, y, z):
        nx = 0
        return nx

    def _Q(self, x, y, z):
        ny = -z + self.coor_origin[1]
        return ny

    def _R(self, x, y, z):
        nz = y - self.coor_origin[2]
        return nz

    def get(self, x, y, z):
        old_pos = np.array([x, y, z])
        curl_pos = np.array([
            self._P(x, y, z),
            self._Q(x, y, z),
            self._R(x, y, z),
        ])

        return curl_pos * self.vec_len


curl = Curl(
    np.array([
        conf.WORLD_DIMENSION[0] / 2,
        conf.WORLD_DIMENSION[1] / 2,
        conf.WORLD_DIMENSION[2] / 2
    ]),
    0.002
)


def enforce_movement(cell):
    global curl
    new_pos = curl.get(cell.pos.x, cell.pos.y, cell.pos.z)
    cell.pos.x += new_pos[0]
    cell.pos.y += new_pos[1]
    cell.pos.z += new_pos[2]


def feed_cell(cell):
    f = random.uniform(0, 1)
    if f < conf.FOOD_THRESHOLD:
        cell.energy_level += conf.FOOD_ENERGY
    # These Values are suppose to be extracted from DNA
    energy_consumption = conf.GENERAL_ENERGY_CONSUMPTION
    starvation_threshold = conf.ENERGY_THRESHOLD

    cell.energy_level -= energy_consumption
