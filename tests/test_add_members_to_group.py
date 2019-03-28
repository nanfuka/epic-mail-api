from tests.base_test import BaseTestCase
import json


class Test_messages(BaseTestCase):
    def test_add_members_to_group(self):
        """
        Test successfully add members to a group
        """
        with self.client:
            response = self.add_members_togroup(1, "treasures")
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['status'], 201)
            self.assertEqual(data['data'][0]['id'], 1)
            self.assertEqual(data['data'][0]['userid'], 1)
            self.assertEqual(data['data'][0]['userrole'], 'treasures')

    def test_add_members_to_group_without_userid(self):
        """
        Test successfully add members to a group
        """
        with self.client:
            response = self.add_members_togroup("", "treasures")
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['status'], 400)

            self.assertEqual(data['error'], 'Enter user_id')

    def test_add_members_to_group_without_role(self):
        """
        Test successfully add members to a group
        """
        with self.client:
            response = self.add_members_togroup(1, "")
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['status'], 400)

            self.assertEqual(data['error'], 'Enter userrole')

    def test_add_members_to_group_with_invalid_userid(self):
        """
        Test successfully add members to a group
        """
        with self.client:
            response = self.add_members_togroup("dsdsa", "treasures")
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['status'], 400)
            self.assertEqual(data['error'], 'The user_id should be a number')

    def test_add_members_to_group_with_invalid_role(self):
        """
        Test successfully add members to a group
        """
        with self.client:
            response = self.add_members_togroup(1, 1)
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['status'], 400)
            self.assertEqual(data['error'], 'User role should be a string')
