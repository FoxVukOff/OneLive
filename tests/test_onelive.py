import tempfile
import unittest
from pathlib import Path

from onelive import Config, RICKROLL_URL, execute_source, parse_args, run_file


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

    def test_rickroll_url_is_original(self):
        self.assertEqual(RICKROLL_URL, "ASCII.live/can-you-hear-me")

    def test_run_file_passes_script_args(self):
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "echoargs.py"
            out = Path(tmp) / "args.txt"
            script.write_text(
                "import sys\nfrom pathlib import Path\nPath('args.txt').write_text('|'.join(sys.argv))\n",
                encoding="utf-8",
            )
            rc = run_file(script, Config(no_rickroll=True, cwd=tmp), script_argv=["a", "b"])
            self.assertEqual(rc, 0)
            self.assertIn("echoargs.py|a|b", out.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
