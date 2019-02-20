from bitstring import BitArray
import os
import cis_config as config
initial_energy_feature = BitArray(bytes=bytearray(b'\xff'))
division_treshold_feature = BitArray(bytes=bytearray(b'\xa0'))
food_treshold_feature = BitArray(bytes=bytearray(b'\x21'))
food_amount_feature = BitArray(bytes=bytearray(b'\x40'))

def feature_in_dna(dna, feature):
  feature_hit_count = 0
  for b in dna:
    bits = BitArray(bytes=[b])
    overlap = bits & feature
    feature_hit_count += overlap.bin.count('1')
  max_hits = len(dna) * feature.bin.count('1')
  return feature_hit_count / max_hits

def initial_energy(dna):
  return int(feature_in_dna(dna, initial_energy_feature) * config.INITIAL_ENERGY_LEVEL)

def division_treshold(dna):
  return feature_in_dna(dna, division_treshold_feature) * config.DIVISION_THRESHOLD

def food_theshold(dna):
  return feature_in_dna(dna, food_treshold_feature) * config.FOOD_THRESHOLD

def food_amount(dna):
  return int(feature_in_dna(dna, food_amount_feature) * config.FOOD_ENERGY)

