import abc
import attr
import typing
import attr
from attr.validators import instance_of
from sqlalchemy import Table, MetaData, create_engine, Column, Integer, String, Float, Text

import re
from commons.data import *
        
# Variant
@attr.s
class Variant(JSONifiable):
    """

    DTO containing variant information

    """
    chromosome = attr.ib(validator=instance_of(str))
    position = attr.ib(validator=instance_of(int))
    reference = attr.ib(validator=instance_of(str))
    alternate = attr.ib(validator=instance_of(str))

    PARSER = re.compile('''^(chr)?
                            (?P<chromosome>( M | MT | X | Y |
                                             1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 
                                             11 | 12 | 13 | 14 | 15 |16 | 17 | 18 | 19 | 20 | 
                                             21 | 22 | 23 | 24 | 25))
                                             
                            (?P<separator>[_:/])
                            
                            (?P<position>\d+)

                            (?P=separator)
                            
                            (?P<reference>( \<[^\>]{1,998}\>
                                          | [^_:/]{1,1000} ))
                            
                            [_:/]
                            
                            (?P<alternate>( .{1,1000}  ))$
                        ''', re.VERBOSE)
    @staticmethod
    def from_str(text: str) -> typing.Optional["Variant"]:
        fragments = Variant.PARSER.match(text)
        if fragments is None:
            raise Exception(text)
            None 
        else:
            return Variant(chromosome=fragments.group('chromosome'),
                           position=int(fragments.group('position')),
                           reference=fragments.group('reference'),
                           alternate=fragments.group('alternate'))

    def __str__(self) -> str:
        return "{chromosome}:{position}:{reference}:{alternate}".format(chromosome=self.chromosome,
                                                                        position=self.position,
                                                                        reference=self.reference,
                                                                        alternate=self.alternate)

    def json_rep(self):
        return self.__dict__

    def __repr__(self) -> typing.Dict[str, typing.Any]:
        return self.__dict__

    @staticmethod
    def columns(prefix : typing.Optional[str] = None, primary_key=False, nullable=False) -> typing.List[Column]:
        prefix = prefix if prefix is not None else ""
        return [ Column('{}chromosome'.format(prefix), String(2), primary_key=primary_key, nullable=nullable),
                 Column('{}position'.format(prefix), Integer, primary_key=primary_key, nullable=nullable),
                 Column('{}ref'.format(prefix), String(1000), primary_key=primary_key, nullable=nullable),
                 Column('{}alt'.format(prefix), String(1000), primary_key=primary_key, nullable=nullable), ]


    def __composite_values__(self):
        """
        These are artifacts needed for composition by sqlalchemy.
        Returns a tuple containing the constructor args.

        :return: tuple (chromosome, position, reference, alternate)
        """
        return self.chromosome, self.position, self.reference, self.alternate


# 
@attr.s
class Locus(JSONifiable):
    """
        Chromosome coordinate range

        chromosome: chromosome
        start: start of range
        stop: end of range
    """
    chromosome = attr.ib(validator=attr.validators.and_(instance_of(str)))
    start = attr.ib(validator=instance_of(int))
    stop = attr.ib(validator=instance_of(int))

    @staticmethod
    def from_str(text: str) -> typing.Optional["Locus"]:
        """
        Takes a string representing a range and returns a tuple of integers
        (chromosome,start,stop).  Returns None if it cannot be parsed.
        """
        fragments = re.match(r'(?P<chromosome>[A-Za-z0-9]+):(?P<start>\d+)-(?P<stop>\d+)', text)
        result = None
        if fragments is None:
            result = None
        else:
            chromosome=fragments.group('chromosome')
            start=int(fragments.group('start'))
            stop=int(fragments.group('stop'))
            if start <= stop:
                result = Locus(chromosome, start, stop)
            else:
                result = None
        return result

    def __str__(self):
        """

        :return: string representation of range
        """
        return "{chromosome}:{start}-{stop}".format(chromosome=self.chromosome,
                                                    start=self.start,
                                                    stop=self.stop)

    def json_rep(self):
        return self.__dict__

    def __repr__(self) -> typing.Dict[str, typing.Any]:
        return self.__dict__

    @staticmethod
    def columns(prefix : typing.Optional[str] = None) -> typing.List[Column]:
        prefix = prefix if prefix is not None else ""
        return [ Column('{}chromosome'.format(prefix), String(2), unique=False, nullable=False),
                 Column('{}start'.format(prefix), Integer, unique=False, nullable=False),
                 Column('{}stop'.format(prefix), Integer, unique=False, nullable=False) ]

    def __composite_values__(self):
        """
        These are artifacts needed for composition by sqlalchemy.
        Returns a tuple containing the constructor args.

        :return: tuple (chromosome, start, stop)
        """
        return self.chromosome, self.start, self.stop

