import json
import unittest

from test_helper import create_group, create_user, delete_group, \
    delete_user, get_or_delete, get_group, put, unique_id


TEST_HOST = 'localhost'
TEST_PORT = 8000
GROUPS_URL = '/groups'


class TestUpdateGroups(unittest.TestCase):

    def setUp(self):
        self.group_name = unique_id()
        group_data = {'name': self.group_name}
        self.user_1_name = unique_id()
        self.user_2_name = unique_id()
        user_1_data = {
            'first_name': 'first',
            'last_name': 'user',
            'userid': self.user_1_name,
            'groups': [self.group_name]
        }
        user_2_data = {
            'first_name': 'second',
            'last_name': 'user',
            'userid': self.user_2_name,
            'groups': []
        }
        create_group(group_data)
        create_user(user_1_data)
        create_user(user_2_data)

    def tearDown(self):
        delete_user(self.user_1_name)
        delete_user(self.user_2_name)
        delete_group(self.group_name)

    def test_update_group(self):
        response = get_group(self.group_name)
        response_string = response.read().decode()
        response_json = json.loads(response_string)
        self.assertEqual(response.status, 200)
        users = response_json['userids']
        self.assertTrue(self.user_1_name in users)
        self.assertTrue(self.user_2_name not in users)

        new_members = {'userids': [self.user_2_name]}
        response = put(TEST_HOST, TEST_PORT,
                       GROUPS_URL, self.group_name, new_members)
        self.assertEqual(response.status, 200)

        response = get_group(self.group_name)
        response_string = response.read().decode()
        response_json = json.loads(response_string)
        self.assertEqual(response.status, 200)
        users = response_json['userids']
        self.assertTrue(self.user_2_name in users)
        self.assertTrue(self.user_1_name not in users)


    def test_update_group_missing_members(self):
        response = put(TEST_HOST, TEST_PORT,
                       GROUPS_URL, self.group_name, {})
        self.assertEqual(response.status, 400)

    def test_update_nonexistent_group(self):
        members = {'userids': []}
        response = put(TEST_HOST, TEST_PORT,
                       GROUPS_URL, 'foobar', members)
        self.assertEqual(response.status, 404)

    def test_update_group_no_name(self):
        members = {'userids': []}
        response = put(TEST_HOST, TEST_PORT,
                       GROUPS_URL, '', members)
        self.assertEqual(response.status, 405)


if __name__ == '__main__':
    unittest.main()
