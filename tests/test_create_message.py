from tests.base_test import BaseTestCase
# from app.models.user import User

import json


class Test_messages(BaseTestCase):
    def test_post_a_message(self):
        """
        Test a user is successfully created through the api
        """
        with self.client:
            response = self.post_a_message("bookstore", "can you shift it",1,"draft",  1, 1)
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['status'], 201)  
            self.assertEqual(data['data'][0]['subject'], "bookstore")  
            self.assertEqual(data['data'][0]['message'], 'can you shift it') 
            self.assertEqual(data['data'][0]['parentMessageId'], 1)  
            self.assertEqual(data['data'][0]['status'], 'draft') 

    def test_post_a_message_with_very_short_subject(self):
        """
        Test a user is successfully created through the api
        """
        with self.client:
            response = self.post_a_message("df", "can you shift it",1,"draft",  1, 1)
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['status'], 400) 
            self.assertEqual(data['error'], ' the subject of the mail is too short')  

    def test_post_a_message_with_very_long_subject(self):
        """
        Test a user is successfully created through the api
        """
        with self.client:
            response = self.post_a_message("ddsffffffffffffffffffffffffffffffffffffssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddsssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssf", "can you shift it",1,"draft",  1, 1)
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['status'], 400) 
            self.assertEqual(data['error'], " the subject line is too long, write your message in the message box")          



    def test_post_a_message_without_token(self):
        """
        Test a user is successfully created through the api
        """
        with self.client:
            response = self.post_a_message_without_token("bookstore", "can you shift it",1,"draft",  1, 1)
            self.assertEqual(response.status_code, 401)
            data = json.loads(response.data)
            self.assertEqual(data['message'], 'Token does not exist')  

    def test_post_a_message_with_invalid_token(self):
        """
        Test a user is successfully created through the api
        """
        with self.client:
            response = self.post_a_message_with_invalid_token("bookstore", "can you shift it",1,"draft",  1, 1)
            self.assertEqual(response.status_code, 401)
            data = json.loads(response.data)
            self.assertEqual(data['message'], 'Token Decode Failed!') 

    def test_post_a_message_without_subject(self):
        """
        Test post amessage without a subject
        """
        with self.client:
            response = self.post_a_message("", "can you shift it",1,"draft",  1, 1)
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'please enter the subject of your message')  
            self.assertEqual(data['status'], 400)  
         
    def test_post_a_message_without_message(self):
        """
        Test post amessage without a subject
        """
        with self.client:
            response = self.post_a_message("bookstore", "",1,"draft",  1, 1)
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'please enter your message')  
            self.assertEqual(data['status'], 400) 

    def test_post_a_message_with_invalid_parent_id(self):
        """
        Test post amessage without a subject
        """
        with self.client:
            response = self.post_a_message("bookstore", "can you shift it","jsdfhs","draft",  1, 1)
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'parentMessageId should be a number')  
            self.assertEqual(data['status'], 400) 

    def test_post_a_message_with_invalid_status(self):
        """
        Test post amessage without a subject
        """
        with self.client:
            response = self.post_a_message("bookstore", "can you shift it",1,"pending",  1, 1)
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'status should either be sent, read or draft')  
            self.assertEqual(data['status'], 400) 

    # def test_post_a_message_with_invalid_sender_id(self):
    #     """
    #     Test post amessage with invalid sender_id
    #     """
    #     with self.client:
    #         response = self.post_a_message("bookstore", "can you shift it",1,"draft", "", 1)
    #         self.assertEqual(response.status_code, 200)
    #         data = json.loads(response.data)
    #         self.assertEqual(data['error'], 'sender_id should be a number')  
    #         self.assertEqual(data['status'], 400) 

    def test_post_a_message_with_invalid_reciever_id(self):
        """
        Test post amessage without a subject
        """
        with self.client:
            response = self.post_a_message("bookstore", "can you shift it",1,"draft",  1, 'hgjhg')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'reciever_id should be a number')  
            self.assertEqual(data['status'], 400)

    # def test_post_a_message_with_unregistered_reciever_id(self):
    #     """
    #     Test post amessage without a subject
    #     """
    #     with self.client:
    #         response = self.post_a_message("bookstore", "can you shift it",1,"draft",  1, 10)
    #         self.assertEqual(response.status_code, 200)
    #         data = json.loads(response.data)
    #         self.assertEqual(data['error'], 'The submited reciever_id is not registered with the application. please enter a valid reciever_id')  
    #         self.assertEqual(data['status'], 400) 

    # def test_get_all_recieved_mail(self):
    #     with self.client:
    #         response = self.get_all_recieved_mail()
    #         self.assertEqual(response.status_code, 200) 

    #     # def test_get_all_unrecieved_mail(self):
    #     #     response = self.view_sent_messages()
    #     #     self.assertEqual(response.status_code, 200) 

    #     def test_get_all_unread_mail(self):
    #         pass
    # def test_get_all_sent_mail(self):
    #     with self.client:
    #         response = self.view_sent_messages()
    #         self.assertEqual(response.status_code, 200) 
            
    #     def test_get_specific_users_email(self):
    #         pass

    #     def test_delete_specific_users_email(self):
    #         pass



    #  def test_post_without_a_subject(self):
    #     """
    #     Test a user is successfully created through the api
    #     """
    #     with self.client:


    #         response = self.post_a_message("", "can you shift it", 1, "draft", 1)
    #         self.assertEqual(response.status_code, 200)
    #         data = json.loads(response.data)
    #         self.assertEqual(data['status'], 400)  
        

    # def test_view_all_sent_messages(self):
    #     """
    #     Test view all sent messages
    #     """
    #     with self.client:


    #         response = self.view_sent_messages()
    #         self.assertEqual(response.status_code, 200) 

    # def test_retrieve_a_particular_message(self):
    #     """
    #             Test retrieve a particular message
    #     """
    #     with self.client:


    #         response = self.retrieve_a_message()
    #         self.assertEqual(response.status_code, 200)

    # def test_delete_a_particular_message(self):
    #     """
    #             Test retrieve a particular message
    #     """
    #     with self.client:


    #         response = self.delete_a_particular_message()
    #         self.assertEqual(response.status_code, 200)