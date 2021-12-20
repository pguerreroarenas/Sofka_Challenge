import os
import sqlite3 as sql
from sqlite3.dbapi2 import OperationalError


class DBgestor:
    def __init__(self, nameDB):
        self.CurrenRute = os.path.dirname(os.path.realpath(__file__)) + '/' + nameDB
    
    def validateRute(self):
        #verifica que la ruta exista 
        return os.path.isfile(self.CurrenRute)
        
    
    def existTable(self):
        if self.validateRute():
            query = "SELECT count(NAME) FROM sqlite_master WHERE type='table' AND NAME=?"
            tables = [('USERS',), ('FORMS',) ]
            for parameters in tables:
                result = self.runQuery(query, parameters)
                if result[0][0]!=1:
                    return False
            return True

    def crateTable(self):
        if not self.existTable():
            query1 = """create table USERS (
                            ID integer primary key autoincrement unique,
                            NAME text unique not null,
                            PASSW text not null,  
                            SCORE integer,
                            TRIES integer
                            )"""
            query2 = """create table FORMS (
                            ID integer primary key autoincrement unique,
                            LEVEL integer,
                            QUESTION text,
                            OPTION text,
                            ANSWER integer
                            )"""
            try:
                self.runQuery(query1)
            except sql.OperationalError:
                print("la tabla USERS ya existe")
            try:
                self.runQuery(query2)
            except sql.OperationalError:
                print("la tabla FORMS ya existe")


    def runQuery(self,query, parameters=()):
        with sql.connect(self.CurrenRute) as con:
            cur = con.cursor()
            cur.execute(query, parameters)
            result=cur.fetchall()
            con.commit()
            return result
    
    def existUser(self, name):
        #verifica la existencia de un usuario en la base de datos 
        query =f"select ID from USERS where NAME=?"
        parameters = (name,)
        result = self.runQuery(query, parameters)
        if len(result)>0:
            return True
        else:
            return False
        
    def getPassW(self, user):
        query="select PASSW from USERS where NAME=?"
        parameters = (user,)
        result = self.runQuery(query, parameters)
        return result[0][0]

    def insertUser(self, name, passw, score, tries):
        """
        insertUser trata de ingresar el usuario a la base de datos, si lo logra retorna una lista vacia, 
        si no lologra presentara un error de ingreso o retorna None si el usuario ya existe en la base de datos.
        """
        if not self.existUser(name):
            try: 
                query="insert into USERS (NAME, PASSW,SCORE, TRIES) values (?,?,?,?)"
                parameters=(name, passw, score, tries)
                result = self.runQuery(query, parameters)
                return result
            except:
                result = "No fue posible ingresear el usuario a la base de datos"
                return result
        else:
            return None
    
    def loadUser(self, name):
        query = "select * from USERS where NAME=?"
        parameters = (name,)
        result = self.runQuery(query, parameters)
        return result[0]

    def updateUser(self, name, score, tries):
        query="update USERS set SCORE=?, TRIES=? where NAME=?"
        parameters = (score, tries, name)
        result = self.runQuery(query, parameters)
        
        

    def loadQuestions(self, ID):
        query= "select * from FORMS where ID=?"
        parameters = (ID,)
        result = self.runQuery(query, parameters)
        return result
    
    def minimaQuestion(self):
        query = "select * from FORMS"
        result = self.runQuery(query)
        if len(result)<25:
            return False
        else:
            return True
    
    def topPodio(self):
        query ="select * from USERS order by SCORE DESC"
        result = self.runQuery(query)
        return result[:3]

