.. _ansible.utils.ipv6form_filter:


**********************
ansible.utils.ipv6form
**********************

**This filter is designed to convert ipv6 address in different formats. For example expand, compressetc.**


Version added: 2.11.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This filter is designed to convert ipv6 addresses in different formats.




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
                    <b>format</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Different formats example. compress, expand, x509</div>
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
                        <div>individual ipv6 address input for ipv6_format plugin.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    #### examples
    # Ipv6form filter plugin with different format.
    - name: Expand given Ipv6 address
      debug:
          msg: "{{ '1234:4321:abcd:dcba::17' | ansible.utils.ipv6form('expand') }}"

    - name: Compress  given Ipv6 address
      debug:
          msg: "{{ '1234:4321:abcd:dcba:0000:0000:0000:0017' | ansible.utils.ipv6form('compress') }}"

    - name: Covert given Ipv6 address in x509
      debug:
          msg: "{{ '1234:4321:abcd:dcba::17' | ansible.utils.ipv6form('x509') }}"

    # TASK [Expand given Ipv6 address] ************************************************************************************
    # task path: /home/amhatre/dev/playbook/test_ipform.yaml:7
    # Loading collection ansible.utils from /home/amhatre/dev/collections/ansible_collections/ansible/utils
    # ok: [localhost] => {
    #     "msg": "1234:4321:abcd:dcba:0000:0000:0000:0017"
    # }

    # TASK [Compress  given Ipv6 address] *********************************************************************************
    # task path: /home/amhatre/dev/playbook/test_ipform.yaml:11
    # Loading collection ansible.utils from /home/amhatre/dev/collections/ansible_collections/ansible/utils
    # ok: [localhost] => {
    #     "msg": "1234:4321:abcd:dcba::17"
    # }

    # TASK [Covert given Ipv6 address in x509] ****************************************************************************
    # task path: /home/amhatre/dev/playbook/test_ipform.yaml:15
    # Loading collection ansible.utils from /home/amhatre/dev/collections/ansible_collections/ansible/utils
    # ok: [localhost] => {
    #     "msg": "1234:4321:abcd:dcba:0:0:0:17"
    # }

    # PLAY RECAP **********************************************************************************************************
    # localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0



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
                            <div>Returns result ipv6 address in expected format.</div>
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
