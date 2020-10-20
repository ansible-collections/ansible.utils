#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: validate
author: 
- Bradley Thornton (@cidrblock)
- Ganesh Nalawade (@ganeshrn)
short_description: Validate data with provided criteria 
description:
- Validate data with provided criteria based on the validation engine.
version_added: 1.0.0
options:
    data:
        type: raw
        description:
        - A data that will be validated against C(criteria). 
          For the type of data refer documentation of individual
          validator plugins
        required: True
    engine:
        type: str
        description:
        - The name of the validator to use. The engine value should  follow
          the fully qualified collection name foramt that is
          <org-name>.<collection-name>.<validator-plugin-name>.
        default: ansible.utils.jsonschema
    criteria:
        type: raw
        description:
        - The criteria used for validation of C(data). For the type of criteria refer
          documentation of individual validator plugins.
        required: True
Notes:
- 
"""


EXAMPLES = r"""
- name: set facts for data and criteria
  set_fact:
    data: "{{ lookup('file', './validate/data/show_interfaces_iosxr.json')}}"
    criteria: "{{ lookup('file', './validate/criteria/jsonschema/show_interfaces_iosxr.json')}}"

- name: validate data in using jsonschema engine with validate module
  ansible.utils.validate:
    data: "{{ data }}"
    criteria: "{{ criteria }}"
    engine: ansible.utils.jsonschema
  vars:
    ansible_jsonschema_draft: draft7
"""

RETURN = r"""
msg:
  description: 
  - The msg indicates if the C(data) is valid as per the C(criteria).
  - In case data is valid return success message I(all checks passed)
  - In case data is invalid return error message I(Validation errors were found)
    along with more information on error is available 
  returned: always
  type: str
errors:
  description: The list of errors in C(data) based on the C(criteria).
  returned: when C(data) value is invalid
  type: list
"""
