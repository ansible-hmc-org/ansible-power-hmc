#!/usr/bin/python

# Copyright: (c) 2018- IBM, Inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: firmware_update
short_description: Change firmware level on Managed Systems
notes:
    - All operations support passwordless authentication.
version_added: "1.1.0"
description:
    - Update/Upgrade a managed system.
options:
    hmc_host:
        description:
            - IP address or hostname of the HMC.
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
                    - HMC username.
                required: true
                type: str
            password:
                description:
                    - HMC password.
                type: str
    system_name:
        description:
            - The name or mtms (machine type model serial) of the managed system.
        required: true
        type: str
    repository:
        description:
            - The repository from which to retrieve the firmware updates. Valid values are ibmwebsite for the IBM service website,
              ftp for a remote FTP site, sftp for a remote secure FTP (SFTP) site
        type: str
        default: ibmwebsite
        choices: ['ibmwebsite', 'ftp', 'sftp']
    remote_repo:
        description: When the image repository needs credentials to be accessed remotely.
        type: dict
        suboptions:
            hostname:
                description:
                    - The hostname or IP address of the remote server where the
                      firmware image is located.
                required: true
                type: str
            userid:
                description:
                    - The user ID to use to log in to the remote FTP or SFTP server.
                      This option is required when the firmware image is located on a remote FTP or SFTP server
                      Otherwise, this option is not valid.
                required: true
                type: str
            passwd:
                description:
                    - The password to use to log in to the remote FTP or SFTP server.
                      The I(passwd) and I(sshkey) options are mutually exclusive in case if I(location_type=sftp).
                      This option is only valid when the firmware image is located on a remote FTP or SFTP server.
                type: str
            sshkey_file:
                description:
                    - The name of the file that contains the SSH private key.
                      This option is only valid if I(location_type=sftp).
                type: str
            directory:
                description:
                    - Location where the images are stored.
                required: true
                type: str
    level:
        description:
            -  Specify sss to retrieve a specific level of Managed System or Power LIC updates, even if disruptive.
               sss is the three character identifier of the specific level to retrieve.
               This is only valid when the LIC type is either Managed System only or Power only.
            -  Specify ccc,ppp to retrieve a specific level of Managed System and Power LIC updates, even if disruptive.
               ccc is the three character identifier of the specific level of Managed System LIC updates to retrieve.
               ppp is the three character identifier of the specific level of Power LIC updates to retrieve.
               This is only valid when the LIC type is both Managed System and Power.
            -  Specify release1_level1,release2_level2,... to retrieve specific levels of LIC updates, even if disruptive.
               The level specified in each entry indicates the desired level
               for all components which are running the release specified in the entry.
        type: str
        default: latest
    state:
        description:
            - C(updated) executes an update on target system.
            - C(upgraded) executes an upgrade on target system.
        type: str
        choices: ['updated', 'upgraded']
    action:
        description:
            - C(accept) accepts firmware level for target system.
        type: str
        choices: ['accept']

author:
    - Mario Maldonado (@Mariomds)
'''

EXAMPLES = r'''
- name: Update to latest level with default values (latest at ibmwebsite).
  ibm.power_hmc.firmware_update:
      hmc_host: '{{ inventory_hostname }}'
      hmc_auth:
          username: '{{ ansible_user }}'
          password: '{{ hmc_password }}'
      system_name: <System name/mtms>
      state: updated

- name: Upgrade system to specific level at an sftp repo.
  firmware_update:
      hmc_host: '{{ inventory_hostname }}'
      hmc_auth: '{{ curr_hmc_auth }}'
      system_name: <System name/mtms>
      repository: sftp
      remote_repo:
      hostname: 9.3.147.210
      userid: <user>
      passwd: <password>
      directory: /repo/images/
      level: 01VL941_047
      state: upgraded
'''

RETURN = r'''
service_pack:
    description: The service pack representation of the system
    type: str
    returned: always
    sample: 'FW940.20'
level:
    description: The specific level active on the system
    type: str
    returned: always
    sample: '55'
ecnumber:
    description: The engineering change (EC) number associated with the firmware update
    type: str
    returned: always
    sample: '01VL940'
'''
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_cli_client import HmcCliConnection
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_resource import Hmc
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_exceptions import HmcError
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_exceptions import ParameterError

import logging
import sys
LOG_FILENAME = "/tmp/ansible_power_hmc.log"
logger = logging.getLogger(__name__)


def init_logger():
    logging.basicConfig(
        filename=LOG_FILENAME,
        format='[%(asctime)s] %(levelname)s: [%(funcName)s] %(message)s',
        level=logging.DEBUG)


def create_hmc_conn(module, params):
    hmc_host = params['hmc_host']
    hmc_user = params['hmc_auth']['username']
    password = params['hmc_auth']['password']
    hmc_conn = HmcCliConnection(module, hmc_host, hmc_user, password)
    hmc = Hmc(hmc_conn)

    return hmc


def extract_updlic_options(params):
    system_name = params['system_name']
    repo = params['repository']
    level = params['level']
    remote_repo = params['remote_repo']

    return system_name, repo, level, remote_repo


def update_system(module, params):
    hmc = create_hmc_conn(module, params)
    system_name, repo, level, remote_repo = extract_updlic_options(params)
    ret_dict = {}
    try:
        initial_level = hmc.get_firmware_level(system_name)
        hmc.update_managed_system(system_name, False, repo, level, remote_repo)
        ret_dict = {'msg': 'system update finished'}
        new_level = hmc.get_firmware_level(system_name)
        logger.debug("new_level: %s", new_level)
        ret_dict.update(new_level)
    except HmcError as on_system_error:
        return False, None, repr(on_system_error)

    if (initial_level == new_level):
        changed = False
    else:
        changed = True
    ret_dict['diff'] = {'before': initial_level,
                        'after': new_level,
                        }
    return changed, ret_dict, None


def upgrade_system(module, params):
    hmc = create_hmc_conn(module, params)
    system_name, repo, level, remote_repo = extract_updlic_options(params)
    ret_dict = {}
    try:
        initial_level = hmc.get_firmware_level(system_name)
        hmc.update_managed_system(system_name, True, repo, level, remote_repo)
        ret_dict = {'msg': 'system upgrade finished'}
        new_level = hmc.get_firmware_level(system_name)
        logger.debug("new_level: %s", new_level)
        ret_dict.update(new_level)
    except HmcError as on_system_error:
        error_text = repr(on_system_error)
        # HmcAnsible owners suggested to report this as a success since it's due to set up failure
        no_update_avail_snippet = "No updates available"
        changed = False
        if no_update_avail_snippet.lower() in error_text.lower():
            changed = True
        return changed, None, error_text

    if (initial_level == new_level):
        changed = False
    else:
        changed = True
    ret_dict['diff'] = {'before': initial_level,
                        'after': new_level,
                        }
    return changed, ret_dict, None


def accept_level(module, params):
    hmc = create_hmc_conn(module, params)
    system_name = params['system_name']
    ret_dict = {}
    try:
        hmc.accept_level(system_name)
    except HmcError as on_system_error:
        return False, None, repr(on_system_error)

    ret_dict['msg'] = 'level accepted'
    return True, ret_dict, None


def perform_task(module):
    params = module.params
    actions = {
        "updated": update_system,
        "upgraded": upgrade_system,
        "accept": accept_level,
    }
    oper = 'action'
    if params['action'] is None:
        oper = 'state'
    try:
        validate_parameters(params)
        return actions[params[oper]](module, params)
    except Exception as error:
        return False, None, repr(error)


def validate_parameters(params):
    remote_repo = params['remote_repo']
    if remote_repo:
        passwd = remote_repo['passwd']
        sshkey = remote_repo['sshkey_file']
        if passwd and sshkey:
            raise ParameterError("'passwd' and 'sshkey_file' are  mutually exclusive")
        repository = params['repository']
        if repository == 'ftp' and sshkey is not None:
            raise ParameterError("'repository:ftp' and 'sshkey_file' are  incompatible")
        if repository == 'ibmwebsite':
            raise ParameterError("Value 'ibmwebsite' is incompatible with any 'remote_repo' arguments")


def run_module():
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
        system_name=dict(type='str', required=True),
        action=dict(type='str', choices=['accept']),
        state=dict(type='str', choices=['updated', 'upgraded', ]),
        level=dict(type='str', default='latest'),
        repository=dict(type='str', default='ibmwebsite', choices=['ibmwebsite', 'ftp', 'sftp']),
        remote_repo=dict(type='dict', options=dict(
                              hostname=dict(type='str', required=True),
                              userid=dict(type='str', required=True),
                              passwd=dict(type='str', no_log=True),
                              sshkey_file=dict(type='str'),
                              directory=dict(type='str', required=True), )
                         )
    )

    # seed the result dict in the object
    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        mutually_exclusive=[('state', 'action'), ('action', 'repository'), ('action', 'remote_repo'), ('action', 'level')]
    )
    if module._verbosity >= 5:
        init_logger()

    if sys.version_info < (3, 0):
        py_ver = sys.version_info[0]
        module.fail_json(msg="Unsupported Python version {0}, supported python version is 3 and above".format(py_ver))

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    changed, return_dict, error = perform_task(module)
    logger.debug("return-val: %s", return_dict)
    result['changed'] = changed
    if return_dict:
        result.update(return_dict)
    if error:
        result['failed'] = error

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if isinstance(error, str):
        module.fail_json(msg=error)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
