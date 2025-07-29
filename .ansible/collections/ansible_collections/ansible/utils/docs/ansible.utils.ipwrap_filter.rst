.. _ansible.utils.ipwrap_filter:


********************
ansible.utils.ipwrap
********************

**This filter is designed to Wrap IPv6 addresses in [ ] brackets.**


Version added: 2.5.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Some configuration files require IPv6 addresses to be "wrapped" in square brackets ([ ]).To accomplish that,
- you can use the ipwrap() filter.It will wrap all IPv6 addresses and leave any other strings intact.




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
                        <div>You can provide a single argument to each ipwrap() filter.</div>
                        <div>The filter will then treat it as a query and return values modified by that query.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>value</b>
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
                        <div>list of subnets or individual address or any other values input. Example. [&#x27;192.24.2.1&#x27;, &#x27;host.fqdn&#x27;, &#x27;::1&#x27;, &#x27;192.168.32.0/24&#x27;, &#x27;fe80::100/10&#x27;, True, &#x27;&#x27;, &#x27;42540766412265424405338506004571095040/64&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    #### examples
    # Ipwrap filter plugin o Wrap IPv6 addresses in [ ] brackets.
    - name: Set value as input list
      ansible.builtin.set_fact:
        value:
          - 192.24.2.1
          - host.fqdn
          - ::1
          - ''
          - 192.168.32.0/24
          - fe80::100/10
          - 42540766412265424405338506004571095040/64
          - true
    - debug:
        msg: "{{ value|ansible.utils.ipwrap }}"

    - name: |
            ipwrap() did not filter out non-IP address values, which is usually what you want when for example
            you are mixing IP addresses with hostnames. If you still want to filter out all non-IP address values,
            you can chain both filters together.
      debug:
        msg: "{{ value|ansible.utils.ipaddr|ansible.utils.ipwrap  }}"

    # PLAY [Ipwrap filter plugin o Wrap IPv6 addresses in [ ] brackets.] ***************************************************
    # TASK [Set value as input list] ***************************************************************************************
    # ok: [localhost] => {"ansible_facts": {"value": ["192.24.2.1", "host.fqdn", "::1", "", "192.168.32.0/24",
    # "fe80::100/10", "42540766412265424405338506004571095040/64", true]}, "changed": false}
    #
    # TASK [debug] ********************************************************************************************************
    # ok: [localhost] => {
    #     "msg": [
    #         "192.24.2.1",
    #         "::1",
    #         "192.168.32.0/24",
    #         "fe80::100/10",
    #         "2001:db8:32c:faad::/64"
    #     ]
    # }
    #
    # TASK [debug] ************************************************************************************************
    # ok: [localhost] => {
    #     "msg": [
    #         "192.24.2.1",
    #         "host.fqdn",
    #         "[::1]",
    #         "",
    #         "192.168.32.0/24",
    #         "[fe80::100]/10",
    #         "[2001:db8:32c:faad::]/64",
    #         "True"
    #     ]
    # }
    #
    # TASK [ipwrap() did not filter out non-IP address values, which is usually what you want when for example
    # you are mixing IP addresses with hostnames. If you still want to filter out all non-IP address values,
    # you can chain both filters together.] ***
    # ok: [localhost] => {
    #     "msg": [
    #         "192.24.2.1",
    #         "[::1]",
    #         "192.168.32.0/24",
    #         "[fe80::100]/10",
    #         "[2001:db8:32c:faad::]/64"
    #     ]
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
                            <div>Returns values valid for a particular query.</div>
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
