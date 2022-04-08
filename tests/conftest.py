"""The pytest conftest.py file is used to setup the collection for testing."""

import os
import sys
import shutil

import pytest
import yaml
from ansible.utils.collection_loader._collection_finder import (
    _get_collection_metadata,
)


def get_collection_name():
    """Get the collection namespace and name from the galaxy.yml file."""
    info_file = "galaxy.yml"

    with open(info_file, "r") as fd:
        galaxy_info = yaml.safe_load(fd)

    return galaxy_info['namespace'] ,galaxy_info['name']

def pytest_sessionstart(session):
    """Patch the ansible collection finder such that it does not raise a value error.

    This does not allow for loading of any collection metadata or redirects.
    Additionally links the collection to the collections directory.
    """
    # pylint: disable=protected-access
    # pylint: disable=unused-argument
    monkeypatch = pytest.MonkeyPatch()
    original = _get_collection_metadata

    def get_collection_metadata(*args, **kwargs):
        try:
            return original(*args, **kwargs)
        except ValueError:
            return {}

    monkeypatch.setattr(
        "ansible.utils.collection_loader._collection_finder._get_collection_metadata",
        get_collection_metadata,
    )

    parent_directory = os.path.dirname(os.path.dirname(__file__))
    collections_dir = os.path.join(parent_directory, "collections")

    namespace, name = get_collection_name()
    name_dir = os.path.join(collections_dir, "ansible_collections", namespace, name)

    if collections_dir not in sys.path:
        monkeypatch.syspath_prepend(collections_dir)
    if os.path.isdir(name_dir):
        return
       
    os.makedirs(name_dir, exist_ok=True)

    for entry in os.listdir(parent_directory):
        if entry == "collections":
            continue
        os.symlink(os.path.abspath(entry), os.path.join(name_dir, entry))

def pytest_sessionfinish(session):
    """Remove the collections directory"""
    # pylint: disable=unused-argument

    parent_directory = os.path.dirname(os.path.dirname(__file__))
    collections_dir = os.path.join(parent_directory, "collections")
    shutil.rmtree(collections_dir)
