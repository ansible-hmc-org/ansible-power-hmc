Role Name
=========

This Ansible role "Red Hat Linux Installation for IBM PowerVM" automates the process of installing Red Hat Enterprise Linux (RHEL) on IBM PowerVM logical partitions (LPARs) using a **network-based installation via TFTP boot**.

## Overview

There are multiple ways to install RHEL on IBM Power servers. This role focuses on automating the **TFTP-based network installation** method using Ansible. It sets up the necessary infrastructure and orchestrates the installation process end-to-end.

## Required Infrastructure

To perform the installation, the following components must be configured:

1. **HTTP (Repo) Server**  
   Hosts the RHEL distribution files and serves them via HTTP. This can be a dedicated server with multiple distro builds or a simple HTTP server with the required build.

2. **PXE Server**  
   Runs both `tftpd` and `dhcpd` services. This role will configure these services if they are not already running.

3. **LPAR (Logical Partition)**  
   The target system where RHEL will be installed.

## Role Workflow

1. **PXE Server Setup**  
   - Checks for running DHCP and TFTP services.
   - If not found, configures and enables them.
   - DHCP configuration is dynamically generated based on the subnet of the target LPAR using the `dhcp_server_conf.j2` template.
   - TFTP is configured to serve files from `/var/lib/tftpboot`.

2. **Kickstart File Generation**  
   - A kickstart file is created on the HTTP server containing the installation configuration.

3. **Boot File Preparation**  
   - Required boot files are downloaded to the PXE server.
   - A GRUB configuration file is generated using the kickstart file.

4. **Network Boot Trigger**  
   - The `lpar_netboot` command is executed from the HMC to initiate a network boot on the LPAR.
   - The LPAR sends a BOOTP request to the PXE server and begins the OS installation.

5. **Post-Installation Validation**
   - After installation, the role prints the OS distribution name and version installed on the LPAR to verify success.


Role Variables
--------------

1. distro:  
   * type: str
   * required: true
   * description: Redhat distribution version in format Redhat9.3

2. repo_port:
   * type: str
   * required: optional
   * description: The port in which http server is hosting the redhat repository like "81" and is used in roles as http://abc.com:81/

3. repo_dir:
   * type: str
   * required: optional
   * description: The path in which http server is hosting the redhat repository, can be in default path /var/www/html/ a directory "crtl". Specify in        format "crtl", this is used in roles as http://abc.com:81/crtl/

4. curr_hmc_auth:
   * type: str
   * required: true
   * description: Username and Password to login to HMC system, For security purposes, it is highly recommended to store this sensitive information in        an encrypted secret vault file.

5. host_ip/host_gw/host_subnet/host_netmask: 
   * type: str
   * required: true
   * description: lpar Network details in format 9.9.9.9

6. dns_ip: 
   * type: str
   * required: true
   * description: Nameserver IP details in format 9.1.1.1

7. hostname: 
   * type: str
   * required: true
   * description: hostname of the lpar in format aaa.abc.com

8. lpar_name: 
   * type: str
   * required: true
   * desription: name of lpar as in the HMC 

9. hardware_ethernet: 
   * type: str
   * required: true
   * description: MAC address of the lpar in format ff:ff:ff:ff

10. managed_system: 
    * type: str
    * required: true
    * description: system name in HMC in which lpar is available 

Example Playbook
----------------
        ---
        - name: Redhat Install linux
          hosts: localhost
          collections:
            - ibm.power_hmc
          gather_facts: false
          roles:
            - role: redhat_linux_install
              vars:
                host_ip: 9.9.9.9
                host_gw: 9.9.9.1
                host_subnet: 9.9.9.0
                host_netmask: 255.255.255.0
                dns_ip: 9.1.1.1
                hostname: aaa.abc.com
                lpar_name: name_in_hmc
                hardware_ethernet: ff:ff:ff:ff
                managed_system: system_name_in_HMC

Inventory file with detials of pxe server, repository server and HMC server is required while running the playbook
---------
For security purposes, it is highly recommended to store this sensitive information in an encrypted secret vault file.
        
	[repo]
        repo_server  ansible_host=9.4.4.4 ansible_user=abc ansible_password=1234
        [pxe]
        pxe_server   ansible_host=9.3.3.3 ansible_user=abc ansible_password=1234
        [hmcs]
        hmc_server   ansible_host=hmc.com

-----------
License
-------

GPL-3.0-only

Author Information
------------------

Spoorthy S

