import datetime
import jwt
from app.models.mail import Mail, mail_list
from app.auth import Authentication
authentication = Authentication()


class Mail_controller:
    def create_mail(self, **kwargs):
        """function for creating a new message"""
        mail = Mail(**kwargs)
        new_mail = mail.get_dictionary()
        # mail_list.append(new_mail)
        # return new_mail
        message = {"id": new_mail['id'],
                   "createdOn": new_mail['createdOn'],
                   "subject": new_mail['subject'],
                   "message": new_mail['message'],
                   "parentMessageId": new_mail['id'],
                   "status": new_mail['status'],
                   "sender_id": new_mail['sender_id'],
                   "reciever_id": new_mail['reciever_id']}
        mail_list.append(message)

        return {"id": new_mail['id'],
                "createdOn": new_mail['createdOn'],
                "subject": new_mail['subject'],
                "message": new_mail['message'],
                "parentMessageId": new_mail['id'],
                "status": new_mail['status']
                }

    def get_all_recieved_messages_of_a_user(self, reciever_id):
        """
        Function to retrieve all messages
         with a particular user_id as the 
         reciever_id and a status of read 
         """
        recieved_mail = []

        for mail in mail_list:
            if mail['status'] == "read" and mail['reciever_id'] == reciever_id:
                recieved_mail.append(mail)

            if mail['status'] == "sent" and mail['reciever_id'] == reciever_id:
                recieved_mail.append(mail)
                
        if recieved_mail:
            return {'status': 200, "data": recieved_mail}
        return {
                "status": 200, 
                "message":
                "there is no recieved mail to the current reciever_id yet"}
        if not mail_list:
            return {"status": 200,
                    "message": "There isn't any mail in the inbox"}

    def get_all_unread_mail_for_a_user(self, reciever_id):
        """
        Function to retrieve all messages
         with a particular user_id and a status of sent"""
        unread = []
        for mail in mail_list:
            if mail['status'] == "sent" and mail['reciever_id'] == reciever_id:
                unread.append(mail)

        if unread:
            return {"status": 200, "data": unread}
        return {"status": 200,
                "message": "there are no recieved unread mails yet"}
        if not mail_list:
            return {"status": 200,
                    "message": "There isn't any mail in the inbox"}

    def get_all_mail_sent_by_a_user(self, sender_id):
        """
        Function to retrieve all mail whose 
        sender_id is the same as the logged in user_id
        """
        sent = []
        if not mail_list:
            return {"status": 200,
                    "message": "There isn't any mail in the inbox"}
        for mail in mail_list:
            if mail['status'] == "sent" and mail['sender_id'] == sender_id:
                sent.append(mail)
        return {"sent": sent}
        
    def get_specific_users_email(self, mail_id):
        """Function that retrieves a particular mail"""

        for mail in mail_list:

            if mail['id'] != mail_id:
                return {
                    "status": 200,
                    "message": "There isnt any mail with the given mail_id"}
            if mail['id'] == mail_id:
                return {"status": 200, "data": [mail]}
        if not mail_list:
            return {"status": 200,
                    "message": "There isn't any mail in the inbox"}

    def delete_specific_users_email(self, mail_id):
        """A user can delete their email with a particular email_id"""

        for message in mail_list:
            if len(mail_list) < 1:
                return {"message": "there are currently no emails"}
            if message['id'] == mail_id:
                mail_list.remove(message)
                return {
                    "status": 200,
                    "message": "email successfully deleted from the system"}
            return {"status": 200, "message": "the id provided is not yet in the system"}
        if not mail_list:
            return {
                "status": 200,
                "message": "There isn't any mail in the inbox"}

        

    def retrieve_a_message(self):
        """Method to retrieve a message"""
        self.post_a_message()
        return self.client.get(
            'api/v1/message/1'
        )
   
