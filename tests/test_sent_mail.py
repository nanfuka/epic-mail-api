from tests.base_test import BaseTestCase
import json


class Test_messages(BaseTestCase):

    def test_get_all_sent_mail_if_inbox_is_empty(self):
        with self.client:
            token = self.get_token()
            self.post_a_message("bookstore", "can you shift it", "draft",  1)
            response = self.client.get(
                'api/v1/messages/sent',
                content_type='application/json',
                headers=dict(Authorization='Bearer ' + token))

            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)

    def test_get_all_sent_mail_if_mail_list_is_empty(self):
        with self.client:
            response = self.get_all_unread_messages_given_empty_mail_list()
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['status'], 200)
