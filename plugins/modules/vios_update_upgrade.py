# !/usr/bin/python

# Copyright: (c) 2018- IBM, Inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: vios_update_upgrade
author:
    - Sreenidhi S(@SreenidhiS1)
short_description: Manages the update and upgrade of the VIOS
notes:
    - All Operations support passwordless authentication.
description:
    - Updates the VIOS by installing the VIOS installation image located on an NFS/SFTP/HMC hard disk.
    - Upgrades the VIOS by obtaining  the required  files  from NFS/SFTP/HMC hard disk.
    - Update the VIOS from IBM Fix Central website
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
                    - Username of the HMC to login.
                required: true
                type: str
            password:
                description:
                    - Password of the HMC.
                type: str
    attributes:
        description:
            - Configuration parameters required for VIOS backup and restore.
        type: dict
        required: true
        suboptions:
            repository:
                description:
                    - The repository that contains the VIOS installation image.
                    - Valid values are C(sftp)for a secure FTP server, C(ibmwebsite) for the IBM Fix Central website,
                      C(nfs) for an NFS file system, C(disk) for the Hardware Management Console (HMC).
                    - C(ibmwebsite) is only valid for updation of VIOS
                type: str
                choices: ['nfs', 'sftp', 'disk', 'ibmwebsite']
            system_name:
                description:
                    - The name or MTMS(machine type model serial) of the managed system.
                type: str
            vios_id:
                description:
                    - The ID of the VIOS to backup.
                      vios_id, vios_name are mutually exclusive.
                type: str
            vios_name:
                description:
                    - The name of the VIOS to backup.
                      vios_id, vios_name are mutually exclusive.
                type: str
            image_name:
                description:
                    - The name of the VIOS update image.
                    - When the VIOS update image is on the HMC hard disk or the IBM Fix Central website,
                      this option is required to specify the name of the image to use for the update.
                    - When the VIOS update image is on a remote server or a USB data storage device and the --save option is specified,
                      this option is required to specify the name used to save the image to the HMC hard disk.
                type: str
            files:
                description:
                    - The list of the files that is required for update/upgrade
                    - This option is required and only valid when the VIOS installation image is on a remote server.
                type: list
                elements: str
            host_name:
                description:
                    - The host name or IP address of the remote server.
                type: str
            user_id:
                description:
                    - The user ID to use to log in to the remote SFTP server.
                type: str
            password:
                description:
                    - The password to use to log in to the remote SFTP server.
                    - password, ssh_key_file are mutually exclusive.
                type: str
            ssh_key_file:
                description:
                    - The name of the file that contains the SSH private key.
                    - password, ssh_key_file are mutually exclusive.
                type: str
            mount_loc:
                description:
                    - The mount location defined on the NFS server that contains the VIOS update image.
                type: str
            option:
                description:
                    - Options to be passed to the mount command used to mount the NFS file system that contains the VIOS update image.
                    - The HMC supports NFS versions 3 and 4.
                    - Default version is 3.
                type: str
                choices: ['3', '4']
            directory:
                description:
                    - The name of the directory on the remote server that contains the VIOS update image.
                    - If this option is not specified when the VIOS update image is on a SFTP server,
                      the image will be obtained from the user home directory.
                    - If this option is not specified when the VIOS update image is in an NFS file system,
                      the image will be obtained from the mount-location on the NFS server.
                type: str
            disks:
                description:
                    - The name of one or more free VIOS disks to be used for the upgrade.
                    - The total of the specified disk sizes must be a minimum of 30 GB.
                type: list
                elements: str
            restart:
                description:
                    - Restarts the VIOS after installing the update if the update requires a restart.
                type: bool
            save:
                description:
                    - Save the update image on the HMC hard disk.
                type: bool
    state:
        description:
            - The desired build state of the target VIOS.
            - C(facts) does not change anything on the VIOS and returns current version of VIOS.
            - C(updated) ensures the target VIOS is updated with given installation ISO image.
            - C(upgraded) ensures the target VIOS is upgraded with given upgrade files.
        type: str
        choices: ['facts', 'updated', 'upgraded']
'''

EXAMPLES = '''
- name: Get the current version of VIOS
  vios_update_upgrade:
    hmc_host: '{{ hmc_ip }}'
    hmc_auth: '{{ curr_hmc_auth }}'
    attributes:
      vios_name: <vios_name>
      system_name: <sys/MTMS>
    state: facts

- name: Update VIOS using sftp
  vios_update_upgrade:
    hmc_host: '{{ hmc_ip }}'
    hmc_auth: '{{ curr_hmc_auth }}'
    attributes:
      repository: sftp
      vios_id: <vios_id>
      system_name: <sys/MTMS>
      password: <password>
      user_id: <username>
      host_name: <hostip>
      files:
        - <iso file1>
    state: updated

- name: Update VIOS using nfs
  vios_update_upgrade:
    hmc_host: '{{ hmc_ip }}'
    hmc_auth: '{{ curr_hmc_auth }}'
    attributes:
      repository: nfs
      vios_id: <vios_id>
      system_name: <sys/MTMS>
      password: <password>
      user_id: <username>
      host_name: <hostip>
      files:
        - <iso file>
        - <bff file>
    state: updated

- name: Upgrade VIOS using disk
  vios_update_upgrade:
    hmc_host: '{{ hmc_ip }}'
    hmc_auth: '{{ curr_hmc_auth }}'
    attributes:
      repository: disk
      vios_id: <vios_id>
      system_name: <sys/MTMS>
      password: <password>
      user_id: <username>
      host_name: <hostip>
      disks:
        - Disk1
        - Disk2
    state: upgraded
'''

RETURN = '''
Command_output:
    description: Respective build information
    type: dict
    returned: always
'''

import logging
LOG_FILENAME = "/tmp/ansible_power_hmc.log"
logger = logging.getLogger(__name__)
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_cli_client import HmcCliConnection
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_exceptions import ParameterError
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_exceptions import HmcError
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_resource import Hmc
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_constants import HmcConstants
import sys


def init_logger():
    logging.basicConfig(
        filename=LOG_FILENAME,
        format='[%(asctime)s] %(levelname)s: [%(funcName)s] %(message)s',
        level=logging.DEBUG)


def validate_sub_params(params):
    opr = None
    unsupportedList = []
    mandatoryList = []
    opr = params['state']
    params = params['attributes']
    mandatoryList = ['repository', 'system_name']
    if opr == 'facts':
        mandatoryList = ['system_name']
    count = sum(x is not None for x in [params['vios_id'], params['vios_name']])
    if count == 0:
        raise ParameterError("Missing VIOS details")
    if count != 1:
        raise ParameterError("Parameters 'vios_id' and 'vios_name' are mutually exclusive")

    repo = params['repository']

    if opr == 'updated':
        unsupportedList += ['disks']
    elif opr == 'upgraded':
        mandatoryList += ['disks']
        unsupportedList += ['restart']
        if params['repository'] == 'ibmwebsite':
            raise ParameterError("Upgrade using 'ibmwebsite' is not supported")
        if params['repository'] in ['sftp', 'nfs']:
            mandatoryList += ['files']
    elif opr == 'facts':
        unsupportedList += ['files', 'host_name', 'user_id', 'password', 'ssh_key_file', 'repository', 'restart',
                            'mount_loc', 'option', 'directory', 'save', 'disks', 'image_name']

    if repo == 'sftp':
        count = sum(x is not None for x in [params['ssh_key_file'], params['password']])
        if count != 1 and count != 0:
            raise ParameterError("Parameters 'ssh_key_file' and 'password' are mutually exclusive")
        if count == 0:
            raise ParameterError("Either 'ssh_key_file' or 'password' is mandatory")
        mandatoryList += ['user_id', 'host_name']
        unsupportedList += ['mount_loc', 'option']
    elif repo == 'disk':
        mandatoryList += ['image_name']
        unsupportedList += ['files', 'host_name', 'user_id', 'password', 'ssh_key_file', 'mount_loc', 'option', 'directory', 'save']
    elif repo == 'ibmwebsite':
        mandatoryList += ['image_name']
        unsupportedList += ['files', 'host_name', 'user_id', 'password', 'ssh_key_file', 'mount_loc', 'option', 'directory']
    elif repo == 'nfs':
        mandatoryList += ['mount_loc', 'host_name']
        unsupportedList += ['user_id', 'password', 'ssh_key_file']

    collate = []
    for eachUnsupported in unsupportedList:
        if params[eachUnsupported]:
            collate.append(eachUnsupported)

    if collate:
        if len(collate) == 1:
            raise ParameterError("unsupported parameter: %s" % (collate[0]))
        else:
            raise ParameterError("unsupported parameters: %s" % (','.join(collate)))

    collate = []
    for eachMandatory in mandatoryList:
        if not params[eachMandatory]:
            collate.append(eachMandatory)
    if collate:
        if len(collate) == 1:
            raise ParameterError("mandatory parameter '%s' is missing" % (collate[0]))
        else:
            raise ParameterError("mandatory parameters '%s' are missing" % (','.join(collate)))


def validate_parameters(params):
    '''Check that the input parameters satisfy the mutual exclusiveness of HMC'''
    opr = None
    mandatoryList = []

    if params['state'] is not None:
        opr = params['state']
    else:
        opr = params['action']

    if opr in ['update', 'upgrade']:
        mandatoryList = ['hmc_host', 'hmc_auth', 'attributes']

    collate = []
    for eachMandatory in mandatoryList:
        if not params[eachMandatory]:
            collate.append(eachMandatory)
    if collate:
        if len(collate) == 1:
            raise ParameterError("mandatory parameter '%s' is missing" % (collate[0]))
        else:
            raise ParameterError("mandatory parameters '%s' are missing" % (','.join(collate)))
    validate_sub_params(params)


def facts(module, params):
    hmc_host = params['hmc_host']
    hmc_user = params['hmc_auth']['username']
    password = params['hmc_auth']['password']
    validate_parameters(params)
    attributes = params.get('attributes')
    hmc_conn = HmcCliConnection(module, hmc_host, hmc_user, password)
    vios_name = attributes['vios_name'] or attributes['vios_id']
    m_system = attributes['system_name']
    sys_list = (
        hmc_conn.execute("lssyscfg -r sys -F name").splitlines() + hmc_conn.execute("lssyscfg -r sys -F type_model*serial_num").splitlines()
    )
    if m_system not in sys_list:
        module.fail_json(msg="The managed system is not available in HMC")
    else:
        if attributes['vios_name'] is not None:
            vios_list = list(hmc_conn.execute("lssyscfg -r lpar -m {0} -F name".format(m_system)).splitlines())
        elif attributes['vios_id'] is not None:
            vios_list = list(hmc_conn.execute("lssyscfg -r lpar -m {0} -F lpar_id".format(m_system)).splitlines())
        if vios_name not in vios_list:
            module.fail_json(msg="The vios is not available in the managed system")
    if attributes['vios_name'] is not None:
        version = hmc_conn.execute("viosvrcmd -p {0} -m {1} -c ioslevel".format(vios_name, m_system)).strip()
    elif attributes['vios_id'] is not None:
        version = hmc_conn.execute("viosvrcmd --id {0} -m {1} -c ioslevel".format(vios_name, m_system)).strip()
    version = {
        "vios": vios_name,
        "system": m_system,
        "version": version}
    return False, version, None


def ensure_update_upgrade(module, params):
    hmc_host = params['hmc_host']
    hmc_user = params['hmc_auth']['username']
    password = params['hmc_auth']['password']
    validate_parameters(params)
    attributes = params.get('attributes')
    hmc_conn = HmcCliConnection(module, hmc_host, hmc_user, password)
    hmc = Hmc(hmc_conn)

    vios_name = attributes['vios_name'] or attributes['vios_id']
    m_system = attributes['system_name']
    sys_list = (
        hmc_conn.execute("lssyscfg -r sys -F name").splitlines() + hmc_conn.execute("lssyscfg -r sys -F type_model*serial_num").splitlines()
    )
    if m_system not in sys_list:
        module.fail_json(msg="The managed system is not available in HMC")
    else:
        if attributes['vios_name'] is not None:
            vios_list = list(hmc_conn.execute("lssyscfg -r lpar -m {0} -F name".format(m_system)).splitlines())
        elif attributes['vios_id'] is not None:
            vios_list = list(hmc_conn.execute("lssyscfg -r lpar -m {0} -F lpar_id".format(m_system)).splitlines())
        if vios_name not in vios_list:
            module.fail_json(msg="The vios is not available in the managed system")

    if attributes['repository'] in ['nfs', 'sftp']:
        if attributes['save'] is not None and attributes['image_name'] is None:
            raise ParameterError("To save the image to the HMC hard disk, 'image_name' parameter is required")
        if attributes['save'] is None and attributes['image_name'] is not None:
            raise ParameterError("For remote server repository'image_name' parameter is only required if 'save' option is set to 'true'")

    files = ''
    if attributes['files'] is not None:
        for each in attributes['files']:
            files += each + ','
    if files[:-1] != '':
        attributes['files'] = files[:-1]

    disk = ''
    if attributes['disks'] is not None:
        for each in attributes['disks']:
            disk += each + ','
    if disk[:-1] != '':
        attributes['disks'] = disk[:-1]

    option = ''
    if attributes['option'] is not None:
        option += '"ver=' + attributes['option'] + '"'
        attributes['option'] = option

    try:
        hmc.updatevios(module.params['state'], configDict=attributes)
    except HmcError as error:
        if HmcConstants.‎USER_AUTHORITY_ERR in repr(error):
            logger.debug(repr(error))
            return False, None, None
        else:
            raise
    changed = True
    return changed, None, None


def perform_task(module):
    params = module.params
    actions = {
        "updated": ensure_update_upgrade,
        "upgraded": ensure_update_upgrade,
        "facts": facts,
    }

    if not params['hmc_auth']:
        return False, "missing credential info", None
    try:
        return actions[params['state']](module, params)
    except Exception as error:
        return False, repr(error), None


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
        state=dict(type='str', choices=['updated', 'upgraded', 'facts']),
        attributes=dict(type='dict',
                        required=True,
                        options=dict(
                            repository=dict(type='str', choices=['disk', 'nfs', 'sftp', 'ibmwebsite']),
                            system_name=dict(type='str'),
                            vios_id=dict(type='str'),
                            vios_name=dict(type='str'),
                            image_name=dict(type='str'),
                            files=dict(type='list', elements='str'),
                            host_name=dict(type='str'),
                            user_id=dict(type='str'),
                            password=dict(type='str', no_log=True),
                            ssh_key_file=dict(type='str'),
                            mount_loc=dict(type='str'),
                            directory=dict(type='str'),
                            option=dict(type='str', choices=['3', '4']),
                            restart=dict(type='bool'),
                            save=dict(type='bool'),
                            disks=dict(type='list', elements='str'),
                        )
                        ),
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
    if isinstance(info, str):
        module.fail_json(msg=info)

    result = {}
    result['changed'] = changed
    result['info'] = info
    if warning:
        result['warning'] = warning

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
