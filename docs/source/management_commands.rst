Management Commands
===================

Kong ships with management commands that allows you to easily run your tests.  There are a couple of different ways to run tests, based on how you want things to work.

check_sites
-----------

**By default, this runs tests for all your sites**

This is the main command that is used to run kong tests. By default, it does nothing, but you can pass in arguments to it, to make it do what you want.



Arguments
~~~~~~~~~

-t, --test <test_slug>
""""""""""""""""""""""

Run the tests for a specific ``Test``. This might be run across multiple ``Site``s or ``Type``s, whatever the test defines.

-s, --site <site_slug>
""""""""""""""""""""""

Run all of the tests for a specific site. This will run the tests that explicitly point at the ``Site``, as well as the tests for the ``Type`` that the site is.


-T, --type <type_slug>
""""""""""""""""""""""

Run the tests for a specific ``Type``. This will run the tests for all sites for that ``Type``.

