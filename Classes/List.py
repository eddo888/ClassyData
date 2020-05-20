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
class List(Generic):
    '''
    The List class defines a templated generic list of objects.
    '''

    __tablename__ = 'list'
    id            = Column(Integer, ForeignKey('generic.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'list'
    }
    
    def __init__(
        self,
        id=None,
        inherited='list'
    ):
        super(List,self).__init__(
            id=id,
            inherited=inherited
        )
        return

    def __dir__(self):
        return Generic.__dir__(self) + [
        ]


