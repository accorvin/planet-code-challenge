import unittest

from test_helper import delete_group, post, unique_id


TEST_HOST = 'localhost'
TEST_PORT = 8000
GROUPS_URL = '/groups'


class TestCreateGroups(unittest.TestCase):

    def setUp(self):
        self.created_group_names = []

    def tearDown(self):
        for group_name in self.created_group_names:
            delete_group(group_name)

    def test_create_simple_group(self):
        group_name = unique_id()
        self.created_group_names.append(group_name)
        group_data = {
            'name': group_name
        }
        response = post(TEST_HOST, TEST_PORT, GROUPS_URL, group_data)
        self.assertEqual(response.status, 200)

    def test_create_group_missing_name(self):
        group_name = unique_id()
        self.created_group_names.append(group_name)
        group_data = {
        }
        response = post(TEST_HOST, TEST_PORT, GROUPS_URL, group_data)
        self.assertEqual(response.status, 400)

    def test_create_group_existing_group(self):
        group_name = unique_id()
        self.created_group_names.append(group_name)
        group_data = {
            'name': group_name
        }
        response = post(TEST_HOST, TEST_PORT, GROUPS_URL, group_data)
        self.assertEqual(response.status, 200)
        response = post(TEST_HOST, TEST_PORT, GROUPS_URL, group_data)
        self.assertEqual(response.status, 400)


if __name__ == '__main__':
    unittest.main()
