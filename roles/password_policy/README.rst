Role Name
=========

This role is named as Password Policy management for power HMC. The
scope of this role encompasses managing typical password policy
requirements for the client’s power Hardware Management Console (HMC).
Key responsibilities include: - Creating and enforcing new password
policies across multiple HMCs - Applying new password policy
configurations to existing policies - Updating credentials for all
locally authenticated HMC users except root and hscpe to comply with new
policy

Requirements
------------

None

Role Variables
--------------

1. password_policy_hmc_username:

   -  type: str
   -  required: true
   -  description: specifies the username of HMC that the password
      policy role is using.

2. password_policy_hmc_password:

   -  type: str
   -  required: true
   -  description: specifies the logged in user’s HMC password. For
      security purposes, it is highly recommended to store this
      sensitive information in an encrypted secret vault file.

3. password_policy_name:

   -  type: str
   -  required: true
   -  description: specifies the password policy name for which we want
      the role to execute.

4. password_policy_configs:

   -  type: dict
   -  required: true
   -  description: specifies the password policy configurations for a
      new policy or existing policy that needs to be changed. options:

      -  min_pwage
      -  pwage
      -  min_length
      -  hist_size
      -  warn_pwage
      -  min_digits
      -  min_uppercase_chars
      -  min_lowercase_chars
      -  min_special_chars

5. password_policy_user_password:

   -  type: dict
   -  description: specifies the new password for the users in the HMC.
      For security purposes, it is highly recommended to store this
      sensitive information in an encrypted secret vault file. Required
      only when password_policy_password_change is true. options:

      -  passwd

6. password_policy_password_change:

   -  type: boolean
   -  required: false
   -  description: specifies whether to change the password for all the
      users in power HMC except the root, hscpe and logged in user
      according to the activated password policy. Default value is true.

Dependencies
------------

None

Example Playbook
----------------

::

   - name: Create/update/apply a password policy, and modify the credentials of the local power HMC users if desired
     hosts: hmcs
     connection: local
     collections:
       - ibm.power_hmc
     gather_facts: false
     vars_files:
       - 
     roles:
       - role: password_policy
         vars:
           password_policy_name: 
           password_policy_configs:
               min_pwage: 
               pwage: 
               min_length: 
               hist_size: 
               warn_pwage: 
               min_digits: 
               min_uppercase_chars: 
               min_lowercase_chars: 
               min_special_chars: 

License
-------

GPL-3.0-only

Author Information
------------------

-  Manya Aeron
