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
            - Required for I(state=present), I(action=copy).
        type: str
    lpar_name:
        description:
            - The name of the powervm partition.
        required: true
        type: str
    name:
        description:
            - Name of the existing logical partition profile.
            - Used as the source profile when I(action=copy).
        required: true
        type: str
    processor_settings:
        description:
            - Processor configuration settings for the partition profile.
            - Valid only for I(state=present)
        type: dict
        suboptions:
            processor_mode:
                description:
                    - To specify the processor mode setting.
                    - Valid values are C(shared) and C(dedicated).
                type: str
            desired_processors:
                description:
                    - Desired number of processors.
                type: int
            minimum_processors:
                description:
                    - Minimum number of processors.
                type: int
            maximum_processors:
                description:
                    - Maximum number of processors.
                type: int
            desired_processing_units:
                description:
                    - Desired shared processing units for shared processor mode.
                    - Only valid if the C(processor_mode) is shared.
                type: float
            minimum_processing_units:
                description:
                    - Minimum shared processing units.
                    - Only valid if the C(processor_mode) is shared.
                type: float
            maximum_processing_units:
                description:
                    - Maximum shared processing units.
                    - Only valid if the C(processor_mode) is shared.
                type: float
            sharing_mode:
                description:
                    - Processor sharing mode for shared processor configuration.
                    - Only valid if the C(processor_mode) is shared.
                    - Valid values are C(capped) and C(uncapped).
                    - Deafult value is C(capped).
                type: str
            uncapped_weight:
                description:
                    - Weight value used for uncapped shared processor mode.
                    - Only valid if the C(processor_mode) is shared.
                type: int
            allow_processor_sharing:
                description:
                    - Only valid if the C(processor_mode) is dedicated.
                    - Valid values are C(active), C(inactive), C(always), and C(never).
                    - Only valid if the C(processor_mode) is dedicated.
                    - This determines if idle processors are released to the shared pool.
                    - Use C(active) to share idle cycles while the LPAR is running.
                    - Use C(inactive) to share cycles only when the LPAR is inactive.
                    - Use C(always) for continuous sharing of idle processor cycles.
                    - Use C(never) to ensure processors are never shared (performance mode).
                    - Default value is 'never'.
                type: str
            shared_processor_pool:
                description:
                    - Only valid if the C(processor_mode) is shared.
                    - Shared processor pool id.
                type: int
    memory_settings:
        description:
            - Memory configuration settings for the partition profile.
            - Valid only for I(state=present)
        type: dict
        suboptions:
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
            desired_huge_pagecount:
                description:
                    - Desired number of huge pages for the logical partition.
                type: int
            minimum_huge_pagecount:
                description:
                    - Minimum number of huge pages for the logical partition.
                type: int
            maximum_huge_pagecount:
                description:
                    - Maximum number of huge pages for the logical partition.
                type: int
            active_memory_expansion:
                description:
                    - Enable Active Memory Expansion.
                    - Default value is 'false'.
                type: bool
            expansion_factor:
                description:
                    - Active Memory Expansion (AME) expansion factor.
                    - Valid values are from C(0.0) to C(10.0).
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
    duplicate_prof_name:
        description:
            - Name of the new profile to be created by copying an existing profile.
            - Required when I(action=copy)
        type: str
    state:
        description:
            - Desired state of the logical partition profile.
            - C(present) creates a new partition profile.
        type: str
        choices: ['present']
    action:
        description:
            - C(copy) copies an existing partition profile.
        type: str
        choices: ['copy']
'''

EXAMPLES = '''
- name: Create a new partition profile with dedicated processor
  powervm_partition_profile:
    hmc_host: '{{ inventory_hostname }}'
    hmc_auth:
      username: '{{ ansible_user }}'
      password: '{{ hmc_password }}'
    system_name: <system_name/mtms>
    lpar_name: <lpar_name>
    name: dedicated_profile
    processor_settings:
      processor_mode: dedicated
      desired_processors: 1
      maximum_processors: 3
      minimum_processors: 1
      allow_processor_sharing: never
    state: present

- name: Create a new partition profile with shared processor and uncapped sharing mode
  powervm_partition_profile:
    hmc_host: '{{ inventory_hostname }}'
    hmc_auth:
      username: '{{ ansible_user }}'
      password: '{{ hmc_password }}'
    system_name: <system_name/mtms>
    lpar_name: <lpar_name>
    name: shared_testing
    processor_settings:
      processor_mode: shared
      desired_processors: 1
      maximum_processors: 1
      minimum_processors: 1
      minimum_processing_units: 1.0
      maximum_processing_units: 1.0
      desired_processing_units: 1.0
      sharing_mode: uncapped
      uncapped_weight: 100
    memory_settings:
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
    lpar_name: <lpar_name>
    name: shared_testing
    duplicate_prof_name: test
    action: copy
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

import logging
LOG_FILENAME = "/tmp/ansible_power_hmc.log"
logger = logging.getLogger(__name__)


def init_logger():
    logging.basicConfig(
        filename=LOG_FILENAME,
        format='[%(asctime)s] %(levelname)s: [%(funcName)s] %(message)s',
        level=logging.DEBUG)


def validate_sub_dict(sub_key, sub_params):
    """Validate nested dictionary parameters"""
    for key in list(sub_params.keys()):
        if not sub_params[key] and sub_params[key] != 0 and sub_params[key] != False:
            sub_params.pop(key)

    if not sub_params:
        raise ParameterError("Key values of '%s' are invalid or empty" % sub_key)

    if sub_key == 'processor_settings':
        processor_mode = sub_params.get('processor_mode')
        if processor_mode:
            if processor_mode.lower() not in ['dedicated', 'shared']:
                raise ParameterError("processor_mode must be either 'dedicated' or 'shared'")
            if processor_mode.lower() == 'dedicated':
                allow_sharing = sub_params.get('allow_processor_sharing')
                if allow_sharing and allow_sharing.lower() not in ['active', 'inactive', 'always', 'never']:
                    raise ParameterError("allow_processor_sharing must be one of: 'active', 'inactive', 'always', 'never'")
                invalid_params = ['sharing_mode', 'uncapped_weight', 'shared_processor_pool',
                                'minimum_processing_units', 'maximum_processing_units', 'desired_processing_units']
                found_invalid = [p for p in invalid_params if sub_params.get(p) is not None]
                if found_invalid:
                    raise ParameterError("Parameters %s are not valid for dedicated processor mode" % ', '.join(found_invalid))
            elif processor_mode.lower() == 'shared':
                sharing_mode = sub_params.get('sharing_mode')
                if sharing_mode and sharing_mode.lower() not in ['capped', 'uncapped']:
                    raise ParameterError("sharing_mode must be either 'capped' or 'uncapped'")
                if sub_params.get('allow_processor_sharing') is not None:
                    raise ParameterError("allow_processor_sharing is not valid for shared processor mode")
    elif sub_key == 'memory_settings':
        expansion_factor = sub_params.get('expansion_factor')
        if expansion_factor is not None:
            if not (0.0 <= expansion_factor <= 10.0):
                raise ParameterError("expansion_factor must be between 0.0 and 10.0")
        hw_page_ratio = sub_params.get('hardware_page_tableratio')
        if hw_page_ratio is not None:
            if not (5 <= hw_page_ratio <= 9):
                raise ParameterError("hardware_page_tableratio must be between 5 and 9")
        phys_page_ratio = sub_params.get('desired_physical_page_tableratio')
        if phys_page_ratio is not None:
            if not (0 <= phys_page_ratio <= 6):
                raise ParameterError("desired_physical_page_tableratio must be between 0 and 6")


def validate_parameters(params):
    '''Check that the input parameters satisfy the mutual exclusiveness of HMC'''
    opr = None
    if params['state'] is not None:
        opr = params['state']
    else:
        opr = params['action']
    unsupportedList = []
    mandatoryList = []
    if opr == 'present':
        mandatoryList = ['hmc_host', 'hmc_auth', 'system_name', 'lpar_name', 'name']
        unsupportedList = ['duplicate_prof_name']
        if params.get('processor_settings'):
            proc_settings = params['processor_settings']
            validate_sub_dict('processor_settings', proc_settings)
            processor_mode = proc_settings.get('processor_mode')
            if not processor_mode:
                raise ParameterError("processor_mode is required in processor_settings for state=present")
            if processor_mode.lower() == 'dedicated':
                required_fields = ['minimum_processors', 'maximum_processors', 'desired_processors']
            else:
                required_fields = ['minimum_processors', 'maximum_processors', 'desired_processors',
                                 'minimum_processing_units', 'maximum_processing_units', 'desired_processing_units']
            missing = [f for f in required_fields if proc_settings.get(f) is None]
            if missing:
                raise ParameterError("Missing required processor_settings fields: %s" % ', '.join(missing))
            min_proc = proc_settings['minimum_processors']
            des_proc = proc_settings['desired_processors']
            max_proc = proc_settings['maximum_processors']
            if not (min_proc <= des_proc <= max_proc):
                raise ParameterError("Processor values must satisfy: minimum_processors <= desired_processors <= maximum_processors")
            if processor_mode.lower() == 'shared':
                min_units = proc_settings['minimum_processing_units']
                des_units = proc_settings['desired_processing_units']
                max_units = proc_settings['maximum_processing_units']
                if not (min_units <= des_units <= max_units):
                    raise ParameterError("Processing unit values must satisfy: minimum_processing_units <= desired_processing_units <= maximum_processing_units")
                logger.debug("Here error")
                sharing_mode = proc_settings.get('sharing_mode')
                logger.debug("Here aano error")
                if sharing_mode and sharing_mode.lower() == 'uncapped':
                    if proc_settings.get('uncapped_weight') is None:
                        raise ParameterError("uncapped_weight is required when sharing_mode is 'uncapped'")
        else:
            raise ParameterError("processor_settings is required for state=present")
        if params.get('memory_settings'):
            mem_settings = params['memory_settings']
            validate_sub_dict('memory_settings', mem_settings)
            required_mem_fields = ['desired_memory', 'minimum_memory', 'maximum_memory',
                                  'desired_huge_pagecount', 'minimum_huge_pagecount', 'maximum_huge_pagecount']
            missing_mem = [f for f in required_mem_fields if mem_settings.get(f) is None]
            if missing_mem:
                raise ParameterError("Missing required memory_settings fields: %s" % ', '.join(missing_mem))
            min_mem = mem_settings['minimum_memory']
            des_mem = mem_settings['desired_memory']
            max_mem = mem_settings['maximum_memory']
            if not (min_mem <= des_mem <= max_mem):
                raise ParameterError("Memory values must satisfy: minimum_memory <= desired_memory <= maximum_memory")
        else:
            raise ParameterError("memory_settings is required for state=present")
    elif opr == 'copy':
        mandatoryList = ['hmc_host', 'hmc_auth', 'system_name', 'lpar_name', 'name', 'duplicate_prof_name']
        unsupportedList = ['processor_settings', 'memory_settings']
    collate = []
    for eachMandatory in mandatoryList:
        if not params.get(eachMandatory):
            collate.append(eachMandatory)
    if collate:
        if len(collate) == 1:
            raise ParameterError("mandatory parameter '%s' is missing" % (collate[0]))
        else:
            raise ParameterError("mandatory parameters '%s' are missing" % (','.join(collate)))
    collate = []
    for eachUnsupported in unsupportedList:
        if params.get(eachUnsupported):
            collate.append(eachUnsupported)
    if collate:
        if len(collate) == 1:
            raise ParameterError("unsupported parameter: %s" % (collate[0]))
        else:
            raise ParameterError("unsupported parameters: %s" % (', '.join(collate)))


def build_config_dict(params):
    config = {
        'name': params.get('name'),
        'duplicate_prof_name': params.get('duplicate_prof_name')
    }
    sections = ['processor_settings', 'memory_settings']
    for section in sections:
        section_data = params.get(section)
        if isinstance(section_data, dict):
            config.update(section_data) 
    return config


def copy_partition_profile(module, params):
    hmc_host = params['hmc_host']
    hmc_user = params['hmc_auth']['username']
    password = params['hmc_auth']['password']
    system_name = params['system_name']
    lpar_name = params['lpar_name']
    changed = False
    lpar_uuid = None
    name = params['name']
    duplicate_prof_name = params['duplicate_prof_name']
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
            if eachLpar['PartitionName'] == lpar_name:
                lpar_uuid = eachLpar['UUID']
                break
    else:
        module.fail_json(msg=f"Given partition ({lpar_name}) is not present on the system")
    try:
        result = rest_conn.getAllPartitionProfiles(lpar_uuid)
        if name not in result:
            module.fail_json(msg="A profile named " + name + " does not exist for the partition.")
        elif duplicate_prof_name in result:
            msg="A profile named " + duplicate_prof_name + " already exists."
            return False, None, msg
        else:
            config = {'name': name, 'duplicate_prof_name': duplicate_prof_name}
            final_result = rest_conn.copyPartitionProfile(lpar_uuid, config)
            if final_result == 200:
                final_result = {'msg': f"copy of {name} partition profile is created successfully"}
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
    lpar_name = params['lpar_name']
    changed = False
    lpar_uuid = None
    name = params['name']
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
            if eachLpar['PartitionName'] == lpar_name:
                lpar_uuid = eachLpar['UUID']
                break
    else:
        module.fail_json(msg="There are no Logical Partitions present on the system")

    try:
        result = rest_conn.getAllPartitionProfiles(lpar_uuid)
        if name in result:
            msg="A profile named " + name + " already exists."
            return False, None, msg
        else:
            config = build_config_dict(params)
            proc_settings = params.get('processor_settings', {})
            processor_mode = proc_settings.get('processor_mode', '').lower()
            if processor_mode == 'shared':
                config['processor_mode'] = 'false'
                if not config.get('sharing_mode'):
                    config['sharing_mode'] = 'capped'
                    config['uncapped_weight'] = 0
                if not config.get('shared_processor_pool'):
                    logger.debug("is it coming here")
                    config['shared_processor_pool'] = 0
            else:
                config['processor_mode'] = 'true'
                if config.get('allow_processor_sharing'):
                    sharing_input = config.get('allow_processor_sharing', 'never')
                    allow_sharing_mode = allow_processor_sharing_MAP.get(sharing_input)
                    config['allow_processor_sharing'] = allow_sharing_mode
                else:
                    config['allow_processor_sharing'] = allow_processor_sharing_MAP['never']
            mem_settings = params.get('memory_settings', {})
            if config.get('active_memory_expansion') is None:
                config['active_memory_expansion'] = False
            expansion_factor = config.get('expansion_factor')
            if expansion_factor is not None and expansion_factor >= 1:
                config['active_memory_expansion'] = True
            else:
                config['expansion_factor'] = 0.0
            if config.get('hardware_page_tableratio') is None:
                config['hardware_page_tableratio'] = 7
            if config.get('desired_physical_page_tableratio') is None:
                config['desired_physical_page_tableratio'] = 6
            result = rest_conn.createPartitionProfile(lpar_uuid, config)
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
    processor_args = dict(
        processor_mode=dict(type='str'),
        desired_processors=dict(type='int'),
        minimum_processors=dict(type='int'),
        maximum_processors=dict(type='int'),
        desired_processing_units=dict(type='float'),
        minimum_processing_units=dict(type='float'),
        maximum_processing_units=dict(type='float'),
        sharing_mode=dict(type='str'),
        uncapped_weight=dict(type='int'),
        allow_processor_sharing=dict(type='str'),
        shared_processor_pool=dict(type='int'),
    )
    memory_args = dict(
        desired_memory=dict(type='int'),
        minimum_memory=dict(type='int'),
        maximum_memory=dict(type='int'),
        desired_huge_pagecount=dict(type='int'),
        minimum_huge_pagecount=dict(type='int'),
        maximum_huge_pagecount=dict(type='int'),
        active_memory_expansion=dict(type='bool'),
        expansion_factor=dict(type='float'),
        hardware_page_tableratio=dict(type='int'),
        desired_physical_page_tableratio=dict(type='int'),
    )

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
        lpar_name=dict(type='str', required=True),
        name=dict(type='str', required=True),
        processor_settings=dict(type='dict',
                               options=processor_args
                               ),
        memory_settings=dict(type='dict',
                            options=memory_args
                            ),
        duplicate_prof_name=dict(type='str'),
        state=dict(type='str',
                   choices=['present']),
        action=dict(type='str',
                   choices=['copy']),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        mutually_exclusive=[('state', 'action')],
        required_one_of=[('state', 'action')],
        required_if=[['state', 'present', ['hmc_host', 'hmc_auth', 'system_name', 'lpar_name', 'processor_settings', 'memory_settings']],
                     ['action', 'copy', ['hmc_host', 'hmc_auth', 'system_name', 'lpar_name', 'duplicate_prof_name']]]
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
