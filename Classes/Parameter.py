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

from .Type import Type

from jsonweb.encode import to_object
from jsonweb.decode import from_object

@from_object()
@to_object(suppress=['clasz'])
class Parameter(Type):
    '''
    The Parameter class defineds a method parameter that is passed by name, it is stored in the Method as a dictionary.
    '''

    __tablename__ = 'parameter'
    id            = Column(Integer, ForeignKey('type.id'), primary_key=True)
    method_id     = Column(Integer, ForeignKey('method.id'))
    name          = Column(String(256))
    
    __mapper_args__ = {
        'polymorphic_identity':'parameter'
    }

    def __init__(
        self,
        id=None,
        inherited='parameter',
        generic=None,
        clasz_id=None,
        clasz=None,
        name=None
    ):
        super(Parameter,self).__init__(
            id=id,
            inherited=inherited,
            generic=generic,
            clasz_id=clasz_id,
            clasz=clasz
        )
        self.name = name
        return
    
    def __dir__(self):
        return Type.__dir__(self) + [
            'name'
        ]

