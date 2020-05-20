#!/usr/bin/env python3

'''
Created on 12/01/2015

@author: dedson
'''

import sqlalchemy
import sqlalchemy.orm

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.engine import reflection
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.collections import InstrumentedList, InstrumentedDict, InstrumentedSet

from .Base import Base

from jsonweb.encode import to_object
from jsonweb.decode import from_object

@from_object()
@to_object()
class Generic(Base):
    '''
    The Generic class is used to make an attribute or property a list or a set of values. If an Attribute or Property has an null generic, it is a single item.
    '''

    __tablename__ = 'generic'
    id            = Column(Integer, primary_key=True)
    inherited     = Column(String(256))
        
    __mapper_args__ = {
        'polymorphic_identity' : 'generic',
        'polymorphic_on' : inherited
    }
        
    def __init__(
        self,
        id=None,
        inherited='generic'
    ):
        self.id = id
        self.inherited = inherited
        return
    
    def __dir__(self):
        return [
            'id',
        ]

