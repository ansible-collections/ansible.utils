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
short_description: Validate data with provided schema validation 
description:
- Validate data with provided schema validation
version_added: 0.0.1
options:
    data:
        type: raw
        description:
        - A list or dict of data
        required: True
    engine:
        type: str
        description:
        - The name of the validator to use
        default: ansible.utils.jsonschema
    criteria:
        type: raw
        description:
        - The schema used for validation of data. For the type of data refer
          documentation of individual validator plugins.
        required: True
Notes:
- 
"""


EXAMPLES = r"""
"""

RETURN = r"""

"""