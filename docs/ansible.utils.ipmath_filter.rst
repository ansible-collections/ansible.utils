.. _ansible.utils.ipmath_filter:


********************
ansible.utils.ipmath
********************

**This filter is designed to do simple IP math/arithmetic.**


Version added: 2.5.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This filter is designed to do simple IP math/arithmetic.




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
                    <b>amount</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>integer for arithmetic. Example -1,2,3</div>
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
                        <div>list of subnets or individual address or any other values input for ipaddr plugin</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    #### examples
    # Ipmath filter plugin with different arthmetic.
    # Get the next fifth address based on an IP address
    - debug:
        msg: "{{ '192.168.1.5' | ansible.netcommon.ipmath(5) }}"

    # Get the tenth previous address based on an IP address
    - debug:
        msg: "{{ '192.168.1.5' | ansible.netcommon.ipmath(-10) }}"

    # Get the next fifth address using CIDR notation
    - debug:
        msg: "{{ '192.168.1.1/24' | ansible.netcommon.ipmath(5) }}"

    # Get the previous fifth address using CIDR notation
    - debug:
        msg: "{{ '192.168.1.6/24' | ansible.netcommon.ipmath(-5) }}"

    # Get the previous tenth address using cidr notation
    # It returns a address of the previous network range
    - debug:
        msg: "{{ '192.168.2.6/24' | ansible.netcommon.ipmath(-10) }}"

    # Get the next tenth address in IPv6
    - debug:
        msg: "{{ '2001::1' | ansible.netcommon.ipmath(10) }}"

    # Get the previous tenth address in IPv6
    - debug:
        msg: "{{ '2001::5' | ansible.netcommon.ipmath(-10) }}"

    # TASK [debug] **********************************************************************************************************
    # ok: [localhost] => {
    #     "msg": "192.168.1.10"
    # }
    #
    # TASK [debug] **********************************************************************************************************
    # ok: [localhost] => {
    #     "msg": "192.168.0.251"
    # }
    #
    # TASK [debug] **********************************************************************************************************
    # ok: [localhost] => {
    #     "msg": "192.168.1.6"
    # }
    #
    # TASK [debug] **********************************************************************************************************
    # ok: [localhost] => {
    #     "msg": "192.168.1.1"
    # }
    #
    # TASK [debug] **********************************************************************************************************
    # ok: [localhost] => {
    #     "msg": "192.168.1.252"
    # }
    #
    # TASK [debug] **********************************************************************************************************
    # ok: [localhost] => {
    #     "msg": "2001::b"
    # }
    #
    # TASK [debug] **********************************************************************************************************
    # ok: [localhost] => {
    #     "msg": "2000:ffff:ffff:ffff:ffff:ffff:ffff:fffb"
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
                            <div>Returns result of IP math/arithmetic.</div>
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
