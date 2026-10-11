"""The version number is written in three places, and they must agree.

SignPath checks the signed file's version against signpath/artifact-configuration.xml,
the exe's Properties come from uniqr.__version__, and pip reads pyproject.toml.
A release that bumps one and forgets another builds fine and fails at signing.
"""

import re
import tomllib
from pathlib import Path

from uniqr import __version__

ROOT = Path(__file__).resolve().parent.parent


def test_pyproject_matches_the_package():
    declared = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]
    assert declared == __version__


def test_signpath_expects_the_version_the_exe_is_built_with():
    xml = (ROOT / "signpath" / "artifact-configuration.xml").read_text(encoding="utf-8")
    expected = re.search(r'product-version="([^"]+)"', xml).group(1)
    assert expected == __version__
