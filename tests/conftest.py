"""The pytest conftest.py file is used to setup the collection for testing."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import sys

import pytest
import yaml

try:
    from ansible.utils.collection_loader._collection_finder import (
        _get_collection_metadata,
    )

    HAS_GET_COLLECTION_METADATA = True
except ImportError:
    _get_collection_metadata = None
    HAS_GET_COLLECTION_METADATA = False


def get_collection_name():
    """Get the collection namespace and name from the galaxy.yml file."""
    info_file = "galaxy.yml"

    try:
        with open(info_file, "r", encoding="utf-8") as fh:
            galaxy_info = yaml.safe_load(fh)
    except FileNotFoundError:
        return None, None

    return galaxy_info["namespace"], galaxy_info["name"]


def pytest_sessionstart(session):
    """Patch the collection finder such that it does not raise a value error.

    This does not allow for loading of any collection metadata or redirects.
    Additionally links the collection to the collections directory.
    """
    # pylint: disable=unused-argument

    namespace, name = get_collection_name()
    if namespace is None or name is None:
        # Tests may not being run from the root of the repo.
        return

    monkeypatch = pytest.MonkeyPatch()

    original = _get_collection_metadata

    def get_collection_metadata(*args, **kwargs):
        try:
            return original(*args, **kwargs)

        except ValueError:
            return {}

    if HAS_GET_COLLECTION_METADATA:
        monkeypatch.setattr(
            "ansible.utils.collection_loader."
            "_collection_finder._get_collection_metadata",
            get_collection_metadata,
        )

    parent_directory = os.path.dirname(os.path.dirname(__file__))
    collections_dir = os.path.join(parent_directory, "collections")

    name_dir = os.path.join(
        collections_dir, "ansible_collections", namespace, name
    )

    if collections_dir not in sys.path:
        monkeypatch.syspath_prepend(collections_dir)

    # If it's here, we will trust it was from this
    if os.path.isdir(name_dir):
        return

    os.makedirs(name_dir, exist_ok=True)

    for entry in os.listdir(parent_directory):
        if entry == "collections":
            continue
        os.symlink(os.path.abspath(entry), os.path.join(name_dir, entry))
