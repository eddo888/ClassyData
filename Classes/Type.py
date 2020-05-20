#!/usr/bin/env python3

'''
Created on 12/01/2015

@author: dedson
'''

import sqlalchemy
import sqlalchemy.orm

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.engine import reflection
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.collections import InstrumentedList, InstrumentedDict, InstrumentedSet

from .Base import Base

from jsonweb.encode import to_object
from jsonweb.decode import from_object

@from_object()
@to_object()
class Type(Base):
    '''
    The Type class is a generic base type for the Attribute, Property or Returns to allow a back reference to a class type and a generic collection type.
    '''

    __tablename__ = 'type'
    id            = Column(Integer, primary_key=True)
    inherited     = Column(String(256))
    generic_id    = Column(Integer,ForeignKey('generic.id'))
    generic       = relationship("Generic", uselist=False)
    clasz_id      = Column(Integer,ForeignKey('class.id'))
    clasz         = relationship("Class", uselist=False)

    __mapper_args__ = {
        'polymorphic_identity' : 'type',
        'polymorphic_on' : inherited
    }

    def __init__(
        self,
        id=None,
        inherited='type',
        generic=None,
        clasz_id=None,
        clasz=None
    ):
        self.id = id
        self.inherited = inherited
        self.generic = generic
        self.clasz = clasz
        self.clasz_id = clasz_id
        return
        
    def __dir__(self):
        return [
            'id',
            'generic',
            'clasz_id',
            'clasz'
        ]

