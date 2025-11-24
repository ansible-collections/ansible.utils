.. _ansible.utils.network_in_network_filter:


********************************
ansible.utils.network_in_network
********************************

**This filter returns whether an address or a network passed as argument is in a network.**


Version added: 2.5.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This filter returns whether an address or a network passed as argument is in a network.




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
                    <b>test</b>
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
                        <div>The address or network to validate if it is within the range of &#x27;value&#x27;.</div>
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
                        <div>The network address or range to test against.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    #### examples
    - name: Check ip address 1 is part of another network
      debug:
        msg: "{{ '192.168.0.0/24' | ansible.utils.network_in_network( '192.168.0.1' ) }}"

    - name: Check ip address 2 is part of another network
      debug:
        msg: "{{ '192.168.0.0/24' | ansible.utils.network_in_network( '10.0.0.1' ) }}"

    - name: Check in a network is part of another network.
      debug:
        msg: "{{ '192.168.0.0/16' | ansible.utils.network_in_network( '192.168.0.0/24' ) }}"

    # TASK [Check ip address 1 is part of another network] ********************************************************
    # task path: /Users/amhatre/ansible-collections/playbooks/test_network_in_network.yaml:7
    # Loading collection ansible.utils from /Users/amhatre/ansible-collections/collections/ansible_collections/ansible/utils
    # ok: [localhost] => {
    #     "msg": true
    # }
    #
    # TASK [Check ip address 2 is part of another network] ********************************************************
    # task path: /Users/amhatre/ansible-collections/playbooks/test_network_in_network.yaml:11
    # Loading collection ansible.utils from /Users/amhatre/ansible-collections/collections/ansible_collections/ansible/utils
    # ok: [localhost] => {
    #     "msg": false
    # }
    #
    # TASK [Check in a network is part of another network.] *******************************************************
    # task path: /Users/amhatre/ansible-collections/playbooks/test_network_in_network.yaml:15
    # Loading collection ansible.utils from /Users/amhatre/ansible-collections/collections/ansible_collections/ansible/utils
    # ok: [localhost] => {
    #     "msg": true
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
                      <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td></td>
                <td>
                            <div>Returns whether an address or a network passed as argument is in a network.</div>
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
