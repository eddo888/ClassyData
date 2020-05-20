#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import os, re, sys, argparse, json, datetime, xmltodict, inspect, importlib, uuid, logging

from Classes import *
from .Crown import Crown

import sqlalchemy
import sqlalchemy.orm

from Argumental.Argue import Argue
from Spanners.Squirrel import Squirrel
from Baubles.Logger import Logger

args = Argue()
squirrel = Squirrel()
logger = Logger()
logger.setLevel(logging.WARNING)

#____________________________________________________________
@args.command(single=True)
class Jester(object):
    '''
    Helper class for Classy types
    '''
    
    schemaURLs = dict(
        mysql= 'mysql+mysqlconnector://{username}:{password}@{hostname}/{database}',
        sqlite='sqlite:///{database}',
    )
   
    @args.property(short='v', flag=True, help='verbose logging')
    def verbose(self): return 
          
    @args.property(short='s', choices=list(schemaURLs.keys()), help='database schema type', default='sqlite')
    def schema(self): return
    
    @args.property(short='m', flag=True, help='make new schema')
    def make(self): return
    
    @args.property(short='n', help='database host', default='localhost')
    def hostname(self): return
    
    @args.property(short='u', help='database username', default='root')
    def username(self): return  
    
    @args.property(short='d', help='database name', default=':memory:')
    def database(self): return
 
    @args.property(short='p', help='database password')
    def password(self): return squirrel.get('%s:%s:%s'%(self.schema,self.hostname,self.username)) 
     
    #........................................................
    @logger.info
    def __init__(self,session=None):
        self.verbose = False

        if not session:
            keys=['username','password','hostname','database']
            schema = dict([(x,getattr(self,x)) for x in keys])
            url = self.schemaURLs[self.schema].format(**schema)
        
            crown = Crown(url, self.database, verbose=self.verbose)
            engine = crown.connect()
            self.session = crown.session()
        else:
            self.session = session
            
        self.now = datetime.datetime.now()
        self.dawnOfTime = datetime.datetime(1980,1,1,0,0,0,0)
        
        self.list = self._locateType(List)
        self.set  = self._locateType(Set)
        self.dep  = self._locateType(Depends)
        
        self.corePackage   = self._locatePackage('Fundamentals')
        self.sqlPackage    = self._locatePackage('SQL') 
        self.pythonPackage = self._locatePackage('Python')

        self.core = {}
        self.sql = {}
        self.python = {}

        for name, tipe in inspect.getmembers(sys.modules['sqlalchemy.types']):
            if name[0] == '_': continue
            if not inspect.isclass(tipe): continue
            if len(tipe.__bases__) == 0: continue
            parent = tipe.__bases__[0]
            
            if parent.__name__[0] == '_' \
            or parent.__name__ == 'object'\
            : continue
            
            parentClass = self._locateClass(
                name=parent.__name__,
                package=self.corePackage
            )
                
            self.core[parent.__name__] = parentClass
    
        self.session.commit()

        for name, tipe in inspect.getmembers(sys.modules['sqlalchemy.types']):
            if name[0] == '_': continue
            if not inspect.isclass(tipe): continue
            if len(tipe.__bases__) == 0: continue
            parent = tipe.__bases__[0]

            if parent.__name__[0] == '_' \
            or parent.__name__ == 'object'\
            : continue
            
            if name in list(self.core.keys()): continue
            
            parentClass= self._locateClass(
                name=parent.__name__,
                package=self.corePackage
            )
                
            clasz = self._locateClass(
                name=name,
                package=self.sqlPackage
            )

            self.sql[name] = clasz

        for name in ['Class','Module']:
            clasz = self._locateClass(
                name=name,
                package=self.pythonPackage
            )

            self.python[name] = clasz
            
        self.session.commit()

    #........................................................
    def close(self):
        if self.session: self.session.close()
    
    #........................................................
    def packageName(self,package,name=None):
        if package:
            if name:
                name = '%s.%s'%(package.name,name)
            else:
                name = package.name
            name = self.packageName(package.package,name)
        return name
    
    #........................................................
    def _get(self,tipe,id):
        return self.session.query(tipe).filter_by(id=id).first()
    
    #........................................................
    def _locatePackageClass(self,name,create=True):
        dots = re.split('[\.\/]',name)
        packageName = '.'.join(dots[:-1])
        className = dots[-1]
        package = self._locatePackage(packageName, create)
        clasz = self._locateClass(className, package, create)
        return clasz
    
    #........................................................
    def _locatePackage(self,name,create=True):
        parent=None
        package=None
        parts = []
        if name:
            parts = re.split('[\.\/]',name)
        for part in parts:
            package = self.session.query(Package).filter_by(name=part,package=parent).first()
            if not package and create:
                package = Package(
                    name=part,
                    fromDate=self.dawnOfTime,
                    modified=self.now,
                    package=parent
                )
                self.session.add(package)
                self.session.commit()
            parent=package
        return package
    
    #........................................................
    def _locateClass(self,name,package,create=True):
        clasz = self.session.query(Class).filter_by(name=name,package=package).first()
        if not clasz and create:
            clasz = Class(
                guid='%s'%uuid.uuid4(),
                name=name,
                package=package,
                fromDate=self.dawnOfTime,
                modified=self.now
            )
            self.session.add(clasz)
            self.session.commit()
        return clasz
    
    #........................................................
    def _locateNamedType(self,tipe,name, create=True):
        clasz = self.sesson.query(tipe).filter_by(name=name).first()
        if not clasz and create:
            clasz = tipe(name=name)
            self.session.add(clasz)
            self.session.commit()
        return clasz
    
    #........................................................
    def _locateType(self,tipe,create=True):
        clasz = self.session.query(tipe).first()
        if not clasz and create:
            clasz = tipe()
            self.session.add(clasz)
            self.session.commit()
        return clasz
    
    #........................................................
    def _resolve(self,name,package=None):
        clasz = None
        if hasattr(self, '_%s'%name):
            clasz = getattr(self,'_%s'%name)
        else:
            clasz = self._locateClass(name,package)
            setattr(self, '_%s'%name, clasz)
        return clasz
    
    #........................................................
    def heirarchy(self,clasz):
        claszes = []
        
        return claszes
    
    #........................................................
    def packages(self,package=None):
        pakages = []
        for pakage in self.session.query(Package).filter_by(package=package):
            pakages.append(pakage)
        return pakages
    
    #........................................................
    def classes(self,package):
        claszes = []
        for clasz in self.session.query(Class).filter_by(package=package):
            claszes.append(clasz)
        return claszes

    #........................................................
    def names(self):
        names = {}
        for package in self.packages():
            names[package.name] = []
            for clasz in self.classes(package):
                names[package.name].append(clasz.name)
        return names

#____________________________________________________________
if __name__ == '__main__': args.execute()

