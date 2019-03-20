
import datetime


mail_list = []


class Mail:
    self.createdmail = []
   
    def __init__(self, subject, message, parentMessageId, status):
        """This method acts as a constructor
            for the users class, it initialises all class attributes
        """
        
        self.subject = subject
        self.message = message
        self.parentMessageId = parentMessageId
        self.status = status

    def get_dictionary(self):
        """this method converts the class attributes into json objects
        """
        return{
            "id": len(mail_list)+1,
            "createdOn": datetime.datetime.now(),
            "subject": self.subject,
            "message": self.message,
            "parentMessageId": self.parentMessageId,
            "status": self.status

        }


class Sent(Message):
    self.sent = []

    def __init__(self, senderId):
        Message.__init__(self, subject, message, parentMessageId, status)
        self.senderId = kwargs.get('senderId')

    def get_dictionary(self):
        """this method converts the class attributes into json objects
        """
        return{
            "id": len(self.sent)+1,
            "createdOn": datetime.datetime.now(),
            "subject": self.subject,
            "message": self.message,
            "parentMessageId": self.parentMessageId,
            "status": self.status

        }
    

class Inbox(sent):
    self.inbox = []
   
    def __init__(self, receiverId):
        Sent.__init__(self, senderId)
        self.receiverId = receiverId

    def get_dictionary(self):
        """this method converts the class attributes into json objects
        """
        return{
            "id": len(self.inbox)+1,
            "createdOn": datetime.datetime.now(),
            "subject": self.subject,
            "message": self.message,
            "parentMessageId": self.parentMessageId,
            "status": self.status,
            "senderId": self.senderId,
            "receiverId": self.receiverId

        }


