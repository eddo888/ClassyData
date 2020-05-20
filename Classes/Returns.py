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
class Returns(Type):
    '''
    The Returns class defines a return structure for a class method.
    '''

    __tablename__ = 'returns'
    id            = Column(Integer, ForeignKey('type.id'), primary_key=True)
    method_id     = Column(Integer, ForeignKey('method.id'))

    __mapper_args__ = {
        'polymorphic_identity':'returns'
    }

    def __init__(
        self,
        id=None,
        inherited='returns',
        generic=None,
        clasz_id=None,
        clasz=None
    ):
        super(Returns,self).__init__(
            id=id,
            inherited=inherited,
            generic=generic,
            clasz_id=clasz_id,
            clasz=clasz
        )
        return
    
    def __dir__(self):
        return Type.__dir__(self) + [
        ]

