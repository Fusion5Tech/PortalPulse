import os
import subprocess

class FirewallService:
    async def allow_access(self, rule):
        # Placeholder for iptables/nftables command
        subprocess.run(["iptables", "-I", "FORWARD", "-s", rule.ip_address, "-j", "ACCEPT"])
        return rule

    async def block_access(self, rule):
        # Placeholder for iptables/nftables command
        subprocess.run(["iptables", "-I", "FORWARD", "-s", rule.ip_address, "-j", "DROP"])
        return rule
