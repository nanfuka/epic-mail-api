from tests.base_test import BaseTestCase
# from app.models.user import User

import json


class Test_messages(BaseTestCase):
    def test_get_recieved_messages(self):
        """
        Test a user is successfully created through the api
        """
        with self.client:
            response = self.get_all_recieved_mail()
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['status'], 200)  
            self.assertEqual(data['data'][0]['subject'], "graduation ceremony")  
            self.assertEqual(data['data'][0]['message'], 'invitation to attend my graduation') 
            self.assertEqual(data['data'][0]['parentMessageId'], 1)  
            self.assertEqual(data['data'][0]['status'], 'sent')
            self.assertEqual(data['data'][0]['sender_id'], 1)
            self.assertEqual(data['data'][0]['reciever_id'], 1)