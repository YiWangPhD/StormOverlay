import io
from contextlib import redirect_stdout
from pathlib import Path
import unittest
from unittest.mock import patch

from stormoverlay.stormoverlay import main


class TestStormOverlayMain(unittest.TestCase):
    def test_main_with_dfs0_file(self):
        repo_root = Path(__file__).resolve().parents[2]
        dfs0_file = repo_root / "VSA_Rainfall_Data_PDT.dfs0"

        test_args = [
            "stormoverlay",
            "BU80",
            "2024-10-10",
            "2024-10-20",
            "--dfs0",
            str(dfs0_file),
        ]

        stdout = io.StringIO()
        with patch("sys.argv", test_args), redirect_stdout(stdout):
            main()

        output = stdout.getvalue()

        self.assertIn("Working on gauge BU80 from 2024-10-10 to 2024-10-20", output)
        self.assertIn("Gauge ID: BU80, from 2024-10-10 to 2024-10-20", output)
        self.assertIn("Existing Climate", output)
