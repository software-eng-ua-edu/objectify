#!/usr/bin/python2
import sqlite3
from os.path import exists
from contextlib import contextmanager
from contextlib import closing
import log
import os

db_location = os.path.join(os.getcwd(), "objectify.sqlite")

class Sqlite(object):
    def __init__(self):
        self.logger = log.setup_custom_logger(__name__)

    def execute_atomic(self, command, values):
	"""Execute command using supplied list of tuples; if values is empty, run command only"""
        conn = self.get_conn()
        with closing(conn.cursor()) as cursor:
            self.logger.debug("Executing command '%s'" % (command))
	    if val_length == 0:
		cursor.execute(command)
            elif val_length == 1:
                cursor.execute(command, values)
            else:
                cursor.executemany(command,values)
            conn.commit() 


    def create_table(self, name, columns):
        """Create a table (if it doesn't already exist) based on input; name is a string name; columns is a tuple of the form: column_name column_type, ...)"""
        try:
            command = "CREATE TABLE IF NOT EXISTS %s (%s)" % (name, ",".join(columns))
            self.logger.debug("Creating table with statement '%s'" % command)
            self.execute_atomic(command)
            self.logger.debug("Created table %s, or table already existed." % (name))
        except sqlite3.OperationalError:
            self.logger.exception("Unable to create table %s." % (name))
        except:
            self.logger.exception("Unexpected error.")


    def insert_rows(self, tablename, values):
        """Insert a row into the table name you supply. Values is a list of tuples with values in column order"""
        val_length = len(values)
        if val_length == 0:
		self.logger.info("No values to insert. Returning...")
        #placeholder for query 
        placeholder = "?"
        #generate the correct number of '?' for parameter substitution using the length of the list 
        placeholders = ",".join(placeholder*len(values[0]))
        print values
        command = "INSERT INTO %s VALUES (%s)" % (tablename, placeholders)
        self.logger.debug("Inserting values into %s with command '%s'" % (tablename, command))


    def list_all_tables(self):
        """Print list of all tables in database"""
        conn = self.get_conn()
        with closing(conn.cursor()) as cursor:
            cursor.execute('select * from sqlite_master')
            for row in cursor:
                print row 


    def get_conn(self):
        location = db_location
        """Return sqlite3 connection"""
        try:
            conn = sqlite3.connect(location)
            self.logger.debug("Database connection established to %s" % location)
            return conn
        except sqlite3.DatabaseError:
            self.logger.exception("Unable to open database: %s" % (location))
