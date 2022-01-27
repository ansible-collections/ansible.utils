.. _ansible.utils.keep_keys_filter:


***********************
ansible.utils.keep_keys
***********************

**Keep specific keys from a data recursively.**


Version added: 2.5.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This plugin keep only specified keys from a provided data recursively.
- Matching parameter defaults to equals unless ``matching_parameter`` is explicitly mentioned.
- Using the parameters below- ``data|ansible.utils.keep_keys(target([....]``))




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                <th>Configuration</th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>data</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">raw</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>This option represents a list of dictionaries or a dictionary with any level of nesting data.</div>
                        <div>For example <code>config_data|ansible.utils.keep_keys(target([....]</code>)), in this case <code>config_data</code> represents this option.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>matching_parameter</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>starts_with</li>
                                    <li>ends_with</li>
                                    <li>regex</li>
                        </ul>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Specify the matching configuration of target keys and data attributes.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>target</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Specify the target keys to keep in list format.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    ##example.yaml
    interfaces:
      - name: eth0
        enabled: true
        duplex: auto
        speed: auto
        note:
          - Connected green wire
      - name: eth1
        description: Configured by Ansible - Interface 1
        mtu: 1500
        speed: auto
        duplex: auto
        enabled: true
        note:
          - Connected blue wire
          - Configured by Paul
        vifs:
        - vlan_id: 100
          description: Eth1 - VIF 100
          mtu: 400
          enabled: true
          comment: Needs reconfiguration
        - vlan_id: 101
          description: Eth1 - VIF 101
          enabled: true
      - name: eth2
        description: Configured by Ansible - Interface 2 (ADMIN DOWN)
        mtu: 600
        enabled: false

    ##Playbook
    vars_files:
      - "example.yaml"
    tasks:
      - name: keep selective keys from dict/list of dict data
        ansible.builtin.set_fact:
          data: "{{ interfaces }}"

      - debug:
          msg:  "{{ data|ansible.utils.keep_keys(target=['description', 'name', 'mtu', 'duplex', 'enabled', 'vifs', 'vlan_id']) }}"

    ##Output
    # TASK [keep selective keys from python dict/list of dict] ****************************************************************************************
    # ok: [localhost] => {
    #     "ansible_facts": {
    #         "data": [
    #             {
    #                 "duplex": "auto",
    #                 "enabled": true,
    #                 "name": "eth0",
    #                 "note": [
    #                     "Connected green wire"
    #                 ],
    #                 "speed": "auto"
    #             },
    #             {
    #                 "description": "Configured by Ansible - Interface 1",
    #                 "duplex": "auto",
    #                 "enabled": true,
    #                 "mtu": 1500,
    #                 "name": "eth1",
    #                 "note": [
    #                     "Connected blue wire",
    #                     "Configured by Paul"
    #                 ],
    #                 "speed": "auto",
    #                 "vifs": [
    #                     {
    #                         "comment": "Needs reconfiguration",
    #                         "description": "Eth1 - VIF 100",
    #                         "enabled": true,
    #                         "mtu": 400,
    #                         "vlan_id": 100
    #                     },
    #                     {
    #                         "description": "Eth1 - VIF 101",
    #                         "enabled": true,
    #                         "vlan_id": 101
    #                     }
    #                 ]
    #             },
    #             {
    #                 "description": "Configured by Ansible - Interface 2 (ADMIN DOWN)",
    #                 "enabled": false,
    #                 "mtu": 600,
    #                 "name": "eth2"
    #             }
    #         ]
    #     },
    #     "changed": false
    # }
    # Read vars_file 'example.yaml'

    # TASK [debug] *************************************************************************************************************
    # ok: [localhost] => {
    #     "msg": [
    #         {
    #             "duplex": "auto",
    #             "enabled": true,
    #             "name": "eth0"
    #         },
    #         {
    #             "description": "Configured by Ansible - Interface 1",
    #             "duplex": "auto",
    #             "enabled": true,
    #             "mtu": 1500,
    #             "name": "eth1",
    #             "vifs": [
    #                 {
    #                     "description": "Eth1 - VIF 100",
    #                     "enabled": true,
    #                     "mtu": 400,
    #                     "vlan_id": 100
    #                 },
    #                 {
    #                     "description": "Eth1 - VIF 101",
    #                     "enabled": true,
    #                     "vlan_id": 101
    #                 }
    #             ]
    #         },
    #         {
    #             "description": "Configured by Ansible - Interface 2 (ADMIN DOWN)",
    #             "enabled": false,
    #             "mtu": 600,
    #             "name": "eth2"
    #         }
    #     ]
    # }

    ##example.yaml
    interfaces:
      - name: eth0
        enabled: true
        duplex: auto
        speed: auto
        note:
          - Connected green wire
      - name: eth1
        description: Configured by Ansible - Interface 1
        mtu: 1500
        speed: auto
        duplex: auto
        enabled: true
        note:
          - Connected blue wire
          - Configured by Paul
        vifs:
        - vlan_id: 100
          description: Eth1 - VIF 100
          mtu: 400
          enabled: true
          comment: Needs reconfiguration
        - vlan_id: 101
          description: Eth1 - VIF 101
          enabled: true
      - name: eth2
        description: Configured by Ansible - Interface 2 (ADMIN DOWN)
        mtu: 600
        enabled: false

    ##Playbook
    vars_files:
      - "example.yaml"
    tasks:
      - name: keep selective keys from dict/list of dict data
        ansible.builtin.set_fact:
          data: "{{ interfaces }}"

      - debug:
          msg:  "{{ data|ansible.utils.keep_keys(target=['desc', 'name'], matching_parameter= 'starts_with') }}"

    ##Output
    # TASK [keep selective keys from python dict/list of dict] **************************
    # ok: [localhost] => {
    #     "ansible_facts": {
    #         "data": [
    #             {
    #                 "duplex": "auto",
    #                 "enabled": true,
    #                 "name": "eth0",
    #                 "note": [
    #                     "Connected green wire"
    #                 ],
    #                 "speed": "auto"
    #             },
    #             {
    #                 "description": "Configured by Ansible - Interface 1",
    #                 "duplex": "auto",
    #                 "enabled": true,
    #                 "mtu": 1500,
    #                 "name": "eth1",
    #                 "note": [
    #                     "Connected blue wire",
    #                     "Configured by Paul"
    #                 ],
    #                 "speed": "auto",
    #                 "vifs": [
    #                     {
    #                         "comment": "Needs reconfiguration",
    #                         "description": "Eth1 - VIF 100",
    #                         "enabled": true,
    #                         "mtu": 400,
    #                         "vlan_id": 100
    #                     },
    #                     {
    #                         "description": "Eth1 - VIF 101",
    #                         "enabled": true,
    #                         "vlan_id": 101
    #                     }
    #                 ]
    #             },
    #             {
    #                 "description": "Configured by Ansible - Interface 2 (ADMIN DOWN)",
    #                 "enabled": false,
    #                 "mtu": 600,
    #                 "name": "eth2"
    #             }
    #         ]
    #     },
    #     "changed": false
    # }
    # Read vars_file 'example.yaml'

    # TASK [debug] **********************************************************************************
    # ok: [localhost] => {
    #     "msg": [
    #         {
    #             "name": "eth0"
    #         },
    #         {
    #             "description": "Configured by Ansible - Interface 1",
    #             "name": "eth1",
    #             "vifs": [
    #                 {
    #                     "description": "Eth1 - VIF 100"
    #                 },
    #                 {
    #                     "description": "Eth1 - VIF 101"
    #                 }
    #             ]
    #         },
    #         {
    #             "description": "Configured by Ansible - Interface 2 (ADMIN DOWN)",
    #             "name": "eth2"
    #         }
    #     ]
    # }




Status
------


Authors
~~~~~~~

- Sagar Paul (@KB-perByte)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
