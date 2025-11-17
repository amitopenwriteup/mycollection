# System Checks Collection

This collection provides modules and plugins to check Linux system configurations.

## Modules
- `system_check`: Check sudo users, NTP, and DNS configuration

## Installation
```bash
ansible-galaxy collection install mycompany.systemchecks
```

## Usage
```yaml
- hosts: all
  tasks:
    - name: Check system configuration
      mycompany.systemchecks.system_check:
        check_sudo: yes
        check_ntp: yes
        check_dns: yes
```


