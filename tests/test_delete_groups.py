import unittest

from test_helper import create_group, delete_group, \
    delete_user, get_or_delete, get_group, unique_id


TEST_HOST = 'localhost'
TEST_PORT = 8000
GROUPS_URL = '/groups'


class TestDeleteGroups(unittest.TestCase):

    def setUp(self):
        self.group_name = unique_id()
        create_group({'name': self.group_name})
        self.created_group_names = [self.group_name]

    def tearDown(self):
        for group_name in self.created_group_names:
            delete_group(group_name)

    def test_delete_group(self):
        response = get_group(self.group_name)
        self.assertEqual(response.status, 200)

        response = get_or_delete('DELETE', TEST_HOST, TEST_PORT,
                                  GROUPS_URL, self.group_name)
        self.assertEqual(response.status, 200)

        response = get_group(self.group_name)
        self.assertEqual(response.status, 404)


    def test_delete_missing_group(self):
        response = get_or_delete('DELETE', TEST_HOST, TEST_PORT,
                                  GROUPS_URL, 'foobar')
        self.assertEqual(response.status, 404)

    def test_delete_group_no_name(self):
        response = get_or_delete('DELETE', TEST_HOST, TEST_PORT,
                                  GROUPS_URL, '')
        self.assertEqual(response.status, 405)


if __name__ == '__main__':
    unittest.main()
