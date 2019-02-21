from bitstring import BitArray
import os
import cis_config as config
import random

initial_energy_feature = BitArray(bytes=bytearray(b'\xff'))
division_treshold_feature = BitArray(bytes=bytearray(b'\xa0'))
food_treshold_feature = BitArray(bytes=bytearray(b'\x21'))
food_amount_feature = BitArray(bytes=bytearray(b'\x40'))
builds_connection_after_division_feature = BitArray(bytes=bytearray(b'\x60'))
should_sub_slice_feature = BitArray(bytes=bytearray(b'\x10'))
sub_slice_start_feature = BitArray(bytes=bytearray(b'\x10'))
sub_slice_start_feature = BitArray(bytes=bytearray(b'\x30'))
sub_slice_end_feature = BitArray(bytes=bytearray(b'\x50'))


def feature_in_dna(dna, feature, shift_by=0, start_at=0):
    feature_hit_count = 0
    feature_copy = feature.copy()
    start_index = start_at % len(dna)
    for b in dna[start_index:]:
        bits = BitArray(bytes=[b])
        overlap = bits & feature
        feature_hit_count += overlap.bin.count('1')
        feature_copy = shift_bits_by(feature_copy, shift_by)
    max_hits = len(dna) * feature.bin.count('1')
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


def should_sub_slice(dna, current_connection_count):
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
    end_index = start_index + round(max_end_step * end_feature_value)
    return dna[start_index:end_index]


def shift_bits_by(bits, n):
    rest = n % 8
    if rest == 0:
        return bits

    bit_string = bits.bin
    shifted_bits = bit_string[rest:] + bit_string[:rest]
    return BitArray(bin=shifted_bits)


def mutate_dna_with_chance(dna, chance):
    new_dna_bit_string = ''
    for b in dna:
        bit_string = BitArray(bytes=[b]).bin
        if random_bool_with_threshold(chance):
            bit_string = mutate_bit_string(bit_string)
        new_dna_bit_string += bit_string
    if random_bool_with_threshold(chance):
        new_dna_bit_string += '0'*8
    return BitArray(bin=new_dna_bit_string).bytes


def random_bool_with_threshold(threshold):
    return random.uniform(0, 1) < threshold


def mutate_bit_string(bit_string):
    random_index = random.randint(0, len(bit_string) - 1)
    new_bit = ''
    if bit_string[random_index] == '0':
        new_bit = '1'
    else:
        new_bit = '0'
    return bit_string[:random_index] + new_bit + bit_string[random_index + 1:]
