#!/usr/bin/env python3

import os, re, sys, json, datetime, xmltodict, inspect

from io import StringIO

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.orm import sessionmaker, scoped_session

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.engine import reflection
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.collections import InstrumentedList, InstrumentedDict, InstrumentedSet

from Baubles.Logger import Logger
logger = Logger()

from Classes import *

#____________________________________________________________
class Crown(object):

    @logger.info
    def __init__(self, url, database, verbose=False):
        self.database = database
        self.engine = None
        self.factory = None
        self.verbose = verbose
        self.url = url
        return

    #........................................................
    @logger.info
    def create(self):
        url = self.url.replace('/%s'%self.database,'')
        engine = sqlalchemy.create_engine(url, echo=self.verbose)
        for dbr in engine.execute('show databases'):
            if '%s'%dbr[0] == self.database:
                sys.stderr.write('dropping %s\n'%self.database)
                engine.execute('drop database %s'%self.database)
        sys.stderr.write('creating %s\n'%self.database) 
        engine.execute('create database %s'%self.database)
        engine.execute('use %s'%self.database)
        del engine
        return

    #........................................................
    def connect(self):
        self.engine = sqlalchemy.create_engine(self.url, echo=self.verbose)
        try:
            Base.metadata.create_all(self.engine)
        except:
            logger.error('using cached Base')
        self.factory = scoped_session(
            sessionmaker(
                autoflush=False,
                autocommit=False,
                bind=self.engine
            )
        )
        return self.engine

    #........................................................
    def session(self):
        return self.factory()

    #........................................................
    @logger.info
    def reflect(self):
        inspector = reflection.Inspector.from_engine(self.engine)
        sys.stderr.write('%s\n'%inspector)
        for table in inspector.get_table_names():
            sys.stderr.write('%s\n'%table)
            for column in inspector.get_columns(table):
                sys.stderr.write('\t%s : %s\n'%(column['name'], column['type']))
            for relates in inspector.get_foreign_keys(table):
                sys.stderr.write('\tRelation:\n')
                for key in list(relates.keys()):
                    sys.stderr.write('\t\t%s : %s\n'%(key,relates[key]))
        return #todo XSD format, to be JSONified

    #........................................................
    def disconnect(self):
        self.factory.remove()
        
#____________________________________________________________

