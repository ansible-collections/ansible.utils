======================================
Ansible Utils Collection Release Notes
======================================

.. contents:: Topics


v2.3.0
======

Minor Changes
-------------

- Add usable_range test plugin

Bugfixes
--------

- Also include empty lists and mappings into the output dictionary (https://github.com/ansible-collections/ansible.utils/pull/58).

Documentation Changes
---------------------

- Update doc for usable_range filter plugin

v2.2.0
======

Minor Changes
-------------

- Add in_any_network, in_network, in_one_network test plugins
- Add ip, ip_address test plugins
- Add ipv4, ipv4_address, ipv4_hostmask, ipv4_netmask test plugins
- Add ipv6, ipv6_address, ipv6_ipv4_mapped, ipv6_sixtofour, ipv6_teredo test plugins
- Add loopback, mac, multicast test plugins
- Add private, public, reserved test plugins
- Add resolvable test plugins
- Add subnet_of, supernet_of, unspecified test plugins

v2.1.0
======

Minor Changes
-------------

- Add from_xml and to_xml fiter plugin (https://github.com/ansible-collections/ansible.utils/pull/56).

Bugfixes
--------

- Add missing test requirements (https://github.com/ansible-collections/ansible.utils/pull/57).

v2.0.2
======

Bugfixes
--------

- Fix cli_parse template_path read error (https://github.com/ansible-collections/ansible.utils/pull/51).
- Fix jsonschema input data format checking (https://github.com/ansible-collections/ansible.utils/pull/50).

v2.0.1
======

Bugfixes
--------

- Fix ansible.utils.cli_parse action plugin to support old cli_parse sub-plugin structure in ansible.netcommon collection.

v2.0.0
======

Breaking Changes / Porting Guide
--------------------------------

- If added custom sub plugins in your collection move from old location `plugins/<sub-plugin-name>` to the new location `plugins/sub_plugins/<sub-plugin-name>` and update the imports as required
- Move sub plugins cli_parsers, fact_diff and validate to `plugins/sub_plugins` folder
- The `cli_parsers` sub plugins folder name is changed to `cli_parse` to have consistent naming convention, that is all the cli_parse subplugins will now be in `plugins/sub_plugins/cli_parse` folder

v1.0.1
======

Minor Changes
-------------

- Move CHANGELOG.rst file under changelogs folder as required

v1.0.0
======

Minor Changes
-------------

- Add cli_parse module and plugins (https://github.com/ansible-collections/ansible.utils/pull/28)
- Added fact_diff plugin and sub plugin
- Added validate module/lookup/filter/test plugin to validate data based on given criteria

Bugfixes
--------

- linting and formatting for CI

New Plugins
-----------

Lookup
~~~~~~

- get_path - Retrieve the value in a variable using a path
- index_of - Find the indices of items in a list matching some criteria
- to_paths - Flatten a complex object into a dictionary of paths and values
- validate - Validate data with provided criteria

New Modules
-----------

- cli_parse - Parse cli output or text using a variety of parsers
- fact_diff - Find the difference between currently set facts
- update_fact - Update currently set facts
- validate - Validate data with provided criteria
