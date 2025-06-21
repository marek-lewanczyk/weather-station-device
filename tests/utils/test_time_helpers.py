import unittest
import time


def get_unix_time():
    return 1718928000  # przykładowa wartość


def get_local_time(timezone):
    offset = timezone * 3600
    return time.localtime(get_unix_time() + offset)


def format_timestamp(ts=None):
    if ts is None:
        ts = get_local_time(2)
    return "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(*ts[:6])


class TestTimeHelpers(unittest.TestCase):
    def test_get_unix_time(self):
        self.assertIsInstance(get_unix_time(), int)

    def test_get_local_time_structure(self):
        lt = get_local_time(2)
        self.assertEqual(len(lt), 9)
        self.assertIn(lt.tm_isdst, (0, 1, -1))

    def test_format_timestamp(self):
        ts = (2025, 6, 21, 15, 30, 45, 0, 0, 0)
        result = format_timestamp(ts)
        self.assertEqual(result, "2025-06-21 15:30:45")

    def test_format_timestamp_default(self):
        result = format_timestamp()
        self.assertRegex(result, r"^20\d{2}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")


if __name__ == "__main__":
    unittest.main()