#!/usr/bin/python2
import cil_xml_extract
import ooc
import log
import argparse
import sys, os

def objectify(structs, functions):
    logger = log.setup_custom_logger(__name__)
    #for (index, item) in enumerate(structs):
    #for (index, item) in enumerate(functions):
    for struct in structs:
        logger.debug("struct {0}:{1} has {2} fields".format(struct.fileName, struct.name, len(struct.fields)))
        for function in functions:
            logger.debug("function {0}:{1} has {2} arguments".format(function.fileName, function.name, len(function.arguments)))
            if len(struct.fields) == len(function.arguments):
                logger.info("Struct {0}:{1} and Function {2}:{3} have matching field/argument lengths".format(struct.fileName, struct.name, function.fileName, function.name))


if __name__ == "__main__":
  logger = log.setup_custom_logger(__name__)
  parser = argparse.ArgumentParser(description='Runs metac compliant XML processor.')
  parser.add_argument ('-p', action="store", dest="path")
  parser.add_argument ('-c', action="store", dest="cil")
  args = parser.parse_args()
  ex = cil_extract.CilExtract()
  ex.extract(args.path, args.cil)
  objects = objectify(ex.structs, ex.functions);
