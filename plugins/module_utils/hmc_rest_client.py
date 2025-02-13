from __future__ import absolute_import, division, print_function
__metaclass__ = type
import time
import json
from ansible.module_utils.urls import open_url
import ansible.module_utils.six.moves.urllib.error as urllib_error
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_exceptions import HmcError
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_exceptions import Error
from ansible_collections.ibm.power_hmc.plugins.module_utils.hmc_exceptions import ParameterError
import re
import xml.etree.ElementTree as ET
NEED_LXML = False
try:
    from lxml import etree, objectify
except ImportError:
    NEED_LXML = True

import logging
LOG_FILENAME = "/tmp/ansible_power_hmc.log"
logger = logging.getLogger(__name__)

PCM_TEMPLATE_NS = 'ManagedSystemPcmPreference xmlns:ManagedSystemPcmPreference="http://www.ibm.com/xmlns/systems/power/\
firmware/pcm/mc/2012_10/" xmlns="http://www.ibm.com/xmlns/systems/power/firmware/pcm/\
mc/2012_10/" xmlns:ns2="http://www.w3.org/XML/1998/namespace/k2"'
LPAR_TEMPLATE_NS = 'PartitionTemplate xmlns="http://www.ibm.com/xmlns/systems/power/\
firmware/templates/mc/2012_10/" xmlns:ns2="http://www.w3.org/XML/1998/namespace/k2"'
LPAR_NS = 'LogicalPartition xmlns:LogicalPartition="http://www.ibm.com/xmlns/\
systems/power/firmware/uom/mc/2012_10/" xmlns="http://www.ibm.com/xmlns/systems/power\
/firmware/uom/mc/2012_10/" xmlns:ns2="http://www.w3.org/XML/1998/namespace/k2"'
VIOS_NS = 'VirtualIOServer xmlns:VirtualIOServer="http://www.ibm.com/xmlns/\
systems/power/firmware/uom/mc/2012_10/" xmlns="http://www.ibm.com/xmlns/systems/power\
/firmware/uom/mc/2012_10/" xmlns:ns2="http://www.w3.org/XML/1998/namespace/k2"'


def xml_strip_namespace(xml_str):
    parser = etree.XMLParser(recover=True, encoding='utf-8')
    root = etree.fromstring(xml_str, parser)
    for elem in root.getiterator():
        if not hasattr(elem.tag, 'find'):
            continue
        i = elem.tag.find('}')
        if i >= 0:
            elem.tag = elem.tag[i + 1:]

    objectify.deannotate(root, cleanup_namespaces=True)
    return root


def parse_error_response(error):
    if isinstance(error, urllib_error.HTTPError):
        xml_str = error.read().decode()
        if not xml_str:
            logger.debug(error.url)
            error_msg = "HTTP Error {0}: {1}".format(error.code, error.reason)
        else:
            dom = xml_strip_namespace(xml_str)
            error_msg_l = dom.xpath("//Message")
            if error_msg_l:
                error_msg = error_msg_l[0].text
                if "Failed to unmarshal input payload" in error_msg:
                    error_msg = "Current HMC version might not support some of input settings or invalid input"
            else:
                error_msg = "Unknown http error"
    else:
        error_msg = repr(error)
    logger.debug(error_msg)
    return error_msg


def _logonPayload(user, password):
    root = ET.Element("LogonRequest")
    root.attrib = {"schemaVersion": "V1_0",
                   "xmlns": "http://www.ibm.com/xmlns/systems/power/firmware/web/mc/2012_10/",
                   "xmlns:mc": "http://www.ibm.com/xmlns/systems/power/firmware/web/mc/2012_10/"}

    ET.SubElement(root, "UserID").text = user
    ET.SubElement(root, "Password").text = password
    return ET.tostring(root)


def _jobHeader(session):

    header = {'Content-Type': 'application/vnd.ibm.powervm.web+xml; type=JobRequest',
              'Accept': 'application/atom+xml',
              'Authorization': 'Basic Og=='}
    header['X-API-Session'] = session

    return header


def _kxe_kb_schema(kxe=None, kb=None, schema=None):
    attrib = {}
    if kxe:
        attrib.update({"kxe": kxe})
    if kb:
        attrib.update({"kb": kb})
    if schema:
        attrib.update({"schemaVersion": schema})

    return attrib


def _job_parameter(parameter, parameterVal, schemaVersion="V1_0"):

    metaData = ET.Element("Metadata")
    metaData.insert(1, ET.Element("Atom"))

    jobParameter = ET.Element("JobParameter")
    jobParameter.attrib = _kxe_kb_schema(schema=schemaVersion)
    jobParameter.insert(1, metaData)
    parameterName = ET.Element("ParameterName")
    parameterName.attrib = _kxe_kb_schema("false", "ROR")
    parameterName.text = parameter
    parameterValue = ET.Element("ParameterValue")
    parameterValue.attrib = _kxe_kb_schema("false", "CUR")
    parameterValue.text = parameterVal
    jobParameter.insert(2, parameterName)
    jobParameter.insert(3, parameterValue)

    return jobParameter


def _job_RequestPayload(reqdOperation, jobParams, schemaVersion="V1_0"):
    root = ET.Element("JobRequest")
    root.attrib = {"xmlns:JobRequest": "http://www.ibm.com/xmlns/systems/power/firmware/web/mc/2012_10/",
                   "xmlns": "http://www.ibm.com/xmlns/systems/power/firmware/web/mc/2012_10/",
                   "xmlns:ns2": "http://www.w3.org/XML/1998/namespace/k2",
                   "schemaVersion": schemaVersion
                   }

    metaData = ET.Element("Metadata")
    metaData.insert(1, ET.Element("Atom"))
    root.insert(1, metaData)

    requestedOperation = ET.Element("RequestedOperation")
    requestedOperation.attrib = _kxe_kb_schema("false", "CUR", schemaVersion)
    requestedOperation.insert(1, metaData)

    index = 2
    requestedOperationTags = ['OperationName', 'GroupName', 'ProgressType']
    for each in requestedOperationTags:
        operationName = ET.Element(each)
        operationName.attrib = _kxe_kb_schema("false", "ROR")
        operationName.text = reqdOperation[each]
        requestedOperation.insert(index, operationName)
        index = index + 1

    jobParameters = ET.Element("JobParameters")
    jobParameters.attrib = _kxe_kb_schema("false", "CUR", schemaVersion)
    jobParameters.insert(1, metaData)

    index = 2
    for each in jobParams:
        jobParameters.insert(index, _job_parameter(each, jobParams[each]))
        index = index + 1

    root.insert(2, requestedOperation)
    root.insert(3, jobParameters)

    return ET.tostring(root)


def add_taggedIO_details(lpar_template_dom):
    taggedIO_payload = '''<iBMiPartitionTaggedIO kxe="false" kb="CUD" schemaVersion="V1_0">
                <Metadata>
                    <Atom/>
                </Metadata>
                <console kxe="false" kb="CUD">HMC</console>
                <operationsConsole kxe="false" kb="CUD">NONE</operationsConsole>
                <loadSource kb="CUD" kxe="false">NONE</loadSource>
                <alternateLoadSource kxe="false" kb="CUD">NONE</alternateLoadSource>
                <alternateConsole kxe="false" kb="CUD">NONE</alternateConsole>
            </iBMiPartitionTaggedIO>'''

    ioConfigurationTag = lpar_template_dom.xpath("//ioConfiguration/isUseCapturedPhysicalIOInformationEnabled")[0]
    ioConfigurationTag.addnext(etree.XML(taggedIO_payload))


def lookup_physical_io(rest_conn, server_dom, drcname):
    physical_io_list = server_dom.xpath("//AssociatedSystemIOConfiguration/IOSlots/IOSlot")
    drcname_occurences = server_dom.xpath("//AssociatedSystemIOConfiguration/IOSlots/"
                                          + "IOSlot/RelatedIOAdapter/IOAdapter/"
                                          + "DynamicReconfigurationConnectorName[contains(text(),'" + drcname + "')]")
    if len(drcname_occurences) > 1:
        occurence = 0
        for each in drcname_occurences:
            # End Charater matching, handles the case where P1-C1 and P1-C12 should not be considered same
            if each.text.endswith(drcname):
                logger.debug("End Charaters matching")
                occurence += 1
                drcname = each.text

        if occurence > 1:
            raise Error("Given location code matching with adapters from multiple drawer")
        elif occurence == 0:
            return None
    elif len(drcname_occurences) == 1:
        drcname = drcname_occurences[0].text

    for each in physical_io_list:
        each_eletree = etree.ElementTree(each)
        if drcname == each_eletree.xpath("//RelatedIOAdapter/IOAdapter/DynamicReconfigurationConnectorName")[0].text:
            return each_eletree

    return None


def add_physical_io(rest_conn, server_dom, lpar_template_dom, drcnames):
    profileioslot_payload = ''
    for drcname in drcnames:
        # find the physical io adpater details from managed system dom
        io_adapter_dom = lookup_physical_io(rest_conn, server_dom, drcname)
        if not io_adapter_dom:
            raise Error("Not able to find the matching IO Adapter on the Server")

        drc_index = io_adapter_dom.xpath("//IOAdapter/AdapterID")[0].text
        location_code = io_adapter_dom.xpath("//IOAdapter/DynamicReconfigurationConnectorName")[0].text
        logger.debug("Location_code %s", location_code)

        profileioslot_payload += '''<ProfileIOSlot schemaVersion="V1_0">
                        <Metadata>
                            <Atom/>
                        </Metadata>
                        <drcIndex kxe="false" kb="CUD">{0}</drcIndex>
                        <locationCode kb="CUD" kxe="false">{1}</locationCode>
                    </ProfileIOSlot>'''.format(drc_index, location_code)

    profileioslots_payload = '''<profileIOSlots kxe="false" kb="CUD" schemaVersion="V1_0">
                    <Metadata>
                        <Atom/>
                    </Metadata>
                    {0}
                  </profileIOSlots>'''.format(profileioslot_payload)
    ioConfigurationTag = lpar_template_dom.xpath("//ioConfiguration/Metadata")[0]
    ioConfigurationTag.addnext(etree.XML(profileioslots_payload))


class HmcRestClient:

    def __init__(self, hmc_ip, username, password):
        if NEED_LXML:
            raise Error("Missing prerequisite lxml package. Hint pip install lxml")
        self.hmc_ip = hmc_ip
        self.username = username
        self.password = password

        self.session = self.logon()
        logger.debug(self.session)

    def logon(self):
        header = {'Content-Type': 'application/vnd.ibm.powervm.web+xml; type=LogonRequest'}

        url = "https://{0}/rest/api/web/Logon".format(self.hmc_ip)

        resp = open_url(url,
                        headers=header,
                        method='PUT',
                        data=_logonPayload(self.username, self.password),
                        validate_certs=False,
                        force_basic_auth=True,
                        timeout=300)
        logger.debug(resp.code)

        response = resp.read()
        doc = xml_strip_namespace(response)
        session = doc.xpath('X-API-Session')[0].text
        return session

    def logoff(self):
        header = {'Content-Type': 'application/vnd.ibm.powervm.web+xml; type=LogonRequest',
                  'Authorization': 'Basic Og==',
                  'X-API-Session': self.session}
        url = "https://{0}/rest/api/web/Logon".format(self.hmc_ip)

        open_url(url,
                 headers=header,
                 method='DELETE',
                 validate_certs=False,
                 force_basic_auth=True,
                 timeout=300)

    def fetchJobStatus(self, jobId, template=False, timeout_in_min=30):

        if template:
            url = "https://{0}/rest/api/templates/jobs/{1}".format(self.hmc_ip, jobId)
        else:
            url = "https://{0}/rest/api/uom/jobs/{1}".format(self.hmc_ip, jobId)

        header = {'X-API-Session': self.session, 'Accept': "application/atom+xml"}
        result = None

        jobStatus = ''
        timeout_counter = 0
        while True:
            time.sleep(30)
            timeout_counter += 1
            resp = open_url(url,
                            headers=header,
                            method='GET',
                            validate_certs=False,
                            force_basic_auth=True,
                            timeout=300).read()
            doc = xml_strip_namespace(resp)

            jobStatus = doc.xpath('//Status')[0].text
            logger.debug("jobStatus: %s", jobStatus)

            if jobStatus == 'COMPLETED_OK':
                logger.debug(resp)
                result = doc
                break

            if jobStatus == 'COMPLETED_WITH_ERROR':
                logger.debug("jobStatus: %s", jobStatus)
                resp_msg = None
                resp_msg = doc.xpath("//ParameterName[text()='result']/following-sibling::ParameterValue")
                if resp_msg:
                    logger.debug("debugger: %s", resp_msg[0].text)
                    raise HmcError(resp_msg[0].text.strip('\n'))
                else:
                    err_msg = "Failed: Job completed with error"
                    raise HmcError(err_msg)

            if jobStatus != 'RUNNING':
                logger.debug("jobStatus: %s", jobStatus)
                err_msg_l = doc.xpath("//ResponseException//Message")
                err_msg_l = doc.xpath("//ParameterName[text()='ExceptionText']/following-sibling::ParameterValue") if not err_msg_l else err_msg_l
                if not err_msg_l:
                    err_msg = 'Job failed.'
                else:
                    err_msg = err_msg_l[0].text
                raise HmcError(err_msg)

            if timeout_counter == timeout_in_min * 2:
                job_name = doc.xpath("//OperationName")[0].text.strip()
                logger.debug("%s job stuck in %s state. Timed out!!", job_name, jobStatus)
                raise HmcError("Job: {0} timed out!!".format(job_name))

        return result

    def getManagedSystem(self, system_name):
        url = "https://{0}/rest/api/uom/ManagedSystem/search/(SystemName=='{1}')".format(self.hmc_ip, system_name)
        header = {'X-API-Session': self.session,
                  'Accept': 'application/vnd.ibm.powervm.uom+xml; type=ManagedSystem'}
        response = open_url(url,
                            headers=header,
                            method='GET',
                            validate_certs=False,
                            force_basic_auth=True,
                            timeout=300)
        if response.code == 204:
            return None, None

        managedsystem_root = xml_strip_namespace(response.read())

        uuid = managedsystem_root.xpath("//AtomID")[0].text
        return uuid, managedsystem_root.xpath("//ManagedSystem")[0]

    def getManagedSystems(self):
        url = "https://{0}/rest/api/uom/ManagedSystem".format(self.hmc_ip)
        header = {'X-API-Session': self.session,
                  'Accept': 'application/vnd.ibm.powervm.uom+xml; type=ManagedSystem'}

        response = open_url(url,
                            headers=header,
                            method='GET',
                            validate_certs=False,
                            force_basic_auth=True,
                            timeout=3600)

        if response.code == 204:
            return None, None

        managedsystems_root = xml_strip_namespace(response.read())
        return managedsystems_root

    def getManagedSystemsQuick(self):
        url = "https://{0}/rest/api/uom/ManagedSystem/quick/All".format(self.hmc_ip)
        header = {'X-API-Session': self.session,
                  'Accept': '*/*'}
        resp = open_url(url,
                        headers=header,
                        method='GET',
                        validate_certs=False,
                        force_basic_auth=True,
                        timeout=300)
        if resp.code != 200:
            logger.debug("Get of Managed Systems failed. Respsonse code: %d", resp.code)
            return None
        response = resp.read()
        return response

    def getManagedSystemQuick(self, system_uuid):
        url = "https://{0}/rest/api/uom/ManagedSystem/{1}/quick".format(self.hmc_ip, system_uuid)
        header = {'X-API-Session': self.session,
                  'Accept': '*/*'}
        resp = open_url(url,
                        headers=header,
                        method='GET',
                        validate_certs=False,
                        force_basic_auth=True,
                        timeout=300)
        if resp.code != 200:
            logger.debug("Get of Logical Partition failed. Respsonse code: %d", resp.code)
            return None
        response = resp.read()
        return response

    def getLogicalPartition(self, system_uuid, partition_name=None, partition_uuid=None):
        lpar_uuid = None
        if partition_uuid is None:
            lpar_quick_list = []
            lpar_response = self.getLogicalPartitionsQuick(system_uuid)
            if lpar_response:
                lpar_quick_list = json.loads(lpar_response)

            if lpar_quick_list:
                for eachLpar in lpar_quick_list:
                    if eachLpar['PartitionName'] == partition_name:
                        lpar_uuid = eachLpar['UUID']
                        break

            if not lpar_uuid:
                return None, None
        else:
            lpar_uuid = partition_uuid

        url = "https://{0}/rest/api/uom/LogicalPartition/{1}".format(self.hmc_ip, lpar_uuid)
        header = {'X-API-Session': self.session,
                  'Accept': 'application/vnd.ibm.powervm.uom+xml; type=LogicalPartition'}

        resp = open_url(url,
                        headers=header,
                        method='GET',
                        validate_certs=False,
                        force_basic_auth=True,
                        timeout=300)
        if resp.code != 200:
            logger.debug("Get of Logical Partition failed. Respsonse code: %d", resp.code)
            return None, None

        response = resp.read()
        partition_dom = xml_strip_namespace(response)
        if partition_dom:
            return lpar_uuid, partition_dom

        return None, None

    def getLogicalPartitions(self, system_uuid):
        url = "https://{0}/rest/api/uom/ManagedSystem/{1}/LogicalPartition?group=Advanced".format(self.hmc_ip, system_uuid)
        header = {'X-API-Session': self.session,
                  'Accept': 'application/vnd.ibm.powervm.uom+xml; type=LogicalPartition'}
        resp = open_url(url,
                        headers=header,
                        method='GET',
                        validate_certs=False,
                        force_basic_auth=True,
                        timeout=3600)
        if resp.code != 200:
            logger.debug("Get of Logical Partitions failed. Respsonse code: %d", resp.code)
            return None
        response = resp.read()
        return response

    def getLogicalPartitionsQuick(self, system_uuid):
        url = "https://{0}/rest/api/uom/ManagedSystem/{1}/LogicalPartition/quick/All".format(self.hmc_ip, system_uuid)
        header = {'X-API-Session': self.session,
                  'Accept': '*/*'}
        resp = open_url(url,
                        headers=header,
                        method='GET',
                        validate_certs=False,
                        force_basic_auth=True,
                        timeout=300)
        if resp.code != 200:
            logger.debug("Get of Logical Partitions failed. Respsonse code: %d", resp.code)
            return None
        response = resp.read()
        return response

    def getLogicalPartitionQuick(self, partition_uuid):
        url = "https://{0}/rest/api/uom/LogicalPartition/{1}/quick".format(self.hmc_ip, partition_uuid)
        header = {'X-API-Session': self.session,
                  'Accept': '*/*'}
        resp = open_url(url,
                        headers=header,
                        method='GET',
                        validate_certs=False,
                        force_basic_auth=True,
                        timeout=300)
        if resp.code != 200:
            logger.debug("Get of Logical Partition failed. Respsonse code: %d", resp.code)
            return None
        response = resp.read()
        return response

    def getSystemPCMpreferences(self, system_uuid):
        url = "https://{0}/rest/api/pcm/ManagedSystem/{1}/preferences".format(self.hmc_ip, system_uuid)
        header = {'X-API-Session': self.session,
                  'Content-Type': 'application/xml'}
        resp = open_url(url,
                        headers=header,
                        method='GET',
                        validate_certs=False,
                        force_basic_auth=True,
                        timeout=3600)
        if resp.code != 200:
            logger.debug("Get of preferences failed. Respsonse code: %d", resp.code)
            return None
        response = resp.read()
        return response

    def getPCM(self, system_uuid, action):
        preference_map = {'LTM': 'LongTermMonitorEnabled', 'STM': 'ShortTermMonitorEnabled',
                          'AM': 'AggregationEnabled', 'CLTM': 'ComputeLTMEnabled', 'EM': 'EnergyMonitorEnabled'}
        url = "https://{0}/rest/api/pcm/ManagedSystem/{1}/preferences".format(self.hmc_ip, system_uuid)
        header = {'X-API-Session': self.session,
                  'Content-Type': 'application/xml'}
        resp = open_url(url,
                        headers=header,
                        method='GET',
                        validate_certs=False,
                        force_basic_auth=True,
                        timeout=3600)
        if resp.code != 200:
            logger.debug("Get of preferences failed. Respsonse code: %d", resp.code)
            return None
        response = resp.read()
        if action is not None:
            doc = xml_strip_namespace(response)
            path = doc.xpath("//ManagedSystemPcmPreference")[0]
            output = dict()
            for item in preference_map:
                if (path.xpath(preference_map[item])[0].text == "true"):
                    value = "Enabled"
                else:
                    value = "Disabled"
                output[preference_map[item]] = value
            return output
        return response

    def updatePCM(self, system_uuid, metrics, disable):
        logon_res = self.logon()
        url = "https://{0}/rest/api/pcm/ManagedSystem/{1}/preferences".format(self.hmc_ip, system_uuid)
        header = {'Content-Type': 'application/xml',
                  'X-API-Session': logon_res}
        sys_details = self.getPCM(system_uuid, None)
        doc = xml_strip_namespace(sys_details)
        preference_map = {'LTM': 'LongTermMonitorEnabled', 'STM': 'ShortTermMonitorEnabled',
                          'AM': 'AggregationEnabled', 'CLTM': 'ComputeLTMEnabled', 'EM': 'EnergyMonitorEnabled'}
        existing_enabled = []
        existing_disabled = []
        flag = False
        path = doc.xpath("//ManagedSystemPcmPreference")[0]
        for item in preference_map:
            if path.xpath(preference_map[item])[0].text == "true":
                existing_enabled.append(item)
            elif path.xpath(preference_map[item])[0].text == "false":
                existing_disabled.append(item)
        if disable == 'true':
            # LTM and CM is dependent on AM"
            if ("LTM" in metrics or "EM" in metrics) and "AM" not in metrics:
                metrics.append("AM")
            preference = list(set(metrics) | set(existing_disabled))
            if (set(existing_disabled) != set(preference) and (set(preference).issubset(set(existing_disabled)) is False)):
                flag = True
                for item in preference:
                    path.xpath(preference_map[item])[0].text = "false"
        else:
            if "AM" in metrics and ("LTM" not in metrics or "EM" not in metrics):
                metrics.append("LTM")
                metrics.append("EM")
            preference = list(set(metrics) | set(existing_enabled))
            if (set(existing_enabled) != set(preference) and (set(preference).issubset(set(existing_enabled)) is False)):
                flag = True
                for item in preference:
                    path.xpath(preference_map[item])[0].text = "true"
        if flag is True:
            payload_content = etree.tostring(path)
            payload_content = payload_content.decode("utf-8").replace("ManagedSystemPcmPreference", PCM_TEMPLATE_NS, 1)
            payload_content = payload_content.replace('\n', ' ').replace('\"', '\'')
            payload_content = etree.fromstring(payload_content)
            payload_content = etree.tostring(payload_content, encoding='unicode')
            logger.debug(payload_content)
            resp = open_url(url,
                            headers=header,
                            method='POST',
                            data=payload_content,
                            validate_certs=False,
                            force_basic_auth=True,
                            timeout=3600)
            if resp.code != 200:
                logger.debug("Get of preferences failed. Respsonse code: %d", resp.code)
                return None
            else:
                # response = resp.read()
                output = dict()
                for item in preference_map:
                    if (path.xpath(preference_map[item])[0].text == "true"):
                        value = "Enabled"
                    else:
                        value = "Disabled"
                    output[preference_map[item]] = value
                return output

    def getVirtualIOServers(self, system_uuid, group='Advanced'):
        url = "https://{0}/rest/api/uom/ManagedSystem/{1}/VirtualIOServer?group={2}".format(self.hmc_ip, system_uuid, group)
        header = {'X-API-Session': self.session,
                  'Accept': 'application/vnd.ibm.powervm.uom+xml; type=VirtualIOServer'}
        resp = open_url(url,
                        headers=header,
                        method='GET',
                        validate_certs=False,
                        force_basic_auth=True,
                        timeout=3600)
        if resp.code != 200:
            logger.debug("Get of Virtual IO Servers failed. Respsonse code: %d", resp.code)
            return None
        response = resp.read()
        return response

    def getVirtualIOServersQuick(self, system_uuid):
        url = "https://{0}/rest/api/uom/ManagedSystem/{1}/VirtualIOServer/quick/All".format(self.hmc_ip, system_uuid)
        header = {'X-API-Session': self.session,
                  'Accept': '*/*'}
        resp = open_url(url,
                        headers=header,
                        method='GET',
                        validate_certs=False,
                        force_basic_auth=True,
                        timeout=300)
        if resp.code != 200:
            logger.debug("Get of Virtual IO Servers failed. Respsonse code: %d", resp.code)
            return None
        response = resp.read()
        return response

    def getVirtualIOServer(self, vios_uuid, group=None):
        header = {'X-API-Session': self.session,
                  'Accept': 'application/vnd.ibm.powervm.uom+xml; type=VirtualIOServer'}

        if group:
            url = "https://{0}/rest/api/uom/VirtualIOServer/{1}?group={2}".format(self.hmc_ip, vios_uuid, group)
        else:
            url = "https://{0}/rest/api/uom/VirtualIOServer/{1}".format(self.hmc_ip, vios_uuid)

        resp = open_url(url,
                        headers=header,
                        method='GET',
                        validate_certs=False,
                        force_basic_auth=True,
                        timeout=3600)

        if resp.code != 200:
            logger.debug("Get of Virtual IO Server failed. Respsonse code: %d", resp.code)
            return None
        response = xml_strip_namespace(resp.read())
        return response

    def deleteLogicalPartition(self, partition_uuid):
        url = "https://{0}/rest/api/uom/LogicalPartition/{1}".format(self.hmc_ip, partition_uuid)
        header = {'X-API-Session': self.session,
                  'Accept': 'application/vnd.ibm.powervm.uom+xml; type=LogicalPartition'}

        open_url(url,
                 headers=header,
                 method='DELETE',
                 validate_certs=False,
                 force_basic_auth=True,
                 timeout=300)

    def updateLparNameAndIDToDom(self, template_xml, config_dict):
        if 'lpar_id' in config_dict:
            template_xml.xpath("//partitionId")[0].text = config_dict['lpar_id']
        else:
            lpar_id_tag = template_xml.xpath("//partitionId")[0]
            lpar_id_tag.getparent().remove(lpar_id_tag)
        template_xml.xpath("//currMaxVirtualIOSlots")[0].text = config_dict['max_virtual_slots']
        template_xml.xpath("//partitionName")[0].text = config_dict['vm_name']

    def updateProcMemSettingsToDom(self, template_xml, config_dict):
        shared_config_tag = None
        # shared processor configuration
        if config_dict['proc_unit']:
            shared_payload = '''<sharedProcessorConfiguration kxe="false" kb="CUD" schemaVersion="V1_0">
                <Metadata>
                    <Atom/>
                </Metadata>
                <sharedProcessorPoolId kxe="false" kb="CUD">{7}</sharedProcessorPoolId>
                <uncappedWeight kxe="false" kb="CUD">{0}</uncappedWeight>
                <minProcessingUnits kb="CUD" kxe="false">{1}</minProcessingUnits>
                <desiredProcessingUnits kxe="false" kb="CUD">{2}</desiredProcessingUnits>
                <maxProcessingUnits kb="CUD" kxe="false">{3}</maxProcessingUnits>
                <minVirtualProcessors kb="CUD" kxe="false">{4}</minVirtualProcessors>
                <desiredVirtualProcessors kxe="false" kb="CUD">{5}</desiredVirtualProcessors>
                <maxVirtualProcessors kxe="false" kb="CUD">{6}</maxVirtualProcessors>
                </sharedProcessorConfiguration>'''.format(config_dict['weight'], config_dict['min_proc_unit'],
                                                          config_dict['proc_unit'], config_dict['max_proc_unit'],
                                                          config_dict['min_proc'], config_dict['proc'],
                                                          config_dict['max_proc'], config_dict['shared_proc_pool'])

            shared_config_tag = template_xml.xpath("//sharedProcessorConfiguration")[0]
            if shared_config_tag:
                shared_config_tag.getparent().remove(shared_config_tag)
            sharingMode_tag = template_xml.xpath("//sharingMode")[0]
            sharingMode_tag.addnext(etree.XML(shared_payload))

            dedi_tag = template_xml.xpath("//dedicatedProcessorConfiguration")[0]
            if dedi_tag:
                dedi_tag.getparent().remove(dedi_tag)

            template_xml.xpath("//currHasDedicatedProcessors")[0].text = 'false'
            template_xml.xpath("//currSharingMode")[0].text = config_dict['proc_mode']
        else:
            template_xml.xpath("//minProcessors")[0].text = config_dict['min_proc']
            template_xml.xpath("//desiredProcessors")[0].text = config_dict['proc']
            template_xml.xpath("//maxProcessors")[0].text = config_dict['max_proc']

        template_xml.xpath("//currMinMemory")[0].text = config_dict['min_mem']
        template_xml.xpath("//currMemory")[0].text = config_dict['mem']
        template_xml.xpath("//currMaxMemory")[0].text = config_dict['max_mem']
        if config_dict['proc_comp_mode']:
            template_xml.xpath("//currProcessorCompatibilityMode")[0].text = config_dict['proc_comp_mode']

    def updatePartitionTemplate(self, uuid, template_xml):
        templateUrl = "https://{0}/rest/api/templates/PartitionTemplate/{1}".format(self.hmc_ip, uuid)
        header = {'X-API-Session': self.session,
                  'Content-Type': 'application/vnd.ibm.powervm.templates+xml;type=PartitionTemplate'}

        partiton_template_xmlstr = etree.tostring(template_xml)
        partiton_template_xmlstr = partiton_template_xmlstr.decode("utf-8").replace("PartitionTemplate", LPAR_TEMPLATE_NS, 1)
        logger.debug(partiton_template_xmlstr)

        resp = open_url(templateUrl,
                        headers=header,
                        data=partiton_template_xmlstr,
                        method='POST',
                        validate_certs=False,
                        force_basic_auth=True,
                        timeout=300).read()
        logger.debug(resp.decode("utf-8"))

    def quickGetPartition(self, lpar_uuid):
        header = {'X-API-Session': self.session}
        url = "https://{0}/rest/api/uom/LogicalPartition/{1}/quick".format(self.hmc_ip, lpar_uuid)
        resp = open_url(url,
                        headers=header,
                        method='GET',
                        validate_certs=False,
                        force_basic_auth=True,
                        timeout=300)

        lpar_quick_dom = resp.read()
        lpar_dict = json.loads(lpar_quick_dom)
        return lpar_dict

    def getPartitionTemplateUUID(self, name):
        header = {'X-API-Session': self.session}
        url = "https://{0}/rest/api/templates/PartitionTemplate?draft=false&detail=table".format(self.hmc_ip)

        resp = open_url(url,
                        headers=header,
                        method='GET',
                        validate_certs=False,
                        force_basic_auth=True,
                        timeout=300)
        if resp.code == 200:
            response = resp.read()
        else:
            return None

        root = xml_strip_namespace(response)
        element = root.xpath("//partitionTemplateName[text()='{0}']/preceding-sibling::Metadata//AtomID".format(name))
        uuid = element[0].text if element else None
        return uuid

    def getPartitionTemplate(self, uuid=None, name=None):
        logger.debug("Get partition template...")
        header = {'X-API-Session': self.session}

        if name:
            uuid = self.getPartitionTemplateUUID(name)

        if not uuid:
            return None

        templateUrl = "https://{0}/rest/api/templates/PartitionTemplate/{1}".format(self.hmc_ip, uuid)
        logger.debug(templateUrl)
        resp = open_url(templateUrl,
                        headers=header,
                        method='GET',
                        validate_certs=False,
                        force_basic_auth=True,
                        timeout=300)
        if resp.code == 200:
            response = resp.read()
        else:
            return None

        partiton_template_root = xml_strip_namespace(response)
        return partiton_template_root.xpath("//PartitionTemplate")[0]

    def copyPartitionTemplate(self, from_name, to_name):
        header = {'X-API-Session': self.session,
                  'Content-Type': 'application/vnd.ibm.powervm.templates+xml;type=PartitionTemplate'}

        partiton_template_doc = self.getPartitionTemplate(name=from_name)
        if not partiton_template_doc:
            raise HmcError("Not able to fetch the template")
        partiton_template_doc.xpath("//partitionTemplateName")[0].text = to_name
        templateNamespace = 'PartitionTemplate xmlns="http://www.ibm.com/xmlns/systems/power/firmware/templates/mc/2012_10/" \
                             xmlns:ns2="http://www.w3.org/XML/1998/namespace/k2"'
        partiton_template_xmlstr = etree.tostring(partiton_template_doc)
        partiton_template_xmlstr = partiton_template_xmlstr.decode("utf-8").replace("PartitionTemplate", templateNamespace, 1)

        templateUrl = "https://{0}/rest/api/templates/PartitionTemplate".format(self.hmc_ip)
        resp = open_url(templateUrl,
                        headers=header,
                        data=partiton_template_xmlstr,
                        method='PUT',
                        validate_certs=False,
                        force_basic_auth=True,
                        timeout=300)
        # This is to handle the case of unauthorized access, instead of getting error http code seems to be 200
        response = resp.read()
        response_dom = xml_strip_namespace(response)
        error_msg_l = response_dom.xpath("//Message")
        if error_msg_l:
            error_msg = error_msg_l[0].text
            raise HmcError(error_msg)

    def deletePartitionTemplate(self, template_name):
        logger.debug("Delete partition template...")
        header = {'X-API-Session': self.session,
                  'Accept': 'application/vnd.ibm.powervm.web+xml'}

        partiton_template_doc = self.getPartitionTemplate(name=template_name)
        if not partiton_template_doc:
            raise HmcError("Not able to fetch the partition template")
        template_uuid = partiton_template_doc.xpath("//AtomID")[0].text

        templateUrl = "https://{0}/rest/api/templates/PartitionTemplate/{1}".format(self.hmc_ip, template_uuid)
        logger.debug(templateUrl)
        open_url(templateUrl,
                 headers=header,
                 method='DELETE',
                 validate_certs=False,
                 force_basic_auth=True,
                 timeout=300)

    def checkPartitionTemplate(self, template_name, cec_uuid):
        header = _jobHeader(self.session)

        partiton_template_doc = self.getPartitionTemplate(name=template_name)
        if not partiton_template_doc:
            raise HmcError("Not able to fetch the partition template")
        template_uuid = partiton_template_doc.xpath("//AtomID")[0].text
        check_url = "https://{0}/rest/api/templates/PartitionTemplate/{1}/do/check".format(self.hmc_ip, template_uuid)

        reqdOperation = {'OperationName': 'Check',
                         'GroupName': 'PartitionTemplate',
                         'ProgressType': 'DISCRETE'}

        jobParams = {'K_X_API_SESSION_MEMENTO': self.session,
                     'TargetUuid': cec_uuid}

        payload = _job_RequestPayload(reqdOperation, jobParams)
        resp = open_url(check_url,
                        headers=header,
                        data=payload,
                        method='PUT',
                        validate_certs=False,
                        force_basic_auth=True,
                        timeout=300).read()

        checkjob_resp = xml_strip_namespace(resp)

        jobID = checkjob_resp.xpath('//JobID')[0].text

        return self.fetchJobStatus(jobID, template=True)

    def deployPartitionTemplate(self, draft_uuid, cec_uuid):

        url = "https://{0}/rest/api/templates/PartitionTemplate/{1}/do/deploy".format(self.hmc_ip, draft_uuid)

        header = _jobHeader(self.session)

        reqdOperation = {'OperationName': 'Deploy',
                         'GroupName': 'PartitionTemplate',
                         'ProgressType': 'DISCRETE'}

        jobParams = {'K_X_API_SESSION_MEMENTO': self.session,
                     'TargetUuid': cec_uuid}

        payload = _job_RequestPayload(reqdOperation, jobParams)
        resp = open_url(url,
                        headers=header,
                        data=payload,
                        method='PUT',
                        validate_certs=False,
                        force_basic_auth=True,
                        timeout=300).read()

        deploy_resp = xml_strip_namespace(resp)
        jobID = deploy_resp.xpath('//JobID')[0].text
        return self.fetchJobStatus(jobID, template=True)

    def transformPartitionTemplate(self, draft_uuid, cec_uuid):

        url = "https://{0}/rest/api/templates/PartitionTemplate/{1}/do/transform".format(self.hmc_ip, draft_uuid)
        header = _jobHeader(self.session)

        reqdOperation = {'OperationName': 'Transform',
                         'GroupName': 'PartitionTemplate',
                         'ProgressType': 'DISCRETE'}

        jobParams = {'K_X_API_SESSION_MEMENTO': self.session,
                     'TargetUuid': cec_uuid}

        payload = _job_RequestPayload(reqdOperation, jobParams)

        resp = open_url(url,
                        headers=header,
                        data=payload,
                        method='PUT',
                        validate_certs=False,
                        force_basic_auth=True,
                        timeout=300).read()

        transform_resp = xml_strip_namespace(resp)
        jobID = transform_resp.xpath('//JobID')[0].text
        return self.fetchJobStatus(jobID, template=True)

    def poweroffPartition(self, vm_uuid, restart, shutdown_option):
        url = "https://{0}/rest/api/uom/LogicalPartition/{1}/do/PowerOff".format(self.hmc_ip, vm_uuid)
        header = _jobHeader(self.session)

        reqdOperation = {'OperationName': 'PowerOff',
                         'GroupName': 'LogicalPartition',
                         'ProgressType': 'DISCRETE'}
        immediate = 'false'
        operation = 'shutdown'

        if shutdown_option == 'Delayed':
            immediate = 'false'
            operation = 'shutdown'
        elif shutdown_option == 'Immediate':
            immediate = 'true'
            operation = 'shutdown'
        elif shutdown_option == 'OperatingSystem':
            immediate = 'false'
            operation = 'osshutdown'
        elif shutdown_option == 'OSImmediate':
            immediate = 'true'
            operation = 'osshutdown'
        elif shutdown_option == 'Dump':
            immediate = 'false'
            operation = 'dumprestart'
            restart = 'false'
        elif shutdown_option == 'DumpRetry':
            immediate = 'false'
            operation = 'retrydump'
            restart = 'false'

        jobParams = {'immediate': immediate,
                     'restart': restart,
                     'operation': operation}

        payload = _job_RequestPayload(reqdOperation, jobParams)

        resp = open_url(url,
                        headers=header,
                        data=payload,
                        method='PUT',
                        validate_certs=False,
                        force_basic_auth=True,
                        timeout=300).read()

        shutdown_resp = xml_strip_namespace(resp)
        jobID = shutdown_resp.xpath('//JobID')[0].text
        return self.fetchJobStatus(jobID, timeout_in_min=10)

    def poweronPartition(self, vm_uuid, prof_uuid, keylock, iIPLsource, os_type):
        url = "https://{0}/rest/api/uom/LogicalPartition/{1}/do/PowerOn".format(self.hmc_ip, vm_uuid)
        header = _jobHeader(self.session)

        reqdOperation = {'OperationName': 'PowerOn',
                         'GroupName': 'LogicalPartition',
                         'ProgressType': 'DISCRETE'}

        jobParams = {'force': 'false',
                     'novsi': 'true',
                     'bootmode': 'norm'}

        if prof_uuid:
            jobParams.update({'LogicalPartitionProfile': prof_uuid})

        if keylock:
            if keylock == 'normal':
                keylock = 'norm'
            jobParams.update({'keylock': keylock})

        if os_type == 'OS400' and iIPLsource:
            jobParams.update({'iIPLsource': iIPLsource})

        payload = _job_RequestPayload(reqdOperation, jobParams)

        resp = open_url(url,
                        headers=header,
                        data=payload,
                        method='PUT',
                        validate_certs=False,
                        force_basic_auth=True,
                        timeout=300).read()

        activate_resp = xml_strip_namespace(resp)
        jobID = activate_resp.xpath('//JobID')[0].text
        return self.fetchJobStatus(jobID, timeout_in_min=10)

    def getPartitionProfiles(self, vm_uuid):
        url = "https://{0}/rest/api/uom/LogicalPartition/{1}/LogicalPartitionProfile".format(self.hmc_ip, vm_uuid)
        header = {'X-API-Session': self.session,
                  'Accept': 'application/vnd.ibm.powervm.uom+xml; type=LogicalPartitionProfile'}

        response = open_url(url,
                            headers=header,
                            method='GET',
                            validate_certs=False,
                            force_basic_auth=True,
                            timeout=300)

        if response.code == 204:
            return None

        lparProfiles_root = xml_strip_namespace(response.read())
        lparProfiles = lparProfiles_root.xpath('//LogicalPartitionProfile')
        return lparProfiles

    def add_vscsi_payload(self, pv_tup):
        payload = ''
        pv_tup_list_slice = pv_tup[:2]
        for pv_name, vios_name, pv_obj in pv_tup_list_slice:
            payload += '''
            <VirtualSCSIClientAdapter schemaVersion="V1_0">
                    <Metadata>
                            <Atom/>
                    </Metadata>
                    <name kb="CUD" kxe="false"></name>
                    <associatedLogicalUnits kb="CUD" kxe="false" schemaVersion="V1_0">
                            <Metadata>
                                    <Atom/>
                            </Metadata>
                    </associatedLogicalUnits>
                    <associatedPhysicalVolume kb="CUD" kxe="false" schemaVersion="V1_0">
                            <Metadata>
                                    <Atom/>
                            </Metadata>
                            <PhysicalVolume schemaVersion="V1_0">
                                    <Metadata>
                                            <Atom/>
                                    </Metadata>
                                    <name kb="CUD" kxe="false">{0}</name>
                            </PhysicalVolume>
                    </associatedPhysicalVolume>
                    <connectingPartitionName kxe="false" kb="CUD">{1}</connectingPartitionName>
                    <AssociatedTargetDevices kb="CUD" kxe="false" schemaVersion="V1_0">
                            <Metadata>
                                    <Atom/>
                            </Metadata>
                    </AssociatedTargetDevices>
                    <associatedVirtualOpticalMedia kb="CUD" kxe="false" schemaVersion="V1_0">
                            <Metadata>
                                    <Atom/>
                            </Metadata>
                    </associatedVirtualOpticalMedia>
            </VirtualSCSIClientAdapter>'''.format(pv_name, vios_name)
        return payload

    def add_vscsi(self, lpar_template_dom, vscsi_clients):
        vscsi_client_payload = '''
        <virtualSCSIClientAdapters kxe="false" kb="CUD" schemaVersion="V1_0">
        <Metadata>
                <Atom/>
        </Metadata>
        {0}
        </virtualSCSIClientAdapters>'''.format(vscsi_clients)
        suspendEnableTag = lpar_template_dom.xpath("//suspendEnable")[0]
        suspendEnableTag.addprevious(etree.XML(vscsi_client_payload))

    def getFreePhyVolume(self, vios_uuid):
        logger.debug(vios_uuid)
        url = "https://{0}/rest/api/uom/VirtualIOServer/{1}/do/GetFreePhysicalVolumes".format(self.hmc_ip, vios_uuid)
        header = _jobHeader(self.session)

        reqdOperation = {'OperationName': 'GetFreePhysicalVolumes',
                         'GroupName': 'VirtualIOServer',
                         'ProgressType': 'DISCRETE'}
        jobParams = {}

        payload = _job_RequestPayload(reqdOperation, jobParams, "V1_3_0")

        resp = open_url(url,
                        headers=header,
                        data=payload,
                        method='PUT',
                        validate_certs=False,
                        force_basic_auth=True,
                        timeout=300).read()

        resp = xml_strip_namespace(resp)
        jobID = resp.xpath('//JobID')[0].text

        pv_resp = self.fetchJobStatus(jobID)
        logger.debug("Free Physical Volume job response")
        logger.debug(pv_resp)
        pv_xml = pv_resp.xpath("//Results//ParameterName[text()='result']//following-sibling::ParameterValue")[0].text
        pv_xml = pv_xml.encode()
        resp = xml_strip_namespace(pv_xml)
        list_pv_elem = resp.xpath("//PhysicalVolume")
        return list_pv_elem

    def getVirtualNetworksQuick(self, system_uuid):
        url = "https://{0}/rest/api/uom/ManagedSystem/{1}/VirtualNetwork/quick/All".format(self.hmc_ip, system_uuid)
        header = {'X-API-Session': self.session,
                  'Accept': '*/*'}
        resp = open_url(url,
                        headers=header,
                        method='GET',
                        validate_certs=False,
                        force_basic_auth=True,
                        timeout=300)
        if resp.code != 200:
            logger.debug("Get of Logical Partitions failed. Respsonse code: %d", resp.code)
            return None
        response = resp.read()
        vnw_quick_list = json.loads(response)
        return vnw_quick_list

    def updateVirtualNWSettingsToDom(self, template_xml, config_dict_list):
        vn_payload = ''
        for each_vn in config_dict_list:
            vsn_payload = ''
            if each_vn['virtual_slot_number'] is not None:
                vsn_payload = '''
                <VirtualSlotNumber kb="CUD" kxe="false">{0}</VirtualSlotNumber>'''.format(each_vn['virtual_slot_number'])
            vn_payload += '''
            <ClientNetworkAdapter schemaVersion="V1_0">
                <Metadata>
                    <Atom/>
                </Metadata>
                {2}
                <clientVirtualNetworks kb="CUD" kxe="false" schemaVersion="V1_0">
                    <Metadata>
                        <Atom/>
                    </Metadata>
                    <ClientVirtualNetwork schemaVersion="V1_0">
                        <Metadata>
                            <Atom/>
                        </Metadata>
                        <name kxe="false" kb="CUD">{0}</name>
                        <uuid kb="CUD" kxe="false">{1}</uuid>
                    </ClientVirtualNetwork>
                </clientVirtualNetworks>
            </ClientNetworkAdapter>'''.format(each_vn['nw_name'], each_vn['nw_uuid'], vsn_payload)

        vnw_payload = '''
        <clientNetworkAdapters kb="CUD" kxe="false" schemaVersion="V1_0">
            <Metadata>
                <Atom/>
            </Metadata>
            {0}
        </clientNetworkAdapters>'''.format(vn_payload)

        vnw_payload_xml = etree.XML(vnw_payload)
        client_nw_adapter_tag = template_xml.xpath("//ioConfiguration")[0]
        client_nw_adapter_tag.addnext(vnw_payload_xml)

    def vios_fetch_fcports_info(self, viosuuid):
        vios_dom = self.getVirtualIOServer(viosuuid)
        phys_fc_ports = vios_dom.xpath("//PhysicalFibreChannelPort")
        fc_ports = []
        available_ports = None
        for each in phys_fc_ports:
            # check if <AvailablePorts> is present for respective fc adapter
            available_ports = each.xpath("AvailablePorts")
            if not available_ports:
                logger.debug("Skipping since not NPIV capable")
                continue
            fcport = {}
            fcport['LocationCode'] = each.xpath("LocationCode")[0].text
            fcport['PortName'] = each.xpath("PortName")[0].text
            fc_ports.append(fcport)
        return fc_ports

    def updateFCSettingsToDom(self, lpar_template_dom, config_list):
        fc_client_adapter = None
        fc_clients = ''
        for fc in config_list:
            fc_client_adapter = '''<VirtualFibreChannelClientAdapter schemaVersion="V1_0">
                <Metadata>
                    <Atom/>
                </Metadata>
                <locationCode kb="CUD" kxe="false">{0}</locationCode>
                <connectingPartitionName kb="CUD" kxe="false">{1}</connectingPartitionName>
                <portName kb="CUD" kxe="false">{2}</portName>
            </VirtualFibreChannelClientAdapter>'''.format(fc['LocationCode'], fc['viosname'], fc['PortName'])

            fc_client_adpt_dom = etree.XML(fc_client_adapter)
            if 'wwpn_pair' in fc:
                wwpn_str = ' '.join(fc['wwpn_pair'].split(';'))
                wwpn_xml = '<wwpns kb="CUD" kxe="false">{0}</wwpns>'.format(wwpn_str)
                fc_client_adpt_dom.xpath("//locationCode")[0].addnext(etree.XML(wwpn_xml))
            if 'client_adapter_id' in fc:
                caid_str = fc['client_adapter_id']
                caid_xml = '<VirtualSlotNumber kb="CUD" kxe="false">{0}</VirtualSlotNumber>'.format(caid_str)
                fc_client_adpt_dom.xpath("//locationCode")[0].addprevious(etree.XML(caid_xml))
            if 'server_adapter_id' in fc:
                said_str = fc['server_adapter_id']
                said_xml = '<remoteAdapterID kb="CUD" kxe="false">{0}</remoteAdapterID>'.format(said_str)
                fc_client_adpt_dom.xpath("//connectingPartitionName")[0].addnext(etree.XML(said_xml))

            fc_clients += ET.tostring(fc_client_adpt_dom).decode("utf-8")

        virtualFibreChannelClientAdapters = '''<virtualFibreChannelClientAdapters kb="CUD" kxe="false" schemaVersion="V1_0">
            <Metadata>
                <Atom/>
            </Metadata>
            {0}
            </virtualFibreChannelClientAdapters>'''.format(fc_clients)

        suspendEnableTag = lpar_template_dom.xpath("//suspendEnable")[0]
        suspendEnableTag.addprevious(etree.XML(virtualFibreChannelClientAdapters))

    def fetchFCDetailsFromVIOS(self, system_uuid, lpar_id, vios_list):
        vfcs = []
        if not vios_list:
            return vfcs
        vios_dict = {vios['PartitionID']: vios['PartitionName'] for vios in vios_list}

        try:
            vios_fc_xml = xml_strip_namespace(self.getVirtualIOServers(system_uuid, 'ViosFCMapping'))
            vios_fcs = vios_fc_xml.xpath('//VirtualFibreChannelMapping')
            for vios_fc_raw in vios_fcs:
                vfc_dict = {}
                vios_fc = etree.ElementTree(vios_fc_raw)
                if vios_fc.find('//ClientAdapter') is None:
                    continue
                part_id = vios_fc.xpath('//ClientAdapter/LocalPartitionID')[0].text
                if str(lpar_id) == str(part_id):
                    vios_id = int(vios_fc.xpath('//ClientAdapter/ConnectingPartitionID')[0].text)
                    vfc_dict['PortName'] = vios_fc.xpath('//ServerAdapter/PhysicalPort/PortName')[0].text
                    vfc_dict['vios'] = vios_dict[vios_id]
                    vfc_dict['LocationCode'] = vios_fc.xpath('//ServerAdapter/PhysicalPort/LocationCode')[0].text
                    vfc_dict['WWPNs'] = vios_fc.xpath('//ClientAdapter/WWPNs')[0].text
                    vfc_dict['ClientVirtualSlotNumber'] = vios_fc.xpath('//ClientAdapter/VirtualSlotNumber')[0].text
                    vfc_dict['ServerVirtualSlotNumber'] = vios_fc.xpath('//ClientAdapter/ConnectingVirtualSlotNumber')[0].text
                    vfcs.append(vfc_dict)
        except Exception:
            pass

        return vfcs

    def fetchSCSIDetailsFromVIOS(self, system_uuid, lpar_id, vios_list):
        vscsis = []
        if not vios_list:
            return vscsis
        vios_dict = {vios['PartitionID']: vios['PartitionName'] for vios in vios_list}

        try:
            vios_scsi_xml = xml_strip_namespace(self.getVirtualIOServers(system_uuid, 'ViosSCSIMapping'))
            vios_scsis = vios_scsi_xml.xpath('//VirtualSCSIMapping')
            for vios_scsi_raw in vios_scsis:
                vscsi_dict = {}
                vios_scsi = etree.ElementTree(vios_scsi_raw)
                # This code is to handle stale adapters
                if len(vios_scsi.xpath('//ClientAdapter')) < 1:
                    continue
                part_id = vios_scsi.xpath('//ClientAdapter/LocalPartitionID')[0].text
                if str(lpar_id) == str(part_id):
                    # Adds the PVs
                    if len(vios_scsi.xpath('//Storage/PhysicalVolume/VolumeUniqueID')) >= 1:
                        volumeUniqueID = vios_scsi.xpath('//Storage/PhysicalVolume/VolumeUniqueID')[0].text
                        vscsi_dict['VolumeUniqueID'] = volumeUniqueID
                        vios_id = int(vios_scsi.xpath('//ClientAdapter/RemoteLogicalPartitionID')[0].text)
                        vol_dict = {"vios": vios_dict[vios_id], 'name': vios_scsi.xpath('//Storage/PhysicalVolume/VolumeName')[0].text}
                        vscsi_dict['Volume'] = [vol_dict]
                        flag = False
                        for vscsi in vscsis:
                            if 'VolumeUniqueID' in vscsi and vscsi['VolumeUniqueID'] == volumeUniqueID:
                                vscsi['Volume'].append(vol_dict)
                                flag = True
                        if not flag:
                            vscsi_dict['ClientVirtualSlotNumber'] = vios_scsi.xpath('//ClientAdapter/VirtualSlotNumber')[0].text
                            vscsi_dict['ServerVirtualSlotNumber'] = vios_scsi.xpath('//ClientAdapter/RemoteSlotNumber')[0].text
                            vscsi_dict['TargetDeviceName'] = vios_scsi.xpath('//TargetDevice//TargetName')[0].text
                            vscsi_dict['VolumeCapacity'] = vios_scsi.xpath('//Storage/PhysicalVolume/VolumeCapacity')[0].text
                            vscsis.append(vscsi_dict)
                    # Adds the VOD
                    elif len(vios_scsi.xpath('//TargetDevice/VirtualOpticalTargetDevice')) >= 1:
                        vscsi_dict['ClientVirtualSlotNumber'] = vios_scsi.xpath('//ClientAdapter/VirtualSlotNumber')[0].text
                        vscsi_dict['ServerVirtualSlotNumber'] = vios_scsi.xpath('//ClientAdapter/RemoteSlotNumber')[0].text
                        vscsi_dict['TargetName'] = vios_scsi.xpath('//TargetDevice/VirtualOpticalTargetDevice/TargetName')[0].text
                        if len(vios_scsi.xpath('//Storage')) >= 1:
                            vscsi_dict['MediaName'] = vios_scsi.xpath('//Storage//MediaName')[0].text
                            vscsi_dict['MountType'] = vios_scsi.xpath('//Storage//MountType')[0].text
                            vscsi_dict['Size'] = vios_scsi.xpath('//Storage//Size')[0].text
                        vscsis.append(vscsi_dict)
        except Exception:
            pass
        return vscsis

    def getSharedProcessorPools(self, system_uuid):
        url = "https://{0}/rest/api/uom/ManagedSystem/{1}/SharedProcessorPool".format(self.hmc_ip, system_uuid)
        header = {'X-API-Session': self.session,
                  'Accept': '*/*'}
        resp = open_url(url,
                        headers=header,
                        method='GET',
                        validate_certs=False,
                        force_basic_auth=True,
                        timeout=300)
        if resp.code != 200:
            logger.debug("Get of Shared Processor Pool failed. Respsonse code: %d", resp.code)
            return None
        sharedProcPool_root = xml_strip_namespace(resp.read())
        sharedProcPool = sharedProcPool_root.xpath('//entry')
        return sharedProcPool

    def validateSharedProcessorPoolNameAndID(self, system_uuid, user_spp):
        spps = self.getSharedProcessorPools(system_uuid)
        spp_dict = {}
        spp_id = None
        for spp_raw in spps:
            spp = etree.ElementTree(spp_raw)
            v = spp.xpath('//PoolName')[0].text
            k = spp.xpath('//PoolID')[0].text
            spp_dict[k] = v
        if user_spp.isdigit():
            if user_spp in spp_dict:
                spp_id = user_spp
        else:
            logger.debug(spp_dict)
            for key, value in spp_dict.items():
                if value == user_spp:
                    spp_id = key
        return spp_id

    def add_vnic_payload(self, lpar_template_dom, vnic_tup, sriov_dvc_col, vios_name_list):
        payload = ''
        default_vnic_no = 65535
        count = 0
        for vnic in vnic_tup:
            vnic_id = vnic['vnic_adapter_id'] if vnic['vnic_adapter_id'] else str(default_vnic_no - count)
            use_nxt_slot = "false" if vnic['vnic_adapter_id'] else "true"
            backing_devices = vnic['backing_devices']
            backing_devices_payload = self.get_vnic_backing_devices_payload(backing_devices, sriov_dvc_col, vios_name_list)
            payload += '''
            <VirtualNICDedicated schemaVersion="V1_0">
                    <Metadata>
                           <Atom/>
                    </Metadata>
                    <VirtualSlotNumber kb="CUD" kxe="false">{0}</VirtualSlotNumber>
                    <drcName kb="CUD" kxe="false">CUSTOM_1653548478255-{1}9747</drcName>
                    <UseNextAvailableSlotID kxe="false" kb="CUD">{2}</UseNextAvailableSlotID>
                    <Details kxe="false" kb="CUR" schemaVersion="V1_0">
                            <Metadata>
                                    <Atom/>
                            </Metadata>
                            <PortVLANID kxe="false" kb="CUD">0</PortVLANID>
                            <PortVLANIDPriority kxe="false" kb="CUD">0</PortVLANIDPriority>
                            <AllowedVLANIDs kxe="false" kb="CUD">ALL</AllowedVLANIDs>
                            <MACAddress kxe="false" kb="COD">HMC-ASSIGNED</MACAddress>
                            <AllowedOperatingSystemMACAddresses kxe="false" kb="CUD">ALL</AllowedOperatingSystemMACAddresses>
                            <DesiredMode kxe="false" kb="CUD">DEDICATED</DesiredMode>
                            <AutoPriorityFailover kxe="false" kb="CUD">true</AutoPriorityFailover>
                    </Details>
                    <AssociatedBackingDevices kb="CUR" kxe="false" schemaVersion="V1_0">
                            <Metadata>
                                    <Atom/>
                            </Metadata>
                                    {3}
                    </AssociatedBackingDevices>
            </VirtualNICDedicated>'''.format(vnic_id, str(default_vnic_no - count), use_nxt_slot, backing_devices_payload)
            count += 1

        vnic_payload = '''
        <DedicatedVirtualNICs kxe="false" kb="CUD" schemaVersion="V1_0">
        <Metadata>
                <Atom/>
        </Metadata>
                {0}
        </DedicatedVirtualNICs>'''.format(payload)
        dedicatedvnicstag = lpar_template_dom.xpath('//DedicatedVirtualNICs')[0]
        dedicatedvnicstag.getparent().replace(dedicatedvnicstag, etree.XML(vnic_payload))

    def get_vnic_backing_devices_payload(self, backing_devices, sriov_dvc_col, vios_name_list):
        eval_backing_devices = []
        if backing_devices is None:
            for sriov_dvc in sriov_dvc_col:
                if sriov_dvc["LinkStatus"] == "true":
                    eval_dvc_dict = {}
                    eval_dvc_dict['partitionName'] = vios_name_list[0]
                    eval_dvc_dict['RelatedSRIOVAdapterID'] = sriov_dvc['RelatedSRIOVAdapterID']
                    if round((100.0 - float(sriov_dvc['AllocatedCapacity'])), 1) >= 2.0:
                        eval_dvc_dict['DesiredCapacityPercentage'] = "2.0"
                    else:
                        continue
                    eval_dvc_dict['RelatedSRIOVPhysicalPortID'] = sriov_dvc['RelatedSRIOVPhysicalPortID']
                    eval_backing_devices.append(eval_dvc_dict)
                    break
            else:
                for sriov_dvc in sriov_dvc_col:
                    if round((100.0 - float(sriov_dvc['AllocatedCapacity'])), 1) >= 2.0:
                        eval_dvc_dict = {}
                        eval_dvc_dict['partitionName'] = vios_name_list[0]
                        eval_dvc_dict['RelatedSRIOVAdapterID'] = sriov_dvc['RelatedSRIOVAdapterID']
                        eval_dvc_dict['DesiredCapacityPercentage'] = "2.0"
                        eval_dvc_dict['RelatedSRIOVPhysicalPortID'] = sriov_dvc['RelatedSRIOVPhysicalPortID']
                        eval_backing_devices.append(eval_dvc_dict)
                        break
                else:
                    raise Error('Their are no backing device with link status up or available capacity more than 2.0 in the managed system')
        else:
            for backing_device in backing_devices:
                for sriov_dvc in sriov_dvc_col:
                    if (backing_device['location_code'] is None) or (re.search(r'[a-zA-Z]\d{1,2}-[a-zA-Z]\d{1,2}$', backing_device['location_code']) is None):
                        msg = ('mandatory parameter backing device location_code is missing '
                               'or location_code is not in C1-T1 or XXXXX.XXXXX.XXX-P1-C1-T1 format')
                        raise ParameterError(msg)
                    if sriov_dvc['LocationCode'] == backing_device['location_code'] or (sriov_dvc['LocationCode']).endswith(backing_device['location_code']):
                        eval_dvc_dict = {}
                        if backing_device['hosting_partition'] is None:
                            eval_dvc_dict['partitionName'] = vios_name_list[0]
                        elif backing_device['hosting_partition'] in vios_name_list:
                            eval_dvc_dict['partitionName'] = backing_device['hosting_partition']
                        else:
                            msg = ("Given backing device hosting partition name: {0} not found in the managed system "
                                   "or RMC of state is not active")
                            raise Error(msg.format(backing_device['hosting_partition']))
                        eval_dvc_dict['RelatedSRIOVAdapterID'] = sriov_dvc['RelatedSRIOVAdapterID']
                        if backing_device['capacity']:
                            if round(backing_device['capacity'], 1) <= round(100.0 - float(sriov_dvc['AllocatedCapacity']), 1):
                                eval_dvc_dict['DesiredCapacityPercentage'] = str(backing_device['capacity'])
                            else:
                                msg = 'Available Capacity of the backing device:{0} is {1} but desired capacity is: {2}'
                                raise Error(msg.format(sriov_dvc['LocationCode'], round(100.0 - float(sriov_dvc['AllocatedCapacity']), 1),
                                            backing_device['capacity']))
                        else:
                            if round(100.0 - float(sriov_dvc['AllocatedCapacity']), 1) >= 2.0:
                                eval_dvc_dict['DesiredCapacityPercentage'] = "2.0"
                            else:
                                msg = 'Available Capacity of the backing device:{0} is {1} but desired capacity is: 2.0'
                                raise Error(msg.format(sriov_dvc['LocationCode'], round(100.0 - float(sriov_dvc['AllocatedCapacity']), 1)))
                        eval_dvc_dict['RelatedSRIOVPhysicalPortID'] = sriov_dvc['RelatedSRIOVPhysicalPortID']
                        eval_backing_devices.append(eval_dvc_dict)
                        break
                else:
                    msg = "Given VNIC SRIOV backing device location code: {0} not found in the managed system or exhausted with Ethernet LogicalPort limit"
                    raise Error(msg.format(backing_device['location_code']))
        payload = ''
        for ev_bck_dvc in eval_backing_devices:
            payload += '''
            <VirtualNICBackingDeviceChoice>
            <VirtualNICSRIOVBackingDevice schemaVersion="V1_0">
                    <Metadata>
                            <Atom/>
                    </Metadata>
                    <DeviceType kb="COR" kxe="false">SRIOV</DeviceType>
                    <AssociatedVirtualIOServer kxe="false" kb="COR" schemaVersion="V1_0">
                            <Metadata>
                                    <Atom/>
                            </Metadata>
                            <partitionName kb="CUD" kxe="false">{0}</partitionName>
                    </AssociatedVirtualIOServer>
                    <FailOverPriority kb="CUD" kxe="false">50</FailOverPriority>
                    <RelatedSRIOVAdapterID kxe="false" kb="COR">{1}</RelatedSRIOVAdapterID>
                    <DesiredCapacityPercentage kxe="false" kb="ROR">{2}%</DesiredCapacityPercentage>
                    <RelatedSRIOVPhysicalPortID kb="COR" kxe="false">{3}</RelatedSRIOVPhysicalPortID>
            </VirtualNICSRIOVBackingDevice>
            </VirtualNICBackingDeviceChoice>
            '''.format(ev_bck_dvc['partitionName'], ev_bck_dvc['RelatedSRIOVAdapterID'],
                       ev_bck_dvc['DesiredCapacityPercentage'], ev_bck_dvc['RelatedSRIOVPhysicalPortID'])
        return payload

    def create_sriov_collection(self, sriov_adapters_dom):
        sriov_col_li = []
        for sriov_adapter_dom_raw in sriov_adapters_dom:
            sriov_adapter_dom = etree.ElementTree(sriov_adapter_dom_raw)
            try:
                sriov_adapter_id = sriov_adapter_dom.xpath('//SRIOVAdapterID')[0].text
                sriov_ce_pps = sriov_adapter_dom.xpath('//ConvergedEthernetPhysicalPorts//SRIOVConvergedNetworkAdapterPhysicalPort')
                sriov_et_pps = sriov_adapter_dom.xpath('//EthernetPhysicalPorts//SRIOVEthernetPhysicalPort')
                sriov_rc_pps = sriov_adapter_dom.xpath('//SRIOVRoCEPhysicalPorts//SRIOVRoCEPhysicalPort')
                sriov_pps = sriov_ce_pps + sriov_et_pps + sriov_rc_pps
                for sriov_pp_raw in sriov_pps:
                    sriov_pp = etree.ElementTree(sriov_pp_raw)
                    sriov_dict = {}
                    maxELP = int(sriov_pp.xpath("//ConfiguredMaxEthernetLogicalPorts")[0].text)
                    cELP = int(sriov_pp.xpath("//ConfiguredEthernetLogicalPorts")[0].text)
                    if maxELP - cELP == 0:
                        continue
                    sriov_dict['RelatedSRIOVAdapterID'] = sriov_adapter_id
                    sriov_dict['LocationCode'] = sriov_pp.xpath("//LocationCode")[0].text
                    sriov_dict['RelatedSRIOVPhysicalPortID'] = sriov_pp.xpath("//PhysicalPortID")[0].text
                    sriov_dict['LinkStatus'] = sriov_pp.xpath("//LinkStatus")[0].text
                    sriov_dict['AllocatedCapacity'] = sriov_pp.xpath("//AllocatedCapacity")[0].text.strip('%')
                    sriov_col_li.append(sriov_dict)
            except Exception:
                continue
        return sriov_col_li

    def generic_get(self, url):
        header = {'X-API-Session': self.session,
                  'Accept': '*/*'}
        resp = open_url(url,
                        headers=header,
                        method='GET',
                        validate_certs=False,
                        force_basic_auth=True,
                        timeout=3600)
        if resp.code != 200:
            logger.debug("Get operation failed. Respsonse code: %d", resp.code)
            return None
        response = resp.read()
        gen_response = xml_strip_namespace(response)
        return gen_response

    def isDedicatedProcConfig(self, partition_dom):
        return True if partition_dom.xpath('//HasDedicatedProcessors')[0].text == 'true' else False

    def updateProc(self, partition_dom, isDedicated, proc=None, proc_unit=None):
        if isDedicated:
            partition_dom.xpath('//DedicatedProcessorConfiguration/DesiredProcessors')[0].text = proc
        else:
            if proc:
                partition_dom.xpath('//SharedProcessorConfiguration/DesiredVirtualProcessors')[0].text = proc
            if proc_unit:
                partition_dom.xpath('//SharedProcessorConfiguration/DesiredProcessingUnits')[0].text = proc_unit
        return partition_dom

    def updateProcSharingMode(self, partition_dom, sharingMode):
        modeMapping = {'keep_idle_procs': 'keep idle procs',
                       'share_idle_procs': 'sre idle proces',
                       'share_idle_procs_active': 'sre idle procs active',
                       'share_idle_procs_always': 'sre idle procs always',
                       'uncapped': 'uncapped',
                       'capped': 'capped'
                       }
        partition_dom.xpath('//SharingMode')[0].text = modeMapping[sharingMode]
        return partition_dom

    def getProcSharingMode(self, partition_dom):
        return partition_dom.xpath('//CurrentSharingMode')[0].text

    def updateProcUncappedWeight(self, partition_dom, weight):
        sharedProcElement = partition_dom.xpath('//UncappedWeight')
        if isinstance(sharedProcElement, list) and len(sharedProcElement) > 0:
            partition_dom.xpath('//UncappedWeight')[0].text = weight
        else:
            weightXml = '<UncappedWeight kxe="false" kb="CUD">{0}</UncappedWeight>'.format(weight)
            sharedProcessorPoolIDElement = partition_dom.xpath('//SharedProcessorPoolID')[0]
            sharedProcessorPoolIDElement.addnext(etree.XML(weightXml))
        return partition_dom

    def getProcUncappedWeight(self, partition_dom):
        element = partition_dom.xpath('//UncappedWeight')
        if isinstance(element, list) and len(element) > 0:
            return element[0].text
        else:
            return None

    def getProcPool(self, partition_dom):
        return partition_dom.xpath('//CurrentSharedProcessorPoolID')[0].text

    def updateProcPool(self, partition_dom, poolId):
        partition_dom.xpath('//SharedProcessorPoolID')[0].text = poolId
        return partition_dom

    def getProcs(self, isDedicated, partition_dom):
        if isDedicated:
            procs = partition_dom.xpath('//CurrentDedicatedProcessorConfiguration/CurrentProcessors')[0].text
        else:
            procs = partition_dom.xpath('//CurrentSharedProcessorConfiguration/AllocatedVirtualProcessors')[0].text
        return procs

    def getProcUnits(self, partition_dom):
        return partition_dom.xpath('//CurrentSharedProcessorConfiguration/CurrentProcessingUnits')[0].text

    def getMem(self, partition_dom):
        return partition_dom.xpath('//CurrentMemory')[0].text

    def updateMem(self, partition_dom, mem):
        partition_dom.xpath('//DesiredMemory')[0].text = mem
        return partition_dom

    def updateLogicalPartition(self, partition_dom, timeout=None):
        header = {'X-API-Session': self.session,
                  'Accept': '*/*',
                  'Content-Type': 'application/vnd.ibm.powervm.uom+xml; type=LogicalPartition'}

        partition_uuid = partition_dom.xpath('//AtomID')[0].text
        timeout_in_sec = 3600
        if timeout:
            if timeout > 60:
                timeout_in_sec = timeout * 60

            url = "https://{0}/rest/api/uom/LogicalPartition/{1}?timeout={2}".format(
                  self.hmc_ip, partition_uuid, timeout)
        else:
            url = "https://{0}/rest/api/uom/LogicalPartition/{1}".format(
                  self.hmc_ip, partition_uuid)

        partition_dom = partition_dom.xpath("//LogicalPartition")[0]

        partiton_xmlstr = etree.tostring(partition_dom)
        partiton_xmlstr = partiton_xmlstr.decode("utf-8").replace("LogicalPartition", LPAR_NS, 1)
        logger.debug("INPUT PAYLOAD: \n %s", partiton_xmlstr)
        resp = open_url(url,
                        headers=header,
                        method='POST',
                        data=partiton_xmlstr,
                        validate_certs=False,
                        force_basic_auth=True,
                        timeout=timeout_in_sec)
        if resp.code != 200:
            logger.debug("Post operation failed. Respsonse code: %d", resp.code)
            return None
        response = resp.read()
        logger.debug("POST RESPONSE: \n %s", response)
        post_response = xml_strip_namespace(response)
        return post_response

    def fetchDedicatedVirtualNICs(self, system_uuid, lpar_uuid, vm_name, vios_list):
        lpar_uuid, partition_dom = self.getLogicalPartition(system_uuid,
                                                            partition_name=vm_name, partition_uuid=lpar_uuid)
        vios_dict = {}
        if vios_list:
            vios_dict = {vios['UUID']: vios['PartitionName'] for vios in vios_list}
        vnics_list = []
        vnic_links = partition_dom.xpath('//DedicatedVirtualNICs//link')
        if vnic_links:
            for vnic_link_raw in vnic_links:
                vnic_dict = {}
                vnic_link = etree.ElementTree(vnic_link_raw)
                href = vnic_link.xpath('./@href')[0]
                vnic_dom = self.generic_get(href)
                vnic_dict['vnic_adapter_id'] = vnic_dom.xpath('//VirtualSlotNumber')[0].text
                vnic_backing_devices = vnic_dom.xpath('//VirtualNICBackingDeviceChoice')
                bck_dvcs = []
                for vnic_bck_dvc_raw in vnic_backing_devices:
                    bck_dvc_dict = {}
                    vnic_bck_dvc = etree.ElementTree(vnic_bck_dvc_raw)
                    bck_dvc_dict['Capacity'] = vnic_bck_dvc.xpath('//CurrentCapacityPercentage')[0].text
                    bck_dvc_dict['DeviceType'] = vnic_bck_dvc.xpath('//DeviceType')[0].text
                    bck_dvc_dict['Status'] = vnic_bck_dvc.xpath('//Status')[0].text
                    bck_dvc_dict['RelatedSRIOVAdapterID'] = vnic_bck_dvc.xpath('//RelatedSRIOVAdapterID')[0].text
                    vios_href = vnic_bck_dvc.xpath('//AssociatedVirtualIOServer')[0].attrib['href']
                    bck_dvc_dict['AssociatedVirtualIOServer'] = vios_dict[(vios_href.split('/'))[-1]]
                    sriov_href = vnic_bck_dvc.xpath('//RelatedSRIOVLogicalPort')[0].attrib['href']
                    bck_dvc_dict['RelatedSRIOVLocationCode'] = self.generic_get(sriov_href).xpath('//LocationCode')[0].text
                    bck_dvcs.append(bck_dvc_dict)
                vnic_dict['backing_devices'] = bck_dvcs
                vnics_list.append(vnic_dict)
        return vnics_list

    def fetchTaggedGroupItems(self):
        url = "https://{0}/rest/api/uom/Group".format(self.hmc_ip)
        resp_dom = self.generic_get(url)
        resp_dict = {}
        if resp_dom is not None:
            group_dom_list = resp_dom.xpath("//Group")
            for group_dom_raw in group_dom_list:
                uuid_list = []
                group_dom = etree.ElementTree(group_dom_raw)
                group_name = group_dom.xpath("//GroupName")[0].text
                assc_lpar_links = group_dom.xpath("//AssociatedLogicalPartitions//link")
                assc_ms_links = group_dom.xpath("//AssociatedManagedSystems//link")
                assc_vios_links = group_dom.xpath("//AssociatedVirtualIOServers//link")
                for assc_raw_lpar in assc_lpar_links:
                    assc_lpar = etree.ElementTree(assc_raw_lpar)
                    lpar_uuid = (assc_lpar.xpath('./@href')[0]).split('/')[-1]
                    uuid_list.append(lpar_uuid)
                for assc_raw_ms in assc_ms_links:
                    assc_ms = etree.ElementTree(assc_raw_ms)
                    ms_uuid = (assc_ms.xpath('./@href')[0]).split('/')[-1]
                    uuid_list.append(ms_uuid)
                for assc_raw_vios in assc_vios_links:
                    assc_vios = etree.ElementTree(assc_raw_vios)
                    vios_uuid = (assc_vios.xpath('./@href')[0]).split('/')[-1]
                    uuid_list.append(vios_uuid)
                resp_dict[group_name] = uuid_list
        return resp_dict

    def fetchPVsFromVIOSDOM(self, vios_dom, vios_name):
        # Generate the list of PhysicalVolumes available in the VIOS DOM
        pvs_raw = []
        pvs = []
        fc_ports_dom = vios_dom.xpath("//PhysicalFibreChannelPorts/PhysicalFibreChannelPort")
        for fc_port_raw in fc_ports_dom:
            fc_port_dom = etree.ElementTree(fc_port_raw)
            pvs_raw = pvs_raw + fc_port_dom.xpath("//PhysicalVolumes/PhysicalVolume")
        if pvs_raw:
            pvs = [etree.ElementTree(pv_raw) for pv_raw in pvs_raw]
        else:
            raise HmcError("There are no Physical Volumes Available in VIOS: {0}".format(vios_name))
        return pvs

    def build_SCSI_MappingPayload(self, pv_dom_list, pv_setting, lpar_UUID, lpar_id, vios_id):
        payload = ""
        target_name_payload = ""
        server_adapter_id_payload = ""
        client_adapter_id_payload = ""
        pv_payload = ""

        for pv_dom in pv_dom_list:
            disk_name = pv_dom.xpath("//VolumeName")[0].text
            if disk_name == pv_setting['disk_name']:
                pv_payload = pv_dom
                break
        else:
            raise HmcError("Disk_Name provided: {0} not found in the vios {1}".format(pv_setting['disk_name'], pv_setting['vios_name']))

        # build a payload for target name, if user provides
        if pv_setting['target_name']:
            target_name_payload = '''
            <TargetDevice kb="CUR" kxe="false">
                <PhysicalVolumeVirtualTargetDevice schemaVersion="V1_0">
                    <Metadata>
                        <Atom/>
                    </Metadata>
                <TargetName kb="CUR" kxe="false">{0}</TargetName>
                </PhysicalVolumeVirtualTargetDevice>
            </TargetDevice>
            '''.format(pv_setting['target_name'])

        # build a payload for client adapter id, if user provides
        if pv_setting['server_adapter_id']:
            server_adapter_id_payload = '''
            <ClientAdapter kb="CUR" kxe="false" schemaVersion="V1_0">
                <Metadata>
                    <Atom/>
                </Metadata>
                <LocalPartitionID kxe="false" kb="CUR">{0}</LocalPartitionID>
                <VirtualSlotNumber kb="COD" kxe="false">{1}</VirtualSlotNumber>
                <RemoteLogicalPartitionID kxe="false" kb="CUR">{2}</RemoteLogicalPartitionID>
            </ClientAdapter>
            '''.format(lpar_id, str(pv_setting['server_adapter_id']), vios_id)

        # build a payload for server adapter id, if user provides
        if pv_setting['client_adapter_id']:
            client_adapter_id_payload = '''
            <ServerAdapter kb="CUR" kxe="false" schemaVersion="V1_0">
                <Metadata>
                    <Atom/>
                </Metadata>
                <LocalPartitionID kxe="false" kb="CUR">{0}</LocalPartitionID>
                <VirtualSlotNumber kb="COD" kxe="false">{1}</VirtualSlotNumber>
                <RemoteLogicalPartitionID kxe="false" kb="CUR">{2}</RemoteLogicalPartitionID>
            </ServerAdapter>
            '''.format(vios_id, str(pv_setting['client_adapter_id']), lpar_id)

        payload = '''
        <VirtualSCSIMapping schemaVersion="V1_0">
            <Metadata>
                <Atom/>
            </Metadata>
            <AssociatedLogicalPartition kxe="false" kb="CUR" href="https://localhost:443/rest/api/uom/LogicalPartition/{0}" rel="related"/>
            {1}
            {2}
            <Storage kb="CUR" kxe="false">
            {3}
            </Storage>
            {4}
        </VirtualSCSIMapping>
        '''.format(lpar_UUID, server_adapter_id_payload, client_adapter_id_payload, (etree.tostring(pv_payload)).decode("utf-8"), target_name_payload)

        return payload.replace('\n\n', '').replace('\n', '')

    def getVIOSSCSCIMappings_dictionary(self, vios_uuid):
        vscsis_pv = []
        vscsis_vod = []
        try:
            vios_scsi_xml = self.getVirtualIOServer(vios_uuid, 'ViosSCSIMapping')
            vios_scsis = vios_scsi_xml.xpath('//VirtualSCSIMapping')
            for vios_scsi_raw in vios_scsis:
                vscsi_dict = {}
                vios_scsi = etree.ElementTree(vios_scsi_raw)
                try:
                    # Fills the vscsi_pv dictionary
                    vscsi_dict['BackingDeviceName'] = vios_scsi.xpath('//ServerAdapter/BackingDeviceName')[0].text
                    vscsi_dict['RemoteLogicalPartitionID'] = vios_scsi.xpath('//ServerAdapter/RemoteLogicalPartitionID')[0].text
                    vscsis_pv.append(vscsi_dict)
                except Exception:
                    pass
                try:
                    # Fills the vscsi_vod dictionary
                    vscsi_dict['TargetName'] = vios_scsi.xpath('//TargetDevice/VirtualOpticalTargetDevice/TargetName')[0].text
                    vscsis_vod.append(vscsi_dict)
                except Exception:
                    pass
        except Exception:
            pass
        return vscsis_pv, vscsis_vod

    def updateVIOSwithSCSIMappings(self, vios_UUID, pv_settings_list, lpar_UUID, vios_name, partition_dom, timeout):
        payload = ""
        flag = False
        vios_dom = self.getVirtualIOServer(vios_UUID)
        vios_vscsi_dict = self.getVIOSSCSCIMappings_dictionary(vios_UUID)
        mapped_dvc_names = [item['BackingDeviceName'] for item in vios_vscsi_dict[0]]
        pv_dom_list = self.fetchPVsFromVIOSDOM(vios_dom, vios_name)
        lpar_id = partition_dom.xpath("//PartitionID")[0].text
        vios_id = vios_dom.xpath("//PartitionID")[0].text
        for pv_settings in pv_settings_list:
            if pv_settings['disk_name'] not in mapped_dvc_names:
                payload = self.build_SCSI_MappingPayload(pv_dom_list, pv_settings, lpar_UUID, lpar_id, vios_id)
                vSCSIMappingsTag = vios_dom.xpath("//VirtualSCSIMappings")[0]
                vSCSIMappingsTag.append(etree.XML(payload))
                flag = True
        if flag:
            self.updateVirtualIOServer(vios_dom, timeout)
        return flag

    def fetchVIOSFcDetails(self, vios_dom):
        fc_ports_list = []
        fc_ports = vios_dom.xpath("//PhysicalFibreChannelAdapter/PhysicalFibreChannelPorts/PhysicalFibreChannelPort")
        for fc_port_raw in fc_ports:
            fc_dict = {}
            fc_dict['AvailablePorts'] = "0"
            fc_dict['TotalPorts'] = "0"
            fc_port = etree.ElementTree(fc_port_raw)
            try:
                fc_dict['PortName'] = fc_port.xpath("//PortName")[0].text
                fc_dict['AvailablePorts'] = fc_port.xpath("//AvailablePorts")[0].text
                fc_dict['TotalPorts'] = fc_port.xpath("//TotalPorts")[0].text
                fc_dict['LocationCode'] = fc_port.xpath("//LocationCode")[0].text
            except Exception:
                pass
            finally:
                fc_ports_list.append(fc_dict)

        return fc_ports_list

    def build_FC_MappingPayload(self, location_code, npiv_setting, lpar_UUID, lpar_id, vios_id):
        payload = ""
        server_adapter_id_payload = ""
        client_adapter_id_payload = ""
        wwpn_pair_payload = ""
        client_adapter_payload = ""
        # build client adapter_id payload
        if npiv_setting['wwpn_pair']:
            if ';' in npiv_setting['wwpn_pair']:
                wwpn_pair = npiv_setting['wwpn_pair'].replace(";", " ")
                wwpn_pair_payload = '''
                <WWPNs kb="CUR" kxe="false">{0}</WWPNs>'''.format(wwpn_pair)
            else:
                raise ParameterError("Invalid WWPN pair format: {0}, Correct format is <wwpn1;wwpn2>".format(npiv_setting['wwpn_pair']))
        if npiv_setting['client_adapter_id']:
            client_adapter_payload = '''
            <VirtualSlotNumber kb="COD" kxe="false">{0}</VirtualSlotNumber>
            <ConnectingPartitionID kxe="false" kb="CUR">{1}</ConnectingPartitionID>'''.format(str(npiv_setting['client_adapter_id']), vios_id)
        if wwpn_pair_payload or client_adapter_payload:
            client_adapter_id_payload = '''
            <ClientAdapter kxe="false" kb="CUR" schemaVersion="V1_0">
                <Metadata>
                    <Atom/>
                </Metadata>
                <LocalPartitionID kxe="false" kb="CUR">{0}</LocalPartitionID>
                {1}
                {2}
            </ClientAdapter>
            '''.format(lpar_id, client_adapter_payload, wwpn_pair_payload)
        # build server adapter id payload
        if npiv_setting['server_adapter_id']:
            server_adapter_id_payload = '''
            <ServerAdapter kxe="false" kb="CUR" schemaVersion="V1_0">
                <Metadata>
                    <Atom/>
                </Metadata>
                <VirtualSlotNumber kb="COD" kxe="false">{0}</VirtualSlotNumber>
                <ConnectingPartitionID kxe="false" kb="CUR">{1}</ConnectingPartitionID>
            </ServerAdapter>
            '''.format(str(npiv_setting['server_adapter_id']), lpar_id)
        # build Virtual Fibre Channel Mapping payload
        payload = '''
        <VirtualFibreChannelMapping schemaVersion="V1_0">
            <Metadata>
                <Atom/>
            </Metadata>
            <AssociatedLogicalPartition kxe="false" kb="CUR" href="https://localhost:443/rest/api/uom/LogicalPartition/{0}" rel="related"/>
            {1}
            <Port kxe="false" kb="CUR" schemaVersion="V1_0">
                <Metadata>
                    <Atom/>
                </Metadata>
                <LocationCode kb="ROR" kxe="false">{2}</LocationCode>
                <PortName kxe="false" kb="CUR">{3}</PortName>
            </Port>
            {4}
        </VirtualFibreChannelMapping>
        '''.format(lpar_UUID, client_adapter_id_payload, location_code, npiv_setting['fc_port_name'], server_adapter_id_payload)
        return payload

    def updateVIOSwithNPIVMappings(self, vios_UUID, npiv_settings_list, lpar_UUID, vios_name, partition_dom, timeout):
        payload = ""
        flag = False
        vios_dom = self.getVirtualIOServer(vios_UUID)
        vios_npiv_dict_list = self.fetchVIOSFcDetails(vios_dom)
        lpar_id = partition_dom.xpath("//PartitionID")[0].text
        vios_id = vios_dom.xpath("//PartitionID")[0].text
        for npiv_settings in npiv_settings_list:
            for vios_npiv_dict in vios_npiv_dict_list:
                if npiv_settings['fc_port_name'] == vios_npiv_dict['PortName']:
                    if int(vios_npiv_dict['AvailablePorts']) > 0:
                        payload = self.build_FC_MappingPayload(vios_npiv_dict['LocationCode'], npiv_settings, lpar_UUID, lpar_id, vios_id)
                        FCMappingsTag = vios_dom.xpath("//VirtualFibreChannelMappings")[0]
                        FCMappingsTag.append(etree.XML(payload))
                        flag = True
                        break
                    raise HmcError("There are only {0} available ports in the fc_port_name: {1}"
                                   .format(vios_npiv_dict['AvailablePorts'], npiv_settings['fc_port_name']))
            else:
                raise HmcError("fc_port_name: {0} provided is not found in the vios: {1}".format(npiv_settings['fc_port_name'], vios_name, ))
        if flag:
            self.updateVirtualIOServer(vios_dom, timeout)
        return flag

    def build_SCSI_VOD_MappingPayload(self, vod_setting, lpar_UUID, lpar_id, vios_id, vom_dict):
        payload = ""
        server_adapter_id_payload = ""
        client_adapter_id_payload = ""
        media_name_payload = ""

        # build a payload for client adapter id, if user provides
        if vod_setting['server_adapter_id']:
            server_adapter_id_payload = '''
            <ClientAdapter kb="CUR" kxe="false" schemaVersion="V1_0">
                <Metadata>
                    <Atom/>
                </Metadata>
                <LocalPartitionID kxe="false" kb="CUR">{0}</LocalPartitionID>
                <VirtualSlotNumber kb="COD" kxe="false">{1}</VirtualSlotNumber>
                <RemoteLogicalPartitionID kxe="false" kb="CUR">{2}</RemoteLogicalPartitionID>
            </ClientAdapter>
            '''.format(lpar_id, str(vod_setting['server_adapter_id']), vios_id)

        # build a payload for server adapter id, if user provides
        if vod_setting['client_adapter_id']:
            client_adapter_id_payload = '''
            <ServerAdapter kb="CUR" kxe="false" schemaVersion="V1_0">
                <Metadata>
                    <Atom/>
                </Metadata>
                <LocalPartitionID kxe="false" kb="CUR">{0}</LocalPartitionID>
                <VirtualSlotNumber kb="COD" kxe="false">{1}</VirtualSlotNumber>
                <RemoteLogicalPartitionID kxe="false" kb="CUR">{2}</RemoteLogicalPartitionID>
            </ServerAdapter>
            '''.format(vios_id, str(vod_setting['client_adapter_id']), lpar_id)

        # build payload for loading media
        if vod_setting['media_name']:
            if vod_setting['media_name'] in vom_dict:
                media_name_payload = '''
                <Storage kb="CUR" kxe="false">
                    <VirtualOpticalMedia schemaVersion="V1_0">
                        <Metadata>
                            <Atom/>
                        </Metadata>
                        <MediaName kxe="false" kb="CUR">{0}</MediaName>
                    </VirtualOpticalMedia>
                </Storage>
                '''.format(vod_setting['media_name'])
            else:
                raise HmcError("MediaName: {0} not found in the VIOS".format(vod_setting['media_name']))

        payload = '''
        <VirtualSCSIMapping schemaVersion="V1_0">
            <Metadata>
                <Atom/>
            </Metadata>
            <AssociatedLogicalPartition kxe="false" kb="CUR" href="https://localhost:443/rest/api/uom/LogicalPartition/{0}" rel="related"/>
            {1}
            {2}
            {3}
            <TargetDevice kb="CUR" kxe="false">
                <VirtualOpticalTargetDevice schemaVersion="V1_0">
                    <Metadata>
                        <Atom/>
                    </Metadata>
                    <TargetName kb="CUR" kxe="false">{4}</TargetName>
                </VirtualOpticalTargetDevice>
            </TargetDevice>
        </VirtualSCSIMapping>
        '''.format(lpar_UUID, server_adapter_id_payload, client_adapter_id_payload, media_name_payload, vod_setting['device_name'])

        return payload.replace('\n\n', '').replace('\n', '')

    def getVIOSVirtualOpticalMediaDetails(self, vios_dom):
        voms_dict = {}
        if len(vios_dom.xpath("//MediaRepositories/VirtualMediaRepository/OpticalMedia/VirtualOpticalMedia")) >= 1:
            voms = vios_dom.xpath("//MediaRepositories/VirtualMediaRepository/OpticalMedia/VirtualOpticalMedia")
            for vom_raw in voms:
                vom_dict = {}
                vom = etree.ElementTree(vom_raw)
                media_name = vom.xpath('//MediaName')[0].text
                vom_dict['MediaUDID'] = vom.xpath('//MediaUDID')[0].text
                vom_dict['MountType'] = vom.xpath('//MountType')[0].text
                vom_dict['Size'] = vom.xpath('//Size')[0].text
                voms_dict[media_name] = vom_dict
        return voms_dict

    def updateVIOSwithVODMappings(self, vios_UUID, vod_settings_list, lpar_UUID, partition_dom, timeout):
        payload = ""
        flag = False
        vios_dom = self.getVirtualIOServer(vios_UUID)
        vios_vscsi_dict = self.getVIOSSCSCIMappings_dictionary(vios_UUID)
        mapped_dvc_names = [item['TargetName'] for item in vios_vscsi_dict[1]]
        lpar_id = partition_dom.xpath("//PartitionID")[0].text
        vios_id = vios_dom.xpath("//PartitionID")[0].text
        vom_dict = self.getVIOSVirtualOpticalMediaDetails(vios_dom)
        for vod_settings in vod_settings_list:
            if vod_settings['device_name'] not in mapped_dvc_names:
                payload = self.build_SCSI_VOD_MappingPayload(vod_settings, lpar_UUID, lpar_id, vios_id, vom_dict)
                vSCSIMappingsTag = vios_dom.xpath("//VirtualSCSIMappings")[0]
                vSCSIMappingsTag.append(etree.XML(payload))
                flag = True
        if flag:
            self.updateVirtualIOServer(vios_dom, timeout)
        return flag

    def updateVirtualIOServer(self, vios_dom, timeout=None):
        header = {'X-API-Session': self.session,
                  'Accept': '*/*',
                  'Content-Type': 'application/vnd.ibm.powervm.uom+xml; type=VirtualIOServer'}

        vios_uuid = vios_dom.xpath('//AtomID')[0].text
        timeout_in_sec = 3600
        if timeout:
            if timeout > 60:
                timeout_in_sec = timeout * 60

            url = "https://{0}/rest/api/uom/VirtualIOServer/{1}?timeout={2}".format(
                  self.hmc_ip, vios_uuid, timeout)
        else:
            url = "https://{0}/rest/api/uom/VirtualIOServer/{1}".format(
                  self.hmc_ip, vios_uuid)

        vios_dom = vios_dom.xpath("//VirtualIOServer")[0]
        vios_xmlstr = etree.tostring(vios_dom)
        vios_xmlstr = vios_xmlstr.decode("utf-8").replace("VirtualIOServer", VIOS_NS, 1)
        logger.debug("INPUT PAYLOAD: \n %s", vios_xmlstr)
        resp = open_url(url,
                        headers=header,
                        method='POST',
                        data=vios_xmlstr,
                        validate_certs=False,
                        force_basic_auth=True,
                        timeout=timeout_in_sec)
        if resp.code != 200:
            logger.debug("Post operation failed. Respsonse code: %d", resp.code)
            return None
        response = resp.read()
        logger.debug("POST RESPONSE: \n %s", response)
        post_response = xml_strip_namespace(response)
        return post_response
