
import datetime


mail_list = []


class Mail:
    def __init__(self, **kwargs):
        """This method acts as a constructor
            for the users class, it initialises all class attributes
        """

        self.subject = kwargs.get('subject')
        self.message = kwargs.get('message')
        self.parentMessageId = kwargs.get('parentMessageId')
        self.status = kwargs.get('status')
        self.reciever_id = kwargs.get('reciever_id')
        self.sender_id = kwargs.get('sender_id')

    def get_dictionary(self):
        """this method converts the class attributes into json objects
        """
        return{
            "id": len(mail_list)+1,
            "createdOn": datetime.datetime.now(),
            "subject": self.subject,
            "message": self.message,
            "parentMessageId": self.parentMessageId,
            "status": self.status,
            "reciever_id": self.reciever_id,
            "sender_id": self.sender_id


        }
