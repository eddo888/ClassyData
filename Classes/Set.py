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

from .Generic import Generic

from jsonweb.encode import to_object
from jsonweb.decode import from_object

@from_object()
@to_object()
class Set(Generic):
    '''
    The Set class is a generic list that has a dict lookup key attribute.
    '''

    __tablename__ = 'set'
    id            = Column(Integer, ForeignKey('generic.id'), primary_key=True)
    key           = Column(String(256))

    __mapper_args__ = {
        'polymorphic_identity':'set'
    }
    
    def __init__(
        self,
        id=None,
        inherited='set',
        key=None
    ):
        super(Set,self).__init__(
            id=id,
            inherited=inherited
        )
        self.key = key
        return

    def __dir__(self):
        return Generic.__dir__(self) + [
            'key'
        ]


