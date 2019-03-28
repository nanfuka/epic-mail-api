from tests.base_test import BaseTestCase
import json


class Test_messages(BaseTestCase):
    def test_deleted_mail(self):
        """
        Test delete a mail with unavailable message_id
        """
        with self.client:
            response = self.delete_a_particular_message()
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['status'], 404)
            self.assertEqual(
                data['message'],
                'the message with supplied message_id is not available')
