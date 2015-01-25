__author__ = 'kujaomega'
import MySQLdb


class MySQLConnect():
    def __init__(self):
        self.db = MySQLdb.Connect(host='192.168.44.129',# your host, usually localhost
                             port=3306,
                             user="root", # your username
                             passwd="P@@ssw0rd", # your password
                             db="basketpc") # name of the data base
        self.players_table = 'temp74test3'
        self.teams_table = 'teamstemp74'

    def setPlayersTable(self, table):
        self.players_table = table

    def setTeamsTable(self, table):
        self.teams_table = table

    def createPlayersTable(self):
        query = \
'CREATE TABLE IF NOT EXISTS ' + self.players_table+ \
'( ' \
    'posicion CHAR(5), ' \
    'altura INT, ' \
    'nombre CHAR(50), ' \
    'edad INT, ' \
    'calidad INT, ' \
    'defensa INT, ' \
    'tiro3 INT, ' \
    'tiro2 INT, ' \
    'tiro1 INT, ' \
    'velocidad INT, ' \
    'resistencia INT, ' \
    'pase INT, ' \
    'dribling INT, ' \
    'rebote INT, ' \
    'media INT, ' \
    'ficha CHAR(7), ' \
    'clausula FLOAT(6,2), ' \
    'tiempo_contrato INT, ' \
    'id INT, ' \
    'equipo CHAR(50), ' \
    'categoria CHAR(10), ' \
    'fatiga FLOAT(6,2), ' \
    'ef FLOAT(6,2), ' \
    'moral FLOAT(6,2), ' \
'PRIMARY KEY(id)' \
')'
        cursor = self.db.cursor()
        cursor.execute(query)

    def createPlayersTable4teamsparser(self):
        query = \
'CREATE TABLE IF NOT EXISTS ' + self.players_table + \
'( ' \
    'nombre CHAR(50), ' \
    'edad INT, ' \
    'semanas INT, ' \
    'nacionalidad CHAR(50), ' \
    'altura INT, ' \
    'peso INT, ' \
    'posicion CHAR(5), ' \
    'clausula DOUBLE, ' \
    'ficha INT, ' \
    'contrato INT, ' \
    'media INT, ' \
    'clase CHAR(10), ' \
    'calidad INT, ' \
    'defensa INT, ' \
    'tiro3 INT, ' \
    'tiro2 INT, ' \
    'tiro1 INT, ' \
    'velocidad INT, ' \
    'resistencia INT, ' \
    'pase INT, ' \
    'dribling INT, ' \
    'rebote INT, ' \
    'fatiga FLOAT(6,2), ' \
    'ef FLOAT(6,2), ' \
    'moral FLOAT(6,2), ' \
    'equipo CHAR(50), ' \
    'id INT, ' \
'PRIMARY KEY(id)' \
')'
        cursor = self.db.cursor()
        cursor.execute(query)

    def createTeamsTable(self):
        query = \
'CREATE TABLE IF NOT EXISTS ' + self.teams_table + \
'( ' \
    'nombre CHAR(50), ' \
    'id INT, ' \
    'division CHAR(5), ' \
    'pais CHAR(50), ' \
'PRIMARY KEY(id)' \
')'
        cursor = self.db.cursor()
        cursor.execute(query)

    def selectIdPlayers(self):
        # Use all the SQL you like
        cursor = self.db.cursor()
        query = \
'SELECT * FROM ' + self.players_table
        cursor.execute(query)
        return cursor.fetchall()
        # print all the first cell of all the rows
        # for row in cursor.fetchall():
        #     print row[0]

    def selectPlayersFromId(self, id):
        cursor = self.db.cursor()
        query = \
'SELECT ' \
    'id, ' \
    'altura, ' \
    'peso, ' \
    'edad, ' \
    'clase, ' \
    'media, ' \
    'posicion, ' \
    'calidad, ' \
    'defensa, ' \
    'tiro3, ' \
    'tiro2, ' \
    'tiro1, ' \
    'velocidad, ' \
    'resistencia, ' \
    'pase, ' \
    'dribling, ' \
    'rebote ' \
'FROM ' + self.players_table + \
        'WHERE id=' + id
        cursor.execute(query)
        return cursor.fetchall()
        # print all the first cell of all the rows
        # for row in cursor.fetchall():
        #     print row[0]

    def insertTeams(self, data):
        values = '\'), ( \''.join(['\', \''.join(x for x in y) for y in data])
        query = \
'INSERT INTO ' + self.teams_table + \
'( ' \
    'nombre, ' \
    'id, ' \
    'division, ' \
    'pais ' \
    ')' \
' VALUES ' + '( \'' + values + '\')' \
'ON DUPLICATE KEY UPDATE ' \
    'nombre=VALUES(nombre)'
        cursor = self.db.cursor()
        query = query.encode('utf8')
        cursor.execute(query)
        self.db.commit()

    def insert30val(self, data):
        # values = '\'), ( \''.join(['\', \''.join(codecs.latin_1_encode(x)[0] for x in y) for y in data])
        values = '\'), ( \''.join(['\', \''.join(x for x in y) for y in data])
        query = \
'INSERT INTO ' + self.players_table + \
'( ' \
    'posicion, ' \
    'altura, ' \
    'nombre, ' \
    'edad, ' \
    'calidad, ' \
    'defensa, ' \
    'tiro3, ' \
    'tiro2, ' \
    'tiro1, ' \
    'velocidad, ' \
    'resistencia, ' \
    'pase, ' \
    'dribling, ' \
    'rebote, ' \
    'media, ' \
    'ficha, ' \
    'clausula, ' \
    'tiempo_contrato, ' \
    'id, ' \
    'equipo, ' \
    'categoria, ' \
    'fatiga, ' \
    'ef, ' \
    'moral' \
    ')' \
' VALUES ' + '( \'' + values + '\')'
        cursor = self.db.cursor()
        query = query.encode('utf8')
        cursor.execute(query)
        self.db.commit()

    def insertPlayers(self, data):
        # values = '\'), ( \''.join(['\', \''.join(codecs.latin_1_encode(x)[0] for x in y) for y in data])
        values = '\'), ( \''.join(['\', \''.join(x for x in y) for y in data])
        query = \
'INSERT INTO ' + self.players_table + \
'( ' \
    'posicion, ' \
    'altura, ' \
    'nombre, ' \
    'edad, ' \
    'calidad, ' \
    'defensa, ' \
    'tiro3, ' \
    'tiro2, ' \
    'tiro1, ' \
    'velocidad, ' \
    'resistencia, ' \
    'pase, ' \
    'dribling, ' \
    'rebote, ' \
    'media, ' \
    'ficha, ' \
    'clausula, ' \
    'tiempo_contrato, ' \
    'id, ' \
    'equipo, ' \
    'categoria, ' \
    'fatiga, ' \
    'ef, ' \
    'moral' \
    ')' \
' VALUES ' + "( '" + values + '\')' \
'ON DUPLICATE KEY UPDATE ' \
    'fatiga=VALUES(fatiga), ' \
    'ef=VALUES(ef), ' \
    'moral=VALUES(moral)'
        print query
        cursor = self.db.cursor()
        query = query.encode('utf8')
        cursor.execute(query)
        self.db.commit()

    def insertPlayersTeamParsing(self, data):
        values = '\'), ( \''.join(['\', \''.join(x for x in y) for y in data])
        query = \
'INSERT INTO ' + self.players_table + \
'( ' \
    'nombre, ' \
    'edad, ' \
    'semanas, ' \
    'nacionalidad, ' \
    'altura, ' \
    'peso, ' \
    'posicion, ' \
    'clausula, ' \
    'ficha, ' \
    'contrato, ' \
    'media, ' \
    'clase, ' \
    'calidad, ' \
    'defensa, ' \
    'tiro3, ' \
    'tiro2, ' \
    'tiro1, ' \
    'velocidad, ' \
    'resistencia, ' \
    'pase, ' \
    'dribling, ' \
    'rebote, ' \
    'fatiga, ' \
    'ef, ' \
    'moral, ' \
    'equipo, ' \
    'id ' \
    ')' \
' VALUES ' + '( \'' + values + '\')' \
'ON DUPLICATE KEY UPDATE ' \
    'nombre=VALUES(nombre),' \
    'edad=VALUES(edad),' \
    'semanas=VALUES(semanas),' \
    'altura=VALUES(altura), ' \
    'peso=VALUES(peso), ' \
    'posicion=VALUES(posicion), ' \
    'clausula=VALUES(clausula), ' \
    'ficha=VALUES(ficha), ' \
    'contrato=VALUES(contrato), ' \
    'media=VALUES(media), ' \
    'clase=VALUES(clase), ' \
    'calidad=VALUES(calidad), ' \
    'defensa=VALUES(defensa), ' \
    'tiro3=VALUES(tiro3), ' \
    'tiro2=VALUES(tiro2), ' \
    'tiro1=VALUES(tiro1), ' \
    'velocidad=VALUES(velocidad), ' \
    'resistencia=VALUES(resistencia), ' \
    'pase=VALUES(pase), ' \
    'dribling=VALUES(dribling), ' \
    'rebote=VALUES(rebote), ' \
    'fatiga=VALUES(fatiga), ' \
    'ef=VALUES(ef), ' \
    'moral=VALUES(moral), ' \
    'equipo=VALUES(equipo)'
        cursor = self.db.cursor()
        query = query.encode('utf8')
        cursor.execute(query)
        self.db.commit()

    def updatePlayersTeamParsing(self, data):
        values = '\'), ( \''.join(['\', \''.join(x for x in y) for y in data])
        # query1 =
        query = \
'INSERT INTO ' + self.players_table + \
'( ' \
    'nombre, ' \
    'edad, ' \
    'semanas, ' \
    'nacionalidad, ' \
    'altura, ' \
    'peso, ' \
    'posicion, ' \
    'clausula, ' \
    'ficha, ' \
    'contrato, ' \
    'media, ' \
    'clase, ' \
    'calidad, ' \
    'defensa, ' \
    'tiro3, ' \
    'tiro2, ' \
    'tiro1, ' \
    'velocidad, ' \
    'resistencia, ' \
    'pase, ' \
    'dribling, ' \
    'rebote, ' \
    'fatiga, ' \
    'ef, ' \
    'moral, ' \
    'equipo, ' \
    'id ' \
    ')' \
' VALUES ' + '( \'' + values + '\')' \
'ON DUPLICATE KEY UPDATE ' \
    'posicion=VALUES(posicion), ' \
    'clausula=VALUES(clausula), ' \
    'ficha=VALUES(ficha), ' \
    'media=VALUES(media), ' \
    'equipo=VALUES(equipo), ' \
    'fatiga=VALUES(fatiga), ' \
    'ef=VALUES(ef), ' \
    'moral=VALUES(moral)'
        cursor = self.db.cursor()
        query = query.encode('utf8')
        cursor.execute(query)
        self.db.commit()

    def deletePlayersTable(self):
        query = \
'DROP TABLE IF EXISTS ' + self.players_table
        cursor = self.db.cursor()
        cursor.execute(query)
        self.db.commit()

    def deleteTeamsTable(self):
        query = \
'DROP TABLE IF EXISTS ' + self.teams_table
        cursor = self.db.cursor()
        cursor.execute(query)
        self.db.commit()