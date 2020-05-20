#!/usr/bin/env python3

'''
Created on 12/01/2015

@author: dedson
'''

import uuid

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
class Version(Base):
    '''
    The Version class stores the class version history allowing historical views of a class to be stored, searched and used.
    '''

    __tablename__ = 'version'
    id            = Column(Integer, primary_key=True)
    guid          = Column(String(256))
    inherited     = Column(String(256))
    version       = Column(String(256))
    fromDate      = Column(DateTime())
    toDate        = Column(DateTime())
    modified      = Column(DateTime())
    
    __mapper_args__ = {
        'polymorphic_identity' : 'version',
        'polymorphic_on' : inherited
    }

    def __init__(self,
        id=None,
        guid=None,
        inherited='version',
        version=None,
        fromDate=None,
        toDate=None,
        modified=None
    ):
        self.id = id
        if not guid:
            self.guid = '%s'%uuid.uuid4()
        else:
            self.guid = guid
        self.inherited = inherited
        self.version = version
        self.fromDate = fromDate
        self.toDate = toDate
        self.modified = modified
        return
      
    def __dir__(self):
        return [
            'id',
            'guid',
            'version',
            'fromDate',
            'toDate',
            'modified'
        ]

