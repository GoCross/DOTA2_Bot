from unittest import TestCase
import message_sender


class TestMessage(TestCase):
    def test_message(self):
        message_sender.message('test')
        self.fail()
