import datetime


user_list = []


class User:
    def __init__(self, **kwargs):
        """This method acts as a constructor
            for the users class, it initialises all class attributes
        """

        self.email = kwargs.get('email')
        self.firstname = kwargs.get('firstname')
        self.lastname = kwargs.get('lastname')
        self.password = kwargs.get('password')

    def get_dictionary(self):
        """this method converts the class attributes into json objects
        """
        return{
            "id": len(user_list)+1,
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "password": self.password

        }
