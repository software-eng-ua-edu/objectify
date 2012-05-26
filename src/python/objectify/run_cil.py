#!/usr/bin/python2
import os.path
from os.path import exists
import log
import util
#import argparse

cilArgs = ["--disallowDuplication", "--noLowerConstants", "--noInsertImplicitCasts", "--dowritexml"]

def ctoxml(filePath, cilPath):
    logger = log.setup_custom_logger(__name__)
    logger.debug("Using CIL executable located at %s" % (cilPath))
    if os.path.isdir(filePath):
        for root, dirs, files in os.walk(filePath):
          #excludes files that don't end in .c
          files = [fi for fi in files if fi.endswith(".c")]
          for cfile in files:
            fileName = os.path.abspath(os.path.join(root,cfile))
            xmlName = "%s.xml" % (os.path.splitext(cfile)[0]) 
            #if the generated XML exists, do not re-run CIL on the C file
            if not exists(xmlName): 
              logger.info("Running CIL on %s" % (fileName))
              result, data = util.myrun([cilPath] +  [fileName] + cilArgs)
              if result:
                  logger.error("CIL processing of %s failed: %s" % (fileName, data))
                  break
              cXmlName= os.path.join(root,xmlName)
              logger.debug("Writing results of CIL processing to %s" % (cXmlName))
              util.writefile(cXmlName, data)
    else:
      result, data = util.myrun([cilPath] +  [filePath] + cilArgs)
      logger.debug("Writing results of CIL proceesing to %s" % (cXmlName))
      til.writefile(cXmlName, data)

if __name__ == "__main__":
  import sys
  logger = log.setup_custom_logger("run_cil")
  #parser = argparse.ArgumentParser(description='Runs CIL to convert C to XML.')
  #parser.add_argument ('-p', action="store", dest="path")
  #parser.add_argument ('-c', action="store", dest="cil")
  #args = parser.parse_args()
  ctoxml(str(sys.argv[1]), str(sys.argv[2]))
