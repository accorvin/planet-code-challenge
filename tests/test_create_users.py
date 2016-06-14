import unittest

from test_helper import delete_user, post, unique_id


TEST_HOST = 'localhost'
TEST_PORT = 8000
USERS_URL = '/users'


class TestCreateUsers(unittest.TestCase):

    def setUp(self):
        self.created_user_ids = []

    def tearDown(self):
        for user_id in self.created_user_ids:
            delete_user(user_id)

    def test_create_simple_user(self):
        user_id = unique_id()
        self.created_user_ids.append(user_id)
        user_data = {
            'first_name': 'simple',
            'last_name': 'user',
            'userid': user_id,
            'groups': ['group1', 'group2']
        }
        response = post(TEST_HOST, TEST_PORT, USERS_URL, user_data)
        self.assertEqual(response.status, 200)


    def test_create_user_missing_fname(self):
        user_id = unique_id()
        self.created_user_ids.append(user_id)
        user_data = {
            'last_name': 'user',
            'userid': user_id,
            'groups': ['group1', 'group2']
        }
        response = post(TEST_HOST, TEST_PORT, USERS_URL, user_data)
        self.assertEqual(response.status, 400)


    def test_create_user_missing_lname(self):
        user_id = unique_id()
        self.created_user_ids.append(user_id)
        user_data = {
            'first_name': 'user',
            'userid': user_id,
            'groups': ['group1', 'group2']
        }
        response = post(TEST_HOST, TEST_PORT, USERS_URL, user_data)
        self.assertEqual(response.status, 400)


    def test_create_user_missing_uid(self):
        user_id = unique_id()
        self.created_user_ids.append(user_id)
        user_data = {
            'first_name': 'user',
            'last_name': 'lname',
            'groups': ['group1', 'group2']
        }
        response = post(TEST_HOST, TEST_PORT, USERS_URL, user_data)
        self.assertEqual(response.status, 400)


    def test_create_user_missing_groups(self):
        user_id = unique_id()
        self.created_user_ids.append(user_id)
        user_data = {
            'first_name': 'user',
            'last_name': 'lname',
            'userid': user_id
        }
        response = post(TEST_HOST, TEST_PORT, USERS_URL, user_data)
        self.assertEqual(response.status, 400)


    def test_create_user_existing_user(self):
        user_id = unique_id()
        self.created_user_ids.append(user_id)
        user_data = {
            'first_name': 'existing',
            'last_name': 'user',
            'userid': user_id,
            'groups': ['group1', 'group2']
        }
        response = post(TEST_HOST, TEST_PORT, USERS_URL, user_data)
        self.assertEqual(response.status, 200)
        response = post(TEST_HOST, TEST_PORT, USERS_URL, user_data)
        self.assertEqual(response.status, 400)


if __name__ == '__main__':
    unittest.main()
