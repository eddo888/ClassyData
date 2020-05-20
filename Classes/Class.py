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

from .Access import Access
from .Attribute import Attribute
from .Method import Method

from jsonweb.encode import to_object
from jsonweb.decode import from_object

@from_object()
@to_object(suppress=['parent'])
class Class(Access):
    '''
    The Class class represents an entity, the entity can have attributes, methods and the class may inherit from a parent. Classses are contained in a Package for grouping.
    '''

    __tablename__ = 'class'
    id            = Column(Integer, ForeignKey('access.id'), primary_key=True)
    name          = Column(String(256))
    abstract      = Column(Boolean())
    attributes    = relationship("Attribute", uselist=True, foreign_keys=[Attribute.class_id])
    methods       = relationship("Method", uselist=True, foreign_keys=[Method.class_id])
    parent_id     = Column(Integer, ForeignKey('class.id'))
    parent        = relationship("Class", uselist=False, foreign_keys=[parent_id], remote_side=[id])
    package_id    = Column(Integer,ForeignKey('package.id'))
    package       = relationship("Package", uselist=False, foreign_keys=[package_id])
    
    def __init__(
        self,
        id=None,
        guid=None,
        inherited='class',
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
        name=None,
        abstract=False,
        attributes=[],
        methods=[],
        parent=None,
        package=None,
        package_id=None
    ):
        super(Class,self).__init__(
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
            modifiers=modifiers
        )
        self.name = name
        self.abstract = abstract
        self.attributes = attributes
        self.methods = methods
        self.parent = parent
        if package_id:
            self.package_id = package_id
        else:
            self.package = package
        return

    __mapper_args__ = {
        'polymorphic_identity':'class'
    }
    
    def __dir__(self):
        return Access.__dir__(self) + [
            'name',
            'abstract',
            'attributes',
            'methods',
            'parent_id',
            'parent',
            'package_id',
            'package'
        ]

    def fullname(self):
        if self.package:
            return '%s.%s'%(self.package.fullname(), self.name)
        return self.name
    

