#!/usr/bin/python

from pysqlite2 import dbapi2 as sqlite
import os, sys, logging
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from logging import info, debug, warning, error, critical
from urlparse import urlparse


class Database:
    CREATE_QUERY = "CREATE TABLE pairs ( key VARCHAR(64), value VARCHAR(64) )"
    INSERT_QUERY = "INSERT INTO pairs VALUES ( ?, ? )"
    UPDATE_QUERY = "UPDATE pairs SET value=? WHERE key=?"
    SELECT_QUERY = "SELECT * FROM pairs WHERE key=?"
    DELETE_QUERY = "DELETE FROM pairs WHERE key=?"

    def __init__(self, filename):
        self.dbfile = filename
        self.initDB()

    def initDB(self):
        info("Creating Database connection")
        alreadyExists = os.path.exists(self.dbfile)
        self.connection = sqlite.connect(self.dbfile)
        if not alreadyExists:
            info("Creating pairs table in database")
            cursor = self.connection.cursor()
            cursor.execute( self.CREATE_QUERY )
            self.connection.commit()
            cursor.close()

    def close(self):
        info("Closing database")
        self.connection.close()

    def post(self, key, value):
        info("Database: executing insert query for key %s value %s" % (key, value))
        cursor = self.connection.cursor()
        cursor.execute( self.INSERT_QUERY, (key, value) )
        self.connection.commit()
        cursor.close()

    def get(self, key):
        info("Database: executing select query for key %s" % key)
        cursor = self.connection.cursor()
        cursor.execute( self.SELECT_QUERY, (key, ) )
        self.connection.commit()
        results = cursor.fetchall()
        cursor.close()
        return results

    def put(self, key, value):
        info("Database: executing update query for key %s value %s" % (key, value))
        cursor = self.connection.cursor()
        cursor.execute( self.UPDATE_QUERY, (value, key) )
        self.connection.commit()
        cursor.close()

    def delete(self, key):
        info("Database: executing delete query for key %s" % key)
        cursor = self.connection.cursor()
        cursor.execute( self.DELETE_QUERY, (key, ) )
        self.connection.commit()
        cursor.close()


class Handler(BaseHTTPRequestHandler):
    def urlParse(self, url):
        info("parsing url %s", url)
        urlp = urlparse(url)
        vals = dict()
        for part in urlp[4].split('&'):
            splits = part.split('=')
            if len(splits) == 2:
                vals[splits[0]]=splits[1]
        return urlp[2], vals

    def do_POST(self):
        path, vals = self.urlParse(self.path)
        global DB
        DB.post(path, vals.get("value", ""))
        self.send_response(200)
        self.end_headers()
        self.wfile.write("OK\n")

    def do_GET(self):
        path, vals = self.urlParse(self.path)
        global DB
        self.send_response(200)
        self.end_headers()
        res = DB.get(path)
        info(res)
        for row in res:
            self.wfile.write("%s\n" % row[1])

    def do_PUT(self):
        path, vals = self.urlParse(self.path)
        global DB
        DB.put(path, vals.get("value", ""))
        self.send_response(200)
        self.end_headers()
        self.wfile.write("OK\n")

    def do_DELETE(self):
        path, vals = self.urlParse(self.path)
        global DB
        DB.delete(path)
        self.send_response(200)
        self.end_headers()
        self.wfile.write("OK\n")


def setupLogging():
    logging.basicConfig( level=logging.INFO,
                         format="%(levelname)s: %(message)s" )

def main():
    setupLogging()
    global DB
    try:
        DB = Database("kvsuck.db")
    except Exception as e:
        error("Exception caught: %s" % e)
        return

    info("Starting HTTPServer on port 8080")
    server = HTTPServer(("",8080), Handler)
    try:
        server.serve_forever()
    except:
        info("Shutting down HTTPServer")
    server.socket.close()
    DB.close()

if __name__=="__main__":
    main()

