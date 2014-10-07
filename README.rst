Membership - Video On Demand
============================

Library and utilities to interface with PBS's Membership Vault, which manages member access to MVOD.


Setup
=====

Copy *config.py.dist* to *config.py* and add your Membership Vault credentials.  Run the unit tests in the *tests* directory (or run *fab tests* if you have fabric installed).


Usage
=====

The module be imported and used for creating, updating, and listing Member records in the PBS Membership Vault.  There are also two functions on the command line that can be called to list the members or a specific member record in the Vault.  Check for usage on the command line::

    ./mvault.py --help

Check the tests for code examples.


TODO
====

* Account for pagination in the returned lists.
* Include command line parameters for credentials.
* Better error handling from API responses.