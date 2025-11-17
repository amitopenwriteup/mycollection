#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r'''
---
module: system_check
short_description: Check Linux system configuration
description:
    - Check sudo users, NTP status, and DNS configuration
options:
    check_sudo:
        description: Check sudo users
        required: false
        type: bool
        default: true
    check_ntp:
        description: Check NTP service status
        required: false
        type: bool
        default: true
    check_dns:
        description: Check DNS configuration
        required: false
        type: bool
        default: true
author:
    - System Admin Team
'''

EXAMPLES = r'''
- name: Check all system configurations
  mycompany.systemchecks.system_check:
    check_sudo: yes
    check_ntp: yes
    check_dns: yes

- name: Check only sudo users
  mycompany.systemchecks.system_check:
    check_sudo: yes
    check_ntp: no
    check_dns: no
'''

RETURN = r'''
sudo_users:
    description: List of users with sudo access
    type: list
    returned: when check_sudo is true
ntp_status:
    description: NTP service status
    type: dict
    returned: when check_ntp is true
dns_servers:
    description: Configured DNS servers
    type: list
    returned: when check_dns is true
'''

from ansible.module_utils.basic import AnsibleModule
import os
import subprocess

def get_sudo_users():
    """Get list of users with sudo access"""
    sudo_users = []
    try:
        # Check /etc/sudoers and /etc/sudoers.d/
        with open('/etc/group', 'r') as f:
            for line in f:
                if line.startswith('sudo:') or line.startswith('wheel:'):
                    parts = line.strip().split(':')
                    if len(parts) >= 4:
                        users = parts[3].split(',')
                        sudo_users.extend([u for u in users if u])
        return list(set(sudo_users))
    except Exception as e:
        return []

def check_ntp_status():
    """Check NTP service status"""
    status = {
        'service': 'unknown',
        'active': False,
        'synchronized': False
    }
    
    try:
        # Check systemd-timesyncd
        result = subprocess.run(['systemctl', 'is-active', 'systemd-timesyncd'],
                              capture_output=True, text=True)
        if result.returncode == 0:
            status['service'] = 'systemd-timesyncd'
            status['active'] = True
        
        # Check chronyd
        result = subprocess.run(['systemctl', 'is-active', 'chronyd'],
                              capture_output=True, text=True)
        if result.returncode == 0:
            status['service'] = 'chronyd'
            status['active'] = True
        
        # Check ntpd
        result = subprocess.run(['systemctl', 'is-active', 'ntpd'],
                              capture_output=True, text=True)
        if result.returncode == 0:
            status['service'] = 'ntpd'
            status['active'] = True
        
        # Check time sync status
        result = subprocess.run(['timedatectl', 'status'],
                              capture_output=True, text=True)
        if 'synchronized: yes' in result.stdout.lower():
            status['synchronized'] = True
            
    except Exception as e:
        status['error'] = str(e)
    
    return status

def get_dns_servers():
    """Get configured DNS servers"""
    dns_servers = []
    
    try:
        # Check /etc/resolv.conf
        with open('/etc/resolv.conf', 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('nameserver'):
                    parts = line.split()
                    if len(parts) >= 2:
                        dns_servers.append(parts[1])
    except Exception as e:
        pass
    
    return dns_servers

def main():
    module = AnsibleModule(
        argument_spec=dict(
            check_sudo=dict(type='bool', default=True),
            check_ntp=dict(type='bool', default=True),
            check_dns=dict(type='bool', default=True),
        ),
        supports_check_mode=True
    )
    
    result = {
        'changed': False,
        'checks_performed': []
    }
    
    # Check sudo users
    if module.params['check_sudo']:
        result['sudo_users'] = get_sudo_users()
        result['checks_performed'].append('sudo')
    
    # Check NTP
    if module.params['check_ntp']:
        result['ntp_status'] = check_ntp_status()
        result['checks_performed'].append('ntp')
    
    # Check DNS
    if module.params['check_dns']:
        result['dns_servers'] = get_dns_servers()
        result['checks_performed'].append('dns')
    
    module.exit_json(**result)

if __name__ == '__main__':
    main()

