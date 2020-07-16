import abc
import attr
import typing
import attr
from attr.validators import instance_of
from sqlalchemy import Table, MetaData, create_engine, Column, Integer, String, Float, Text
from commons.genomics import *
from commons.data import *
@attr.s
class Colocalization(JSONifiable):
    """
    DTO for colocalization.

    https://github.com/FINNGEN/colocalization/blob/master/docs/data_dictionary.txt

    Note : the column order is defined here.  This column order determines
    how data is loaded.

    """
    source1 = attr.ib(validator=instance_of(str))
    source2 = attr.ib(validator=instance_of(str))
    phenotype1 = attr.ib(validator=instance_of(str))
    phenotype1_description = attr.ib(validator=instance_of(str))
    phenotype2 = attr.ib(validator=instance_of(str))
    phenotype2_description = attr.ib(validator=instance_of(str))
    tissue1 = attr.ib(validator=attr.validators.optional(instance_of(str)))
    tissue2 = attr.ib(validator=instance_of(str))
    locus_id1 = attr.ib(validator=instance_of(Locus))
    locus_id2 = attr.ib(validator=instance_of(Locus))
    chromosome = attr.ib(validator=instance_of(str))
    start = attr.ib(validator=instance_of(int))
    stop = attr.ib(validator=instance_of(int))
    clpp = attr.ib(validator=instance_of(float))
    clpa = attr.ib(validator=instance_of(float))
    beta_id1 = attr.ib(validator=attr.validators.optional(instance_of(float)))
    beta_id2 = attr.ib(validator=attr.validators.optional(instance_of(float)))
    variation = attr.ib(validator=instance_of(str))
    vars_pip1 = attr.ib(validator=instance_of(str))
    vars_pip2 = attr.ib(validator=instance_of(str))
    vars_beta1 = attr.ib(validator=instance_of(str))
    vars_beta2 = attr.ib(validator=instance_of(str))
    len_cs1 = attr.ib(validator=instance_of(int))
    len_cs2 = attr.ib(validator=instance_of(int))
    len_inter = attr.ib(validator=instance_of(int))

    @staticmethod
    def from_str(text: str) -> typing.Optional["ChromosomeRange"]:
        line = text.split("\t")
        """
        Constructor method used to create colocalization from
        a row of data.

        the order of the columns are:
        01..05 source1, source2, phenotype1, phenotype1_description, phenotype2
        06..10 phenotype2_description, tissue1, tissue2, locus_id1, locus_id2
        11..15 chromosome, start, stop, clpp, clpa
        16..20 beta_id1, beta_id2, variation, vars_pip1, vars_pip2
        21..25 vars_beta1, vars_beta2, len_cs1, len_cs2, len_inter

        :param line: string array with value
        :return: colocalization object
        """
        colocalization = Colocalization(source1=nvl(line[0], str),
                                        source2=nvl(line[1], str),
                                        # note - ascii  = are to strip out
                                        phenotype1=nvl(line[2], ascii),
                                        phenotype1_description=nvl(line[3], ascii), 
                                        phenotype2=nvl(line[4], ascii),
                                        phenotype2_description=nvl(line[5], ascii),
                                        
                                        tissue1=nvl(line[6], str),
                                        tissue2=nvl(line[7], str),
                                        locus_id1=nvl(line[8], Locus.from_str),
                                        locus_id2=nvl(line[9], Locus.from_str),

                                        chromosome=nvl(line[10], str),
                                        start=nvl(line[11], na(int)),
                                        stop=nvl(line[12], na(int)),

                                        clpp=nvl(line[13], float),
                                        clpa=nvl(line[14], float),
                                        beta_id1=nvl(line[15], na(float)),
                                        beta_id2=nvl(line[16], na(float)),

                                        variation=nvl(line[17], str),
                                        vars_pip1=nvl(line[18], str),
                                        vars_pip2=nvl(line[19], str),
                                        vars_beta1=nvl(line[20], str),
                                        vars_beta2=nvl(line[21], str),
                                        len_cs1=nvl(line[22], na(int)),
                                        len_cs2=nvl(line[23], na(int)),
                                        len_inter=nvl(line[24], na(int)))
        return colocalization

    @staticmethod
    def columns(prefix : typing.Optional[str] = None) -> typing.List[Column]:
        prefix = prefix if prefix is not None else ""
        return [ Column('{}id'.format(prefix), Integer, primary_key=True, autoincrement=True),
                 Column('{}source1'.format(prefix), String(80), unique=False, nullable=False),
                 Column('{}source2'.format(prefix), String(80), unique=False, nullable=False),
                 Column('{}phenotype1'.format(prefix), LONGTEXT(), unique=False, nullable=False),
                 Column('{}phenotype1_description'.format(prefix), LONGTEXT(), unique=False, nullable=False),
                 Column('{}phenotype2'.format(prefix), LONGTEXT(), unique=False, nullable=False),
                 Column('{}phenotype2_description'.format(prefix), LONGTEXT(), unique=False, nullable=False),
                 Column('{}tissue1'.format(prefix), String(80), unique=False, nullable=True),
                 Column('{}tissue2'.format(prefix), String(80), unique=False, nullable=False),

                 # locus_id1
                 Column('{}locus_id1_chromosome'.format(prefix), String(2), unique=False, nullable=False), 
                 Column('{}locus_id1_position'.format(prefix), Integer, unique=False, nullable=False),
                 Column('{}locus_id1_ref'.format(prefix), String(100), unique=False, nullable=False),
                 Column('{}locus_id1_alt'.format(prefix), String(100), unique=False, nullable=False),

                 # locus_id2
                 Column('{}locus_id2_chromosome'.format(prefix), String(2), unique=False, nullable=False),
                 Column('{}locus_id2_position'.format(prefix), Integer, unique=False, nullable=False),
                 Column('{}locus_id2_ref'.format(prefix), String(100), unique=False, nullable=False),
                 Column('{}locus_id2_alt'.format(prefix), String(100), unique=False, nullable=False),
                 
                 Column('{}chromosome'.format(prefix),  String(2), unique=False, nullable=False),
                 Column('{}start'.format(prefix), Integer, unique=False, nullable=False),
                 Column('{}stop'.format(prefix), Integer, unique=False, nullable=False),
                 
                 Column('{}clpp'.format(prefix), Float, unique=False, nullable=False),
                 Column('{}clpa'.format(prefix), Float, unique=False, nullable=False),
                 Column('{}beta_id1'.format(prefix), Float, unique=False, nullable=True),
                 Column('{}beta_id2'.format(prefix), Float, unique=False, nullable=True),
                 
                 Column('{}variation'.format(prefix), LONGTEXT(), unique=False, nullable=False),
                 Column('{}vars_pip1'.format(prefix), LONGTEXT(), unique=False, nullable=False),
                 Column('{}vars_pip2'.format(prefix), LONGTEXT(), unique=False, nullable=False),
                 Column('{}vars_beta1'.format(prefix), LONGTEXT(), unique=False, nullable=False),
                 Column('{}vars_beta2'.format(prefix), LONGTEXT(), unique=False, nullable=False),
                 Column('{}len_cs1'.format(prefix), Integer, unique=False, nullable=False),
                 Column('{}len_cs2'.format(prefix), Integer, unique=False, nullable=False),
                 Column('{}len_inter'.format(prefix), Integer, unique=False, nullable=False) ]

        
    def __repr__(self) -> typing.Dict[str, typing.Any]:
        return self.__dict__

    def json_rep(self):
        d = self.__dict__
        d["locus_id1"] = d["locus_id1"].to_str()
        d["locus_id2"] = d["locus_id2"].to_str()
        return d

