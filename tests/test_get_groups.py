import json
import unittest

from test_helper import create_group, create_user, delete_group, \
    delete_user, get_or_delete, post, unique_id


TEST_HOST = 'localhost'
TEST_PORT = 8000
GROUPS_URL = '/groups'


class TestGetGroups(unittest.TestCase):

    def setUp(self):
        self.group_name = unique_id()
        group_data = {
            'name': self.group_name
        }
        create_group(group_data)
        self.created_group_names = [self.group_name]
        self.created_user_ids = []

    def tearDown(self):
        for group_name in self.created_group_names:
            delete_group(group_name)
        for user_id in self.created_user_ids:
            delete_user(user_id)

    def test_get_created_group(self):
        response = get_or_delete('GET', TEST_HOST, TEST_PORT,
                                  GROUPS_URL, self.group_name)
        response_string = response.read().decode()
        response_json = json.loads(response_string)

        self.assertEqual(response.status, 200)
        self.assertTrue('userids' in response_json)
        self.assertEqual(response_json['userids'], [])

    def test_get_nonexistent_group(self):
        response = get_or_delete('GET', TEST_HOST, TEST_PORT,
                                 GROUPS_URL, 'foobar')
        response_string = response.read().decode()
        self.assertEqual(response.status, 404)

    def test_get_group_with_users(self):
        user_id = unique_id()
        self.created_user_ids.append(user_id)
        user_data = {
            'first_name': 'simple',
            'last_name': 'user',
            'userid': user_id,
            'groups': [self.group_name]
        }
        create_user(user_data)

        response = get_or_delete('GET', TEST_HOST, TEST_PORT,
                                  GROUPS_URL, self.group_name)
        response_string = response.read().decode()
        response_json = json.loads(response_string)

        self.assertEqual(response.status, 200)
        self.assertTrue('userids' in response_json)
        self.assertEqual(response_json['userids'], [user_id])

    def test_get_group_no_name(self):
        response = get_or_delete('GET', TEST_HOST, TEST_PORT,
                                  GROUPS_URL, '')
        self.assertEqual(response.status, 405)


if __name__ == '__main__':
    unittest.main()
