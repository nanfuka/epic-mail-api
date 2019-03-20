from tests.base_test import BaseTestCase
# from app.models.user import User

import json


class Test_messages(BaseTestCase):
    
    def test_get_all_sent_mail(self):
        with self.client:
            response = self.view_sent_messages()
            self.assertEqual(response.status_code, 200) 
            data = json.loads(response.data)
            self.assertEqual(data['status'], 200)  
            self.assertEqual(data['data'][0]['subject'], "graduation ceremony")  
            self.assertEqual(data['data'][0]['message'], 'invitation to attend my graduation') 
            self.assertEqual(data['data'][0]['parentMessageId'], 1)  
            self.assertEqual(data['data'][0]['status'], 'sent') 

    def test_get_all_sent_mail_if_inbox_is_empty(self):
        with self.client:
            token = self.get_token()
            self.post_a_message("bookstore", "can you shift it",1,"draft",  1, 1)
            response = self.client.get('api/v1/messages/sent', content_type='application/json', headers=dict(Authorization='Bearer ' + token))
            # response = self.view_sent_messages()
            self.assertEqual(response.status_code, 200) 
            data = json.loads(response.data)
            self.assertEqual(data['status'], 200) 

            # data = json.loads(response.data)
            # self.assertEqual(data['status'], 200)  
            # self.assertEqual(data['data'][0]['subject'], "graduation ceremony")  
            # self.assertEqual(data['data'][0]['message'], 'invitation to attend my graduation') 
            # self.assertEqual(data['data'][0]['parentMessageId'], 1)  
            # self.assertEqual(data['data'][0]['status'], 'sent') 
