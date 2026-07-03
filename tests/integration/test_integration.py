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
        },
    ]


def run(target, target_dir):
    __tracebackhide__ = True
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        playbook_path = tmp / "playbook.yaml"
        artifact_path = tmp / "artifact.json"
        log_path = tmp / "ansible-navigator.log"
        cache_path = tmp / "collection-doc-cache.db"

        playbook_path.write_text(yaml.dump(build_playbook(target_dir), default_flow_style=False))

        result = subprocess.run(
            [
                "ansible-navigator",
                "run",
                str(playbook_path),
                "--ee",
                "false",
                "--mode",
                "stdout",
                "--pas",
                str(artifact_path),
                "--ll",
                "debug",
                "--lf",
                str(log_path),
                "--cdcp",
                str(cache_path),
                "-vvvv",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode:
            pytest.fail(reason=f"Integration test failed: {target}")


@pytest.mark.parametrize("target", get_targets())
def test_integration(target):
    run(target, (TARGETS_DIR / target).resolve())
