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
        table_users = """CREATE TABLE IF NOT EXISTS users(ID SERIAL PRIMARY KEY NOT NULL, firstname VARCHAR(20) NOT NULL,lastname VARCHAR(20) NOT NULL, email VARCHAR(20) NOT NULL, password VARCHAR(20) NOT NULL);"""        
        self.cursor.execute(table_users)

        table_contacts = """CREATE TABLE IF NOT EXISTS contacts(ID SERIAL PRIMARY KEY NOT NULL, firstname VARCHAR(20) NOT NULL,lastname VARCHAR(20) NOT NULL, email VARCHAR(20) NOT NULL, password VARCHAR(20) NOT NULL);"""        
        self.cursor.execute(table_contacts)

        table_messages = """CREATE TABLE IF NOT EXISTS messages(ID SERIAL PRIMARY KEY NOT NULL, firstname VARCHAR(20) NOT NULL,lastname VARCHAR(20) NOT NULL, email VARCHAR(20) NOT NULL, password VARCHAR(20) NOT NULL);"""        
        self.cursor.execute(table_messages)

        table_sent = """CREATE TABLE IF NOT EXISTS sent(ID SERIAL PRIMARY KEY NOT NULL, firstname VARCHAR(20) NOT NULL,lastname VARCHAR(20) NOT NULL, email VARCHAR(20) NOT NULL, password VARCHAR(20) NOT NULL);"""        
        self.cursor.execute(table_sent)

        table_inbox = """CREATE TABLE IF NOT EXISTS inbox(ID SERIAL PRIMARY KEY NOT NULL, firstname VARCHAR(20) NOT NULL,lastname VARCHAR(20) NOT NULL, email VARCHAR(20) NOT NULL, password VARCHAR(20) NOT NULL);"""        
        self.cursor.execute(table_inbox)

        table_group = """CREATE TABLE IF NOT EXISTS groups(ID SERIAL PRIMARY KEY NOT NULL, firstname VARCHAR(20) NOT NULL,lastname VARCHAR(20) NOT NULL, email VARCHAR(20) NOT NULL, password VARCHAR(20) NOT NULL);"""        
        self.cursor.execute(table_group)

        table_groupmembers = """CREATE TABLE IF NOT EXISTS groupmembers(ID SERIAL PRIMARY KEY NOT NULL, firstname VARCHAR(20) NOT NULL,lastname VARCHAR(20) NOT NULL, email VARCHAR(20) NOT NULL, password VARCHAR(20) NOT NULL);"""        
        self.cursor.execute(table_groupmembers)


    def signup(self, **kwargs):
        insert = f"""INSERT INTO users(firstname, lastname, email, password) VALUES ('{kwargs.get("firstname")}', '{kwargs.get("lastname")}', '{kwargs.get("email")}', '{kwargs.get("password")}') RETURNING id, firstname, lastname, email, password;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()
    def check_email(self, email):
        query = "SELECT * FROM users WHERE email = '{}'".format(email)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def login(self, email, password):
        query = "SELECT * FROM users WHERE email = '{}' and password = '{}'".format(email, password)
        self.cursor.execute(query)
        return self.cursor.fetchone()
    def create_message(self, **kwargs)
        insert = f"""INSERT INTO messages(createdOn, subject, message, parentMessageId, status) VALUES ('{kwargs.get("createdOn")}', '{kwargs.get("subject")}', '{kwargs.get("message")}', '{kwargs.get("parentMessageId"), }') RETURNING id, firstname, lastname, email;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()

    def create_sent(self, **kwargs)
        insert = f"""INSERT INTO table_sent(senderId, message_id, createdOn) VALUES ('{kwargs.get("senderId")}', '{kwargs.get("message_id")}', '{kwargs.get("createdOn")}')) RETURNING senderId, message_id, createdOn;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()
    
    def create_inbox(self, **kwargs)
        insert = f"""INSERT INTO table_inbox(receiverId, message_id, createdOn) VALUES ('{kwargs.get("receiverId")}', '{kwargs.get("message_id")}', '{kwargs.get("createdOn")}')) RETURNING senderId, message_id, createdOn;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()
    def create_group(self, **kwargs)
        insert = f"""INSERT INTO table_group(groupId, name) VALUES ('{kwargs.get("groupId")}', '{kwargs.get("name")}')) RETURNING groupId, name;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()
    def create_group_members(self, **kwargs)
        insert = f"""INSERT INTO table_groupmembers(group_id, member_id) VALUES ('{kwargs.get("group_id")}', '{kwargs.get("member_id")}')) RETURNING group_id, member_id;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()