# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


"""
The index_of filter plugin
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: xml_to_json
    author: Ashwini Mhatre (@amhatre)
    version_added: "1.0.0"
    short_description: convert given xml string to json
    description:
        - This plugin converts the xml string to json.
        - Using the parameters below- C(data|ansible.utils.xml_to_json)
    options:
      data:
        description:
        - The input xml string .
        - This option represents the xml value that is passed to the filter plugin in pipe format.
        - For example C(config_data|ansible.utils.xml_to_json), in this case C(config_data) represents this option.
        type: str
        required: True
"""

EXAMPLES = r"""

#### Simple examples

tasks:
  - name: convert given xml to json
    ansible.builtin.set_fact:
      data: "
        <netconf-state xmlns=\"urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring\"><schemas><schema/></schemas></netconf-state>
            "

  - debug:
      msg:  "{{ data|ansible.utils.xml_to_json }}"

##TASK######
TASK [convert given xml to json] *****************************************************************************************************
task path: /Users/amhatre/ansible-collections/playbooks/test_utils.yaml:5
ok: [localhost] => {
    "ansible_facts": {
        "data": " <netconf-state xmlns=\"urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring\"><schemas><schema/></schemas></netconf-state> "
    },
    "changed": false
}

TASK [debug] *************************************************************************************************************************
task path: /Users/amhatre/ansible-collections/playbooks/test_utils.yaml:13
Loading collection ansible.utils from /Users/amhatre/ansible-collections/collections/ansible_collections/ansible/utils
ok: [localhost] => {
    "msg": {
        "netconf-state": {
            "@xmlns": "urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring",
            "schemas": {
                "schema": null
            }
        }
    }
}
"""

from ansible.errors import AnsibleFilterError
from jinja2.filters import environmentfilter
from ansible_collections.ansible.utils.plugins.module_utils.common.xml_to_json import (
    xml_to_json,
)
from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)


@environmentfilter
def _xml_to_json(*args, **kwargs):
    """Convert the given data from xml to json."""

    keys = [
        "environment",
        "data",
    ]
    data = dict(zip(keys, args))
    data.update(kwargs)
    environment = data.pop("environment")
    aav = AnsibleArgSpecValidator(
        data=data, schema=DOCUMENTATION, name="xml_to_json"
    )
    valid, errors, updated_data = aav.validate()
    if not valid:
        raise AnsibleFilterError(errors)
    return xml_to_json(**updated_data)


class FilterModule(object):
    """ xml_to_json  """

    def filters(self):

        """a mapping of filter names to functions"""
        return {"xml_to_json": _xml_to_json}