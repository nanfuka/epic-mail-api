import psycopg2
from psycopg2.extras import RealDictCursor
from pprint import pprint
import os
from os import environ
from flask import Flask, jsonify, request, json


class Database:
    def __init__(self):

        if os.getenv('DB_NAME') == 'epicmail':
            self.db_name = 'epicmail'
        self.db_name = 'epik'

        self.db_connect = psycopg2.connect(
            database=self.db_name, user='postgres', password='test',
            host='127.0.0.1', port=5432)
        self.db_connect.autocommit = True
        self.cursor = self.db_connect.cursor(cursor_factory=RealDictCursor)
        self.create_tables()

        #     if not environ.get('DATABASE_URL'):
        #         self.connection = psycopg2.connect(
        #             "postgres://postgres:test@localhost:5432/epicmail")
        #     else:
        #         self.connection = psycopg2.connect(environ.get('DATABASE_URL'))
        #     self.connection.autocommit = True
        #     self.cursor = self.connection.cursor(
        #         cursor_factory=RealDictCursor
        #     )
        #     self.create_tables()

        # except psycopg2.OperationalError as e:
        #     print(e, "Database Connection failed")

    def create_tables(self):
        """Function which creates all the tables with in the database"""
        users = """CREATE TABLE IF NOT EXISTS users(
            ID SERIAL PRIMARY KEY NOT NULL,
            firstname VARCHAR(20) NOT NULL,
            lastname VARCHAR(20) NOT NULL,
            email VARCHAR(20) NOT NULL,
            password VARCHAR(20) NOT NULL);"""
        self.cursor.execute(users)

        table_contacts = """CREATE TABLE IF NOT EXISTS contacts(
            ID SERIAL PRIMARY KEY NOT NULL,
            firstname VARCHAR(20) NOT NULL,
            lastname VARCHAR(20) NOT NULL,
            email VARCHAR(20) NOT NULL,
            password VARCHAR(20) NOT NULL);"""
        self.cursor.execute(table_contacts)

        messages = """CREATE TABLE IF NOT EXISTS messages(
            ID SERIAL PRIMARY KEY NOT NULL,
            created_on DATE,
            subject VARCHAR(20) NOT NULL,
            message VARCHAR(20) NOT NULL,
            status VARCHAR(20) NOT NULL,
            sender_id integer,
            reciever_id  integer);"""
        self.cursor.execute(messages)

        table_groupmessages = """CREATE TABLE IF NOT EXISTS groupmessages(
            id SERIAL PRIMARY KEY NOT NULL,
            group_id integer,
            created_on DATE,
            subject VARCHAR(20) NOT NULL,
            message VARCHAR(20) NOT NULL,
            status VARCHAR(20) NOT NULL,
            sender_id integer);"""
        self.cursor.execute(table_groupmessages)

        table_inbox = """CREATE TABLE IF NOT EXISTS inbox(
            id SERIAL PRIMARY KEY NOT NULL,
            created_on DATE, subject VARCHAR(20) NOT NULL,
            message VARCHAR NOT NULL, sender_id integer,
            reciever_id integer,
            parent_message_id integer,
            status VARCHAR(20) NOT NULL);"""
        self.cursor.execute(table_inbox)

        table_outbox = """CREATE TABLE IF NOT EXISTS outbox(
            id SERIAL PRIMARY KEY NOT NULL,
            created_on DATE, subject VARCHAR(20) NOT NULL,
            message VARCHAR NOT NULL, sender_id integer,
            reciever_id integer, parent_message_id integer,
            status VARCHAR(20) NOT NULL);"""
        self.cursor.execute(table_outbox)

        table_sent = """CREATE TABLE IF NOT EXISTS sent(
            id SERIAL PRIMARY KEY NOT NULL,
            message_id INTEGER REFERENCES messages(ID),
            created_on DATE, sender_id integer);"""
        self.cursor.execute(table_sent)

        table_draft = """CREATE TABLE IF NOT EXISTS draft(
            ID SERIAL PRIMARY KEY NOT NULL,
            firstname VARCHAR(20) NOT NULL,
            lastname VARCHAR(20) NOT NULL,
            email VARCHAR(20) NOT NULL,
            password VARCHAR(20) NOT NULL);"""
        self.cursor.execute(table_sent)

        self.cursor.execute(table_inbox)

        table_group = """CREATE TABLE IF NOT EXISTS epicgroups(
            id SERIAL PRIMARY KEY NOT NULL,
            name VARCHAR(20) NOT NULL,
            admin VARCHAR(20) NOT NULL,
            role VARCHAR(20) NOT NULL);"""
        self.cursor.execute(table_group)

        table_cluster = """CREATE TABLE IF NOT EXISTS clusters(
            id SERIAL PRIMARY KEY NOT NULL,
            group_id integer,
            userid integer,
            userrole VARCHAR(20) NOT NULL);"""
        self.cursor.execute(table_cluster)

        table_groupmembers = """CREATE TABLE IF NOT EXISTS groupmembers(
            ID SERIAL PRIMARY KEY NOT NULL,
            firstname VARCHAR(20) NOT NULL,
            lastname VARCHAR(20) NOT NULL,
            email VARCHAR(20) NOT NULL,
            password VARCHAR(20) NOT NULL);"""
        self.cursor.execute(table_groupmembers)

        table_outbox = """CREATE TABLE IF NOT EXISTS outbox(
            id SERIAL PRIMARY KEY NOT NULL,
            message_id INTEGER REFERENCES messages(ID),
            created_on DATE, sender_id integer);"""
        self.cursor.execute(table_inbox)

    def drop_table(self, table_name):
        drop_table = "DROP TABLE IF EXISTS {}".format(table_name)
        self.cursor.execute(drop_table)
