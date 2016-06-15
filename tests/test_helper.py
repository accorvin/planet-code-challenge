import http.client
import json
import urllib
import uuid


TEST_HOST = 'localhost'
TEST_PORT = 8000
USERS_URL = '/users'
GROUPS_URL = '/groups'


def unique_id():
    return str(uuid.uuid1())


def post(host, port, url, body_data):
    headers = {'Content-type': 'application/x-www-form-urlencoded',
               'Accept': 'text/plain'}
    conn = http.client.HTTPConnection(host, port)
    conn.request('POST', url, json.dumps(body_data), headers)
    response = conn.getresponse()

    return response


def get_or_delete(method, host, port, url, identifier):
    full_url = '{0}/{1}'.format(url, identifier)
    headers = {'Content-type': 'application/x-www-form-urlencoded',
               'Accept': 'text/plain'}
    conn = http.client.HTTPConnection(host, port)
    conn.request(method, full_url, '', headers)
    response = conn.getresponse()

    return response


def get_user(user_id):
    return get_or_delete('GET', TEST_HOST, TEST_PORT, USERS_URL, user_id)


def create_user(user_data):
    post(TEST_HOST, TEST_PORT, USERS_URL, user_data)


def create_group(group_data):
    post(TEST_HOST, TEST_PORT, GROUPS_URL, group_data)


def delete_user(user_id):
    get_or_delete('DELETE', TEST_HOST, TEST_PORT, USERS_URL, user_id)


def delete_group(group_name):
    get_or_delete('DELETE', TEST_HOST, TEST_PORT, GROUPS_URL, group_name)
