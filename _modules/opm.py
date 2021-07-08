# -*- coding: utf-8 -*-
"""
Manage Openresty Package Manager modules.
"""
from __future__ import absolute_import, print_function, unicode_literals

import os
import logging

# Import Salt libs
import salt.utils.platform
from salt.exceptions import CommandExecutionError

log = logging.getLogger(__name__)  # pylint: disable=C0103


def _opm(command, runas=None, env={}):
    """
    Run the actual opm command.
    :param command: string
    Command to run
    :param runas: string : None
    The user to run opm as.
    :param env: {}
    Additional environment variables to run the opm with.
    """
    cmdline = ["opm"] + command

    # use the current user's home as fallback if HOME is undefined
    if ("HOME" not in env) and (not salt.utils.platform.is_windows()):
        env["HOME"] = os.path.expanduser("~")
        log.debug("HOME environment set to %s", env["HOME"])

    ret = __salt__["cmd.run_all"](cmdline, runas=runas, env=env, python_shell=False)

    if ret["retcode"] == 0:
        return ret["stdout"]

    raise CommandExecutionError(ret["stderr"])


def install(package, version=None, runas=None, env={}):
    if version:
        if version[0] in "<>=":
            package += version
        else:
            package += "=" + version

    return _opm(["get"] + [package], runas=runas, env=env)


def remove(package, runas=None, env={}):
    return _opm(["remove"] + [package], runas=runas, env=env)


def list(runas=None, env={}):
    command = ["list"]

    stdout = _opm(command, runas=runas, env=env)

    ret = {}
    for line in stdout.splitlines():
        name, version = line.split()
        ret[name] = version

    return ret
