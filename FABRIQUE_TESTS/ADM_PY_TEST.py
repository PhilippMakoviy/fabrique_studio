import requests
from requests.auth import HTTPBasicAuth
#from rest_framework.parsers import MultiPartParser , FormParser, JSONParser

from settings import API_URL, ADMIN_USERNAME, ADMIN_PASSWORD

basicAuth = HTTPBasicAuth(ADMIN_USERNAME, ADMIN_PASSWORD)


class TestAdmin:
    poll_id = None

    def get_first_poll(self):
        res = requests.get(API_URL + '/admin/polls', auth=basicAuth)
        assert res.status_code == 200
        data = res.json()
        return data[0]['id']

    def test_no_auth(self):
        res = requests.get(API_URL + '/admin/polls')
        assert res.status_code == 401

    def test_auth(self):
        res = requests.get(API_URL + '/admin/polls', auth=basicAuth)
        assert res.status_code == 200
        data = res.json()
        assert type(data) is list

    def test_create_poll(self):
        poll = {
            'name': 'Test1',
            'description': 'description1',
            'start_date': '2021-05-02',
            'end_date': '2021-05-30'
        }
        res = requests.post(API_URL + '/admin/polls', auth=basicAuth, data=poll)
        assert res.status_code == 200
        data = res.json()
        TestAdmin.poll_id = data['id']

    def test_create_poll_with_invalid_dates(self):
        poll = {
            'name': 'Test invalid dates',
            'description': 'description',
            'start_date': '2021-05-02',
            'end_date': '2020-05-30'
        }
        res = requests.post(API_URL + '/admin/polls', auth=basicAuth, data=poll)
        assert res.status_code == 400

    def test_poll_by_id(self):
        res = requests.get(API_URL + '/admin/polls/%d' % TestAdmin.poll_id, auth=basicAuth)
        assert res.status_code == 200
        data = res.json()
        assert data['id'] == TestAdmin.poll_id

    def test_poll_by_invalid_id(self):
        id = 98765
        res = requests.get(API_URL + '/admin/polls/%d' % id, auth=basicAuth)
        assert res.status_code == 404

    def test_edit_poll(self):
        res = requests.get(API_URL + '/admin/polls/%d' % TestAdmin.poll_id, auth=basicAuth)
        assert res.status_code == 200
        prevPoll = res.json()

        edit = {
            'name': 'Test edited',
            'description': 'Description updated',
            'end_date': '2021-05-31'
        }
        res = requests.patch(API_URL + '/admin/polls/%d' % TestAdmin.poll_id, auth=basicAuth, data=edit)
        assert res.status_code == 200
        updatedPoll = res.json()
        assert prevPoll['id'] == updatedPoll['id']
        assert prevPoll['name'] != updatedPoll['name']
        assert prevPoll['description'] != updatedPoll['description']
        assert prevPoll['end_date'] != updatedPoll['end_date']

    def test_edit_poll_start_date(self):
        res = requests.get(API_URL + '/admin/polls/%d' % TestAdmin.poll_id, auth=basicAuth)
        assert res.status_code == 200
        prevPoll = res.json()

        edit = {
            'start_date': '2021-05-02'
        }
        res = requests.patch(API_URL + '/admin/polls/%d' % TestAdmin.poll_id, auth=basicAuth, data=edit)
        assert res.status_code == 200
        updatedPoll = res.json()
        assert prevPoll['start_date'] == updatedPoll['start_date']

    def test_delete_poll(self):
        res = requests.delete(API_URL + '/admin/polls/%d' % TestAdmin.poll_id, auth=basicAuth)
        assert res.status_code == 200
        TestAdmin.poll_id = None

    def test_delete_nonexistent_poll(self):
        id = 98765
        res = requests.delete(API_URL + '/admin/polls/%d' % id, auth=basicAuth)
        assert res.status_code == 404