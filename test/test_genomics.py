import os
import tempfile
import tempfile
import uuid
import random
import pytest

from finngen_common_data_model.genomics import Locus, Variant

def test_locus_1():
    expected = Locus(chromosome = "15",start = 78464464, stop =78864464)
    actual = Locus.from_str("15:78464464-78864464")
    assert expected == actual
    
def test_locus_2():
    expected = "15:78464464-78864464"
    actual = str(Locus.from_str("15:78464464-78864464"))
    assert expected == actual
    
def test_variant_1():
    expected = Variant(chromosome = "1", position = 2, reference = "A", alternate = "G")
    actual = Variant.from_str("1_2_A_G")
    assert expected == actual
                

def test_variant_2():
    variant = "1_2_A_G"
    expected = "1:2:A:G"
    actual = str(Variant.from_str(variant))
    assert expected == actual

def test_variant_3():
    variant = "1:2:A:G"
    expected = "1:2:A:G"
    actual = str(Variant.from_str(variant))
    assert expected == actual

def test_variant_3():
    variant = "1_2_A/G"
    expected = "1:2:A:G"
    actual = str(Variant.from_str(variant))
    assert expected == actual

def test_structural_variants_1():
    expected = "9:96792507:T:<INS:ME:ALU>"
    variant = "chr9_96792507_T_<INS:ME:ALU>"
    actual = str(Variant.from_str(variant))
    print(actual)
    assert expected == actual
    

def test_structural_variants_2():
    expected = "9:96792507:<INS:ME:ALU>:<INS:ME:ALU>"
    variant = "chr9_96792507_<INS:ME:ALU>_<INS:ME:ALU>"
    actual = str(Variant.from_str(variant))
    print(actual)
    assert expected == actual
