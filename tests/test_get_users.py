import json
import unittest

from test_helper import create_group, create_user, delete_group, delete_user, \
    get_or_delete, post, unique_id


TEST_HOST = 'localhost'
TEST_PORT = 8000
USERS_URL = '/users'


class TestGetUsers(unittest.TestCase):

    def setUp(self):
        self.first_name = 'first_name'
        self.last_name = 'last_name'
        self.user_id = unique_id()
        self.groups = ['group1', 'group2']
        user_data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'userid': self.user_id,
            'groups': self.groups
        }
        create_group({'name': 'group1'})
        create_group({'name': 'group2'})
        create_user(user_data)
        self.created_user_ids = [self.user_id]

    def tearDown(self):
        for user_id in self.created_user_ids:
            delete_user(user_id)
        delete_group('group1')
        delete_group('group2')

    def test_get_created_user(self):
        response = get_or_delete('GET', TEST_HOST, TEST_PORT,
                                  USERS_URL, self.user_id)
        response_string = response.read().decode()
        response_json = json.loads(response_string)

        self.assertEqual(response.status, 200)
        self.assertTrue('first_name' in response_json)
        self.assertTrue('last_name' in response_json)
        self.assertTrue('userid' in response_json)
        self.assertTrue('groups' in response_json)

        self.assertEqual(self.first_name, response_json['first_name'])
        self.assertEqual(self.last_name, response_json['last_name'])
        self.assertEqual(self.user_id, response_json['userid'])
        self.assertEqual(self.groups, response_json['groups'])


if __name__ == '__main__':
    unittest.main()
