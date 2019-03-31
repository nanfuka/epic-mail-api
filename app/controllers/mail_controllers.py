from app.db import Database
import psycopg2
from psycopg2.extras import RealDictCursor
from pprint import pprint
import os
from os import environ
from flask import Flask, jsonify, request, json
# import json


class Mail(Database):
    def signup(self, **kwargs):
        insert = f"""INSERT INTO users(
            firstname,
            lastname,
            email,
            password) VALUES (
                '{kwargs.get("firstname")}',
                '{kwargs.get("lastname")}',
                '{kwargs.get("email")}',
                '{kwargs.get("password")}') RETURNING id,
                firstname, lastname, email;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()

    def check_email(self, email):
        query = "SELECT * FROM users WHERE email = '{}'".format(email)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def login(self, email, password):
        query = "SELECT * FROM users WHERE email = '{}'\
            and password = '{}'".format(
            email, password)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def create_message(self, **kwargs):
        insert = f"""INSERT INTO messages(subject, message, status) \
            VALUES ( '{kwargs.get("subject")}',
            '{kwargs.get("message")}',
            '{kwargs.get("status")}') RETURNING ID,
            subject, message, status;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()

    def create_groupmessage(self, **kwargs):
        insert = f"""INSERT INTO groupmessages(
            group_id,
            subject,
            message,
            status,
            created_on) VALUES ( 
                '{kwargs.get("group_id")}',
                '{kwargs.get("subject")}',
                '{kwargs.get("message")}',
                '{kwargs.get("status")}',
                '{kwargs.get("created_on")}')\
                     RETURNING id,
                     subject,
                     message,
                     status,
                     created_on;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()

    def create_sent(self, **kwargs):

        insert = f"""INSERT INTO sent(
            sender_id,
            message_id,
            created_on)\
                 VALUES ('{kwargs.get("sender_id")}',
                 '{kwargs.get("message_id")}',
                 '{kwargs.get("created_on")}')\
                     RETURNING sender_id,
                     message_id,
                     created_on;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()

    def get_outtbox(self, sender_id):
        insert = f"""INSERT INTO outbox(
            created_on,
            subject,
            message,
            sender_id,
            reciever_id,
            parent_message_id,
            status) VALUES ( 
                '{kwargs.get("created_on")}',
                '{kwargs.get("subject")}',
                '{kwargs.get("message")}',
                '{kwargs.get("sender_id")}',
                '{kwargs.get("reciever_id")}',
                '{kwargs.get("parent_message_id")}',
                '{kwargs.get("status")}') \
                    RETURNING id,
                    created_on,
                    subject,
                    message,
                    sender_id,
                    reciever_id,
                    parent_message_id,
                    status;
                    """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def create_inbox(self, **kwargs):
        insert = f"""INSERT INTO inbox(
            created_on,
            subject,
            message,
            sender_id,
            reciever_id,
            parent_message_id,
            status) VALUES (
                 '{kwargs.get("created_on")}',
                 '{kwargs.get("subject")}',
                 '{kwargs.get("message")}',
                 '{kwargs.get("sender_id")}',
                 '{kwargs.get("reciever_id")}',
                 '{kwargs.get("parent_message_id")}',
                 '{kwargs.get("status")}')\
                      RETURNING id,
                      created_on,
                      subject,
                      message,
                      sender_id,
                      reciever_id,
                      parent_message_id,
                      status;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()

    def create_group_members(self, **kwargs):
        insert = f"""INSERT INTO table_groupmembers(
            group_id,
            member_id)\
                 VALUES ('{kwargs.get("group_id")}',
                 '{kwargs.get("member_id")}'))\
                      RETURNING group_id,
                      member_id;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()

    def create_message(self, **kwargs):
        insert = f"""INSERT INTO messages(
            created_on,
            subject,
            message,
            status,
            sender_id,
            reciever_id) VALUES ('{kwargs.get("created_on")}',
            '{kwargs.get("subject")}',
            '{kwargs.get("message")}',
            '{kwargs.get("status")}',
            {kwargs.get("sender_id")},
            {kwargs.get("reciever_id")}) \
                RETURNING ID,
                created_on,
                subject,
                message,
                status;"""
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
        query = "SELECT * FROM messages WHERE status = read \
            or status= sent and reciever_id ='{}'".format(
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
        query = "UPDATE  inbox SET status = '{}'\
             WHERE reciever_id = {} AND id = {}".format(
            status, reciever_id, message_id)
        self.cursor.execute(query)
        # return self.cursor.fetchone()

    def get_unread_mail_from_inbox(self, status, reciever_id):
        """get all unread from the inbox"""
        query = "SELECT * FROM inbox WHERE status ='{}' \
            and reciever_id = {}".format(status, reciever_id)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def delete_mail(self, message_id, reciever_id):
        """delete particular mail"""
        query = "DELETE FROM inbox WHERE id = {} AND reciever_id = {}".format(
            message_id, reciever_id)
        self.cursor.execute(query)

    def get_particular_message(self, message_id, reciever_id):
        query = "SELECT * FROM inbox WHERE id = {} \
            AND reciever_id = {}".format(
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
        insert = f"""INSERT INTO epicgroups( admin, name, role) VALUES \
            ('{admin}',
            '{name}',
            '{role}') RETURNING id, name, role;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()

    def fetch_all_groups(self, admin):
        query = "SELECT id, name, role FROM epicgroups \
            WHERE admin = '{}'".format(admin)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def patch_group_name(self, group_id, group_name):
        query = "UPDATE epicgroups SET name = '{}' WHERE id = '{}'\
         RETURNING * ;".format(
            group_name, group_id)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def delete_particular_groups(self, group_id, admin):
        """Method to delete a particular group from the database"""
        query = "DELETE FROM epicgroups WHERE id = '{}' \
            AND admin = '{}'".format(group_id, admin)
        self.cursor.execute(query)

    def create_group(self, group_id, userid, userrole):
        """Function to add members to a group"""
        insert = f"""INSERT INTO clusters(group_id, userid, userrole)\
             VALUES ('{group_id}', '{userid}',
        '{userrole}') RETURNING id, userid, userrole;"""
        self.cursor.execute(insert)
        return self.cursor.fetchone()

    def get_all_group_members(self, group_id):
        query = "SELECT id, userid, userrole FROM clusters \
            WHERE group_id = '{}'".format(group_id)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def delete_user_from_specific_group(self, userid, group_id):
        query = "DELETE FROM clusters WHERE userid = {} AND\
             group_id = {}".format(userid, group_id)
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

    def check_if_message_id_exists(self, id):
        """Method to check whether the
        message id given exists in the inbox
        """
        query = "SELECT * FROM inbox WHERE id = '{}'".format(id)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def drop_table(self, table_name):
        drop_table = "DROP TABLE IF EXISTS {}".format(table_name)
        self.cursor.execute(drop_table)
