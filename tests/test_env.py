import pytest
import random
import numpy as np

from cis import cell
from cis import env
from cis import helper
import cis.config as conf
import tests.mocking as mck


class TestClass(object):

    # energy consumptions
    def test_move_cells(self):

        cells = mck.mock_cell_batch()
        test_position = [(cell.pos.x, cell.pos.y, cell.pos.z) for cell in cells]

        id_to_cell_dict = {}
        helper.map_cells_to_dict(cells, id_to_cell_dict)

        env.move_cells(cells, id_to_cell_dict)
        assert [(cell.pos.x, cell.pos.y, cell.pos.z) for cell in cells] != test_position

    def test_move_cell_and_connected_cells(self):

        cells = mck.mock_cell_batch()
        single_cell = cells[random.randint(0, len(cells))]
        test_position = (single_cell.pos.x, single_cell.pos.y, single_cell.pos.z)

        id_to_cell_dict = {}
        helper.map_cells_to_dict(cells, id_to_cell_dict)
        moved_dict = {}

        env.move_cell_and_connected_cells(single_cell, id_to_cell_dict, moved_dict)
        assert (single_cell.pos.x, single_cell.pos.y, single_cell.pos.z) != test_position

    def test_curl(self):

        pos = mck.Vector(10, 15, 20)

        curled = env.curl(pos)
        assert np.array_equal(curled, np.array([0, 3.92, -3.94]))

    # # food
    # def test_feed_cells(self):
    #     env.feed_cells(cells, time_step)

    # def test_feed_cell(self):
    #     env.feed_cell(cell, time_step, food_factor=1)

    # def test_food_function(self):
    #     env.food_function(cell_pos, time_step)

    # def test_wave_function(self):
    #     env.wave_function(x, t, max_ampli=1, oscillation_period=1, init_deflection=0)

    # def test_noramlize_food_value(self):
    #     env.normalize_food_value(num, definition_area_size=6)
