======================================
Ansible Utils Collection Release Notes
======================================

.. contents:: Topics


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
