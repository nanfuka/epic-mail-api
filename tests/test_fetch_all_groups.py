from tests.base_test import BaseTestCase

import json


class Test_messages(BaseTestCase):
    def test_fetch_all_groups(self):
        """
        Test get recieved mail
        """
        with self.client:
            response = self.fetch_all_groups()
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['status'], 200)
 
            # self.assertEqual(data['data'][0]['subject'], 'bnbjhb')
            # self.assertEqual(
            #     data['data'][0]['message'],
            #     '1')
         
            # self.assertEqual(data['data'][0]['status'], 'sent')
            # self.assertEqual(data['data'][0]['sender_id'], 1)
            # self.assertEqual(data['data'][0]['reciever_id'], 1)