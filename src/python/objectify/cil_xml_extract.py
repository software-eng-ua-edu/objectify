#!/usr/bin/python2
from lxml import etree
import util
import os
import metac
import os.path
import log

class CilExtract(object):
  def __init__(self):
    self.logger = log.setup_custom_logger(__name__)

  def extract(self, input, cilPath):
    """Extract metac objects from XML"""
    self.structs = []
    self.functions = []
    if os.path.isdir(input):
        for root, dirs, files in os.walk(input):
          #excludes files that don't end in .cilxml
          files = [fi for fi in files if fi.endswith(".cilxml")]
          for xmlfile in files:
              xmlPath = os.path.join(root,xmlfile)
              openFile = open(xmlPath)
              self.simple_parse_file(etree.parse(openFile), xmlPath)
    else:
      result, data = util.myrun([cilPath] +  [input] + ["--disallowDuplication", "--noLowerConstants", "--noInsertImplicitCasts", "--dowritexml"])
      name = '%s.xml' % (os.path.splitext(input)[0]) 
      self.simple_parse_file(etree.parse(open(name)), input)

  def simple_parse_file(self, input, name):
    """Load functions and structs for the provided file"""
    root = input.getroot()
    self.parse_functions(root.findall('functionDefinition'), name)
    self.parse_structs(root.findall('compositeTagDefinition'), name)


  def print_summary(self):
    """Print simple summary of functions and structs per file"""
    for i in self.structs:
      for f in i.fields:
          self.logger.debug("Struct: {0} -> func ptr field: {1} {2} {3}".format(i.name, f.returnType.typeName, f.name, f.fileName))
          for p in f.arguments:
             self.logger.debug("param: %s %s" % (p.typeName, p.name))

    for i in self.functions:
      self.logger.debug("Function: {0} -> type: {1}".format(i.name, i.returnType.typeName))
    


  def parse_functions(self, input, fileName):
    """Parse and load functions from XML"""
    funcDefs = input
    for i in funcDefs:
      returnType = i.find('type/result/type')
      self.functions.append(metac.Function(returnType.attrib.get('kind'), i.get('name'), fileName))
    return
 

  def parse_structs(self, input, fileName):
    """Parse and load structs from XML"""
    ctds = input  
    for i in ctds:
      if(i.attrib.has_key('kind')):
        if(i.get('kind') == 'struct'):
          self.parse_ptrs(i.findall('fieldDeclaration'), i.get('name'), fileName)
    return 
 

  def parse_ptrs(self, input, name, fileName):      
    """Parse and load function pointers in a struct"""
    fieldDecs = input
    struct = metac.Struct(name, fileName)
    for fieldDec in fieldDecs:
      tp = fieldDec.find('type')
      tp2 = tp.find('type')
      if (tp.get('kind') == 'pointer'):
       if (tp2.attrib['kind'] == 'function'):
         f = metac.Function(tp2.attrib['kind'], fieldDec.attrib['name'], fileName)
         returnType = fieldDec.find('type/result/type')
         if returnType is not None:
           self.logger.info(returnType.get('kind'))
           for i in fieldDec.findall('parameter'):
             self.logger.info("parameters: %s" % (i))
             f.arguments.append(metac.Variable(i,i))
      struct.fields.append(metac.Function(tp2.attrib['kind'], fieldDec.attrib['name'], fileName))

    self.structs.append(struct)
