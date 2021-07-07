from my_logger import ProfilLogger, JsonHandler, LogEntry, log_entry
import unittest
import os
import json
import unittest.mock as mock
from datetime import datetime


CORRECT_JSON = """
[
    {
        "date": "2021-07-06T21:53:16.837733",
        "level": "INFO",
        "msg": "this is json test file number 1"
    },
    {
        "date": "2021-07-06T21:53:16.837885",
        "level": "WARNING",
        "msg": "this is json test file number 2"
    }
]
"""

JSON_FILENAME = "test.json"


class TestLJsonHandler(unittest.TestCase):
    def setUp(self) -> None:
        if os.path.exists(JSON_FILENAME):
            os.remove(JSON_FILENAME)
        return super().setUp()

    def tearDown(self) -> None:
        if os.path.exists(JSON_FILENAME):
            os.remove(JSON_FILENAME)
        return super().tearDown()

    def test_handler_basic_usage(self):
        plogger = ProfilLogger([JsonHandler(JSON_FILENAME)])

        plogger.info("this is json test file")
        plogger.warning("this is json test file")
        plogger.error("this is json test file")

    def test_logger_bad_file(self):
        with open(JSON_FILENAME, "w") as json_test:
            json_test.write("ndsjkandksa dksa djks ajkdjksandkwq dsanm d")

        plogger = ProfilLogger([JsonHandler(JSON_FILENAME)])

        self.assertRaises(
            json.decoder.JSONDecodeError, plogger.info, "lorem ipsum"
        )

    def test_append_to_existing_json(self):
        with open(JSON_FILENAME, "w") as json_file:
            json_file.write(CORRECT_JSON)

        ref_list = [
            LogEntry(
                date=datetime(2021, 7, 6, 21, 53, 16, 837733),
                level="INFO",
                msg="this is json test file number 1",
            ),
            LogEntry(
                date=datetime(2021, 7, 6, 21, 53, 16, 837885),
                level="WARNING",
                msg="this is json test file number 2",
            ),
        ]

        handler = JsonHandler(JSON_FILENAME)
        log_entry = LogEntry(
            datetime(2021, 1, 6, 22, 53, 16, 837885),
            "ERROR",
            "this is test error log",
        )
        ref_list.append(log_entry)
        handler.add_log(log_entry)

        base_form = handler.get_base_form()
        self.assertEqual(base_form, ref_list)

    def test_logger_read(self):
        m = mock.mock_open(read_data=CORRECT_JSON)

        ref_log_list = [
            LogEntry(
                date=datetime(2021, 7, 6, 21, 53, 16, 837733),
                level="INFO",
                msg="this is json test file number 1",
            ),
            LogEntry(
                date=datetime(2021, 7, 6, 21, 53, 16, 837885),
                level="WARNING",
                msg="this is json test file number 2",
            ),
        ]
        handler = JsonHandler(JSON_FILENAME)

        with mock.patch("builtins.open", m):
            base_form = handler.get_base_form()
            self.assertEqual(base_form, ref_log_list)
            m.assert_called_once_with(JSON_FILENAME, "r")
