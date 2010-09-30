Settings
========

Kong has a number of settings that will effect the behavior of Kong. Mostly related to the sending of notifications.


KONG_MAIL_MANAGERS
------------------

Default: False

When set to true, this mails notifications to the people defined in Django's MANAGERS setting.

KONG_MAIL_ADMINS
----------------

Default: False

Like :ref:`KONG_MAIL_MANAGERS`, when set to ``True``, this mails notifications to the people defined in Django's ADMINS setting.

KONG_MAIL_ON_RECOVERY
---------------------

Default: True

When ``True``, you are notified when your test has been fixed, as well as when it breaks.


KONG_MAIL_ON_EVERY_FAILURE
--------------------------

Default: False

When ``True``, this will send you an email on every test that fails. If ``False``, you will only get emails on the first time that this test fails. This would presumably be used along with :ref:`KONG_MAIL_ON_RECOVERY`, so that you only get mails when a test fails and then passes again.

KONG_MAIL_ON_CONSECUTIVE_FAILURES
---------------------------------

Default: 1

When set to a value above ``1``, only send emails when a test has failed x number of times.

KONG_RESET_BROWSER
------------------

Default: False

When set to ``True``, the browser is reset between tests. This means in essence that all cookies are reset.
