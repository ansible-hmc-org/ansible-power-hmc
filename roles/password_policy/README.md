Role Name
=========
This role is named as Password Policy management for power HMC. The scope of this role encompasses managing typical password policy requirements for the client's power Hardware Management Console (HMC). Key responsibilities include:
Creating and enforcing new password policies across multiple HMCs
Applying new password policy configurations to existing policies
Updating credentials for all locally authenticated HMC users except root and hscpe to comply with new policy


Requirements
------------
None


Role Variables
--------------
- password_policy_hmc_username:
    type: str
    required: true
    description: specifies the username of HMC that the password policy role is using.

- password_policy_hmc_password:
    type: str
    required: true
    description: specifies the logged in user's HMC password. For security purposes, it is highly recommended to store this sensitive information in an encrypted vault file.

- password_policy_name:
    type: str
    required: true
    description: specifies the password policy name for which we want the role to execute.

- password_policy_configs:
    type: dict
    required: true
    description: specifies the password policy configurations for a new policy or existing policy that needs to be changed.
    options:
      - min_pwage
      - pwage
      - min_length
      - hist_size
      - warn_pwage
      - min_digits
      - min_uppercase_chars
      - min_lowercase_chars
      - min_special_chars

- password_policy_user_password:
    type: str
    description: specifies the new password for the users in the HMC. For security purposes, it is highly recommended to store this sensitive information in an encrypted vault file.

- password_policy_password_change:
    type: boolean
    description: specifies whether to change the password for all the users in power HMC except the root, hscpe and logged in user according to the activated password policy. Default value is true.


Dependencies
------------
None


Example Playbook
----------------
- name: HMC Password Policy Management
  hosts: localhost
  gather_facts: false
  vars_files:
    - <secret_vars_path>
  roles:
    - <role_name>


License
-------
GPL-3.0-only


Author Information
------------------
- Manya Aeron
