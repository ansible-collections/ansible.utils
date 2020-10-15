# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The action plugin file for cli_parse
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.utils.plugins.module_utils.common.utils import (
    dict_merge,
)

try:
    import yaml

    try:
        # use C version if possible for speedup
        from yaml import CSafeLoader as SafeLoader
    except ImportError:
        from yaml import SafeLoader
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

OPTION_METADATA = (
    "type",
    "choices",
    "default",
    "required",
    "aliases",
    "elements",
    "fallback",
    "no_log",
    "apply_defaults",
    "deprecated_aliases",
    "removed_in_version",
)
OPTION_CONDITIONALS = (
    "mutually_exclusive",
    "required_one_of",
    "required_together",
    "required_by",
    "required_if",
)

VALID_ANSIBLEMODULE_ARGS = (
    "bypass_checks",
    "no_log",
    "add_file_common_args",
    "supports_check_mode",
) + OPTION_CONDITIONALS


def extract_argspec(doc_obj, argpsec):
    options_obj = doc_obj.get("options")
    for okey, ovalue in iteritems(options_obj):
        argpsec[okey] = {}
        for metakey in list(ovalue):
            if metakey == "suboptions":
                argpsec[okey].update({"options": {}})
                suboptions_obj = {"options": ovalue["suboptions"]}
                extract_argspec(suboptions_obj, argpsec[okey]["options"])
            elif metakey in OPTION_METADATA + OPTION_CONDITIONALS:
                argpsec[okey].update({metakey: ovalue[metakey]})


# TODO: Support extends_documentation_fragment
def convert_doc_to_ansible_module_kwargs(doc):
    doc_obj = yaml.load(doc, SafeLoader)
    argspec = {}
    spec = {}
    extract_argspec(doc_obj, argspec)
    spec.update({"argument_spec": argspec})
    for item in doc_obj:
        if item in VALID_ANSIBLEMODULE_ARGS:
            spec.update({item: doc_obj[item]})
    return spec


def generate_argspec(doc, conditionals={}):
    """ Generate an argspec
    """
    argspec = convert_doc_to_ansible_module_kwargs(doc)
    if conditionals:
        argspec = dict_merge(argspec, conditionals)
    return argspec
