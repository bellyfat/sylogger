About
=====

OUTDATED!

Sylogger is `Application Service <http://matrix.org/docs/guides/application_services.html>`_
 for `matrix-org/synapse <https://github.com/matrix-org/synapse>`_
 server. It provide ability for logging every communication event on homeserver.

In this log you can see:

- who, when and what wrote
- who and where upload file, link to uploaded file
- who and when create/rename/modify room

What you will not see in log:

- End-2-end encrypted comunications - they can not be decrypted on the server side.

For test run
============

1. Clone ``git clone https://github.com/matrix-org/sylogger``
2. Change dir to clonned source
3. Edit your ``homeserver.yaml``: add to list ``app_service_config_files:`` path to ``sylogger.yaml`` 
4. Edit ``sylogger.yaml`` if you need change listen ip or port (do not foget to set same settings in ``sylogger.conf``)
5. Edit ``sylogger.conf`` to setup listen ip, port, path to log file
6. Restart synapse service to reload configuration
7. Start sylogger  from source root by ``python -m sylogger.sylogger``

Installation
============

1. Run ``pip install https://github.com/matrix-org/sylogger/tarball/master``
2. Edit your ``homeserver.yaml``: add to list ``app_service_config_files:`` path to ``sylogger.yaml`` (by default ``/etc/matrix-synapse/sylogger.yaml``)
3. Edit ``sylogger.yaml`` if you need change listen ip or port (do not foget to set same settings in ``sylogger.conf``)
4. Edit ``sylogger.conf`` to setup listen ip, port, path to log file
5. Check ``/lib/systemd/system/matrix-sylogger.unit``:

- specified user must exist
- specified paths must exist
- specified path to ``sylogger.conf`` must match the path in your system

6. Restart you synapse server for configuration reload
7. Roload systemd units ``systemctl daemon-reload``
8. Start sylogger ``systemctl start matrix-sylogger``
9. Enable sylogger autostart if needs ``systemctl enable matrix-sylogger``

What happens if new types of events appear in synapse?
======================================================

If after synapse update appear new types of events sylogger will not lose them: all events that hasn't special handler in sylogger will redirected to default handler. Default handler dumps all event data.
