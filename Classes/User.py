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
class User(Accessor):
    '''
    A User class is an accessor sub class used to define a user access permission.
    '''

    __tablename__ = 'user'
    id            = Column(Integer, ForeignKey('accessor.id'), primary_key=True)
    name          = Column(String(256))
    md5           = Column(String(256))
    
    __mapper_args__ = {
        'polymorphic_identity':'user'
    }
    
    def __init__(
        self,
        id=None,
        inherited='user',
        name=None,
        md5=None,
        access_id=None
    ):
        super(Accessor,self).__init__(
            id=id,
            inherited=inherited,
            access_id=access_id
        )
        self.name = name
        self.md5 = md5
        return

    def __dir__(self):
        return Accessor.__dir__(self) + [
            'name',
            'md5',
        ]

