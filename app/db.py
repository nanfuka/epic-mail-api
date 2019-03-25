import psycopg2
from psycopg2.extras import RealDictCursor
from pprint import pprint
import os
from os import environ


class Database:
    def __init__(self):
        try:
            if not environ.get('DATABASE_URL'):
                self.connection = psycopg2.connect(
                    "postgres://postgres:test@localhost:5432/epicmail")
            else:
                self.connection = psycopg2.connect(environ.get('DATABASE_URL'))
            self.connection.autocommit = True
            self.cursor = self.connection.cursor(
                cursor_factory=RealDictCursor
            )
            self.create_tables()

        except psycopg2.OperationalError as e:
            print(e, "Database Connection failed")

    def create_tables(self):
        tables = """CREATE TABLE IF NOT EXISTS users(ID SERIAL PRIMARY KEY NOT NULL, firstname VARCHAR(20) NOT NULL,lastname VARCHAR(20) NOT NULL, email VARCHAR(20) NOT NULL, password VARCHAR(20) NOT NULL);"""
        self.cursor.execute(tables)

    def signup(self, **kwargs):
        insert = f"""INSERT INTO users(firstname, lastname, email, password) VALUES ('{kwargs.get("firstname")}', '{kwargs.get("lastname")}', '{kwargs.get("email")}', '{kwargs.get("password")}') RETURNING id, firstname, lastname, email, password;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()
    def check_email(self, email):
        query = "SELECT * FROM users WHERE email = '{}'".format(email)
        self.cursor.execute(query)
        return self.cursor.fetchall()
