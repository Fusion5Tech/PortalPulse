import subprocess


class FirewallService:
    async def allow_access(self, rule):
        # Placeholder for iptables/nftables command
        subprocess.run(
            ["iptables", "-I", "FORWARD", "-s", rule.ip_address, "-j", "ACCEPT"],
            check=False,
        )
        return rule

    async def block_access(self, rule):
        # Placeholder for iptables/nftables command
        subprocess.run(
            ["iptables", "-I", "FORWARD", "-s", rule.ip_address, "-j", "DROP"],
            check=False,
        )
        return rule
