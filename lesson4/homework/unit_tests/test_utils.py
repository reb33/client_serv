import json
import os.path
import sys
from contextlib import redirect_stdout
from io import StringIO
from unittest import TestCase
from unittest.mock import Mock

sys.path.append(os.path.abspath(os.path.join(__file__, '..', '..')))
from common.utils import send_message, receive_message, check_port, print_message


class TestUtils(TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_send_message_call_socket_send(self):
        socket = Mock(spec=['send'])
        value_dict = {'mess': 'mess'}
        value_bytes = json.dumps(value_dict).encode('utf-8')
        send_message(socket, value_dict)
        socket.send.assert_called_with(value_bytes)

    def test_send_message_return_value_equal_socket_send_return(self):
        socket = Mock()
        return_value = 3
        socket.send = Mock(return_value=return_value)
        self.assertEqual(send_message(socket, {'mess': 'mess'}), return_value)

    def test_send_message_raise_exception_if_message_is_not_dict(self):
        socket = Mock(spec=['send'])
        self.assertRaises(ValueError, send_message, socket, 'value')

    def test_receive_message_call_socket_recv(self):
        socket = Mock()
        socket.recv = Mock(return_value=b'{"mess":"mess"}')
        receive_message(socket)
        socket.recv.assert_called()

    def test_receive_message_return_json_loaded_decoded_socket_recv_value(self):
        socket = Mock()
        socket_recv_return_value = b'{"mess":"mess"}'
        expected_value = {'mess': 'mess'}
        socket.recv = Mock(return_value=socket_recv_return_value)
        self.assertEqual(receive_message(socket), expected_value)

    def test_check_port_positive(self):
        self.assertEqual(check_port('8888'), 8888)

    def test_check_port_not_digit_string(self):
        self.assertRaises(ValueError, check_port, 'value')

    def test_check_port_less_1024(self):
        self.assertRaises(ValueError, check_port, '1023')

    def test_check_port_more_65535(self):
        self.assertRaises(ValueError, check_port, '65536')

    def test_print_message(self):
        stream = StringIO()
        with redirect_stdout(stream):
            print_message({'mess': 'mess'})
        self.assertIn('"mess": "mess"', stream.getvalue())
