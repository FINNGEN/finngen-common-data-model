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
    # TODO what is the right term for this object

    DTO containing the chromosome position with
    
    """
    chromosome = attr.ib(validator=instance_of(int))
    position = attr.ib(validator=instance_of(int))
    reference = attr.ib(validator=instance_of(str))
    alternate = attr.ib(validator=instance_of(str))

    @staticmethod
    def from_str(text: str) -> typing.Optional["Variant"]:
        fragments = re.match(r'^chr(?P<chromosome>[0-9]+)_(?P<position>\d+)_(?P<reference>[ACGTU]{1,100})_(?P<alternate>[ACGTU]{1,100})$', text)
        if fragments is None:
            None
        else:
            return Variant(chromosome=int(fragments.group('chromosome')),
                           position=int(fragments.group('position')),
                           reference=fragments.group('reference'),
                           alternate=fragments.group('alternate'))

    def __str__(self) -> str:
        return "chr{chromosome}_{position}_{reference}_{alternate}".format(chromosome=self.chromosome,
                                                                           position=self.position,
                                                                           reference=self.reference,
                                                                           alternate=self.alternate)

    def json_rep(self):
        return self.__dict__

    def __repr__(self) -> typing.Dict[str, typing.Any]:
        return self.__dict__

    @staticmethod
    def columns(prefix : typing.Optional[str] = None) -> typing.List[Column]:
        prefix = prefix if prefix is not None else ""
        return [ Column('{}chromosome'.format(prefix), String(2), unique=False, nullable=False), 
                 Column('{}position'.format(prefix), Integer, unique=False, nullable=False), 
                 Column('{}ref'.format(prefix), String(100), unique=False, nullable=False), 
                 Column('{}alt'.format(prefix), String(100), unique=False, nullable=False), ]


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
    def from_str(text: str) -> typing.Optional["ChromosomeRange"]:
        """
        Takes a string representing a range and returns a tuple of integers
        (chromosome,start,stop).  Returns None if it cannot be parsed.

        TODO : start < stop
        """
        fragments = re.match(r'(?P<chromosome>[A-Za-z0-9]+):(?P<start>\d+)-(?P<stop>\d+)', text)
        if fragments is None:
            return None
        else:
            return Locus(chromosome=fragments.group('chromosome'),
                         start=int(fragments.group('start')),
                         stop=int(fragments.group('stop')))

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

    @staticmethod    
    def __composite_values__(self):
        """
        These are artifacts needed for composition by sqlalchemy.
        Returns a tuple containing the constructor args.

        :return: tuple (chromosome, start, stop)
        """
        return self.chromosome, self.start, self.stop

