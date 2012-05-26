#!/usr/bin/python2
import uuid

class CppObj(object):
	"""base C++ candidate object"""

	def __init__(self, name, fileName):
		self.name = name
		self.uuid = uuid.uuid4()
		self.fileName = fileName 
