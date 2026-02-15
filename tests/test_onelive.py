import unittest

from onelive import Config, execute_source, parse_args


class OneLiveTests(unittest.TestCase):
    def test_execute_source_ok(self):
        rc = execute_source("x = 2 + 2", "<test>", Config(no_rickroll=True))
        self.assertEqual(rc, 0)

    def test_execute_source_syntax_error(self):
        rc = execute_source("if True print('x')", "<test>", Config(no_rickroll=True))
        self.assertEqual(rc, 1)

    def test_parse_args_command_mode(self):
        args = parse_args(["-c", "print('hi')", "--no-rickroll"])
        self.assertEqual(args.command, "print('hi')")
        self.assertTrue(args.no_rickroll)


if __name__ == "__main__":
    unittest.main()
