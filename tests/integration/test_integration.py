from __future__ import absolute_import, division, print_function


__metaclass__ = type

import subprocess
import tempfile

from pathlib import Path

import pytest
import yaml


TARGETS_DIR = Path(__file__).parent / "targets"


def get_targets():
    return sorted(d.name for d in TARGETS_DIR.iterdir() if d.is_dir() and (d / "tasks").exists())


def build_playbook(target_dir):
    return [
        {
            "hosts": "localhost",
            "gather_facts": True,
            "roles": [{"role": str(target_dir)}],
        }
    ]


def run(target, target_dir):
    __tracebackhide__ = True
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(build_playbook(target_dir), f, default_flow_style=False)
        playbook_path = Path(f.name)

    try:
        result = subprocess.run(
            ["ansible-playbook", str(playbook_path), "-vvvv"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode:
            print(result.stdout)
            print(result.stderr)
            pytest.fail(reason=f"Integration test failed: {target}")
    finally:
        playbook_path.unlink(missing_ok=True)


@pytest.mark.parametrize("target", get_targets())
def test_integration(target):
    run(target, (TARGETS_DIR / target).resolve())
