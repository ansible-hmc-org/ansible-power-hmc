from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest
import importlib

IMPORT_HMC_VIOS = "ansible_collections.ibm.power_hmc.plugins.modules.vios"

from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_exceptions import ParameterError

hmc_auth = {'username': 'hscroot', 'password': 'password_value'}
test_data = [
    # ALL vios partition testdata
    # system name is missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'present',
      'system_name': None, 'name': 'vmname', 'settings': "sett"},
     "ParameterError: mandatory parameter 'system_name' is missing"),
    # vios name is missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'present',
      'system_name': 'systemname', 'name': None, 'settings': "sett"},
     "ParameterError: mandatory parameter 'name' is missing"),
    # host is missing
    ({'hmc_host': None, 'hmc_auth': hmc_auth, 'state': 'present',
      'system_name': 'systemname', 'name': "abc", 'settings': "sett"},
     "ParameterError: mandatory parameter 'hmc_host' is missing"),
    # system_name and vios name are missing
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'present',
      'system_name': None, 'name': None, 'settings': "sett"},
     "ParameterError: mandatory parameters 'system_name,name' are missing"),
    # unsupported parameter nim_IP
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'present',
      'system_name': 'sysName', 'name': 'viosName', 'settings': "sett", 'nim_IP': '1.1.1.1',
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: nim_IP"),
    # unsupported parameter nim_gateway
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'present',
      'system_name': 'sysName', 'name': 'viosName', 'settings': "sett", 'nim_IP': None,
      'nim_gateway': '1.1.1.1', 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: nim_gateway"),
    # unsupported parameter nim_viosIP
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'present',
      'system_name': 'sysName', 'name': 'viosName', 'settings': "sett", 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': '1.1.1.1', 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: vios_IP"),
    # unsupported parameter nim_subnetmask
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'present',
      'system_name': 'sysName', 'name': 'viosName', 'settings': "sett", 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': '255.255.256.254', 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: nim_subnetmask"),
    # unsupported parameter prof_name
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'present',
      'system_name': 'sysName', 'name': 'viosName', 'settings': "sett", 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': 'pfnam',
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: prof_name"),
    # unsupported parameter location_code
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'present',
      'system_name': 'sysName', 'name': 'viosName', 'settings': "sett", 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': 'abc:xyz:123', 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: location_code"),
    # unsupported parameter nim_vlan_id
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'present',
      'system_name': 'sysName', 'name': 'viosName', 'settings': "sett", 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': '2', 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: nim_vlan_id"),
    # unsupported parameter nim_vlan_priority
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'present',
      'system_name': 'sysName', 'name': 'viosName', 'settings': "sett", 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': '2', 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: nim_vlan_priority"),
    # unsupported parameter timeout
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'present',
      'system_name': 'sysName', 'name': 'viosName', 'settings': "sett", 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': 50,
      'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: timeout"),
    # unsupported parameter virtual_optical_media
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'present',
      'system_name': 'sysName', 'name': 'viosName', 'settings': "sett", 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': True, 'free_pvs': False},
     "ParameterError: unsupported parameter: virtual_optical_media")]

test_data1 = [
    # ALL vios install using nim testdata
    # system name is missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'action': 'install', 'state': None,
      'system_name': None, 'name': 'vmname', 'nim_IP': '1.1.1.1',
      'nim_gateway': '1.1.1.1', 'vios_IP': '12.13.14.15', 'nim_subnetmask': '2.5.5.4',
      'prof_name': None, 'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None,
      'timeout': 50},
     "ParameterError: mandatory parameter 'system_name' is missing"),
    # vios name is missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'action': 'install', 'state': None,
      'system_name': 'systemname', 'name': None, 'nim_IP': '1.1.1.1',
      'nim_gateway': '1.1.1.1', 'vios_IP': '12.13.14.15', 'nim_subnetmask': '2.5.5.4',
      'prof_name': None, 'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None,
      'timeout': 50},
     "ParameterError: mandatory parameter 'name' is missing"),
    # host is missing
    ({'hmc_host': None, 'hmc_auth': hmc_auth, 'action': 'install', 'state': None,
      'system_name': 'systemname', 'name': "abc", 'nim_IP': '1.1.1.1',
      'nim_gateway': '1.1.1.1', 'vios_IP': '12.13.14.15', 'nim_subnetmask': '2.5.5.4',
      'prof_name': None, 'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None,
      'timeout': 50},
     "ParameterError: mandatory parameter 'hmc_host' is missing"),
    # system_name and vios name are missing
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'action': 'install', 'state': None,
      'system_name': None, 'name': None, 'nim_IP': '1.1.1.1',
      'nim_gateway': '1.1.1.1', 'vios_IP': '12.13.14.15', 'nim_subnetmask': '2.5.5.4',
      'prof_name': None, 'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None,
      'timeout': 50},
     "ParameterError: mandatory parameters 'system_name,name' are missing"),
    # nim_IP is missing
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'action': 'install', 'state': None,
      'system_name': 'sysName', 'name': 'vmName', 'nim_IP': None,
      'nim_gateway': '1.1.1.1', 'vios_IP': '12.13.14.15', 'nim_subnetmask': '2.5.5.4',
      'prof_name': None, 'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None,
      'timeout': 50},
     "ParameterError: mandatory parameter 'nim_IP' is missing"),
    # nim_gateway is missing
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'action': 'install', 'state': None,
      'system_name': 'sysName', 'name': 'vmName', 'nim_IP': '12.13.14.11',
      'nim_gateway': None, 'vios_IP': '12.13.14.15', 'nim_subnetmask': '2.5.5.4',
      'prof_name': None, 'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None,
      'timeout': 50},
     "ParameterError: mandatory parameter 'nim_gateway' is missing"),
    # vios_IP is missing
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'action': 'install', 'state': None,
      'system_name': 'sysName', 'name': 'vmName', 'nim_IP': '12.13.14.11',
      'nim_gateway': '1.1.1.1', 'vios_IP': None, 'nim_subnetmask': '2.5.5.4',
      'prof_name': None, 'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None,
      'timeout': 50},
     "ParameterError: mandatory parameter 'vios_IP' is missing"),
    # nim_subnetmask is missing
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'action': 'install', 'state': None,
      'system_name': 'sysName', 'name': 'vmName', 'nim_IP': '12.13.14.11',
      'nim_gateway': '1.1.1.1', 'vios_IP': '12.13.14.15', 'nim_subnetmask': None,
      'prof_name': None, 'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None,
      'timeout': 50},
     "ParameterError: mandatory parameter 'nim_subnetmask' is missing"),
    # unsupported parameter Settings
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'action': 'install', 'state': None,
      'system_name': 'sysName', 'name': 'viosName', 'settings': "sett", 'nim_IP': '1.1.1.1',
      'nim_gateway': 'ab', 'vios_IP': 'bc', 'nim_subnetmask': 'cd', 'prof_name': 'ef',
      'location_code': 'fg', 'nim_vlan_id': 'dh', 'nim_vlan_priority': 'hi', 'timeout': 'ij',
      'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: settings"),
    # unsupported parameter virtual_optical_media
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'action': 'install', 'state': None,
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': '1.1.1.1',
      'nim_gateway': 'ab', 'vios_IP': 'bc', 'nim_subnetmask': 'cd', 'prof_name': 'ef',
      'location_code': 'fg', 'nim_vlan_id': 'dh', 'nim_vlan_priority': 'hi', 'timeout': 'ij',
      'virtual_optical_media': True, 'free_pvs': False},
     "ParameterError: unsupported parameter: virtual_optical_media"),
    # unsupported parameter free_pvs
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'action': 'install', 'state': None,
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': '1.1.1.1',
      'nim_gateway': 'ab', 'vios_IP': 'bc', 'nim_subnetmask': 'cd', 'prof_name': 'ef',
      'location_code': 'fg', 'nim_vlan_id': 'dh', 'nim_vlan_priority': 'hi', 'timeout': 'ij',
      'virtual_optical_media': False, 'free_pvs': True},
     "ParameterError: unsupported parameter: free_pvs")
     # unsupported parameter img_dir
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'action': 'install', 'state': None,
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': '1.1.1.1',
      'nim_gateway': 'ab', 'vios_IP': 'bc', 'nim_subnetmask': 'cd', 'prof_name': 'ef',
      'location_code': 'fg', 'nim_vlan_id': 'dh', 'nim_vlan_priority': 'hi', 'timeout': 'ij',
      'img_dir':'myvios'},
     "ParameterError: unsupported parameter: img_dir")]

test_data2 = [
    # ALL fetchviosInfo testdata
    # system name is missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'facts',
      'system_name': None, 'name': 'vmname', 'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: mandatory parameter 'system_name' is missing"),
    # vios name is missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': 'facts',
      'system_name': 'systemname', 'name': None, 'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: mandatory parameter 'name' is missing"),
    # host is missing
    ({'hmc_host': None, 'hmc_auth': hmc_auth, 'state': 'facts',
      'system_name': 'systemname', 'name': "abc", 'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: mandatory parameter 'hmc_host' is missing"),
    # system_name and vios name are missing
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts',
      'system_name': None, 'name': None, 'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: mandatory parameters 'system_name,name' are missing"),
    # unsupported parameter nim_IP
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': '1.1.1.1',
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: nim_IP"),
    # unsupported parameter nim_gateway
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': '1.1.1.1', 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: nim_gateway"),
    # unsupported parameter nim_viosIP
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': '1.1.1.1', 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: vios_IP"),
    # unsupported parameter nim_subnetmask
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': '255.255.256.254', 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: nim_subnetmask"),
    # unsupported parameter prof_name
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': 'pfnam',
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: prof_name"),
    # unsupported parameter location_code
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': 'abc:xyz:123', 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: location_code"),
    # unsupported parameter nim_vlan_id
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': '2', 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: nim_vlan_id"),
    # unsupported parameter nim_vlan_priority
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': '2', 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: nim_vlan_priority"),
    # unsupported parameter timeout
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': 50,
      'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: timeout"),
    # unsupported parameter settings
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts',
      'system_name': 'sysName', 'name': 'viosName', 'settings': "sett", 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: settings")]

test_data3 = [
    # ALL accept license testdata
    # system name is missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': None, 'action': 'accept_license',
      'system_name': None, 'name': 'vmname', 'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: mandatory parameter 'system_name' is missing"),
    # vios name is missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': None, 'action': 'accept_license',
      'system_name': 'systemname', 'name': None, 'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: mandatory parameter 'name' is missing"),
    # host is missing
    ({'hmc_host': None, 'hmc_auth': hmc_auth, 'state': None, 'action': 'accept_license',
      'system_name': 'systemname', 'name': "abc", 'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: mandatory parameter 'hmc_host' is missing"),
    # system_name and vios name are missing
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': None, 'action': 'accept_license',
      'system_name': None, 'name': None, 'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: mandatory parameters 'system_name,name' are missing"),
    # unsupported parameter nim_IP
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': None, 'action': 'accept_license',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': '1.1.1.1',
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None, 'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: nim_IP"),
    # unsupported parameter nim_gateway
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': None, 'action': 'accept_license',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': '1.1.1.1', 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None, 'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: nim_gateway"),
    # unsupported parameter nim_viosIP
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': None, 'action': 'accept_license',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': '1.1.1.1', 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None, 'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: vios_IP"),
    # unsupported parameter nim_subnetmask
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': None, 'action': 'accept_license',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': '255.255.256.254', 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None, 'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: nim_subnetmask"),
    # unsupported parameter prof_name
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': None, 'action': 'accept_license',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': 'pfnam',
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None, 'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: prof_name"),
    # unsupported parameter location_code
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': None, 'action': 'accept_license',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': 'abc:xyz:123', 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None, 'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: location_code"),
    # unsupported parameter nim_vlan_id
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': None, 'action': 'accept_license',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': '2', 'nim_vlan_priority': None, 'timeout': None, 'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: nim_vlan_id"),
    # unsupported parameter nim_vlan_priority
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': None, 'action': 'accept_license',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': '2', 'timeout': None, 'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: nim_vlan_priority"),
    # unsupported parameter timeout
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': None, 'action': 'accept_license',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': 50, 'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: timeout"),
    # unsupported parameter settings
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': None, 'action': 'accept_license',
      'system_name': 'sysName', 'name': 'viosName', 'settings': "sett", 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None, 'virtual_optical_media': False, 'free_pvs': False},
     "ParameterError: unsupported parameter: settings"),
    # unsupported parameter virtual_optical_media
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': None, 'action': 'accept_license',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None, 'virtual_optical_media': True, 'free_pvs': False},
     "ParameterError: unsupported parameter: virtual_optical_media"),
    # unsupported parameter free_pvs
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': None, 'action': 'accept_license',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None, 'virtual_optical_media': False, 'free_pvs': True},
     "ParameterError: unsupported parameter: free_pvs")]

test_data4 = [
    # ALL vios install using disk testdata
    # system name is missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'action': 'install', 'state': None, 'vios_iso': 'flash.iso',
      'system_name': None, 'name': 'lpar1', 'img_dir': 'myvios', 'network_macaddr': 'tdbvw45rdvt',
      'vios_gateway': '1.1.1.1', 'vios_IP': '12.13.14.15', 'vios_subnetmask': '2.5.5.4',
      'prof_name': 'default', 'label': 'viostest'},
     "ParameterError: mandatory parameter 'system_name' is missing"),
    # vios name is missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'action': 'install', 'state': None, 'vios_iso': 'flash.iso',
      'system_name': 'hmc-zz', 'name': None, 'img_dir': 'myvios', 'network_macaddr': 'tdbvw45rdvt',
      'vios_gateway': '1.1.1.1', 'vios_IP': '12.13.14.15', 'vios_subnetmask': '2.5.5.4',
      'prof_name': 'default', 'label': 'viostest'},
     "ParameterError: mandatory parameter 'name' is missing"),
    # host is missing
    ({'hmc_host': None, 'hmc_auth': hmc_auth, 'action': 'install', 'state': None, 'vios_iso': 'flash.iso',
      'system_name': 'hmc-zz', 'name': 'lpar1', 'img_dir': 'myvios', 'network_macaddr': 'tdbvw45rdvt',
      'vios_gateway': '1.1.1.1', 'vios_IP': '12.13.14.15', 'vios_subnetmask': '2.5.5.4',
      'prof_name': 'default', 'label': 'viostest'},
     "ParameterError: mandatory parameter 'hmc_host' is missing"),
      # system_name and name are missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'action': 'install', 'state': None, 'vios_iso': 'flash.iso',
      'system_name': None, 'name': None, 'img_dir': 'myvios', 'network_macaddr': 'tdbvw45rdvt',
      'vios_gateway': '1.1.1.1', 'vios_IP': '12.13.14.15', 'vios_subnetmask': '2.5.5.4',
      'prof_name': 'default', 'label': 'viostest'},
     "ParameterError: mandatory parameter 'system_name, name' are missing"),
      # img_dir is missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'action': 'install', 'state': None, 'vios_iso': 'flash.iso',
      'system_name': 'hmc-zz', 'name': 'lpar1', 'img_dir': None, 'network_macaddr': 'tdbvw45rdvt',
      'vios_gateway': '1.1.1.1', 'vios_IP': '12.13.14.15', 'vios_subnetmask': '2.5.5.4',
      'prof_name': 'default', 'label': 'viostest'},
     "ParameterError: mandatory parameter 'img_dir' is missing"),
      # vios_iso is missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'action': 'install', 'state': None, 'vios_iso': None,
      'system_name': 'hmc-zz', 'name': 'lpar1', 'img_dir': 'myvios', 'network_macaddr': 'tdbvw45rdvt',
      'vios_gateway': '1.1.1.1', 'vios_IP': '12.13.14.15', 'vios_subnetmask': '2.5.5.4',
      'prof_name': None, 'label': 'viostest'},
     "ParameterError: mandatory parameter 'vios_iso' is missing"),
    # vios_IP is missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'action': 'install', 'state': None, 'vios_iso': 'flash.iso',
      'system_name': 'hmc-zz', 'name': 'lpar1', 'img_dir': 'myvios', 'network_macaddr': 'tdbvw45rdvt',
      'vios_gateway': '1.1.1.1', 'vios_IP': None, 'vios_subnetmask': '2.5.5.4',
      'prof_name': 'default', 'label': 'viostest'},
     "ParameterError: mandatory parameter 'vios_IP' is missing"),
    # vios_gateway is missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'action': 'install', 'state': None, 'vios_iso': 'flash.iso',
      'system_name': 'hmc-zz', 'name': 'lpar1', 'img_dir': 'myvios', 'network_macaddr': 'tdbvw45rdvt',
      'vios_gateway': None, 'vios_IP': '12.13.14.15', 'vios_subnetmask': '2.5.5.4',
      'prof_name': 'default', 'label': 'viostest'},
     "ParameterError: mandatory parameter 'vios_gateway' is missing"),
    # vios_subnetmask is missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'action': 'install', 'state': None, 'vios_iso': 'flash.iso',
      'system_name': 'hmc-zz', 'name': 'lpar1', 'img_dir': 'myvios', 'network_macaddr': 'tdbvw45rdvt',
      'vios_gateway': '1.1.1.1', 'vios_IP': '12.13.14.15', 'vios_subnetmask': None,
      'prof_name': 'default', 'label': 'viostest'},
     "ParameterError: mandatory parameter 'vios_subnetmask' is missing"),
    # vios_subnetmask and vios_gateway are missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'action': 'install', 'state': None, 'vios_iso': 'flash.iso',
      'system_name': 'hmc-zz', 'name': 'lpar', 'img_dir': 'myvios', 'network_macaddr': 'tdbvw45rdvt',
      'vios_gateway': None, 'vios_IP': '12.13.14.15', 'vios_subnetmask': None,
      'prof_name': 'default', 'label': 'viostest'},
     "ParameterError: mandatory parameter 'vios_subnetmask, vios_gateway' are missing"),
     # unsupported parameter nim_IP
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'action': 'install', 'state': None, 'vios_iso': 'flash.iso',
      'system_name': 'hmc-zz', 'vios_name': 'lpar1', 'img_dir': 'myvios', 'network_macaddr': 'tdbvw45rdvt',
      'vios_gateway': '1.1.1.1', 'vios_IP': '12.13.14.15', 'vios_subnetmask': '2.5.5.4',
      'prof_name': 'default', 'label': 'viostest', 'nim_IP': '1.1.1.1'},
     "ParameterError: unsupported parameter: nim_IP ")
     # unsupported parameter nim_gateway
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'action': 'install', 'state': None, 'vios_iso': 'flash.iso',
      'system_name': 'hmc-zz', 'name': 'lpar1', 'img_dir': 'myvios', 'network_macaddr': 'tdbvw45rdvt',
      'vios_gateway': '1.1.1.1', 'vios_IP': '12.13.14.15', 'vios_subnetmask': '2.5.5.4',
      'prof_name': 'default', 'label': 'viostest', 'nim_gateway': '1.1.1.1'},
     "ParameterError: unsupported parameter: nim_gateway ")
     # unsupported parameter nim_subnetmask
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'action': 'install', 'state': None, 'vios_iso': 'flash.iso',
      'system_name': 'hmc-zz', 'name': 'lpar1', 'img_dir': 'myvios', 'network_macaddr': 'tdbvw45rdvt',
      'vios_gateway': '1.1.1.1', 'vios_IP': '12.13.14.15', 'vios_subnetmask': '2.5.5.4',
      'prof_name': 'default', 'label': 'viostest', 'nim_subnetmask': '1.1.1.1'},
     "ParameterError: unsupported parameter: nim_subnetmask ")
     ]
    


def common_mock_setup(mocker):
    hmc_vios = importlib.import_module(IMPORT_HMC_VIOS)
    mocker.patch.object(hmc_vios, 'HmcCliConnection')
    mocker.patch.object(hmc_vios, 'Hmc', autospec=True)
    return hmc_vios


@pytest.mark.parametrize("vios_test_input, expectedError", test_data)
def test_call_inside_createVios(mocker, vios_test_input, expectedError):
    hmc_vios = common_mock_setup(mocker)
    if 'ParameterError' in expectedError:
        with pytest.raises(ParameterError) as e:
            hmc_vios.createVios(hmc_vios, vios_test_input)
        assert expectedError == repr(e.value)
    else:
        hmc_vios.createVios(hmc_vios, vios_test_input)


@pytest.mark.parametrize("vios_test_input, expectedError", test_data1)
def test_call_inside_installVios(mocker, vios_test_input, expectedError):
    hmc_vios = common_mock_setup(mocker)
    if 'ParameterError' in expectedError:
        with pytest.raises(ParameterError) as e:
            hmc_vios.install(hmc_vios, vios_test_input)
        assert expectedError == repr(e.value)
    else:
        hmc_vios.install(hmc_vios, vios_test_input)


@pytest.mark.parametrize("vios_test_input, expectedError", test_data2)
def test_call_inside_fetchViosInfo(mocker, vios_test_input, expectedError):
    hmc_vios = common_mock_setup(mocker)
    if 'ParameterError' in expectedError:
        with pytest.raises(ParameterError) as e:
            hmc_vios.fetchViosInfo(hmc_vios, vios_test_input)
        assert expectedError == repr(e.value)
    else:
        hmc_vios.fetchViosInfo(hmc_vios, vios_test_input)


@pytest.mark.parametrize("vios_test_input, expectedError", test_data3)
def test_call_inside_(mocker, vios_test_input, expectedError):
    hmc_vios = common_mock_setup(mocker)
    if 'ParameterError' in expectedError:
        with pytest.raises(ParameterError) as e:
            hmc_vios.viosLicenseAccept(hmc_vios, vios_test_input)
        assert expectedError == repr(e.value)
    else:
        hmc_vios.viosLicenseAccept(hmc_vios, vios_test_input)


@pytest.mark.parametrize("vios_test_input, expectedError", test_data4)
def test_call_inside_installViosDisk(mocker, vios_test_input, expectedError):
    hmc_vios = common_mock_setup(mocker)
    if 'ParameterError' in expectedError:
        with pytest.raises(ParameterError) as e:
            hmc_vios.install(hmc_vios, vios_test_input)
        assert expectedError == repr(e.value)
    else:
        hmc_vios.install(hmc_vios, vios_test_input)
