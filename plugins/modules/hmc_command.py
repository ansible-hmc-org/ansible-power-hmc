#!/usr/bin/python

# Copyright: (c) 2018- IBM, Inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: hmc_command
author:
    - Navinakumar Kandakur (@nkandak1)
short_description: Execute HMC command
notes:
    - This module supports passwordless authentication.
description:
    - Generic module that can execute any HMC CLI command.
    - The given command will be executed on all selected HMCs.
    - Information about the HMC CLI commands can be found at U(https://www.ibm.com/docs/en/power10/7063-CR1?topic=hmc-commands).
version_added: 1.0.0
options:
    hmc_host:
        description:
            - The IP address or hostname of the HMC.
        required: true
        type: str
    hmc_auth:
        description:
            - Username and Password credential of the HMC.
        required: true
        type: dict
        suboptions:
            username:
                description:
                    - Username of the HMC to log in.
                required: true
                type: str
            password:
                description:
                    - Password of the HMC.
                type: str
    cmd:
        description:
            - The command to be executed on HMC.
        required: true
        type: str
'''

EXAMPLES = r'''
- name: Execute a command on HMC
  ibm.power_hmc.hmc_command:
    hmc_host: "{{ inventory_hostname }}"
    hmc_auth:
      username: '{{ ansible_user }}'
      password: '{{ hmc_password }}'
    cmd: <cmd>
'''

RETURN = r'''
Command_output:
    description: Respective command output.
    type: str
    returned: always
'''

import logging
import os
import re
import shlex
LOG_FILENAME = "/tmp/ansible_power_hmc_{0}.log".format(os.getpid())
logger = logging.getLogger(__name__)
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_cli_client import HmcCliConnection
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_exceptions import HmcError
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_command_stack import HmcCommandStack
import sys

# Derive allowed verbs directly from HmcCommandStack.HMC_CMD — single source of truth.
# If a new verb is added to HMC_CMD it is automatically permitted here.
_ALLOWED_VERBS = frozenset(v.lower() for v in HmcCommandStack.HMC_CMD.values())

# Shell metacharacters that must never appear anywhere in cmd
_SHELL_METACHAR = re.compile(r'[;&|`$<>\n\\]')


def init_logger():
    old_umask = os.umask(0o177)
    try:
        logging.basicConfig(
            filename=LOG_FILENAME,
            format='[%(asctime)s] %(levelname)s: [%(funcName)s] %(message)s',
            level=logging.DEBUG)
    finally:
        os.umask(old_umask)


def run_hmc_adhoc_command(module, params):
    hmc_host = params['hmc_host']
    hmc_user = params['hmc_auth']['username']
    password = params['hmc_auth']['password']
    cmd = params['cmd'].strip()
    changed = False
    result = None

    # 1. Reject any shell metacharacter anywhere in the command string
    if _SHELL_METACHAR.search(cmd):
        module.fail_json(msg="Invalid characters in cmd. Shell metacharacters are not permitted.")

    # 2. First token must be a known HMC CLI verb from HmcCommandStack.HMC_CMD
    try:
        tokens = shlex.split(cmd)
    except ValueError as e:
        module.fail_json(msg="Malformed cmd: %s" % str(e))

    if not tokens or tokens[0].lower() not in _ALLOWED_VERBS:
        module.fail_json(msg="Command '%s' is not a permitted HMC command." % (tokens[0] if tokens else ''))

    hmc_conn = HmcCliConnection(module, hmc_host, hmc_user, password)

    try:
        result = hmc_conn.execute(cmd)
        output = (result.strip('\n')).split('\n')
        changed = True
    except (HmcError, Exception) as error:
        error_msg = repr(error)
        module.fail_json(msg=error_msg)

    logger.debug(changed)
    return changed, output, None


def perform_task(module):

    params = module.params
    actions = run_hmc_adhoc_command
    try:
        return actions(module, params)
    except (HmcError) as error:
        return False, repr(error), None


def run_module():

    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        hmc_host=dict(type='str', required=True),
        hmc_auth=dict(type='dict',
                      required=True,
                      no_log=True,
                      options=dict(
                          username=dict(required=True, type='str'),
                          password=dict(type='str', no_log=True),
                      )
                      ),
        cmd=dict(type='str', required=True),
    )

    module = AnsibleModule(
        argument_spec=module_args,
    )

    if module._verbosity >= 5:
        init_logger()

    if sys.version_info < (3, 0):
        py_ver = sys.version_info[0]
        module.fail_json(msg="Unsupported Python version {0}, supported python version is 3 and above".format(py_ver))

    changed, info, warning = perform_task(module)

    result = {}
    result['changed'] = changed
    if info:
        result['command_output'] = info

    if warning:
        result['warning'] = warning

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
