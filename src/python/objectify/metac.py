#!/usr/bin/python2
import uuid
import log
from collections import defaultdict

coerce_list = defaultdict(list)
coerce_list['int'].append('double')
coerce_list['double'].append('int')

def coerce(typefrom, typeto):
    """returns boolean indicating whether type is coercible to other type"""

    logger = log.setup_custom_logger(__name__)
    coercible = False
    result = 'failed'
    if typefrom in coerce_list:
        if typeto in coerce_list[typefrom]:
            coercible = True
    if coercible:
        result = 'succeeded'
    logger.info('Cast from \'%s\' to \'%s\' %s' % (typefrom, typeto, result))
    return coercible


class MetaItem(object):
    """base C item"""

    def __init__(self, name, fileName):
        self.name = name
        self.uuid = uuid.uuid4()
        self.fileName = fileName

class Type(object):
    """represent a C type"""

    def __init__(self, typeName):
        self.typeName = typeName

class Variable(MetaItem,Type):
    """represent a C variable"""
    def __init__(self, varType, name):
        MetaItem.__init__(self,name)
        Type.__init__(self,varType)


class Struct(MetaItem):
    """represent a C struct"""
    def __init__(self,name, fileName):
        MetaItem.__init__(self,name, fileName)
        self.fields = []
        self.fileName = fileName

class Function(Variable,MetaItem):
    """represent a C function"""
    def __init__(self, returnType, name, fileName):
        MetaItem.__init__(self,name, fileName)
        self.returnType = Type(returnType)
        self.arguments = []
