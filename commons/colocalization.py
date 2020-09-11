import abc
import attr
import typing
import attr
from attr.validators import instance_of
from sqlalchemy import Table, MetaData, create_engine, Column, Integer, String, Float, Text
from commons.genomics import *
from commons.data import *



@attr.s
class CausalVariant(JSONifiable, Kwargs):
    """
    Causual variant DTO

    pip1, pip2, beta1, beta2, variant

    """
    variant1 = attr.ib(validator=instance_of(Variant))
    variant2 = attr.ib(validator=instance_of(Variant))
    pip1 = attr.ib(validator=attr.validators.optional(instance_of(float)))
    pip2 = attr.ib(validator=attr.validators.optional(instance_of(float)))
    beta1 = attr.ib(validator=attr.validators.optional(instance_of(float)))
    beta2 = attr.ib(validator=attr.validators.optional(instance_of(float)))
    id = attr.ib(validator=attr.validators.optional(instance_of(int)), default= None)

    def kwargs_rep(self) -> typing.Dict[str, typing.Any]:
        return self.__dict__

    def json_rep(self):
        d = self.__dict__
        d = d.copy()
        d.pop("_sa_instance_state", None)
        d["position1"] = self.variant1.position if self.variant1 else None
        d["variant1"] = str(d["variant1"]) if self.variant1 else None
        d["position2"] = self.variant2.position if self.variant2 else None
        d["variant2"] = str(d["variant2"]) if self.variant2 else None
        return d

    @staticmethod
    def from_list(variant1_str: str,
                  variant2_str: str,
                  pip1_str: str,
                  pip2_str: str,
                  beta1_str: str,
                  beta2_str: str) -> typing.List["Colocalization"]:

        variant1_list = list(map(Variant.from_str,variant1_str.split(',')))
        variant2_list = list(map(Variant.from_str,variant2_str.split(',')))
        pip1_list = list(map(na(float),pip1_str.split(',')))
        pip2_list = list(map(na(float),pip2_str.split(',')))
        beta1_list = list(map(na(float),beta1_str.split(',')))
        beta2_list = list(map(na(float),beta2_str.split(',')))
        result = list(map(lambda p : CausalVariant(*p),zip(variant1_list,variant2_list,pip1_list,pip2_list,beta1_list,beta2_list)))
        return result

    @staticmethod
    def columns(prefix : typing.Optional[str] = None) -> typing.List[Column]:
        prefix = prefix if prefix is not None else ""
        return [ Column('{}id'.format(prefix), Integer, primary_key=True, autoincrement=True),
                 Column('{}pip1'.format(prefix), Float, unique=False, nullable=True),
                 Column('{}pip2'.format(prefix), Float, unique=False, nullable=True),
                 Column('{}beta1'.format(prefix), Float, unique=False, nullable=True),
                 Column('{}beta2'.format(prefix), Float, unique=False, nullable=True),
                 *Variant.columns('{}variant1_'.format(prefix), nullable=True),
                 *Variant.columns('{}variant2_'.format(prefix), nullable=True)]
    
    @staticmethod
    def __composite_values__(self):
        """
        These are artifacts needed for composition by sqlalchemy.
        Returns a tuple containing the constructor args.

        :return: tuple (chromosome, start, stop)
        """
        return self.variant , self.pip1 , self.pip2 , self.beta1 ,self.beta2

@attr.s
class Colocalization(Kwargs, JSONifiable):
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

    locus_id1 = attr.ib(validator=instance_of(Variant))
    locus_id2 = attr.ib(validator=instance_of(Variant))

    locus = attr.ib(validator=instance_of(Locus))

    clpp = attr.ib(validator=instance_of(float))
    clpa = attr.ib(validator=instance_of(float))

    beta_id1 = attr.ib(validator=attr.validators.optional(instance_of(float)))
    beta_id2 = attr.ib(validator=attr.validators.optional(instance_of(float)))

    variants = attr.ib(validator=attr.validators.deep_iterable(member_validator=instance_of(CausalVariant),
                                                               iterable_validator=instance_of(typing.List)))
    len_cs1 = attr.ib(validator=instance_of(int))
    len_cs2 = attr.ib(validator=instance_of(int))
    len_inter = attr.ib(validator=instance_of(int))

    id = attr.ib(validator=attr.validators.optional(instance_of(int)), default=None)
    def kwargs_rep(self) -> typing.Dict[str, typing.Any]:
        return self.__dict__

    def json_rep(self):
        d = self.__dict__
        print(d)
        d["locus_id1"] = str(d["locus_id1"]) if self.locus_id1 else None
        d["locus_id2"] = str(d["locus_id2"]) if self.locus_id2  else None
        d["cs_size_1"] = sum(map(lambda c : c.count_variant1(), self.variants))
        d["cs_size_2"] = sum(map(lambda c : c.count_variant2(), self.variants))
        d["variants"] = list(map(lambda c : c.json_rep(), self.variants))
        return d

    @staticmethod
    def column_names() -> typing.List[str]:
        return [c.name for c in Colocalization.__attrs_attrs__]

    @staticmethod
    def from_list(line: typing.List[str]) -> "Colocalization":
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

                                        phenotype1=nvl(line[2], ascii),
                                        phenotype1_description=nvl(line[3], ascii),
                                        phenotype2=nvl(line[4], ascii),
                                        phenotype2_description=nvl(line[5], ascii),

                                        tissue1=nvl(line[6], str),
                                        tissue2=nvl(line[7], str),
                                        locus_id1=nvl(line[8], Variant.from_str),
                                        locus_id2=nvl(line[9], Variant.from_str),

                                        locus = Locus(nvl(line[10], str), # chromosome
                                                      nvl(line[11], na(int)), # start
                                                      nvl(line[12], na(int))), # stop

                                        clpp=nvl(line[13], float),
                                        clpa=nvl(line[14], float),
                                        beta_id1=nvl(line[15], na(float)),
                                        beta_id2=nvl(line[16], na(float)),
                                        variants = CausalVariant.from_list(nvl(line[17], str),
                                                                           nvl(line[17], str),
                                                                           nvl(line[18], str),
                                                                           nvl(line[19], str),
                                                                           nvl(line[20], str),
                                                                           nvl(line[21], str)),

                                        len_cs1=nvl(line[22], na(int)),
                                        len_cs2=nvl(line[23], na(int)),
                                        len_inter=nvl(line[24], na(int)))
        return colocalization

    @staticmethod
    def from_str(text: typing.List[str], delimiter = "\t") -> "Colocalization":
        line = text.split(delimiter)
        return Colocalization.from_list(line)

    @staticmethod
    def columns(prefix : typing.Optional[str] = None) -> typing.List[Column]:
        prefix = prefix if prefix is not None else ""
        return [ Column('{}id'.format(prefix), Integer, primary_key=True, autoincrement=True),
                 Column('{}source1'.format(prefix), String(80), unique=False, nullable=False),
                 Column('{}source2'.format(prefix), String(80), unique=False, nullable=False),
                 Column('{}phenotype1'.format(prefix), String(1000), unique=False, nullable=False),
                 Column('{}phenotype1_description'.format(prefix), String(1000), unique=False, nullable=False),
                 Column('{}phenotype2'.format(prefix), String(1000), unique=False, nullable=False),
                 Column('{}phenotype2_description'.format(prefix), String(1000), unique=False, nullable=False),
                 Column('{}tissue1'.format(prefix), String(80), unique=False, nullable=True),
                 Column('{}tissue2'.format(prefix), String(80), unique=False, nullable=True),

                 # locus_id1
                 *Variant.columns('{}locus_id1_'.format(prefix)),
                 # locus_id2
                 *Variant.columns('{}locus_id2_'.format(prefix)),

                 # locus
                 *Locus.columns(''),

                 Column('{}clpp'.format(prefix), Float, unique=False, nullable=False),
                 Column('{}clpa'.format(prefix), Float, unique=False, nullable=False),
                 Column('{}beta_id1'.format(prefix), Float, unique=False, nullable=True),
                 Column('{}beta_id2'.format(prefix), Float, unique=False, nullable=True),

                 Column('{}len_cs1'.format(prefix), Integer, unique=False, nullable=False),
                 Column('{}len_cs2'.format(prefix), Integer, unique=False, nullable=False),
                 Column('{}len_inter'.format(prefix), Integer, unique=False, nullable=False) ]

