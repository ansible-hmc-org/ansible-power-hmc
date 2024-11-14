Role Name
=========
This role is named as Password Policy management for power HMC, which assists in managing the lifecycle of password policies in power HMC.


Requirements
------------
None


Role Variables
--------------
- password_policy_username:
    type: str
    required: true
    description: specifies the username of HMC that the password policy role is using

- password_policy_configs:
    type: dict
    required: true
    description: specifies the password policy configurations for a new policy
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

- password_policy_new_configs:
    type: dict
    required: true
    description: specifies the updated password policy configurations for an existing policy
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

- password_policy_name:
    type: str
    required: true
    description: specifies the password policy name for which we want the role to execute

- password_policy_users:
    type: list
    required: true
    description: specifies the list of users present in the HMC
    options:
      - name
        taskrole
        authentication_type
        remote_ssh_access

- password_policy_user_pass:
    type: list
    required: true
    description: specifies the existing and new password details for the users in the HMC
    options:
      - passwd
        current_passwd

- password_policy_hmc_pass:
    type: str
    required: true
    description: specifies the HMC password 


Dependencies
------------
None


Example Playbook
----------------
- name: HMC Password Policy Management
  hosts: localhost
  gather_facts: false
  vars_files:
    - <var_files>
  roles:
    - <role_name>


License
-------
GPL-3.0-only


Author Information
------------------
- Manya Aeron
