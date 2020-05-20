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
class Attribute(Type):
    '''
    The Attribute class defines a link to a contained attribute or a referenced attribute. If an attribute is a reference it is a guid link to another class table.
    '''

    __tablename__ = 'attribute'
    id            = Column(Integer, ForeignKey('type.id'), primary_key=True)
    class_id      = Column(Integer, ForeignKey('class.id'))
    name          = Column(String(256))
    reference     = Column(Boolean())
    
    __mapper_args__ = {
        'polymorphic_identity':'attribute'
    }

    def __init__(
        self,
        id=None,
        inherited='attribute',
        generic=None,
        clasz_id=None,
        clasz=None,
        name=None,
        reference=False
    ):
        super(Attribute,self).__init__(
            id=id,
            inherited=inherited,
            generic=generic,
            clasz_id=clasz_id,
            clasz=clasz
        )
        self.name = name
        self.reference = reference
        return
    
    def __dir__(self):
        return Type.__dir__(self) + [
            'name',
            'reference'
        ]

