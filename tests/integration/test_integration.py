from __future__ import absolute_import, division, print_function


__metaclass__ = type

import subprocess
from pathlib import Path

import pytest


TARGETS_DIR = Path(__file__).parent / "targets"
COLLECTION_ROOT = Path(__file__).parent.parent.parent


def get_targets():
    return sorted(
        d.name for d in TARGETS_DIR.iterdir() if d.is_dir() and (d / "tasks").exists()
    )


@pytest.mark.parametrize("target", get_targets())
def test_integration(target):
    result = subprocess.run(
        ["ansible-test", "integration", target, "--local", "-vvvv"],
        capture_output=True,
        text=True,
        check=False,
        cwd=str(COLLECTION_ROOT),
    )
    if result.returncode:
        print(result.stdout)
        print(result.stderr)
        pytest.fail(f"Integration test failed for target: {target}")
