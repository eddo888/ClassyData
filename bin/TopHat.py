#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import os, re, sys, argparse, json, datetime, xmltodict, uuid, logging

sys.path.append('..')

from Classes import *
from Handlers import Jester, args

from io import StringIO

import sqlalchemy
import sqlalchemy.orm

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.engine import reflection
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.collections import InstrumentedList, InstrumentedDict, InstrumentedSet

from Baubles.Logger import Logger
from Perdy.pretty import prettyPrintLn, Style

from jsonweb.encode import dumper
from jsonweb.decode import loader

logger = Logger()

def quiet():
	for name in [
		'sqlalchemy.pool.impl.QueuePool',
   		'boto3.resources.action',
   		'boto3.resources.factory',
   		'botocore.auth',
   		'botocore.client',
   		'botocore.credentials',
   		'botocore.endpoint',
   		'botocore.hooks',
   		'botocore.utils',
   		'botocore.httpsession',
   		'botocore.loaders',
   		'botocore.parsers',
   		'botocore.retryhandler',
   		'sqlalchemy.pool.impl.NullPool',
   		'sqlalchemy.pool.impl.SingletonThreadPool',
   		'urllib3.connectionpool',
		'sqlalchemy.engine.base.Engine',
		'sqlalchemy.engine.Engine',
		'sqlalchemy.pool.NullPool',
		'sqlalchemy.pool.SingletonThreadPool',
	]:
		logging.getLogger(name).setLevel(logging.ERROR)
quiet()

#____________________________________________________________
@args.command(single=True)
class TopHat(Jester):
	
	def __init__(self):
		super().__init__()
	

	#........................................................
	@logger.info
	@args.operation
	def insert(self):
		parentPackage = Package(name="MyPackage")
		childPackage = Package(name='MyChildPackage',package=parentPackage)
		
		group = Group(name='MyGroup')
		self.session.add(group)
		
		user = User(name='MyUser',md5='abc123')
		self.session.add(user)
		
		enum = Enum(name='MyEnum',package=childPackage)
		enum.version = 'v1.0'
		enum.description = 'My Enumeration of one and two'
		enum.path = 'access path for enum'
		enum.addValue('one')
		enum.addValue('two')
		self.session.add(enum)
		self.session.commit()
		
		myBase = Class(
			name='MyBase',
			robes='Class',
			description='Base Class', 
			package=parentPackage,
			attributes = [
				Attribute(
					name='parentAttr',
					clasz=self.core['String']
				)
			],
		   methods = [
				Method(
					name='parentMethod',
					parameters = {
						'p1' : Parameter(
							name='p1',
							clasz=self.core['String']
						)
					},
					returns = Returns(
						clasz=self.core['String']
					),
					logic='return "hello";'
				)
			]
		)
		self.session.add(myBase)
		self.session.commit()
		
		clasz = Class(name="MyClass", package=childPackage, parent=myBase)
		clasz.version = 'v1.0'
		clasz.path = 'myPath'
		clasz.display = 'myDisplay'
		clasz.robes = 'Entity'
		clasz.description = 'this is a class that is stored as metadata in the mysql db'
		clasz.isLabel = False
		clasz.fromDate = datetime.datetime(2015,1,1,0,0,0,0)
		clasz.toDate = datetime.datetime(2015,12,31,23,59,59,0)
		clasz.modified = datetime.datetime.now()
		clasz.accessors.append(group)
		clasz.accessors.append(user)
		self.session.add(clasz)	
	
		list = List()
		attr = Attribute(generic=list,clasz=self.core['String'], name='myAttr')
		self.session.add(attr)
		clasz.attributes.append(attr)
		
		enumattr = Attribute(clasz=enum,name='myEnum')
		self.session.add(enumattr)
		clasz.attributes.append(enumattr)
		
		set = Set(key='name')
		rtrn = Returns(generic=set,clasz=self.core['Integer'])
		self.session.add(rtrn)
	   
		parm = Parameter(generic=None,clasz=self.core['Boolean'], name='myParam')
		self.session.add(parm)
	   
		mthd = Method(
			name='myMethod',
			logic='return -1;'
		)
		mthd.parameters[parm.name] = parm
		mthd.returns = rtrn
		self.session.add(mthd)
		clasz.methods.append(mthd)
	
		self.session.commit()
		
		js_class = json.loads(dumper(clasz)) 
		if self.verbose:
			sys.stdout.write(js_class)
	
		return clasz
	

	#........................................................
	@logger.info
	@args.operation
	@args.parameter(name='query', help='package:class')
	def query(self,query,output=sys.stdout):
		(pname,cname) = query.split(':')
		package = self._locatePackage(pname)
		clasz = self._locateClass(cname,package)
		return clasz


	#........................................................
	@logger.info
	@args.operation
	@args.parameter(name='id', help='id of class')
	def get(self, id):
		clasz = self._locatePackageClass(id, create=False)
		return clasz
		

	#........................................................
	@args.operation(name='packages')
	@args.parameter(name='query', help='name for children, *=root')
	def getPackages(self, query):
		if query == '*':
			parent = None
		else:
			parent = self._locatePackage(query)
		names = []
		for pkg in self.packages(parent):
			names.append(self.packageName(pkg))
		return names


	#........................................................
	@args.operation(name='classes')
	@args.parameter(name='query', help='package name')
	def getClasses(self, query):
		package = self._locatePackage(query)
		names = [x.name for x in self.classes(package)]
		return names


	#........................................................
	@args.operation(name='list')
	def getList(self):
		return self.names()


#____________________________________________________________
if __name__ == '__main__': 
	result = args.execute()
	if result:
		prettyPrintLn(result, ignore=True)



