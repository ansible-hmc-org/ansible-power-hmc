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

DOCUMENTATION = '''
---
module: powervm_partition_profile
author:
    - Sreenidhi (@SreenidhiS1)
short_description: Create, Copy PowerVM Partition Profiles
description:
    - Create new partition profile
    - Copy an existing partition profile
version_added: "1.2.0"
requirements:
- Python >= 3
- lxml
options:
    hmc_host:
        description:
            - IPaddress or hostname of the HMC.
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
            - The name or mtms (machine type model serial) of the managed system..
            - Optional for I(state=present), I(state=copy).
        type: str
    vm_name:
        description:
            - The name of the powervm partition.
        required: true
        type: str
    prof_name:
        description:
            - Name of the existing logical partition profile.
            - Used as the source profile when C(state=copy).
        required: true
        type: str
    processing_mode:
        description:
            - To specify the processor mode setting.
            - Valid values are C(shared) and C(dedicated).
            - Shared will assign partial processor units from the shared processor pool.
            - Dedicated will assign the entire processor that can only be used by the logical partition.
        type: str
    duplicate_prof_name:
        description:
            - Name of the new profile to be created by copying an existing profile.
            - Required when C(state=copy)
        type: str
    desired_processing_units:
        description:
            - Desired shared processing units for shared processor mode.
            - This value must be greater than or equal to C(minimum_processing_units)
              and less than or equal to C(maximum_processing_units).
        type: float
    minimum_processing_units:
        description:
            - Minimum shared processing units.
            - This value must be less than or equal to C(desired_processing_units).
        type: float
    maximum_processing_units:
        description:
            - Maximum shared processing units.
            - This value must be greater than or equal to C(desired_processing_units).
        type: float
    desired_processors:
        description:
            - Desired number of processors.
            - This value must be greater than or equal to C(minimum_processors)
              and less than or equal to C(maximum_processors).
        type: int
    minimum_processors:
        description:
            - Minimum number of processors.
            - This value must be less than or equal to C(desired_processors).
        type: int
    maximum_processors:
        description:
            - Maximum number of processors.
            - This value must be greater than or equal to C(desired_processors).
        type: int
    desired_huge_pagecount:
        description:
            - Desired number of huge pages for the logical partition.
            - This value must be greater than or equal to C(minimum_huge_pagecount)
              and less than or equal to C(maximum_huge_pagecount).
        type: int

    minimum_huge_pagecount:
        description:
            - Minimum number of huge pages for the logical partition.
            - This value must be less than or equal to C(desired_huge_pagecount).
        type: int

    maximum_huge_pagecount:
        description:
            - Maximum number of huge pages for the logical partition.
            - This value must be greater than or equal to C(desired_huge_pagecount).
        type: int
    sharing_mode:
        description:
            - Processor sharing mode for shared processor configuration.
            - Valid values are C(capped) and C(uncapped).
            - Applicable only when C(processing_mode=shared).
            - When set to C(uncapped), C(uncapped_weight) becomes mandatory.
        type: str
    uncapped_weight:
        description:
            - Weight value used for uncapped shared processor mode.
            - Mandatory when C(sharing_mode=uncapped).
        type: int
    allow_processor_sharing:
        description:
            - Controls processor sharing behavior in dedicated processor mode.
            - Valid values are C(active), C(inactive), C(always), and C(never).
            - Applicable only when C(processing_mode=dedicated).
            - Default is C(never).
        type: str
    shared_processor_poolName:
        description:
            - Shared processor pool name or ID.
            - Applicable only when C(processing_mode=shared).
            - Default is C(DefaultPool).
        type: str
    desired_memory:
        description:
            - Desired memory value in MB.
        type: int
    minimum_memory:
        description:
            - Minimum memory value in MB.
        type: int
    maximum_memory:
        description:
            - Maximum memory value in MB.
        type: int
    active_memory_expansion:
        description:
            - Enable Active Memory Expansion.
        type: bool
    expansion_factor:
        description:
            - Active Memory Expansion (AME) expansion factor.
            - Valid values are from C(1.0) to C(10.0).
            - When specified, AME is automatically enabled.
        type: float
    hardware_page_tableratio:
        description:
            - Hardware page table ratio.
            - Valid values are from C(5) to C(9).
        type: int
    desired_physical_page_tableratio:
        description:
            - Desired physical page table ratio.
            - Valid values are from C(0) to C(6).
        type: int
    state:
        description:
            - Desired state of the logical partition profile.
            - C(present) creates a new partition profile.
            - C(copy) copies an existing partition profile.
        required: true
        type: str
        choices: ['present', 'copy']
'''

EXAMPLES = '''
- name: Create a new partition profile with dedicated processor
  powervm_partition_profile:
    hmc_host: '{{ inventory_hostname }}'
    hmc_auth:
      username: '{{ ansible_user }}'
      password: '{{ hmc_password }}'
    system_name: <system_name/mtms>
    vm_name: <vm_name>
    prof_name: dedicated_profile
    desired_processors: 1
    maximum_processors: 3
    minimum_processors: 1
    processing_mode: dedicated
    allow_processor_sharing: never
    state: present

- name: Create a new partition profile with shared processor and uncapped sharing mode
  powervm_partition_profile:
    hmc_host: '{{ inventory_hostname }}'
    hmc_auth:
      username: '{{ ansible_user }}'
      password: '{{ hmc_password }}'
    system_name: <system_name/mtms>
    vm_name: <vm_name>
    prof_name: shared_testing
    desired_processors: 1
    maximum_processors: 1
    minimum_processors: 1
    minimum_processing_units: 1
    maximum_processing_units: 1
    desired_processing_units: 1
    sharing_mode: uncapped
    uncapped_weight: 100
    desired_huge_pagecount: 2
    maximum_huge_pagecount: 2
    minimum_huge_pagecount: 2
    desired_memory: 1024
    maximum_memory: 1024
    minimum_memory: 1024
    expansion_factor: 10
    state: present

- name: Create a copy of already existing partition profile
  powervm_partition_profile:
    hmc_host: '{{ inventory_hostname }}'
    hmc_auth:
      username: '{{ ansible_user }}'
      password: '{{ hmc_password }}'
    system_name: <system_name/mtms>
    vm_name: <vm_name>
    prof_name: shared_testing
    duplicate_prof_name: test
'''

RETURN = '''
changed:
    description:
        - Indicates whether any change was made.
    type: bool
    returned: always
partition_info:
    description:
        - Information about the logical partition profile operation.
        - For C(state=present), contains a success message for the created profile.
        - For C(state=copy), contains a success message for the copied profile.
    type: dict
    returned: on success
    sample:
        {
            "msg": "copy of default_profile partition profile is created successfully"
        }
'''

import sys
import json
import re
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_cli_client import HmcCliConnection
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_resource import Hmc
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_exceptions import HmcError
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_exceptions import ParameterError
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_exceptions import Error
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_rest_client import HmcRestClient
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_constants import HmcConstants

# Generic setting for log initializing and log rotation
import logging
LOG_FILENAME = "/tmp/ansible_power_hmc.log"
logger = logging.getLogger(__name__)


def init_logger():
    logging.basicConfig(
        filename=LOG_FILENAME,
        format='[%(asctime)s] %(levelname)s: [%(funcName)s] %(message)s',
        level=logging.DEBUG)


def validate_parameters(params):
    '''Check that the input parameters satisfy the mutual exclusiveness of HMC'''
    opr = params['state']
    unsupportedList = []
    mandatoryList = []

    if opr == 'present':
        mandatoryList = ['hmc_host', 'hmc_auth', 'system_name', 'vm_name', 'prof_name', 'processing_mode', 'minimum_processors',
                         'maximum_processors', 'desired_processors', 'desired_huge_pagecount', 'maximum_huge_pagecount',
                         'minimum_huge_pagecount', 'desired_memory', 'maximum_memory', 'minimum_memory']
        unsupportedList = ['duplicate_prof_name']

        if 'processing_mode' in params and params['processing_mode'] is not None:
            if params['processing_mode'].lower() not in ['dedicated', 'shared']:
                raise ParameterError("processing_mode must be either 'dedicated' or 'shared'")
            if params['processing_mode'].lower() == 'dedicated':
                unsupportedList += ['sharing_mode', 'uncapped_weight', 'shared_processor_poolName', 'minimum_processing_units',
                                    'maximum_processing_units', 'desired_processing_units']
                if 'allow_processor_sharing' in params and params['allow_processor_sharing'] is not None:
                    if params['allow_processor_sharing'].lower() not in ['active', 'inactive', 'always', 'never']:
                        raise ParameterError("allow_processor_sharing must be one of: 'active', 'inactive', 'always', 'never'")
                else:
                    params['allow_processor_sharing'] = 'never'
            if params['processing_mode'].lower() == 'shared':
                mandatoryList += ['minimum_processing_units', 'maximum_processing_units', 'desired_processing_units']
                unsupportedList += ['allow_processor_sharing']
                if params['shared_processor_poolName'] is None:
                    params['shared_processor_poolName'] = 'DefaultPool'
                if params['sharing_mode'] is not None:
                    if params['sharing_mode'].lower() not in ['capped', 'uncapped']:
                        raise ParameterError("processing_mode must be either 'capped' or 'uncapped'")
                    if params['sharing_mode'].lower() == 'capped':
                        unsupportedList += ['uncapped_weight']
                    elif params['sharing_mode'].lower() == 'uncapped':
                        mandatoryList += ['uncapped_weight']
            if params['expansion_factor'] is not None:
                if not (1 <= params['expansion_factor'] <= 10):
                    raise ParameterError("expansion_factor must be between 1.0 and 10.0")
            if params['hardware_page_tableratio'] is not None:
                if not (5 <= params['hardware_page_tableratio'] <= 9):
                    raise ParameterError("hardware_page_tableratio must be between 5 and 9")
            if params['desired_physical_page_tableratio'] is not None:
                if not (0 <= params['desired_physical_page_tableratio'] <= 6):
                    raise ParameterError("desired_physical_page_tableratio must be between 0 and 6")

    if opr == 'copy':
        mandatoryList = ['hmc_host', 'hmc_auth', 'system_name', 'vm_name', 'prof_name', 'duplicate_prof_name']
        unsupportedList = ['processing_mode', 'minimum_processors', 'maximum_processors', 'desired_processors', 'desired_huge_pagecount',
                           'maximum_huge_pagecount', 'minimum_memory', 'minimum_huge_pagecount', 'desired_physical_page_tableratio',
                           'hardware_page_tableratio', 'minimum_processing_units', 'maximum_processing_units', 'desired_processing_units',
                           'allow_processor_sharing', 'sharing_mode', 'expansion_factor', 'shared_processor_poolName',
                           'uncapped_weight', 'active_memory_expansion', 'desired_memory', 'maximum_memory']

    collate = []
    for eachMandatory in mandatoryList:
        if not params[eachMandatory]:
            collate.append(eachMandatory)
    if collate:
        if len(collate) == 1:
            raise ParameterError("mandatory parameter '%s' is missing" % (collate[0]))
        else:
            raise ParameterError("mandatory parameters '%s' are missing" % (','.join(collate)))

    collate = []
    for eachUnsupported in unsupportedList:
        if params[eachUnsupported]:
            collate.append(eachUnsupported)

    if collate:
        if len(collate) == 1:
            raise ParameterError("unsupported parameter: %s" % (collate[0]))
        else:
            raise ParameterError("unsupported parameters: %s" % (', '.join(collate)))

    if params['processing_mode'] is not None:
        if params['processing_mode'].lower() in ['dedicated', 'shared']:
            if not (params['minimum_processors'] <= params['desired_processors'] <= params['maximum_processors']):
                raise ParameterError("value of minimum_processors <= desired_processors <= maximum_processors")

        if params['processing_mode'].lower() == 'shared':
            if not (params['minimum_processing_units'] <= params['desired_processing_units'] <= params['maximum_processing_units']):
                raise ParameterError("value of minimum_processing_units <= desired_processing_units <= maximum_processing_units")


def copy_partition_profile(module, params):
    hmc_host = params['hmc_host']
    hmc_user = params['hmc_auth']['username']
    password = params['hmc_auth']['password']
    system_name = params['system_name']
    vm_name = params['vm_name']
    changed = False
    lpar_uuid = None
    prof_name = params['prof_name']
    hmc_conn = HmcCliConnection(module, hmc_host, hmc_user, password)
    hmc = Hmc(hmc_conn)
    final_result = {}
    validate_parameters(params)
    if system_name is not None and re.match(HmcConstants.MTMS_pattern, system_name):
        try:
            system_name = hmc.getSystemNameFromMTMS(system_name)
        except HmcError as on_system_error:
            return changed, repr(on_system_error), None
    try:
        rest_conn = HmcRestClient(hmc_host, hmc_user, password)
    except Exception as error:
        logger.debug(repr(error))
        module.fail_json(msg="Logon to HMC failed")

    if system_name:
        system_uuid, server_dom = rest_conn.getManagedSystem(system_name)
    if not system_uuid:
        module.fail_json(msg="Given system is not present")

    lpar_response = rest_conn.getLogicalPartitionsQuick(system_uuid)
    if lpar_response is not None:
        lpar_quick_list = json.loads(lpar_response)
        for eachLpar in lpar_quick_list:
            if eachLpar['PartitionName'] == vm_name:
                lpar_uuid = eachLpar['UUID']
                break
    else:
        module.fail_json(msg="There are no Logical Partitions present on the system")

    try:
        result = rest_conn.getAllPartitionProfiles(lpar_uuid)
        if prof_name not in result:
            module.fail_json(msg="A profile named " + prof_name + " doesnot exist for the partition.")
        elif params['duplicate_prof_name'] in result:
            module.fail_json(msg="A profile named " + params['duplicate_prof_name'] + " already exist.")
        else:
            final_result = rest_conn.copyPartitionProfile(lpar_uuid, params)
            if final_result == 200:
                final_result = {'msg': f"copy of {params['prof_name']} partition profile is created successfully"}
                return True, final_result, None
            else:
                return False, final_result, None
    except Exception as e:
        return False, repr(e), None


def create_partition_profile(module, params):
    hmc_host = params['hmc_host']
    hmc_user = params['hmc_auth']['username']
    password = params['hmc_auth']['password']
    system_name = params['system_name']
    vm_name = params['vm_name']
    changed = False
    lpar_uuid = None
    prof_name = params['prof_name']
    hmc_conn = HmcCliConnection(module, hmc_host, hmc_user, password)
    hmc = Hmc(hmc_conn)
    final_result = {}
    validate_parameters(params)
    allow_processor_sharing_MAP = {
        'inactive': 'sre idle proces',
        'active': 'sre idle procs active',
        'always': 'sre idle procs always',
        'never': 'keep idle procs'
    }

    if system_name is not None and re.match(HmcConstants.MTMS_pattern, system_name):
        try:
            system_name = hmc.getSystemNameFromMTMS(system_name)
        except HmcError as on_system_error:
            return changed, repr(on_system_error), None
    try:
        rest_conn = HmcRestClient(hmc_host, hmc_user, password)
    except Exception as error:
        logger.debug(repr(error))
        module.fail_json(msg="Logon to HMC failed")

    if system_name:
        system_uuid, server_dom = rest_conn.getManagedSystem(system_name)
    if not system_uuid:
        module.fail_json(msg="Given system is not present")

    lpar_response = rest_conn.getLogicalPartitionsQuick(system_uuid)
    if lpar_response is not None:
        lpar_quick_list = json.loads(lpar_response)
        for eachLpar in lpar_quick_list:
            if eachLpar['PartitionName'] == vm_name:
                lpar_uuid = eachLpar['UUID']
                break
    else:
        module.fail_json(msg="There are no Logical Partitions present on the system")

    try:
        result = rest_conn.getAllPartitionProfiles(lpar_uuid)
        if prof_name in result:
            module.fail_json(msg="A profile named " + prof_name + " already exists for this partition.")
        else:
            if params['processing_mode'].lower() == 'shared':
                params['processing_mode'] = 'false'
                if params['sharing_mode'] is None:
                    params['sharing_mode'] = 'capped'
            else:
                params['processing_mode'] = 'true'
                if params['allow_processor_sharing']:
                    sharing_input = params.get('allow_processor_sharing', 'never')
                    allow_sharing_mode = allow_processor_sharing_MAP.get(sharing_input)
                    params['allow_processor_sharing'] = allow_sharing_mode

            if params['active_memory_expansion'] is None:
                params['active_memory_expansion'] = False
            if params['expansion_factor'] is not None and params['expansion_factor'] >= 1:
                params['active_memory_expansion'] = True
            else:
                params['expansion_factor'] = 0.0
            if params['hardware_page_tableratio'] is None:
                params['hardware_page_tableratio'] = 7
            if params['desired_physical_page_tableratio'] is None:
                params['desired_physical_page_tableratio'] = 6
            result = rest_conn.createPartitionProfile(lpar_uuid, params)
        if result.startswith("REST"):
            return False, result, None
        else:
            final_result = {"msg": f"{result} partition profile is created successfully"}
            changed = True
            return changed, final_result, None
    except Exception as e:
        return False, repr(e), None


def perform_task(module):
    params = module.params
    actions = {
        "present": create_partition_profile,
        "copy": copy_partition_profile
    }

    oper = 'state'
    if params['state'] is None:
        oper = 'action'
    try:
        return actions[params[oper]](module, params)
    except (ParameterError, HmcError, Error) as error:
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
        system_name=dict(type='str'),
        vm_name=dict(type='str', required=True),
        prof_name=dict(type='str', required=True),
        processing_mode=dict(type='str'),
        desired_processing_units=dict(type='float'),
        maximum_processing_units=dict(type='float'),
        minimum_processing_units=dict(type='float'),
        desired_processors=dict(type='int'),
        maximum_processors=dict(type='int'),
        minimum_processors=dict(type='int'),
        shared_processor_poolName=dict(type='str'),
        uncapped_weight=dict(type='int'),
        sharing_mode=dict(type='str'),
        allow_processor_sharing=dict(type='str'),
        active_memory_expansion=dict(type='bool'),
        desired_huge_pagecount=dict(type='int'),
        maximum_huge_pagecount=dict(type='int'),
        minimum_huge_pagecount=dict(type='int'),
        desired_memory=dict(type='int'),
        maximum_memory=dict(type='int'),
        minimum_memory=dict(type='int'),
        expansion_factor=dict(type='float'),
        hardware_page_tableratio=dict(type='int'),
        desired_physical_page_tableratio=dict(type='int'),
        duplicate_prof_name=dict(type='str'),
        state=dict(type='str', required=True,
                   choices=['present', 'copy']),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        required_if=[['state', 'present', ['hmc_host', 'hmc_auth', 'system_name', 'vm_name']],
                     ['state', 'copy', ['hmc_host', 'hmc_auth', 'system_name', 'vm_name']]]
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
    if info:
        result['partition_info'] = info

    if warning:
        result['warning'] = warning

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
