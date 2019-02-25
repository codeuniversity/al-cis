from bitstring import BitArray
import os
import cis_config as config
import random

initial_energy_feature = BitArray(bytes=bytearray(b'\xff')).int
division_treshold_feature = BitArray(bytes=bytearray(b'\xa0')).int
food_treshold_feature = BitArray(bytes=bytearray(b'\x21')).int
food_amount_feature = BitArray(bytes=bytearray(b'\x40')).int
builds_connection_after_division_feature = \
    BitArray(bytes=bytearray(b'\x60')).int
should_sub_slice_feature = BitArray(bytes=bytearray(b'\x10')).int
sub_slice_start_feature = BitArray(bytes=bytearray(b'\x10')).int
sub_slice_start_feature = BitArray(bytes=bytearray(b'\x30')).int
sub_slice_end_feature = BitArray(bytes=bytearray(b'\x50')).int


def feature_in_dna(dna, feature, shift_by=0, start_at=0):
    feature_hit_count = 0
    feature_copy = feature
    start_index = start_at % len(dna)
    for b in dna[start_index:]:
        overlap = b & feature_copy
        feature_hit_count += bin(overlap).count('1')
        feature_copy = shift_bits_by(feature_copy, shift_by)
    max_hits = len(dna) * bin(feature).count('1')
    return feature_hit_count / max_hits


def feature_value_with_connections(dna, feature, current_connection_count):
    shift_param = current_connection_count % 8
    start_at_param = int(current_connection_count / 8) % len(dna)
    return feature_in_dna(
        dna,
        builds_connection_after_division_feature,
        shift_by=shift_param,
        start_at=start_at_param
    )


def initial_energy(dna):
    return int(feature_in_dna(dna, initial_energy_feature)
               * config.INITIAL_ENERGY_LEVEL)


def division_treshold(dna):
    return feature_in_dna(dna, division_treshold_feature) * \
        config.DIVISION_THRESHOLD


def builds_connection_after_division(dna, current_connection_count):
    feature_value = feature_value_with_connections(
        dna,
        builds_connection_after_division_feature,
        current_connection_count,
    )
    return feature_value < config.CONNECTION_LIKELYHOOD


def food_theshold(dna):
    return feature_in_dna(dna, food_treshold_feature) * config.FOOD_THRESHOLD


def food_amount(dna):
    return int(feature_in_dna(dna, food_amount_feature) * config.FOOD_ENERGY)


def dna_should_sub_slice(dna, current_connection_count):
    feature_value = feature_value_with_connections(
        dna,
        should_sub_slice_feature,
        current_connection_count
    )
    return feature_value < config.DNA_SUBSLICE_CHANCE


def dna_sub_slice(dna, current_connection_count):
    start_feature_value = feature_value_with_connections(
        dna,
        sub_slice_start_feature,
        current_connection_count,
    )
    end_feature_value = feature_value_with_connections(
        dna,
        sub_slice_end_feature,
        current_connection_count,
    )
    max_start_index = len(dna) - 1
    start_index = round(start_feature_value * max_start_index)
    max_end_step = (len(dna) - 1) - start_index
    end_index = start_index + round(max_end_step * end_feature_value) + 1
    return dna[start_index:end_index]


def shift_bits_by(bits, n):
    offset = n % 8
    if offset == 0:
        return bits

    limit_8bit = 255
    res = bits << offset
    invert = bits >> (8-offset)
    res = res | invert
    res = res & limit_8bit
    return res


def mutate_dna_with_chance(dna, chance):
    new_dna_bit_string = ''
    for b in dna:
        bit_array = BitArray(bytes=[b])
        if random_bool_with_threshold(chance):
            mutate_bit_array(bit_array)
        new_dna_bit_string += bit_array.bin
    if random_bool_with_threshold(chance):
        new_dna_bit_string += '0' * 8
    return BitArray(bin=new_dna_bit_string).bytes


def random_bool_with_threshold(threshold):
    return random.uniform(0, 1) < threshold


def mutate_bit_array(bit_array):
    random_index = random.randint(0, len(bit_array) - 1)
    bit_array[random_index] = not bit_array[random_index]
