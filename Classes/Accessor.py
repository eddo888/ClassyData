#!/usr/bin/env python3

'''
Created on 12/01/2015

@author: dedson
'''


import sqlalchemy
import sqlalchemy.orm

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.engine import reflection
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.collections import InstrumentedList, InstrumentedDict, InstrumentedSet

from .Base import Base

from jsonweb.encode import to_object
from jsonweb.decode import from_object

@from_object()
@to_object()
class Accessor(Base):
    '''
    The Accessor class is a base class used to represent either a group or a user who may access a function or class
    '''
    
    __tablename__ = 'accessor'
    id            = Column(Integer, primary_key=True)
    inherited     = Column(String(256))
    access_id     = Column(Integer, ForeignKey('access.id'))
    
    __mapper_args__ = {
        'polymorphic_identity' : 'accessor',
        'polymorphic_on' : inherited
    }

    def __init__(
        self,
        id=None,
        inherited='accessor',
        access_id=None,
        access=None
    ):
        self.id = id
        if access:
            self.access_id = access.id
        else:
            self.access_id = access_id
        self.inherited = inherited
        return
      
    def __dir__(self):
        return [
            'id'
        ]

