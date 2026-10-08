# -*- coding: utf-8 -*-
from __future__ import annotations
COMMON = [
    ("show version", "نسخه"), ("show running-config", "config"), ("show ip interface brief", "IF"),
    ("show ip route", "route"), ("show logging | last 50", "log"),
    ("copy running-config startup-config", "save"), ("configure terminal", "conf t"), ("end", "end"),
]
_BASE = [
    ("show vlan brief", "vlan"), ("show interfaces trunk", "trunk"),
    ("show ip ospf neighbor", "ospf nbr"), ("show ip bgp summary", "bgp"),
    ("show ip nat translations", "nat"), ("show crypto isakmp sa", "ike"),
    ("show access-lists", "acl"), ("show spanning-tree", "stp"),
    ("ip -br a", "linux IF"), ("ss -tulpn", "sockets"), ("tcpdump -i any -nn -c 20", "pcap"),
    ("ipconfig /all", "win IP"), ("Get-NetTCPConnection", "win TCP"),
    ("ansible all -m ping", "ansible ping"), ("ansible-playbook site.yml --check", "check"),
    ("terraform plan", "tf plan"), ("terraform apply", "tf apply"),
    ("from netmiko import ConnectHandler", "netmiko"),
    ("EXPLAIN ANALYZE SELECT 1", "sql explain"),
    ("requests.get(url, timeout=15)", "http get"),
]
BANKS = {k: list(_BASE) for k in (
    "vlan","ospf","bgp","nat","vpn","dhcp","firewall","stp","linux","windows","ha","acl","qos",
    "wireless","ansible","terraform","python","sql","scrape","general"
)}
BANKS["ansible"] = [
    ("ansible --version", "ver"), ("ansible all -m ping", "ping"),
    ("ansible-playbook site.yml --check --diff", "check"),
    ("ansible-vault encrypt group_vars/all/vault.yml", "vault"),
    ("ansible-galaxy collection install cisco.ios", "collection"),
] + BANKS["ansible"]
BANKS["python"] = [
    ("python -m venv .venv", "venv"), ("pip install netmiko nornir scrapli", "pip"),
    ("from netmiko import ConnectHandler", "import"),
    ("conn.send_command('show version')", "show"),
] + BANKS["python"]
BANKS["sql"] = [
    ("EXPLAIN ANALYZE SELECT * FROM t WHERE id=1", "explain"),
    ("CREATE INDEX idx ON t(col)", "index"),
    ("pg_dump -Fc db > b.dump", "dump"),
] + BANKS["sql"]
ERRORS = {
    "vlan": [("VLAN اشتباه", "access/native", "show vlan brief")],
    "ospf": [("Neighbor down", "area/timer", "show ip ospf neighbor")],
    "ansible": [("UNREACHABLE", "SSH/creds", "ansible all -m ping -vvv")],
    "python": [("Auth fail", "device_type", "session_log")],
    "sql": [("Slow query", "index", "EXPLAIN ANALYZE")],
}
