import unittest
import requests
import json

from constants import *
from dbmanager import create_new_accounts, delete_accounts, get_accounts_by_uuid_list


class TestCreditservice(unittest.TestCase):

    def setUp(self):
        self.accounts_uuid_list = [
            '26c940a1-7228-4ea2-a3bc-e6460b172040',
            '5597cc3d-c948-48a0-b711-393edf20d9c0',
            '7badc8f8-65bc-449a-8cde-855234ac63e1',
            '867f0924-a917-4711-939b-90b179a96392'
        ]
        self.account_list = [
            {'uuid': self.accounts_uuid_list[0], 'full_name': 'Петров Иван Сергеевич',
             'balance': 1700, 'holds': 300, 'is_opened': True},
            {'uuid': self.accounts_uuid_list[1], 'full_name': 'Пархоменко Антон Александрович',
             'balance': 10, 'holds': 300, 'is_opened': True},
            {'uuid': self.accounts_uuid_list[2], 'full_name': 'Kazitsky Jason',
             'balance': 200, 'holds': 200, 'is_opened': True},
            {'uuid': self.accounts_uuid_list[3], 'full_name': 'Петечкин Петр Измаилович',
             'balance': 1000000, 'holds': 1, 'is_opened': False}
        ]

        create_new_accounts(self.account_list)

    def tearDown(self):
        delete_accounts(self.accounts_uuid_list)

    # tests for GET methods
    # positive cases
    def test_get_ping_method_200(self):
        res = requests.get('http://localhost/api/ping')
        res_json = json.loads(res.content)

        self.assertEqual(res.ok, True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_json['status'], 200)
        self.assertEqual(res_json['success'], True)
        self.assertEqual(res_json['description']['server_status'], SERVER_STATUS_STR)
        self.assertEqual(res_json['description']['port'], PORT_OUTER)
        self.assertEqual(res_json['description']['host'], HOST)
        self.assertEqual(len(res_json['description']['ping']), 4)

    def test_get_status_method_200(self):
        res = requests.get('http://localhost/api/status?uuid=867f0924-a917-4711-939b-90b179a96392')
        res_json = json.loads(res.content)

        expected_body_response_addition = {
            'uuid': '867f0924-a917-4711-939b-90b179a96392',
            'full_name': 'Петечкин Петр Измаилович',
            'balance': 1000000,
            'holds': 1,
            'is_opened': False
        }

        self.assertEqual(res.ok, True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_json['status'], 200)
        self.assertEqual(res_json['success'], True)
        self.assertEqual(res_json['addition'], expected_body_response_addition)

    # tests for GET methods
    # negative cases
    def test_get_status_method_invalid_uuid_404(self):
        res = requests.get('http://localhost/api/status?uuid=bad')
        res_json = json.loads(res.content)

        self.assertEqual(res.ok, False)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_json['status'], 404)
        self.assertEqual(res_json['success'], False)
        self.assertEqual(res_json['description'], {'error_message': VALID_UUID_MSG})

    def test_get_status_method_account_not_found_404(self):
        res = requests.get('http://localhost/api/status?uuid=99999999-a917-4711-939b-90b179a96392')
        res_json = json.loads(res.content)

        self.assertEqual(res.ok, False)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_json['status'], 404)
        self.assertEqual(res_json['success'], False)
        self.assertEqual(res_json['description'], {'error_message': DOES_NOT_EXIST_MSG})

    def test_get_method_error_404(self):
        res = requests.get('http://localhost/api/foo')
        res_json = json.loads(res.content)

        self.assertEqual(res.ok, False)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_json['status'], 404)
        self.assertEqual(res_json['success'], False)
        self.assertEqual(res_json['description'], {'error_message': PAGE_NOT_FOUND})

    # test for POST methods
    # positive cases
    def test_post_method_add_200(self):
        data = json.dumps({"addition": {"uuid": "7badc8f8-65bc-449a-8cde-855234ac63e1", "sum": 1000}})
        res = requests.post('http://localhost/api/add', data=data, headers={'content-type': 'application/json'})
        res_json = json.loads(res.content)

        expected_body_response_addition = {
            'uuid': '7badc8f8-65bc-449a-8cde-855234ac63e1',
            'full_name': 'Kazitsky Jason',
            'balance': 1200,
            'holds': 200,
            'is_opened': True
        }

        self.assertEqual(res.ok, True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_json['status'], 200)
        self.assertEqual(res_json['success'], True)
        self.assertEqual(res_json['description'], {'info_message': TOPPED_UP_BALANCE})
        self.assertEqual(res_json['addition'], expected_body_response_addition)

    def test_post_method_subtract_200(self):
        data = json.dumps({"addition": {"uuid": "26c940a1-7228-4ea2-a3bc-e6460b172040", "sum": 500}})
        res = requests.post('http://localhost/api/subtract', data=data, headers={'content-type': 'application/json'})
        res_json = json.loads(res.content)

        expected_body_response_addition = {
            'uuid': '26c940a1-7228-4ea2-a3bc-e6460b172040',
            'full_name': 'Петров Иван Сергеевич',
            'balance': 1700,
            'holds': 800,
            'is_opened': True
        }

        self.assertEqual(res.ok, True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_json['status'], 200)
        self.assertEqual(res_json['success'], True)
        self.assertEqual(res_json['description'], {'info_message': HOLDS_UPDATED})
        self.assertEqual(res_json['addition'], expected_body_response_addition)

    def test_post_method_update_all_holds_200(self):
        res = requests.post('http://localhost/api/update/holds')
        res_json = json.loads(res.content)

        expected_account_list = [
            {'uuid': self.accounts_uuid_list[0], 'full_name': 'Петров Иван Сергеевич',
             'balance': 1400, 'holds': 0, 'is_opened': True},
            {'uuid': self.accounts_uuid_list[1], 'full_name': 'Пархоменко Антон Александрович',
             'balance': 10, 'holds': 300, 'is_opened': True},
            {'uuid': self.accounts_uuid_list[2], 'full_name': 'Kazitsky Jason',
             'balance': 0,'holds': 0, 'is_opened': True},
            {'uuid': self.accounts_uuid_list[3], 'full_name': 'Петечкин Петр Измаилович',
             'balance': 1000000, 'holds': 1, 'is_opened': False}
        ]

        actual_account_list = [{
            'uuid': str(acc.uuid),
            'full_name': acc.full_name,
            'balance': acc.balance,
            'holds': acc.holds,
            'is_opened': acc.is_opened
        } for acc in get_accounts_by_uuid_list(self.accounts_uuid_list)]

        self.assertEqual(res.ok, True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_json['status'], 200)
        self.assertEqual(res_json['success'], True)
        self.assertEqual(res_json['description'], {'info_message': UPDATED_ALL_BALANCES_MSG})
        self.assertEqual(actual_account_list, expected_account_list)

    # test for POST methods
    # negative cases
    def test_post_method_add_negative_400(self):
        data = json.dumps({"addition": {"uuid": "26c940a1-7228-4ea2-a3bc-e6460b172040", "sum": -10}})
        res = requests.post('http://localhost/api/add', data=data, headers={'content-type': 'application/json'})
        res_json = json.loads(res.content)

        self.assertEqual(res.ok, False)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_json['status'], 400)
        self.assertEqual(res_json['success'], False)
        self.assertEqual(res_json['description'], {'error_message': NEGATIVE_SUM_MSG})

    def test_post_method_subtract_negative_400(self):
        data = json.dumps({"addition": {"uuid": "26c940a1-7228-4ea2-a3bc-e6460b172040", "sum": -10}})
        res = requests.post('http://localhost/api/add', data=data, headers={'content-type': 'application/json'})
        res_json = json.loads(res.content)

        self.assertEqual(res.ok, False)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_json['status'], 400)
        self.assertEqual(res_json['success'], False)
        self.assertEqual(res_json['description'], {'error_message': NEGATIVE_SUM_MSG})

    def test_post_method_subtract_over_400(self):
        data = json.dumps({"addition": {"uuid": "26c940a1-7228-4ea2-a3bc-e6460b172040", "sum": 10000}})
        res = requests.post('http://localhost/api/subtract', data=data, headers={'content-type': 'application/json'})
        res_json = json.loads(res.content)

        self.assertEqual(res.ok, False)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_json['status'], 400)
        self.assertEqual(res_json['success'], False)
        self.assertEqual(res_json['description'], {'error_message': INSUFFICIENT_FUNDS_MSG})

    def test_post_method_error_404(self):
        res = requests.post('http://localhost/api/foo')
        res_json = json.loads(res.content)

        self.assertEqual(res.ok, False)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_json['status'], 404)
        self.assertEqual(res_json['success'], False)
        self.assertEqual(res_json['description'], {'error_message': PAGE_NOT_FOUND})

    def test_post_method_invalid_content_type_400(self):
        data = json.dumps({"addition": {"uuid": 111, "sum": 100}})
        res = requests.post('http://localhost/api/add', data=data,
                            headers={'content-type': 'application/x-www-form-urlencoded'})
        res_json = json.loads(res.content)

        self.assertEqual(res.ok, False)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_json['status'], 400)
        self.assertEqual(res_json['success'], False)
        self.assertEqual(res_json['description'],
                         {'error_message': UNSUPPORTED_MT_MSG + 'application/x-www-form-urlencoded'})

    def test_post_method_invalid_json_400(self):
        data = json.dumps({"invalid_json": 111})
        res = requests.post('http://localhost/api/add', data=data, headers={'content-type': 'application/json'})
        res_json = json.loads(res.content)

        self.assertEqual(res.ok, False)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_json['status'], 400)
        self.assertEqual(res_json['success'], False)
        self.assertEqual(res_json['description'], {'error_message': INVALID_JSON_MSG})

    def test_post_method_invalid_json_param_400(self):
        data = json.dumps({"addition": {"uuid": "26c940a1-7228-4ea2-a3bc-e6460b172040", "bad_key": 500}})
        res = requests.post('http://localhost/api/add', data=data, headers={'content-type': 'application/json'})
        res_json = json.loads(res.content)

        self.assertEqual(res.ok, False)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_json['status'], 400)
        self.assertEqual(res_json['success'], False)
        self.assertEqual(res_json['description'], {'error_message': INVALID_JSON_MSG})

    def test_post_method_account_not_found_404(self):
        data = json.dumps({"addition": {"uuid": 111, "sum": 100}})
        res = requests.post('http://localhost/api/add', data=data, headers={'content-type': 'application/json'})
        res_json = json.loads(res.content)

        self.assertEqual(res.ok, False)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_json['status'], 404)
        self.assertEqual(res_json['success'], False)
        self.assertEqual(res_json['description'], {'error_message': DOES_NOT_EXIST_MSG})

    def test_post_method_balance_is_closed_400(self):
        data = json.dumps({"addition": {"uuid": "867f0924-a917-4711-939b-90b179a96392", "sum": 100}})
        res = requests.post('http://localhost/api/add', data=data, headers={'content-type': 'application/json'})
        res_json = json.loads(res.content)

        self.assertEqual(res.ok, False)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_json['status'], 400)
        self.assertEqual(res_json['success'], False)
        self.assertEqual(res_json['description'], {'error_message': BALANCE_IS_CLOSED_MSG})


class TestCreditserviceSpecial(unittest.TestCase):

    def setUp(self):
        self.accounts_uuid_list = [
            '26c940a1-7228-4ea2-a3bc-e6460b172040',
            '5597cc3d-c948-48a0-b711-393edf20d9c0',
            '7badc8f8-65bc-449a-8cde-855234ac63e1',
            '867f0924-a917-4711-939b-90b179a96392'
        ]
        self.account_list = [
            {'uuid': self.accounts_uuid_list[0], 'full_name': 'Петров Иван Сергеевич',
             'balance': 1700, 'holds': 0, 'is_opened': True},
            {'uuid': self.accounts_uuid_list[1], 'full_name': 'Пархоменко Антон Александрович',
             'balance': 10, 'holds': 300, 'is_opened': True},
            {'uuid': self.accounts_uuid_list[2], 'full_name': 'Kazitsky Jason',
             'balance': 0, 'holds': 0, 'is_opened': True},
            {'uuid': self.accounts_uuid_list[3], 'full_name': 'Петечкин Петр Измаилович',
             'balance': 1000000, 'holds': 1, 'is_opened': False}
        ]

        create_new_accounts(self.account_list)

    def tearDown(self):
        delete_accounts(self.accounts_uuid_list)

    # test update all holds post method, if all holds=0 or is_opened=False or balance < holds
    def test_post_method_update_all_holds_200(self):
        res = requests.post('http://localhost/api/update/holds')
        res_json = json.loads(res.content)

        expected_account_list = [
            {'uuid': self.accounts_uuid_list[0], 'full_name': 'Петров Иван Сергеевич',
             'balance': 1700, 'holds': 0, 'is_opened': True},
            {'uuid': self.accounts_uuid_list[1], 'full_name': 'Пархоменко Антон Александрович',
             'balance': 10, 'holds': 300, 'is_opened': True},
            {'uuid': self.accounts_uuid_list[2], 'full_name': 'Kazitsky Jason',
             'balance': 0, 'holds': 0, 'is_opened': True},
            {'uuid': self.accounts_uuid_list[3], 'full_name': 'Петечкин Петр Измаилович',
             'balance': 1000000, 'holds': 1, 'is_opened': False}
        ]

        actual_account_list = [{
            'uuid': str(acc.uuid),
            'full_name': acc.full_name,
            'balance': acc.balance,
            'holds': acc.holds,
            'is_opened': acc.is_opened
        } for acc in get_accounts_by_uuid_list(self.accounts_uuid_list)]

        self.assertEqual(res.ok, True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_json['status'], 200)
        self.assertEqual(res_json['success'], True)
        self.assertEqual(res_json['description'], {'info_message': EMPTY_HOLDS})
        self.assertEqual(actual_account_list, expected_account_list)
