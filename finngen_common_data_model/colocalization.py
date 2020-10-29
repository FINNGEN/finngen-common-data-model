import abc
import attr
import typing
import attr
from attr.validators import instance_of
from sqlalchemy import Table, MetaData, create_engine, Column, Integer, String, Float, Text
from finngen_common_data_model.genomics import *
from finngen_common_data_model.data import *


@attr.s(frozen=True)
class CausalVariant(JSONifiable, Kwargs):
    """
    Causual variant DTO

    pip1, beta1
    pip2, beta2

    """
    variant = attr.ib(validator=attr.validators.optional(instance_of(Variant)))
    
    pip1 = attr.ib(validator=attr.validators.optional(instance_of(float)))
    beta1 = attr.ib(validator=attr.validators.optional(instance_of(float)))
    
    pip2 = attr.ib(validator=attr.validators.optional(instance_of(float)))
    beta2 = attr.ib(validator=attr.validators.optional(instance_of(float)))

    id = attr.ib(validator=attr.validators.optional(instance_of(int)), default= None)

    def kwargs_rep(self) -> typing.Dict[str, typing.Any]:
        return self.__dict__

    def json_rep(self):
        d = self.__dict__
        d = d.copy()

        d.pop("_sa_instance_state", None)
        d["position"] = self.variant.position if self.variant else None
        d["variant"] = str(d["variant"]) if self.variant else None
        d["count_cs"] = self.count_cs()
        d["membership_cs"] = self.membership_cs()
        return d

    def has_cs1(self) -> bool:
        return (self.pip1 is not None) and (self.beta1 is not None)

    def has_cs2(self) -> bool:
        return (self.pip2 is not None) and (self.beta2 is not None)

    def count_cs1(self) -> int:
        return 1 if self.has_cs1() else 0

    def count_cs2(self) -> int:
        return 1 if self.has_cs2() else 0

    def count_cs(self) -> int:
        return self.count_cs1() + self.count_cs2()

    def membership_cs(self) -> int:
        if self.has_cs1() and self.has_cs2():
            label = 'Both'
        elif self.has_cs1():
            label = 'CS1'
        elif self.has_cs2():
            label = 'CS2'
        else:
            label = 'None'
        return label

    @staticmethod
    def parse_causal_variant(x : str):
        variant, pip, beta = x.split(",")
        return (float(pip),float(beta))
    
    
    @staticmethod
    def from_list(variant1_str: str,
                  variant2_str: str) -> typing.List["Colocalization"]:

        vars1_index= { x.split(",")[0]:x for x in variant1_str.split(";") }
        vars2_index= { x.split(",")[0]:x for x in variant2_str.split(";") }

        split = CausalVariant.parse_causal_variant

        # list of all variants
        keys = set([*vars1_index.keys(),*vars2_index.keys()])
        # lookup variants in the two indexes
        keys = map(lambda x : [x,vars1_index.get(x),vars2_index.get(x)],keys)        
        
        keys = [ [Variant.from_str(x[0]),nvl(x[1],split),nvl(x[2],split)] for x in keys]
        keys = [ [k[0],
                  *(k[1] or (None,None)),
                  *(k[2] or (None,None))] for k in keys]
        
        causalvariants = [ CausalVariant(*k) for k in keys]
        return causalvariants
    
    @staticmethod
    def columns(prefix : typing.Optional[str] = None) -> typing.List[Column]:
        prefix = prefix if prefix is not None else ""
        return [
            Column('{}id'.format(prefix), Integer, primary_key=True, autoincrement=True),
            Column('{}pip1'.format(prefix), Float, unique=False, nullable=True),
            Column('{}pip2'.format(prefix), Float, unique=False, nullable=True),
            Column('{}beta1'.format(prefix), Float, unique=False, nullable=True),
            Column('{}beta2'.format(prefix), Float, unique=False, nullable=True),
            *Variant.columns(nullable=True),
        ]

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

    quant1 = attr.ib(validator=attr.validators.optional(instance_of(str)))
    quant2 = attr.ib(validator=attr.validators.optional(instance_of(str)))

    tissue1 = attr.ib(validator=attr.validators.optional(instance_of(str)))
    tissue2 = attr.ib(validator=instance_of(str))

    locus_id1 = attr.ib(validator=instance_of(Variant))
    locus_id2 = attr.ib(validator=instance_of(Variant))

    locus = attr.ib(validator=instance_of(Locus))

    clpp = attr.ib(validator=instance_of(float))
    clpa = attr.ib(validator=instance_of(float))

    len_cs1 = attr.ib(validator=instance_of(int))
    len_cs2 = attr.ib(validator=instance_of(int))
    len_inter = attr.ib(validator=instance_of(int))

    variants = attr.ib(validator=attr.validators.deep_iterable(member_validator=instance_of(CausalVariant),
                                                               iterable_validator=instance_of(typing.List)))
    
    id = attr.ib(validator=attr.validators.optional(instance_of(int)), default=None)

    IMPORT_COLUMN_NAMES = ("source1", "source2", "pheno1", "pheno2", "tissue1", "tissue2",  "locus_id1", "locus_id2", "chrom", "start", "stop", "clpp", "clpa", "vars", "len_cs1", "len_cs2", "len_inter", "vars1_info", "vars2_info", )
    
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
        variants = CausalVariant.from_list(nvl(line[21], str),
                                           nvl(line[22], str))

        colocalization = Colocalization(source1=nvl(line[0], str),
                                        source2=nvl(line[1], str),

                                        phenotype1=nvl(line[2], ascii),
                                        phenotype1_description=nvl(line[3], ascii),
                                        
                                        phenotype2=nvl(line[4], ascii),
                                        phenotype2_description=nvl(line[5], ascii),

                                        quant1=nvl(line[6], str),
                                        quant2=nvl(line[7], str),
                                        
                                        tissue1=nvl(line[8], str),
                                        tissue2=nvl(line[9], str),
                                        
                                        locus_id1=nvl(line[10], Variant.from_str),
                                        locus_id2=nvl(line[11], Variant.from_str),

                                        locus = Locus(nvl(line[12], string_to_chromosome), # chromosome
                                                      nvl(line[13], na(int)), # start
                                                      nvl(line[14], na(int))), # stop

                                        clpp=nvl(line[15], float),
                                        clpa=nvl(line[16], float),
                                        # var line[17]
                                        len_cs1=nvl(line[18], na(int)),
                                        len_cs2=nvl(line[19], na(int)),
                                        len_inter=nvl(line[20], na(int)),
                                        
                                        variants = variants
        )
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

                 Column('{}quant1'.format(prefix), String(80), unique=False, nullable=True),
                 Column('{}quant2'.format(prefix), String(80), unique=False, nullable=True),
                 
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

                 Column('{}len_cs1'.format(prefix), Integer, unique=False, nullable=False),
                 Column('{}len_cs2'.format(prefix), Integer, unique=False, nullable=False),
                 Column('{}len_inter'.format(prefix), Integer, unique=False, nullable=False) ]
