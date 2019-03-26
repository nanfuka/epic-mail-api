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

        table_messages = """CREATE TABLE IF NOT EXISTS messages(ID SERIAL PRIMARY KEY NOT NULL, created_on DATE, subject VARCHAR(20) NOT NULL, message VARCHAR(20) NOT NULL, parent_message_id integer, status VARCHAR(20) NOT NULL, sender_id integer, reciever_id integer);"""        
        self.cursor.execute(table_messages)

        table_sent = """CREATE TABLE IF NOT EXISTS sent(ID SERIAL PRIMARY KEY NOT NULL, firstname VARCHAR(20) NOT NULL,lastname VARCHAR(20) NOT NULL, email VARCHAR(20) NOT NULL, password VARCHAR(20) NOT NULL);"""        
        self.cursor.execute(table_sent)

        table_draft = """CREATE TABLE IF NOT EXISTS draft(ID SERIAL PRIMARY KEY NOT NULL, firstname VARCHAR(20) NOT NULL,lastname VARCHAR(20) NOT NULL, email VARCHAR(20) NOT NULL, password VARCHAR(20) NOT NULL);"""        
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
    def create_message(self, **kwargs):
        insert = f"""INSERT INTO messages(subject, message, status) VALUES ( '{kwargs.get("subject")}', '{kwargs.get("message")}', '{kwargs.get("status")}') RETURNING ID, subject, message, status;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()

    def create_sent(self, **kwargs):
        insert = f"""INSERT INTO table_sent(senderId, message_id, createdOn) VALUES ('{kwargs.get("senderId")}', '{kwargs.get("message_id")}', '{kwargs.get("createdOn")}')) RETURNING senderId, message_id, createdOn;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()
    
    def create_inbox(self, **kwargs):
        insert = f"""INSERT INTO table_inbox(receiverId, message_id, createdOn) VALUES ('{kwargs.get("receiverId")}', '{kwargs.get("message_id")}', '{kwargs.get("createdOn")}')) RETURNING senderId, message_id, createdOn;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()
    def create_group(self, **kwargs):
        insert = f"""INSERT INTO table_group(groupId, name) VALUES ('{kwargs.get("groupId")}', '{kwargs.get("name")}')) RETURNING groupId, name;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()
    def create_group_members(self, **kwargs):
        insert = f"""INSERT INTO table_groupmembers(group_id, member_id) VALUES ('{kwargs.get("group_id")}', '{kwargs.get("member_id")}')) RETURNING group_id, member_id;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()

    def create_message(self, **kwargs):
        insert = f"""INSERT INTO messages(created_on, subject, message, parent_message_id, status, sender_id, reciever_id) VALUES ( '{kwargs.get("created_on")}', '{kwargs.get("subject")}', '{kwargs.get("message")}', '{kwargs.get("parent_message_id")}', '{kwargs.get("status")}', '{kwargs.get("sender_id")}', '{kwargs.get("reciever_id")}') RETURNING ID, created_on, subject, message, parent_message_id, status;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()
    # def get_parent_message_id(self, message_id):
    #     if self.get_all_message_id:

        #     query = "SELECT * FROM messages WHERE incident_id = {} and \
        #     incident_type ='{}'".format(incident_id, incident_type)
        # db.cursor.execute(query)
        # return db.cursor.fetchall()
    def get_all_mails(self):
        query = f"""SELECT * FROM messages"""
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_users(self):
        query = f"""SELECT * FROM users"""
        self.cursor.execute(query)
        return self.cursor.fetchall()

