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
from sqlalchemy.orm.collections import InstrumentedList, InstrumentedDict, InstrumentedSet, attribute_mapped_collection

from .Base import Base

from .Access import Access

from jsonweb.encode import to_object
from jsonweb.decode import from_object

@from_object()
@to_object()
class Method(Access):
    '''
    The Method class defines a method of the entity that may be called. It is an entry point to allow web services to access a class. It is also there to allow an implementation of the functionality by executing some code under that method.
    '''

    __tablename__ = 'method'
    id            = Column(Integer, ForeignKey('access.id'), primary_key=True)
    class_id      = Column(Integer, ForeignKey('class.id'))
    name          = Column(String(256))
    produces      = Column(String(256)) # todo list of enums
    consumes      = Column(String(256)) # todo list of enums
    parameters    = relationship("Parameter", collection_class=attribute_mapped_collection('name'), cascade="all, delete-orphan")
    logic         = Column(String(2048))
    returns       = relationship("Returns", uselist=False)

    __mapper_args__ = {
        'polymorphic_identity':'method'
    }
    
    def __init__(
        self,
        id=None,
        guid=None,
        inherited='method',
        version=None,
        fromDate=None,
        toDate=None,
        modified=None,
        display=None,
        description=None,
        isLabel=None,
        path=None,
        modifiers=None,
        name=None,
        produces=None,
        consumes=None,
        parameters={},
        logic=None,
        returns=None
    ):
        super(Method,self).__init__(
            id=id,
            guid=guid,
            inherited=inherited,
            version=version,
            fromDate=fromDate,
            toDate=toDate,
            modified=modified,
            display=display,
            description=description,
            isLabel=isLabel,
            path=path,
            modifiers=modifiers
        )
        self.name = name
        self.produces = produces
        self.consumes = consumes
        self.parameters = parameters
        self.logic = logic
        self.returns = returns    
        return


    def __dir__(self):
        return Access.__dir__(self) + [
            'name',
            'consumes',
            'produces',
            'parameters',
            'logic',
            'returns',
        ]

