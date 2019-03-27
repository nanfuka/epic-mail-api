import psycopg2
from psycopg2.extras import RealDictCursor
from pprint import pprint
import os
from os import environ
from flask import Flask, jsonify, request, json


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
        table_users = """CREATE TABLE IF NOT EXISTS users(ID SERIAL PRIMARY KEY NOT NULL,
        firstname VARCHAR(20) NOT NULL,lastname VARCHAR(20) NOT NULL, email VARCHAR(20) NOT NULL, password VARCHAR(20) NOT NULL);"""
        self.cursor.execute(table_users)

        table_contacts = """CREATE TABLE IF NOT EXISTS contacts(ID SERIAL PRIMARY KEY NOT NULL, firstname VARCHAR(20) NOT NULL,lastname VARCHAR(20) NOT NULL, email VARCHAR(20) NOT NULL, password VARCHAR(20) NOT NULL);"""
        self.cursor.execute(table_contacts)

        table_messages = """CREATE TABLE IF NOT EXISTS messages(ID SERIAL PRIMARY KEY NOT NULL, created_on DATE, subject VARCHAR(20) NOT NULL, message VARCHAR(20) NOT NULL, status VARCHAR(20) NOT NULL, sender_id integer, reciever_id  integer);"""
        self.cursor.execute(table_messages)
        table_groupmessages = """CREATE TABLE IF NOT EXISTS groupmessages(id SERIAL PRIMARY KEY NOT NULL, group_id integer, created_on DATE, subject VARCHAR(20) NOT NULL, message VARCHAR(20) NOT NULL, status VARCHAR(20) NOT NULL, sender_id integer);"""
        self.cursor.execute(table_groupmessages)

        table_inbox = """CREATE TABLE IF NOT EXISTS inbox(id SERIAL PRIMARY KEY NOT NULL, created_on DATE, subject VARCHAR(20) NOT NULL, message VARCHAR NOT NULL, sender_id integer, reciever_id integer, parent_message_id integer,  status VARCHAR(20) NOT NULL);"""
        self.cursor.execute(table_inbox)

        table_outbox = """CREATE TABLE IF NOT EXISTS outbox(id SERIAL PRIMARY KEY NOT NULL, created_on DATE, subject VARCHAR(20) NOT NULL, message VARCHAR NOT NULL, sender_id integer, reciever_id integer, parent_message_id integer,  status VARCHAR(20) NOT NULL);"""
        self.cursor.execute(table_outbox)

        table_sent = """CREATE TABLE IF NOT EXISTS sent(id SERIAL PRIMARY KEY NOT NULL, message_id INTEGER REFERENCES messages(ID), created_on DATE, sender_id integer);"""
        self.cursor.execute(table_sent)

        table_draft = """CREATE TABLE IF NOT EXISTS draft(ID SERIAL PRIMARY KEY NOT NULL, firstname VARCHAR(20) NOT NULL,lastname VARCHAR(20) NOT NULL, email VARCHAR(20) NOT NULL, password VARCHAR(20) NOT NULL);"""
        self.cursor.execute(table_sent)

        self.cursor.execute(table_inbox)

        table_group = """CREATE TABLE IF NOT EXISTS epicgroups(id SERIAL PRIMARY KEY NOT NULL, name VARCHAR(20) NOT NULL, admin VARCHAR(20) NOT NULL, role VARCHAR(20) NOT NULL);"""
        self.cursor.execute(table_group)

        table_cluster = """CREATE TABLE IF NOT EXISTS clusters(id SERIAL PRIMARY KEY NOT NULL, group_id integer, userid integer, userrole VARCHAR(20) NOT NULL);"""
        self.cursor.execute(table_cluster)

        table_groupmembers = """CREATE TABLE IF NOT EXISTS groupmembers(ID SERIAL PRIMARY KEY NOT NULL, firstname VARCHAR(20) NOT NULL,lastname VARCHAR(20) NOT NULL, email VARCHAR(20) NOT NULL, password VARCHAR(20) NOT NULL);"""
        self.cursor.execute(table_groupmembers)

        table_outbox = """CREATE TABLE IF NOT EXISTS outbox(id SERIAL PRIMARY KEY NOT NULL, message_id INTEGER REFERENCES messages(ID), created_on DATE, sender_id integer);"""
        self.cursor.execute(table_inbox)
        # table_newgroup = """CREATE TABLE IF NOT EXISTS epicgroup(id SERIAL PRIMARY KEY NOT NULL, name VARCHAR(20) NOT NULL, role VARCHAR(20) NOT NULL);"""
        # self.cursor.execute(table_users)

    def signup(self, **kwargs):
        insert = f"""INSERT INTO users(firstname, lastname, email, password) VALUES ('{kwargs.get("firstname")}', '{kwargs.get("lastname")}', '{kwargs.get("email")}', '{kwargs.get("password")}') RETURNING id, firstname, lastname, email, password;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()

    def check_email(self, email):
        query = "SELECT * FROM users WHERE email = '{}'".format(email)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def login(self, email, password):
        query = "SELECT * FROM users WHERE email = '{}' and password = '{}'".format(
            email, password)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def create_message(self, **kwargs):
        insert = f"""INSERT INTO messages(subject, message, status) VALUES ( '{kwargs.get("subject")}', '{kwargs.get("message")}', '{kwargs.get("status")}') RETURNING ID, subject, message, status;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()

    def create_groupmessage(self, **kwargs):
        insert = f"""INSERT INTO groupmessages(group_id, subject, message, status, created_on) VALUES ( '{kwargs.get("group_id")}','{kwargs.get("subject")}', '{kwargs.get("message")}', '{kwargs.get("status")}', '{kwargs.get("created_on")}') RETURNING id, subject, message, status, created_on;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()

    def create_sent(self, **kwargs):

        insert = f"""INSERT INTO sent(sender_id, message_id, created_on) VALUES ('{kwargs.get("sender_id")}', '{kwargs.get("message_id")}', '{kwargs.get("created_on")}') RETURNING sender_id, message_id, created_on;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()

    def get_outtbox(self, sender_id):
        insert = f"""INSERT INTO outbox(created_on, subject, message, sender_id, reciever_id, parent_message_id, status) VALUES ( '{kwargs.get("created_on")}','{kwargs.get("subject")}', '{kwargs.get("message")}','{kwargs.get("sender_id")}','{kwargs.get("reciever_id")}','{kwargs.get("parent_message_id")}', '{kwargs.get("status")}') RETURNING id, created_on, subject, message, sender_id, reciever_id, parent_message_id, status;"""
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def create_inbox(self, **kwargs):
        insert = f"""INSERT INTO inbox(created_on, subject, message, sender_id, reciever_id, parent_message_id, status) VALUES ( '{kwargs.get("created_on")}','{kwargs.get("subject")}', '{kwargs.get("message")}','{kwargs.get("sender_id")}','{kwargs.get("reciever_id")}','{kwargs.get("parent_message_id")}', '{kwargs.get("status")}') RETURNING id, created_on, subject, message, sender_id, reciever_id, parent_message_id, status;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()

    # def create_group(self, **kwargs):
    #     insert = f"""INSERT INTO group(groupId, name) VALUES ('{kwargs.get("groupId")}', '{kwargs.get("name")}')) RETURNING groupId, name;"""
    #     self.cursor.execute(insert)
    #     return self.cursor.fetchone()

    def create_group_members(self, **kwargs):
        insert = f"""INSERT INTO table_groupmembers(group_id, member_id) VALUES ('{kwargs.get("group_id")}', '{kwargs.get("member_id")}')) RETURNING group_id, member_id;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()

    def create_message(self, **kwargs):
        insert = f"""INSERT INTO messages(created_on, subject, message, status, sender_id, reciever_id) VALUES ( '{kwargs.get("created_on")}', '{kwargs.get("subject")}', '{kwargs.get("message")}', '{kwargs.get("status")}', {kwargs.get("sender_id")}, {kwargs.get("reciever_id")}) RETURNING ID, created_on, subject, message, status;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()

    def get_all_mails(self):
        query = f"""SELECT * FROM messages"""
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_recieved_messages_of_a_user(self, reciever_id):
        """
        Function to retrieve all messages
         with a particular user_id as the 
         reciever_id and a status of read 
        """
        query = "SELECT * FROM messages WHERE status = read or status= sent and reciever_id ='{}'".format(
            reciever_id)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_sent_messages_of_a_user(self, sender_id):
        query = "SELECT * FROM outbox WHERE sender_id ='{}'".format(sender_id)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_users(self):
        query = f"""SELECT * FROM users"""
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_induviduals_inbox(self, reciever_id):
        query = "SELECT * FROM inbox WHERE reciever_id ={}".format(reciever_id)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def modify_message_status(self, status, reciever_id, message_id):
        query = "UPDATE  inbox SET status = '{}' WHERE reciever_id = {} AND id = {}".format(
            status, reciever_id, message_id)
        self.cursor.execute(query)
        # return self.cursor.fetchone()

    def get_unread_mail_from_inbox(self, reciever_id):
        """get all unread from the inbox"""
        query = "SELECT * FROM inbox WHERE status = unread AND"

        # query = "SELECT messages.id, subject, status, receiver_id, sender_id FROM messages INNERJOIN inbox on message.id = inbox.message_id WHERE message.status=sent"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def delete_mail(self, message_id, reciever_id):
        """delete particular mail"""
        query = "DELETE FROM inbox WHERE id = {} AND reciever_id = {}".format(
            message_id, reciever_id)
        self.cursor.execute(query)

    def get_particular_message(self, message_id, reciever_id):
        query = "SELECT * FROM inbox WHERE message_id = {} AND reciever_id = {}".format(
            message_id, reciever_id)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_sent_mail_by_a_user(self, sender_id):
        query = "SELECT * FROM inbox WHERE sender_id = '{}'".format(sender_id)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def create_groups(self, admin, name, role):
        """This function creates a new group 
        and inserts the new groups data into the database
        """
        insert = f"""INSERT INTO epicgroups( admin, name, role) VALUES ( '{admin}','{name}', '{role}') RETURNING id, name, role;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()
   
    def fetch_all_groups(self, admin):
        query = "SELECT id, name, role FROM epicgroups WHERE admin = '{}'".format(admin)
        self.cursor.execute(query)
        return self.cursor.fetchall()
   
    def patch_group_name(self, group_id, group_name):
        query = "UPDATE epicgroups SET name = '{}' WHERE id = '{}'\
         RETURNING * ;".format(
            group_name, group_id)
        # query = "UPDATE  epicgroups SET name= '{}' WHERE id = {}.format(name, group_id)RETURNING id, name, role;
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def delete_particular_groups(self, group_id, admin):
        """Method to delete a particular group from the database"""
        # if len(self.check_if_group_id_exists(group_id)) > 1:
        query = "DELETE FROM epicgroups WHERE id = '{}' AND admin = '{}'".format(group_id, admin)
        self.cursor.execute(query)
        # return jsonify({"status": 400, "error": "There is no such group in the system"})

    def create_group(self, group_id, userid, userrole):
        
        """Function to add members to a group"""
        insert = f"""INSERT INTO clusters(group_id, userid, userrole) VALUES ('{group_id}', '{userid}',
        '{userrole}') RETURNING id, userid, userrole;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()

    def get_all_group_members(self, group_id):
        query = "SELECT id, userid, userrole FROM clusters WHERE group_id = '{}'".format(group_id)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def delete_user_from_specific_group(self, userid, group_id):
        query = "DELETE FROM clusters WHERE userid = {} AND group_id = {}".format(userid, group_id)
        self.cursor.execute(query)

    def get_all_groupnames(self, name):
        """Method to check whether the
         group name already exists
        """
        query = "SELECT * FROM epicgroups WHERE name = '{}'".format(name)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def check_if_group_id_exists(self, id):
        """Method to check whether the
         group id exists
        """
        query = "SELECT * FROM epicgroups WHERE id = '{}'".format(id)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_admin_of_a_group(self, group_id):
        query = "SELECT admin FROM epicgroups WHERE id = '{}'".format(group_id)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def check_user_available(self, user_id):
        query = "SELECT * FROM users WHERE id = {}".format(user_id)
        self.cursor.execute(query)
        return self.cursor.fetchone()
        





    
    # def add_user_to_group(self, id, user_id, user_role):
        
        


    # def delete a group(self):
    #     query = "DROP GROUP teachers"
