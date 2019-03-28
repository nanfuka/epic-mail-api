from tests.base_test import BaseTestCase
import json


class Test_messages(BaseTestCase):
    def test_change_group(self):
        """
        Test delete a particular group
        """
        with self.client:
            response = self.change_group_name("treasures")
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['status'], 200)
            # self.assertEqual(
            #     data['message'],
            #     'the message with supplied message_id is not available')
