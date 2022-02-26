import os
import sys
from unittest import TestCase

sys.path.append(os.path.abspath(os.path.join(__file__, '..', '..')))
from client import gen_presence_message,check_response


class TestClient(TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_gen_presence_message_root_params(self):
        self.assertTrue(all(key in gen_presence_message('Name') for key in ['action', 'time', 'user']))

    def test_gen_presence_message_user_params(self):
        self.assertTrue(all(key in gen_presence_message('Name')['user'] for key in ['account_name', 'password']))

    def test_gen_presence_message_check_account_name(self):
        name = 'Vasya'
        self.assertEqual(gen_presence_message(name)['user']['account_name'], name)

    def test_check_response_200(self):
        message = {
            "response": 200,
            "alert": ""
        }
        self.assertEqual(check_response(message, 200), message)

    def test_check_response_400(self):
        message = {
            "response": 400,
            "alert": ""
        }
        self.assertEqual(check_response(message, 400), message)

    def test_check_response_raise_exception(self):
        message = {
            "response": 400,
            "alert": ""
        }
        self.assertRaises(Exception, check_response, message, 200)

    def test_check_response_raise_exception_contain_message(self):
        message = {
            "response": 400,
            "alert": ""
        }
        try:
            check_response(message, 200)
        except Exception as e:
            self.assertIn(str(message), str(e))
