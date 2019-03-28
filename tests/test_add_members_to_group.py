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
            self.assertEqual(data['status'], 404)
            self.assertEqual(data['error'], 'the group is non existant')