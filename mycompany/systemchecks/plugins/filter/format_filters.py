# ==========================================
# FILE: plugins/filter/format_filters.py
# ==========================================
#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Custom filters for system check results"""

def format_sudo_list(users):
    """Format sudo users list"""
    if not users:
        return "No sudo users found"
    return "Sudo users: " + ", ".join(users)

def format_ntp_status(status):
    """Format NTP status"""
    if not status:
        return "NTP status unknown"
    
    service = status.get('service', 'unknown')
    active = status.get('active', False)
    synced = status.get('synchronized', False)
    
    result = "Service: {} | ".format(service)
    result += "Active: {} | ".format('Yes' if active else 'No')
    result += "Synchronized: {}".format('Yes' if synced else 'No')
    
    return result

def format_dns_list(servers):
    """Format DNS servers list"""
    if not servers:
        return "No DNS servers configured"
    return "DNS servers: " + ", ".join(servers)

class FilterModule(object):
    """Ansible filter plugin"""
    
    def filters(self):
        """Return filter mappings"""
        return {
            'format_sudo_list': format_sudo_list,
            'format_ntp_status': format_ntp_status,
            'format_dns_list': format_dns_list
        }
