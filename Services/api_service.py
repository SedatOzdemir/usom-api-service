#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from flask import Flask
import json
from flask import request
from flask import Response
from configparser import ConfigParser

app = Flask(__name__)
DatabasePath = "/Users/sedatozdemir/Desktop/USOM API/Database.db"


def GetConfigurations(get):
    # instantiate
    config = ConfigParser()

    # parse existing file
    config.read('config.ini')

    # read values from a section
    if get == "AccessKey":
        return config.get('Auth', 'AccessKey')
    elif get == "DatabasePath":
        return config.get('DatabaseConfigurations', 'DatabasePath')

def GetDatabaseRowCount(dbname):
    try:
        return sqlite3.connect(GetConfigurations("DatabasePath")).cursor().execute("SELECT COUNT(*) FROM " + dbname).fetchone()
    except:
        # Hide sensitive errors
        pass

@app.route('/api/usom')
def getlinks():
    page = request.args.get('page', default = 1, type = int)
    size = request.args.get('size', default = 10, type = int)
    orderby = request.args.get('orderby', default = "desc", type = str)
    data_type = request.args.get('data_type', default = "malicious_links", type = str)
    access_token = request.args.get('access_token', type = str)

    if access_token != GetConfigurations("AccessKey"):
        return Response('{"status": "error","message": "Access token is not valid"}', mimetype='application/json', status=401)    

    if data_type == "malicious_links":
        DatabaseName = "Phish"
        
    elif data_type == "security_announcement":
        DatabaseName = "Vuln"

    else:
        return Response('{"status": "error","message": "\'data_type\' parameter is not valid"}', mimetype='application/json', status=400)

    if orderby != 'desc' and orderby != 'asc':
        return Response('{"status": "error","message": "\'orderby\' parameter is not valid"}', mimetype='application/json', status=400)
    
    elif isinstance(size, int) == False:
        return Response('{"status": "error","message": "\'size\' parameter not valid"}', mimetype='application/json', status=400)

    elif isinstance(page, int) == False:
        return Response('{"status": "error","message": "\'page\' parameter not valid"}', mimetype='application/json', status=400)


    page = page * size
    Connection = sqlite3.connect( GetConfigurations("DatabasePath") )
    Connection.row_factory = sqlite3.Row
    Cursor = Connection.cursor()
    
    Cursor.execute("SELECT * FROM " +DatabaseName+ " ORDER BY date " + str(orderby) + " LIMIT " + str(size) + " OFFSET " + str(page))
    Rows = Cursor.fetchall()
    Connection.commit()
    Connection.close()

    jsonExport = json.dumps( [dict(ix) for ix in Rows] , ensure_ascii=False)
    JsonResponse = json.loads(jsonExport)

    myjson = {'TotalRecords':GetDatabaseRowCount(DatabaseName)[0],'Size': len(JsonResponse), 'CurrentPage': page, 'Data': JsonResponse}

    printable = json.dumps(myjson)
    return Response(printable, mimetype='application/json', status=200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
