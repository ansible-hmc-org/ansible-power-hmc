from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest
import importlib

IMPORT_HMC_VIOS = "ansible_collections.ibm.power_hmc.plugins.modules.vios"

from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_exceptions import ParameterError

hmc_auth = {'username': 'hscroot', 'password': 'password_value'}
sftp_auth = {'username': 'hmcct', 'password': 'password_value'}
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
      'virtual_optical_media': False, 'free_pvs': False, 'directory_name': None, 'directory_list': None,
      'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: nim_IP"),
    # unsupported parameter nim_gateway
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'present',
      'system_name': 'sysName', 'name': 'viosName', 'settings': "sett", 'nim_IP': None,
      'nim_gateway': '1.1.1.1', 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False, 'directory_name': None, 'directory_list': None,
      'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: nim_gateway"),
    # unsupported parameter nim_viosIP
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'present',
      'system_name': 'sysName', 'name': 'viosName', 'settings': "sett", 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': '1.1.1.1', 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False, 'directory_name': None, 'directory_list': None,
      'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: vios_IP"),
    # unsupported parameter nim_subnetmask
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'present',
      'system_name': 'sysName', 'name': 'viosName', 'settings': "sett", 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': '255.255.256.254', 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False, 'directory_name': None, 'directory_list': None,
      'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: nim_subnetmask"),
    # unsupported parameter prof_name
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'present',
      'system_name': 'sysName', 'name': 'viosName', 'settings': "sett", 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': 'pfnam',
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False, 'directory_name': None, 'directory_list': None,
      'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: prof_name"),
    # unsupported parameter location_code
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'present',
      'system_name': 'sysName', 'name': 'viosName', 'settings': "sett", 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': 'abc:xyz:123', 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False, 'directory_name': None, 'directory_list': None,
      'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: location_code"),
    # unsupported parameter nim_vlan_id
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'present',
      'system_name': 'sysName', 'name': 'viosName', 'settings': "sett", 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': '2', 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False, 'directory_name': None, 'directory_list': None,
      'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: nim_vlan_id"),
    # unsupported parameter nim_vlan_priority
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'present',
      'system_name': 'sysName', 'name': 'viosName', 'settings': "sett", 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': '2', 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False, 'directory_name': None, 'directory_list': None,
      'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: nim_vlan_priority"),
    # unsupported parameter timeout
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'present',
      'system_name': 'sysName', 'name': 'viosName', 'settings': "sett", 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': 50,
      'virtual_optical_media': False, 'free_pvs': False, 'directory_name': None, 'directory_list': None,
      'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: timeout"),
    # unsupported parameter virtual_optical_media
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'present',
      'system_name': 'sysName', 'name': 'viosName', 'settings': "sett", 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': True, 'free_pvs': False, 'directory_name': None, 'directory_list': None,
      'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: virtual_optical_media")]

test_data1 = [
    # ALL vios install testdata
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
      'virtual_optical_media': False, 'free_pvs': False, 'directory_name': None, 'directory_list': None,
      'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: settings"),
    # unsupported parameter virtual_optical_media
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'action': 'install', 'state': None,
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': '1.1.1.1',
      'nim_gateway': 'ab', 'vios_IP': 'bc', 'nim_subnetmask': 'cd', 'prof_name': 'ef',
      'location_code': 'fg', 'nim_vlan_id': 'dh', 'nim_vlan_priority': 'hi', 'timeout': 'ij',
      'virtual_optical_media': True, 'free_pvs': False, 'directory_name': None, 'directory_list': None,
      'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: virtual_optical_media"),
    # unsupported parameter free_pvs
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'action': 'install', 'state': None,
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': '1.1.1.1',
      'nim_gateway': 'ab', 'vios_IP': 'bc', 'nim_subnetmask': 'cd', 'prof_name': 'ef',
      'location_code': 'fg', 'nim_vlan_id': 'dh', 'nim_vlan_priority': 'hi', 'timeout': 'ij',
      'virtual_optical_media': False, 'free_pvs': True, 'directory_name': None, 'directory_list': None,
      'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: free_pvs")]

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
      'virtual_optical_media': False, 'free_pvs': False, 'directory_name': None, 'directory_list': None,
      'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: nim_IP"),
    # unsupported parameter nim_gateway
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': '1.1.1.1', 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False, 'directory_name': None, 'directory_list': None,
      'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: nim_gateway"),
    # unsupported parameter nim_viosIP
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': '1.1.1.1', 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False, 'directory_name': None, 'directory_list': None,
      'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: vios_IP"),
    # unsupported parameter nim_subnetmask
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': '255.255.256.254', 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False, 'directory_name': None, 'directory_list': None,
      'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: nim_subnetmask"),
    # unsupported parameter prof_name
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': 'pfnam',
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False, 'directory_name': None, 'directory_list': None,
      'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: prof_name"),
    # unsupported parameter location_code
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': 'abc:xyz:123', 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False, 'directory_name': None, 'directory_list': None,
      'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: location_code"),
    # unsupported parameter nim_vlan_id
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': '2', 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False, 'directory_name': None, 'directory_list': None,
      'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: nim_vlan_id"),
    # unsupported parameter nim_vlan_priority
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': '2', 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False, 'directory_name': None, 'directory_list': None,
      'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: nim_vlan_priority"),
    # unsupported parameter timeout
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': 50,
      'virtual_optical_media': False, 'free_pvs': False, 'directory_name': None, 'directory_list': None,
      'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: timeout"),
    # unsupported parameter settings
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': 'facts',
      'system_name': 'sysName', 'name': 'viosName', 'settings': "sett", 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None,
      'virtual_optical_media': False, 'free_pvs': False, 'directory_name': None, 'directory_list': None,
      'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
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
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None, 'virtual_optical_media': False, 'free_pvs': False,
      'directory_name': None, 'directory_list': None, 'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: nim_IP"),
    # unsupported parameter nim_gateway
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': None, 'action': 'accept_license',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': '1.1.1.1', 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None, 'virtual_optical_media': False, 'free_pvs': False,
      'directory_name': None, 'directory_list': None, 'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: nim_gateway"),
    # unsupported parameter nim_viosIP
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': None, 'action': 'accept_license',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': '1.1.1.1', 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None, 'virtual_optical_media': False, 'free_pvs': False,
      'directory_name': None, 'directory_list': None, 'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: vios_IP"),
    # unsupported parameter nim_subnetmask
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': None, 'action': 'accept_license',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': '255.255.256.254', 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None, 'virtual_optical_media': False, 'free_pvs': False,
      'directory_name': None, 'directory_list': None, 'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: nim_subnetmask"),
    # unsupported parameter prof_name
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': None, 'action': 'accept_license',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': 'pfnam',
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None, 'virtual_optical_media': False, 'free_pvs': False,
      'directory_name': None, 'directory_list': None, 'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: prof_name"),
    # unsupported parameter location_code
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': None, 'action': 'accept_license',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': 'abc:xyz:123', 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None, 'virtual_optical_media': False, 'free_pvs': False,
      'directory_name': None, 'directory_list': None, 'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: location_code"),
    # unsupported parameter nim_vlan_id
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': None, 'action': 'accept_license',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': '2', 'nim_vlan_priority': None, 'timeout': None, 'virtual_optical_media': False, 'free_pvs': False,
      'directory_name': None, 'directory_list': None, 'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: nim_vlan_id"),
    # unsupported parameter nim_vlan_priority
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': None, 'action': 'accept_license',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': '2', 'timeout': None, 'virtual_optical_media': False, 'free_pvs': False,
      'directory_name': None, 'directory_list': None, 'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: nim_vlan_priority"),
    # unsupported parameter timeout
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': None, 'action': 'accept_license',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': 50, 'virtual_optical_media': False, 'free_pvs': False,
      'directory_name': None, 'directory_list': None, 'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: timeout"),
    # unsupported parameter settings
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': None, 'action': 'accept_license',
      'system_name': 'sysName', 'name': 'viosName', 'settings': "sett", 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None, 'virtual_optical_media': False, 'free_pvs': False,
      'directory_name': None, 'directory_list': None, 'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: settings"),
    # unsupported parameter virtual_optical_media
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': None, 'action': 'accept_license',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None, 'virtual_optical_media': True, 'free_pvs': False,
      'directory_name': None, 'directory_list': None, 'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: virtual_optical_media"),
    # unsupported parameter free_pvs
    ({'hmc_host': '0.0.0.0', 'hmc_auth': hmc_auth, 'state': None, 'action': 'accept_license',
      'system_name': 'sysName', 'name': 'viosName', 'settings': None, 'nim_IP': None,
      'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None,
      'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None, 'virtual_optical_media': False, 'free_pvs': True,
      'directory_name': None, 'directory_list': None, 'sftp_auth': None, 'remote_server': None, 'files': None, 'mount_location': None,
      'ssh_key_file': None, 'remote_directory': None, 'options': None, 'media': None},
     "ParameterError: unsupported parameter: free_pvs")]

test_data4 = [
    # ALL Copy Vios Image via SFTP and NFS testdata
    # media param is missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': None, 'action': 'copy',
      'media': None, 'directory_name': 'test', 'remote_server': "0.0.0.0", 'sftp_auth': sftp_auth, 'files': ['flash.iso']},
     "ParameterError: mandatory parameter 'media' is missing"),
    # hmc_host param is missing
    ({'hmc_host': None, 'hmc_auth': hmc_auth, 'state': None, 'action': 'copy',
      'media': 'sftp', 'directory_name': 'test', 'remote_server': "0.0.0.0", 'sftp_auth': sftp_auth, 'files': ['flash.iso']},
     "ParameterError: mandatory parameter 'hmc_host' is missing"),
    # directory_name param is missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': None, 'action': 'copy',
      'media': 'sftp', 'directory_name': None, 'remote_server': "0.0.0.0", 'sftp_auth': sftp_auth, 'files': ['flash.iso']},
     "ParameterError: mandatory parameter 'directory_name' is missing"),
    # files param is missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': None, 'action': 'copy',
      'media': 'sftp', 'directory_name': 'test', 'remote_server': "0.0.0.0", 'sftp_auth': sftp_auth, 'files': None},
     "ParameterError: mandatory parameter 'files' is missing"),
    # remote_server param is missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': None, 'action': 'copy',
      'media': 'sftp', 'directory_name': 'test', 'remote_server': None, 'sftp_auth': sftp_auth, 'files': ['flash.iso']},
     "ParameterError: mandatory parameter 'remote_server' is missing"),
    # when media is 'sftp' sftp_auth is missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': None, 'action': 'copy',
      'media': 'sftp', 'directory_name': 'test', 'remote_server': "0.0.0.0", 'files': ['flash.iso']},
     "ParameterError: mandatory parameter 'sftp_auth' is missing"),
    # when media is 'nfs' and mount_location is missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': None, 'action': 'copy',
      'media': 'nfs', 'directory_name': 'test', 'remote_server': "0.0.0.0", 'mount_location': None, 'files': ['flash.iso']},
     "ParameterError: mandatory parameter 'mount_location' is missing"),
    # when media is 'sftp' and unsupported param mount_location
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': None, 'action': 'copy',
      'media': 'sftp', 'directory_name': 'test', 'remote_server': "0.0.0.0", 'sftp_auth': sftp_auth, 'mount_location': '/images', 'files': ['flash.iso'],
      'system_name': None, 'directory_list': None, 'name': None, 'options': None, 'nim_IP': None, 'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None,
      'prof_name': None, 'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None, 'settings': None, 'virtual_optical_media': None,
      "free_pvs": None},
     "ParameterError: unsupported parameter: mount_location"),
    # when media is 'nfs' and unsupported param sftp_auth
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': None, 'action': 'copy',
      'media': 'nfs', 'directory_name': 'test', 'remote_server': "0.0.0.0", 'sftp_auth': sftp_auth, 'mount_location': '/images', 'files': ['flash.iso'],
      'ssh_key_file': None, 'system_name': None, 'directory_list': None, 'name': None, 'options': None, 'nim_IP': None, 'nim_gateway': None, 'vios_IP': None,
      'nim_subnetmask': None, 'prof_name': None, 'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None, 'settings': None,
      'virtual_optical_media': None, "free_pvs": None},
     "ParameterError: unsupported parameter: sftp_auth"),
    # when media is 'sftp' and unsupported param options
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': None, 'action': 'copy',
      'media': 'sftp', 'directory_name': 'test', 'remote_server': "0.0.0.0", 'sftp_auth': sftp_auth, 'options': '"vers=4"', 'files': ['flash.iso'],
      'mount_location': None, 'system_name': None, 'directory_list': None, 'name': None, 'nim_IP': None, 'nim_gateway': None, 'vios_IP': None,
      'nim_subnetmask': None, 'prof_name': None, 'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None, 'settings': None,
      'virtual_optical_media': None, "free_pvs": None},
     "ParameterError: unsupported parameter: options"),
    # when media is 'nfs' and unsupported param ssh_key_file
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': None, 'action': 'copy',
      'media': 'nfs', 'directory_name': 'test', 'sftp_auth': None, 'mount_location': '/images', 'remote_server': "0.0.0.0",
      'ssh_key_file': '/home/hmcuser/keys/id_rsa', 'files': ['flash.iso'], 'system_name': None, 'directory_list': None, 'name': None, 'options': None,
      'nim_IP': None, 'nim_gateway': None, 'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None, 'location_code': None, 'nim_vlan_id': None,
      'nim_vlan_priority': None, 'timeout': None, 'settings': None, 'virtual_optical_media': None, "free_pvs": None},
     "ParameterError: unsupported parameter: ssh_key_file"),
    # unsupported param nim_IP
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': None, 'action': 'copy',
      'media': 'nfs', 'directory_name': 'test', 'sftp_auth': None, 'mount_location': '/images', 'remote_server': "0.0.0.0", 'ssh_key_file': None,
      'files': ['flash.iso'], 'system_name': None, 'directory_list': None, 'name': None, 'options': None, 'nim_IP': "9.9.2.2", 'nim_gateway': None,
      'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None, 'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None,
      'settings': None, 'virtual_optical_media': None, "free_pvs": None},
     "ParameterError: unsupported parameter: nim_IP"),
    # unsupported param nim_gateway
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': None, 'action': 'copy',
      'media': 'nfs', 'directory_name': 'test', 'sftp_auth': None, 'mount_location': '/images', 'remote_server': "0.0.0.0", 'ssh_key_file': None,
      'files': ['flash.iso'], 'system_name': None, 'directory_list': None, 'name': None, 'options': None, 'nim_IP': None, 'nim_gateway': "9.9.9.9",
      'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None, 'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None,
      'settings': None, 'virtual_optical_media': None, "free_pvs": None},
     "ParameterError: unsupported parameter: nim_gateway"),
    # unsupported param vios_IP
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': None, 'action': 'copy',
      'media': 'nfs', 'directory_name': 'test', 'sftp_auth': None, 'mount_location': '/images', 'remote_server': "0.0.0.0", 'ssh_key_file': None,
      'files': ['flash.iso'], 'system_name': None, 'directory_list': None, 'name': None, 'options': None, 'nim_IP': None, 'nim_gateway': None,
      'vios_IP': "0.0.0.0", 'nim_subnetmask': None, 'prof_name': None, 'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None,
      'timeout': None, 'settings': None, 'virtual_optical_media': None, "free_pvs": None},
     "ParameterError: unsupported parameter: vios_IP"),
    # unsupported param nim_subnetmask
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': None, 'action': 'copy',
      'media': 'nfs', 'directory_name': 'test', 'sftp_auth': None, 'mount_location': '/images', 'remote_server': "0.0.0.0", 'ssh_key_file': None,
      'files': ['flash.iso'], 'system_name': None, 'directory_list': None, 'name': None, 'options': None, 'nim_IP': None, 'nim_gateway': None,
      'vios_IP': None, 'nim_subnetmask': '8.8.8.8', 'prof_name': None, 'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None,
      'timeout': None, 'settings': None, 'virtual_optical_media': None, "free_pvs": None},
     "ParameterError: unsupported parameter: nim_subnetmask"),
    # unsupported param prof_name
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': None, 'action': 'copy',
      'media': 'nfs', 'directory_name': 'test', 'sftp_auth': None, 'mount_location': '/images', 'remote_server': "0.0.0.0", 'ssh_key_file': None,
      'files': ['flash.iso'], 'system_name': None, 'directory_list': None, 'name': None, 'options': None, 'nim_IP': None, 'nim_gateway': None,
      'vios_IP': None, 'nim_subnetmask': None, 'prof_name': 'prfname', 'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None,
      'timeout': None, 'settings': None, 'virtual_optical_media': None, "free_pvs": None},
     "ParameterError: unsupported parameter: prof_name"),
    # unsupported param location_code
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': None, 'action': 'copy',
      'media': 'nfs', 'directory_name': 'test', 'sftp_auth': None, 'mount_location': '/images', 'remote_server': "0.0.0.0", 'ssh_key_file': None,
      'files': ['flash.iso'], 'system_name': None, 'directory_list': None, 'name': None, 'options': None, 'nim_IP': None, 'nim_gateway': None,
      'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None, 'location_code': '121', 'nim_vlan_id': None, 'nim_vlan_priority': None,
      'timeout': None, 'settings': None, 'virtual_optical_media': None, "free_pvs": None},
     "ParameterError: unsupported parameter: location_code"),
    # unsupported param nim_vlan_id
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': None, 'action': 'copy',
      'media': 'nfs', 'directory_name': 'test', 'sftp_auth': None, 'mount_location': '/images', 'remote_server': "0.0.0.0", 'ssh_key_file': None,
      'files': ['flash.iso'], 'system_name': None, 'directory_list': None, 'name': None, 'options': None, 'nim_IP': None, 'nim_gateway': None,
      'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None, 'location_code': None, 'nim_vlan_id': 1, 'nim_vlan_priority': None, 'timeout': None,
      'settings': None, 'virtual_optical_media': None, "free_pvs": None},
     "ParameterError: unsupported parameter: nim_vlan_id"),
    # unsupported param nim_vlan_priority
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': None, 'action': 'copy',
      'media': 'nfs', 'directory_name': 'test', 'sftp_auth': None, 'mount_location': '/images', 'remote_server': "0.0.0.0", 'ssh_key_file': None,
      'files': ['flash.iso'], 'system_name': None, 'directory_list': None, 'name': None, 'options': None, 'nim_IP': None, 'nim_gateway': None,
      'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None, 'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': 1, 'timeout': None,
      'settings': None, 'virtual_optical_media': None, "free_pvs": None},
     "ParameterError: unsupported parameter: nim_vlan_priority"),
    # unsupported param timeout
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': None, 'action': 'copy',
      'media': 'nfs', 'directory_name': 'test', 'sftp_auth': None, 'mount_location': '/images', 'remote_server': "0.0.0.0", 'ssh_key_file': None,
      'files': ['flash.iso'], 'system_name': None, 'directory_list': None, 'name': None, 'options': None, 'nim_IP': None, 'nim_gateway': None,
      'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None, 'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': 20,
      'settings': None, 'virtual_optical_media': None, "free_pvs": None},
     "ParameterError: unsupported parameter: timeout"),
    # unsupported param settings
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': None, 'action': 'copy',
      'media': 'nfs', 'directory_name': 'test', 'sftp_auth': None, 'mount_location': '/images', 'remote_server': "0.0.0.0", 'ssh_key_file': None,
      'files': ['flash.iso'], 'system_name': None, 'directory_list': None, 'name': None, 'options': None, 'nim_IP': None, 'nim_gateway': None,
      'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None, 'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None, 'timeout': None,
      'settings': 'settings', 'virtual_optical_media': None, "free_pvs": None},
     "ParameterError: unsupported parameter: settings"),
    # unsupported param virtual_optical_media
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': None, 'action': 'copy',
      'media': 'nfs', 'directory_name': 'test', 'sftp_auth': None, 'mount_location': '/images', 'remote_server': "0.0.0.0", 'ssh_key_file': None,
      'files': ['flash.iso'], 'system_name': None, 'directory_list': None, 'name': None, 'options': None, 'nim_IP': None, 'nim_gateway': None,
      'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None, 'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None,
      'timeout': None, 'settings': None, 'virtual_optical_media': True, "free_pvs": None},
     "ParameterError: unsupported parameter: virtual_optical_media"),
    # unsupported param free_pvs
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'state': None, 'action': 'copy',
      'media': 'nfs', 'directory_name': 'test', 'sftp_auth': None, 'mount_location': '/images', 'remote_server': "0.0.0.0", 'ssh_key_file': None,
      'files': ['flash.iso'], 'system_name': None, 'directory_list': None, 'name': None, 'options': None, 'nim_IP': None, 'nim_gateway': None,
      'vios_IP': None, 'nim_subnetmask': None, 'prof_name': None, 'location_code': None, 'nim_vlan_id': None, 'nim_vlan_priority': None,
      'timeout': None, 'settings': None, 'virtual_optical_media': None, "free_pvs": True},
     "ParameterError: unsupported parameter: free_pvs"),
]

test_data5 = [
    # All List Vios Image testdata
    #  hmc_host param missing
    ({'hmc_host': None, 'hmc_auth': hmc_auth, 'state': None, 'action': 'listimages'},
     "ParameterError: mandatory parameter 'hmc_host' is missing"),
]

test_data6 = [
    # All Delete Vios Image testdata
    #  hmc_host param missing
    ({'hmc_host': None, 'hmc_auth': hmc_auth, 'directory_list': ['test'], 'state': None, 'action': 'delete'},
     "ParameterError: mandatory parameter 'hmc_host' is missing"),
    # directory_list param missing
    ({'hmc_host': "0.0.0.0", 'hmc_auth': hmc_auth, 'directory_list': None, 'state': None, 'action': 'delete'},
     "ParameterError: mandatory parameter 'directory_list' is missing"),
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
            hmc_vios.installVios(hmc_vios, vios_test_input)
        assert expectedError == repr(e.value)
    else:
        hmc_vios.installVios(hmc_vios, vios_test_input)


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
def test_call_inside_copy_vios_image(mocker, vios_test_input, expectedError):
    hmc_vios = common_mock_setup(mocker)
    if 'ParameterError' in expectedError:
        with pytest.raises(ParameterError) as e:
            hmc_vios.copy_vios_image(hmc_vios, vios_test_input)
        assert expectedError == repr(e.value)
    else:
        hmc_vios.copy_vios_image(hmc_vios, vios_test_input)


@pytest.mark.parametrize("vios_test_input, expectedError", test_data5)
def test_call_inside_listimages(mocker, vios_test_input, expectedError):
    hmc_vios = common_mock_setup(mocker)
    if 'ParameterError' in expectedError:
        with pytest.raises(ParameterError) as e:
            hmc_vios.list_all_vios_image(hmc_vios, vios_test_input)
        assert expectedError == repr(e.value)
    else:
        hmc_vios.list_all_vios_image(hmc_vios, vios_test_input)


@pytest.mark.parametrize("vios_test_input, expectedError", test_data6)
def test_call_inside_deleteimages(mocker, vios_test_input, expectedError):
    hmc_vios = common_mock_setup(mocker)
    if 'ParameterError' in expectedError:
        with pytest.raises(ParameterError) as e:
            hmc_vios.delete_vios_image(hmc_vios, vios_test_input)
        assert expectedError == repr(e.value)
    else:
        hmc_vios.delete_vios_image(hmc_vios, vios_test_input)
