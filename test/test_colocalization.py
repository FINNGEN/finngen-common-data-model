import os
import tempfile
import tempfile
import uuid
import random
import pytest
from finngen_common_data_model.genomics import Locus, Variant
from finngen_common_data_model.colocalization import Colocalization

def test_colocalization():
    sample = ["source1", # source1
              "source2", # source2
              "phenotype1", # phenotype1
              "phenotype1_description", # phenotype1_description
              "phenotype2", # phenotype2
              "phenotype2_description", # phenotype2_description
              "tissue1", # tissue1
              "tissue2", # tissue2
              "1:2-3", # locus_id1
              "4:5-6", # locus_id2
              "7", # chromosome
              8, # start
              9, # stop
              10.0, # clpp
              11.0, # clpa
              12.0, # beta_id1
              13.0, # beta_id2
              "variation", # variation
              "vars_pip1", # vars_pip1
              "vars_pip2", # vars_pip2
              "vars_beta1", # vars_beta1
              "vars_beta2", #vars_beta2
              14, # len_cs1
              15, # len_cs2
              16, # len_inter
              ]
    expected = Colocalization(source1 = "source1",
                              source2 = "source2",
                              phenotype1 = "phenotype1",
                              phenotype1_description = "phenotype1_description",
                              phenotype2 = "phenotype2",
                              phenotype2_description = "phenotype2_description",
                              tissue1 = "tissue1",
                              tissue2 = "tissue2",
                              locus_id1 = Variant.from_str("chr1_2_A_G"),
                              locus_id2 = Variant.from_str("chr4_5_C_T"),
                              locus = Locus.from_str("7:8-9"),
                              clpp = 10.0,
                              clpa = 11.0,
                              beta_id1 = 12.0,
                              beta_id2 = 13.0,
                              variants = [],
                              len_cs1 = 0,
                              len_cs2 = 0,
                              len_inter = 16)
    sample = "\t".join(map(str,sample))
    #actual = Colocalization.from_str(sample)
    #assert expected == actual
