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
class Depends(Generic):
    '''
    The Depends class defines a dependency relationship.
    '''

    __tablename__ = 'depends'
    id            = Column(Integer, ForeignKey('generic.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'depends'
    }
    
    def __init__(
        self,
        id=None,
        inherited='depends'
    ):
        super(Depends,self).__init__(
            id=id,
            inherited=inherited
        )
        return

    def __dir__(self):
        return Generic.__dir__(self) + [
        ]


