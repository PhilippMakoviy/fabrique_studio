import requests
import pytest
from requests.auth import HTTPBasicAuth

from settings import API_URL, ADMIN_USERNAME, ADMIN_PASSWORD

basicAuth = HTTPBasicAuth(ADMIN_USERNAME, ADMIN_PASSWORD)


@pytest.fixture(scope='class')
def poll_id(request):
    poll = {
        'name': 'Question Test',
        'description': 'Test poll with questions',
        'start_date': '2021-05-02',
        'end_date': '2021-05-30'
    }
    res = requests.post(API_URL + '/admin/polls', auth=basicAuth, data=poll)
    assert res.status_code == 200
    data = res.json()
    id = data['id']

    def deletePoll():
        requests.delete(API_URL + '/admin/polls/%d' % id, auth=basicAuth)

    request.addfinalizer(deletePoll)
    return id


class TestAdminQuestions:
    def test_add_question_to_nonexistent_poll(self):
        id = 12345
        question = {
            'type': 'TEXT',
            'text': 'Text question for open answer'
        }
        res = requests.post(API_URL + '/admin/polls/%d/questions' % id, auth=basicAuth, data=question)
        assert res.status_code == 404

    def test_add_question_with_invalid_type(self, poll_id):
        question = {
            'type': 'INVALID',
            'text': 'Invalid question'
        }
        res = requests.post(API_URL + '/admin/polls/%d/questions' % poll_id, auth=basicAuth, data=question)
        assert res.status_code == 400

    def test_add_text_question(self, poll_id):
        question = {
            'type': 'TEXT',
            'text': 'Text question for open answer'
        }
        res = requests.post(API_URL + '/admin/polls/%d/questions' % poll_id, auth=basicAuth, data=question)
        assert res.status_code == 200
        data = res.json()
        assert data['type'] == 'TEXT'

    def test_add_choice_question(self, poll_id):
        question = {
            'type': 'CHOICE',
            'text': 'Choose one option',
            'options': ['Linus Torwald', 'Albert Einstein', 'Sigmund Freud']
        }
        res = requests.post(API_URL + '/admin/polls/%d/questions' % poll_id, auth=basicAuth, json=question)
        assert res.status_code == 200
        data = res.json()
        assert data['type'] == 'CHOICE'
        assert len(data['options']) == 3

    def test_add_choice_question_without_options(self, poll_id):
        question = {
            'type': 'CHOICE',
            'text': 'Choose one option',
        }
        res = requests.post(API_URL + '/admin/polls/%d/questions' % poll_id, auth=basicAuth, data=question)
        assert res.status_code == 400

    def test_add_choice_question_with_only_option(self, poll_id):
        question = {
            'type': 'CHOICE',
            'text': 'Choose one option',
            'options': ['Only']
        }
        res = requests.post(API_URL + '/admin/polls/%d/questions' % poll_id, auth=basicAuth, data=question)
        assert res.status_code == 400

    def test_add_multiple_choice_question(self, poll_id):
        question = {
            'type': 'MULTIPLE_CHOICE',
            'text': 'Choose as many options as you like!',
            'options': ['Linus Torwald', 'Albert Einstein', 'Sigmund Freud']
        }
        res = requests.post(API_URL + '/admin/polls/%d/questions' % poll_id, auth=basicAuth, json=question)
        assert res.status_code == 200
        data = res.json()
        assert data['type'] == 'MULTIPLE_CHOICE'
        assert len(data['options']) == 3

    def test_delete_question(self, poll_id):
        question = {
            'type': 'TEXT',
            'text': 'Question to be deleted'
        }
        res = requests.post(API_URL + '/admin/polls/%d/questions' % poll_id, auth=basicAuth, data=question)
        assert res.status_code == 200
        data = res.json()
        res = requests.delete(API_URL + '/admin/polls/%d/questions/%d' % (poll_id, data['id']), auth=basicAuth)
        assert res.status_code == 200

    def test_delete_nonexistent_question(self, poll_id):
        id = 12345
        res = requests.delete(API_URL + '/admin/polls/%d/questions/%d' % (poll_id, id), auth=basicAuth)
        assert res.status_code == 404

    def test_edit_question(self, poll_id):
        question = {
            'type': 'CHOICE',
            'text': 'Question to edit',
            'options': ['Linus Torwald', 'Albert Einstein', 'Sigmund Freud']
        }
        res = requests.post(API_URL + '/admin/polls/%d/questions' % poll_id, auth=basicAuth, json=question)
        assert res.status_code == 200
        prevQuestion = res.json()

        edit = {
            'type': 'TEXT',
            'text': 'Updated question'
        }
        res = requests.patch(API_URL + '/admin/polls/%d/questions/%d' % (poll_id, prevQuestion['id']), auth=basicAuth,
                             data=edit)
        assert res.status_code == 200
        updatedQuestion = res.json()
        assert prevQuestion['id'] == updatedQuestion['id']
        assert prevQuestion['type'] != updatedQuestion['type']
        assert prevQuestion['text'] != updatedQuestion['text']
        assert 'options' not in updatedQuestion
