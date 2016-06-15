import unittest

from test_helper import create_group, create_user, delete_group, \
    delete_user, get_or_delete, get_user, post, unique_id


TEST_HOST = 'localhost'
TEST_PORT = 8000
USERS_URL = '/users'


class TestCreateUsers(unittest.TestCase):

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

    def test_delete_user(self):
        response = get_user(self.user_id)
        self.assertEqual(response.status, 200)

        response = get_or_delete('DELETE', TEST_HOST, TEST_PORT,
                                  USERS_URL, self.user_id)
        self.assertEqual(response.status, 200)

        response = get_user(self.user_id)
        self.assertEqual(response.status, 404)


    def test_delete_missing_user(self):
        response = get_or_delete('DELETE', TEST_HOST, TEST_PORT,
                                  USERS_URL, 'foobar')
        self.assertEqual(response.status, 404)

    def test_delete_user_no_userid(self):
        response = get_or_delete('DELETE', TEST_HOST, TEST_PORT,
                                  USERS_URL, '')
        self.assertEqual(response.status, 405)


if __name__ == '__main__':
    unittest.main()
