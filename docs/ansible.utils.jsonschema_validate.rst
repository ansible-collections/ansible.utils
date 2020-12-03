.. _ansible.utils.jsonschema_validate:


************************
ansible.utils.jsonschema
************************

**Define configurable options for jsonschema validate plugin**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This plugin documentation provides the configurable options that can be passed to the validate plugins when *ansible.utils.json* is used as a value for engine option.




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
                    <b>draft</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>draft3</li>
                                    <li>draft4</li>
                                    <li>draft6</li>
                                    <li><div style="color: blue"><b>draft7</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                    <td>
                                <div>env:ANSIBLE_VALIDATE_JSONSCHEMA_DRAFT</div>
                                <div>var: ansible_validate_jsonschema_draft</div>
                    </td>
                <td>
                        <div>This option provides the jsonschema specification that should be used for the validating the data. The <code>criteria</code> option in the <code>validate</code> plugin should follow the specifiaction as mentined by this option</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - The value of ``data`` option should be either of type *dict* or *strings* which should be a valid *dict* when read in python.
   - The value of ``criteria`` should be *list* of *dict* or *list* of *strings* and each *string* within the *list* entry should be a valid *dict* when read in python.







Status
------


Authors
~~~~~~~

- Ganesh Nalawade (@ganeshrn)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
