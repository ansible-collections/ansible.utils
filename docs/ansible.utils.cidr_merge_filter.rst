.. _ansible.utils.cidr_merge_filter:


************************
ansible.utils.cidr_merge
************************

**This filter can be used to merge subnets or individual addresses.**


Version added: 2.5.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This filter can be used to merge subnets or individual addresses into their minimal representation, collapsing
- overlapping subnets and merging adjacent ones wherever possible.




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
                    <b>action</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"merge"</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Action to be performed.example merge,span</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>value</b>
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
                        <div>list of subnets or individual address to be merged</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    #### examples
    - name: cidr_merge with merge action
      ansible.builtin.set_fact:
        value:
          - 192.168.0.0/17
          - 192.168.128.0/17
          - 192.168.128.1
    - debug:
        msg: '{{ value|ansible.utils.cidr_merge }}'

    # TASK [cidr_merge with merge action] **********************************************************************************
    # ok: [localhost] => {
    #     "ansible_facts": {
    #         "value": [
    #             "192.168.0.0/17",
    #             "192.168.128.0/17",
    #             "192.168.128.1"
    #         ]
    #     },
    #     "changed": false
    # }
    # TASK [debug] *********************************************************************************************************
    # ok: [loalhost] => {
    #     "msg": [
    #         "192.168.0.0/16"
    #     ]
    # }

    - name: Cidr_merge with span.
      ansible.builtin.set_fact:
        value:
          - 192.168.1.1
          - 192.168.1.2
          - 192.168.1.3
          - 192.168.1.4
    - debug:
        msg: '{{ value|ansible.utils.cidr_merge(''span'') }}'

    # TASK [Cidr_merge with span.] ********************************************************************
    # ok: [localhost] => {
    #     "ansible_facts": {
    #         "value": [
    #             "192.168.1.1",
    #             "192.168.1.2",
    #             "192.168.1.3",
    #             "192.168.1.4"
    #         ]
    #     },
    #     "changed": false
    # }
    #
    # TASK [debug] ************************************************************************************
    # ok: [localhost] => {
    #     "msg": "192.168.1.0/29"
    # }



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this filter:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>data</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">raw</span>
                    </div>
                </td>
                <td></td>
                <td>
                            <div>Returns a minified list of subnets or a single subnet that spans all of the inputs.</div>
                    <br/>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Ashwini Mhatre (@amhatre)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
