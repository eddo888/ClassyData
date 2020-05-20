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

from .Accessor import Accessor

from jsonweb.encode import to_object
from jsonweb.decode import from_object

@from_object()
@to_object()
class Group(Accessor):
    '''
    The Group class defines a named list of users who may access the class, method or attribute.
    '''

    __tablename__ = 'group'
    id            = Column(Integer, ForeignKey('accessor.id'), primary_key=True)
    name          = Column(String(256))
    
    __mapper_args__ = {
        'polymorphic_identity':'group'
    }
    
    def __init__(
        self,
        id=None,
        inherited='group',
        name=None,
        access_id=None
    ):
        super(Accessor,self).__init__(
            id=id,
            inherited=inherited,
            name=name,
            access_id=access_id
        )
        self.name = name
        return

    def __dir__(self):
        return Accessor.__dir__(self) + [
            'name',
        ]

