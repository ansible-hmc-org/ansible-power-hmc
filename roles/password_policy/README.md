Role Name
=========
This role is named as Password Policy management for power HMC. It assists in checking if a password policy exists in a power HMC and modify it with new configurations or else creating a new password policy if it doesn't exist. It checks the users present in the power HMC with a specific task role and allows the users update their password according to the updated policy.


Requirements
------------
None


Role Variables
--------------
- password_policy_hmc_username:
    type: str
    required: true
    description: specifies the username of HMC that the password policy role is using

- password_policy_configs:
    type: dict
    required: true
    description: specifies the password policy configurations for a new policy or existing policy that needs to be changed
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

- password_policy_user_password:
    type: list
    required: true
    description: specifies the existing and new password details for the users in the HMC. It can be stored in secrets.yml file in vars folder and can be encrypted using ansible-vault.
    options:
      - passwd
        current_passwd

- password_policy_hmc_password:
    type: str
    required: true
    description: specifies the HMC password.It can be stored in secrets.yml file in vars folder and can be encrypted using ansible-vault.


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
