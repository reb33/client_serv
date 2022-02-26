import os
import sys
from unittest import TestCase

sys.path.append(os.path.abspath(os.path.join(__file__, '..', '..')))
from server import gen_response


class TestServer(TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_gen_response_contains_params(self):
        self.assertTrue(all(key in gen_response({'mess': 'mess'}) for key in ['response', 'alert']))

    def test_gen_response_contains_code_200(self):
        self.assertEqual(gen_response({'mess': 'mess'})['response'], 200)
