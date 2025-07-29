from __future__ import absolute_import, division, print_function


__metaclass__ = type

import subprocess

import pytest


def run(localhost_project, environment):
    __tracebackhide__ = True
    args = [
        "ansible-navigator",
        "run",
        str(localhost_project.playbook),
        "--ee",
        "false",
        "--mode",
        "stdout",
        "--pas",
        str(localhost_project.playbook_artifact),
        "--ll",
        "debug",
        "--lf",
        str(localhost_project.log_file),
        "--cdcp",
        str(localhost_project.collection_doc_cache),
        "-vvvv",
    ]
    process = subprocess.run(
        args=args,
        env=environment,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        check=False,
        shell=False,
    )
    if process.returncode:
        print(process.stdout.decode("utf-8"))
        print(process.stderr.decode("utf-8"))

        pytest.fail(reason=f"Integration test failed: {localhost_project.role}")


def test_integration(localhost_project, environment, monkeypatch):
    run(localhost_project, environment)
