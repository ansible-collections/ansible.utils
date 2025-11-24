.. _ansible.utils.hwaddr_filter:


********************
ansible.utils.hwaddr
********************

**HWaddr / MAC address filters**


Version added: 2.5.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This filter check if string is a HW/MAC address and filter it
- You can use the hwaddr() filter to check if a given string is a MAC address or convert it between various formats.




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
                    <b>alias</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"hwaddr"</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>alias</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>query</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">""</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>query string. Example. cisco,linux,unix etc</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>value</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>HW/MAC address.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    #### examples
    - name: Check if given string is a MAC address
      debug:
        msg: "{{ '1a:2b:3c:4d:5e:6f' | ansible.utils.hwaddr }}"

    - name: Convert HW address to Cisco format
      debug:
        msg: "{{ '1a:2b:3c:4d:5e:6f' | ansible.utils.hwaddr('cisco') }}"

    # TASK [Check if given string is a MAC address] ***************************************************************
    # ok: [localhost] => {
    #     "msg": "1a:2b:3c:4d:5e:6f"
    # }
    #
    # TASK [Convert HW address to Cisco format] ******************************************************************
    # ok: [localhost] => {
    #     "msg": "1a2b.3c4d.5e6f"
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
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td></td>
                <td>
                            <div>mac/Hw address</div>
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
