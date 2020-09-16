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
    actual = Variant.from_str("chr1_2_A_G")
    assert expected == actual
                

def test_variant_2():
    expected = "chr1_2_A_G"
    actual = str(Variant.from_str(expected))
    assert expected == actual

def test_structural_variants():
    expected = "chr9_96792507_T_<INS:ME:ALU>"
    actual = str(Variant.from_str(expected))
    print(actual)
    assert expected == actual
    
