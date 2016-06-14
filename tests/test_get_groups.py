import json
import unittest

from test_helper import create_group, delete_group, get_or_delete, post, \
    unique_id


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

    def tearDown(self):
        for group_name in self.created_group_names:
            delete_group(group_name)

    def test_get_created_group(self):
        response = get_or_delete('GET', TEST_HOST, TEST_PORT,
                                  GROUPS_URL, self.group_name)
        response_string = response.read().decode()
        response_json = json.loads(response_string)

        self.assertEqual(response.status, 200)


if __name__ == '__main__':
    unittest.main()
