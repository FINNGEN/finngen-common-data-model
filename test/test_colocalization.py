import os
import tempfile
import tempfile
import uuid
import random
import pytest
from commons.genomics import Locus
from commons.colocalization import Colocalization

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
                              locus_id1 = Locus.from_str("1:2-3"),
                              locus_id2 = Locus.from_str("4:5-6"),
                              chromosome = "7",
                              start = 8,
                              stop = 9,
                              clpp = 10.0,
                              clpa = 11.0,
                              beta_id1 = 12.0,
                              beta_id2 = 13.0,
                              variation = "variation",
                              vars_pip1 = "vars_pip1",
                              vars_pip2 = "vars_pip2",
                              vars_beta1 = "vars_beta1",
                              vars_beta2 = "vars_beta2",
                              len_cs1 = 14,
                              len_cs2 = 15,
                              len_inter = 16)
    sample = "\t".join(map(str,sample))
    actual = Colocalization.from_str(sample)
    assert expected == actual
