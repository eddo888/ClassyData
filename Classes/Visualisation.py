#!/usr/bin/env python3

'''
Created on 12/01/2015

@author: dedson
'''

import sqlalchemy
import sqlalchemy.orm

from sqlalchemy import Column, Integer, String, DateTime, Boolean, CLOB, ForeignKey
from sqlalchemy.engine import reflection
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.collections import InstrumentedList, InstrumentedDict, InstrumentedSet

from .Base import Base

from .Version import Version

from jsonweb.encode import to_object
from jsonweb.decode import from_object

@from_object()
@to_object()
class Visualisation(Version):
    '''
    The Visualisation class is used to allow an entity to have a human readable title and description. The description field may be populated with the __doc__ property.
    '''

    __tablename__ = 'visualisation'
    id            = Column(Integer, ForeignKey('version.id'), primary_key=True)
    display       = Column(String(256))
    robes         = Column(String(256))
    description   = Column(String(2048))
    isLabel       = Column(Boolean())

    __mapper_args__ = {
        'polymorphic_identity':'visualisation',
    }
    
    def __init__(
        self,
        id=None,
        guid=None,
        inherited='visualisation',
        version=None,
        fromDate=None,
        toDate=None,
        modified=None,
        display=None,
        robes=None,
        description=None,
        isLabel=None
    ):
        super(Version,self).__init__(
            id=id,
            guid=guid,
            inherited=inherited,
            version=version,
            fromDate=fromDate,
            toDate=toDate,
            modified=modified
        )
        self.display = display
        self.robes = robes
        self.description = description
        self.isLabel = isLabel
        return

    def __dir__(self):
        return Version.__dir__(self) + [
            'display',
            'robes',
            'description',
            'isLabel',
        ]

