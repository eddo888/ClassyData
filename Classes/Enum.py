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

from .Class import Class
from .Access import Access

@from_object()
@to_object()
class Enum(Class):
    '''
    An Enum class stores an enumeration in a comma seperated values list. Helper methods exist to add/list enum values.
    '''

    __tablename__ = 'enum'
    id            = Column(Integer, ForeignKey('class.id'), primary_key=True)
    #name         # borrowed from Class
    values        = Column(String(1024))  # comma seperated enum list of options
       
    __mapper_args__ = {
        'polymorphic_identity' : 'enum',
    }
        
    def __init__(
        self,
        id=None,
        guid=None,
        inherited='enum',
        version=None,
        fromDate=None,
        toDate=None,
        modified=None,
        display=None,
        robes=None,
        description=None,
        isLabel=None,
        path=None,
        modifiers=None,
        package=None,
        name=None,
        abstract=False,
        values=''
    ):
        super(Enum,self).__init__(
            id=id,
            guid=guid,
            inherited=inherited,
            version=version,
            fromDate=fromDate,
            toDate=toDate,
            modified=modified,
            display=display,
            robes=robes,
            description=description,
            isLabel=isLabel,
            path=path,
            modifiers=modifiers,
            package=package,
            name=name,
            abstract=abstract
        )
        self.id = id
        self.values = values
        return
    
    def __dir__(self):
        ''' don't export class attributes, skip over to Accessor ones '''
        return Access.__dir__(self) + [
            'name',
            'package',
            'values',
        ]

    def getValues(self):
        return self.values.split(',')
    
    def addValue(self,value):
        if len(self.values) == 0:
            values = []
        else:
            values = self.values.split(',')
        if not value in values:
            values.append(value)
        self.values = ','.join(values)
        return
     

