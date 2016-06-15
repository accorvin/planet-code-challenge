import json
import unittest

from test_helper import create_group, create_user, delete_group, \
    delete_user, get_or_delete, get_user, put, unique_id


TEST_HOST = 'localhost'
TEST_PORT = 8000
USERS_URL = '/users'


class TestUpdateUsers(unittest.TestCase):

    def setUp(self):
        self.user_id = unique_id()
        self.group1_name = unique_id()
        self.group2_name = unique_id()

        group1_data = {'name': self.group1_name}
        group2_data = {'name': self.group2_name}

        self.new_user_id = unique_id()
        self.old_user_data = {
            'first_name': 'first',
            'last_name': 'user',
            'userid': self.user_id,
            'groups': [self.group1_name]
        }
        self.new_user_data = {
            'first_name': 'second',
            'last_name': 'user',
            'userid': self.new_user_id,
            'groups': [self.group2_name]
        }
        create_group(group1_data)
        create_group(group2_data)

        create_user(self.old_user_data)

    def tearDown(self):
        delete_user(self.new_user_id)
        delete_user(self.user_id)
        delete_group(self.group1_name)
        delete_group(self.group2_name)

    def test_update_user(self):
        response = get_user(self.user_id)
        response_string = response.read().decode()
        response_json = json.loads(response_string)
        self.assertEqual(response.status, 200)
        self.assertEqual(response_json, self.old_user_data)

        response = put(TEST_HOST, TEST_PORT,
                       USERS_URL, self.user_id, self.new_user_data)
        self.assertEqual(response.status, 200)

        response = get_user(self.new_user_id)
        response_string = response.read().decode()
        response_json = json.loads(response_string)
        self.assertEqual(response.status, 200)
        self.assertEqual(response_json, self.new_user_data)

    def test_update_user_missing_data(self):
        response = put(TEST_HOST, TEST_PORT,
                       USERS_URL, self.user_id, {})
        self.assertEqual(response.status, 400)

    def test_update_nonexistent_user(self):
        user_data = {
            'first_name': 'first',
            'last_name': 'user',
            'userid': 'foobar',
            'groups': []
        }
        response = put(TEST_HOST, TEST_PORT,
                       USERS_URL, 'foobar', user_data)
        self.assertEqual(response.status, 404)

    def test_update_user_no_name(self):
        user_data = {
            'first_name': 'first',
            'last_name': 'user',
            'userid': 'foobar',
            'groups': []
        }
        response = put(TEST_HOST, TEST_PORT,
                       USERS_URL, '', user_data)
        self.assertEqual(response.status, 405)


if __name__ == '__main__':
    unittest.main()
