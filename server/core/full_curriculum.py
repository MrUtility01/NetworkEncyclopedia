# -*- coding: utf-8 -*-
"""v1.0 Dense — ۶۰ فصل | زیر‌فصل متراکم | L0-L4 | سناریوهای سازمانی"""
import re

LEVELS = [
    ("L0", "آشنایی", "Intro"),
    ("L1", "مقدماتی", "Junior"),
    ("L2", "ادمین", "Admin"),
    ("L3", "مهندس", "Senior"),
    ("L4", "خبره", "Architect"),
]

def _expand(topic_fa, topic_en=""):
    return [
        (f"[{c}] {topic_fa} — {fl}", f"[{c}] {topic_en or topic_fa} — {el}")
        for c, fl, el in LEVELS
    ]

def _sub(title, topics):
    lessons = []
    for t in topics:
        fa, en = (t if isinstance(t, tuple) else (t, ""))
        lessons.extend(_expand(fa, en))
    return (title, lessons)

def get_full_curriculum():
    C = []

    levels = []
    levels.append(_sub('۱.۱ پردازنده', [
        ('CPU چیست و چگونه کار می\u200cکند', 'CPU چیست و چگونه کار می\u200cکند'),
        ('ALU و CU', 'ALU و CU'),
        ('Register و Pipeline', 'Register و Pipeline'),
        ('Clock و فرکانس', 'Clock و فرکانس'),
        ('Core و Thread', 'Core و Thread'),
        ('Hyper-Threading SMT', 'Hyper-Threading SMT'),
        ('کش L1 L2 L3', 'کش L1 L2 L3'),
        ('Instruction Set x86', 'Instruction Set x86'),
        ('x64 و ARM', 'x64 و ARM'),
        ('RISC در برابر CISC', 'RISC در برابر CISC'),
        ('معیارهای انتخاب CPU سازمانی', 'معیارهای انتخاب CPU سازمانی'),
    ]))
    levels.append(_sub('۱.۲ مادربرد', [
        ('Chipset نقش آن', 'Chipset نقش آن'),
        ('سوکت و سازگاری', 'سوکت و سازگاری'),
        ('PCIe نسل\u200cها', 'PCIe نسل\u200cها'),
        ('اسلات توسعه', 'اسلات توسعه'),
        ('M.2 و SATA', 'M.2 و SATA'),
        ('USB و هدرها', 'USB و هدرها'),
        ('TPM و امنیت سخت\u200cافزار', 'TPM و امنیت سخت\u200cافزار'),
        ('NIC آنبورد', 'NIC آنبورد'),
        ('BIOS تراشه', 'BIOS تراشه'),
        ('فرم\u200cفاکتور ATX mATX', 'فرم\u200cفاکتور ATX mATX'),
    ]))
    levels.append(_sub('۱.۳ حافظه', [
        ('RAM انواع', 'RAM انواع'),
        ('DDR4 در برابر DDR5', 'DDR4 در برابر DDR5'),
        ('ECC و Registered', 'ECC و Registered'),
        ('کانال Dual Quad', 'کانال Dual Quad'),
        ('تایمینگ و XMP', 'تایمینگ و XMP'),
        ('ظرفیت سازمانی', 'ظرفیت سازمانی'),
        ('عیب\u200cیابی RAM', 'عیب\u200cیابی RAM'),
    ]))
    levels.append(_sub('۱.۴ ذخیره\u200cسازی پایه', [
        ('HDD مکانیک', 'HDD مکانیک'),
        ('SATA SSD', 'SATA SSD'),
        ('NVMe M.2', 'NVMe M.2'),
        ('U.2 سازمانی', 'U.2 سازمانی'),
        ('IOPS و Latency', 'IOPS و Latency'),
        ('TBW و DWPD', 'TBW و DWPD'),
        ('انتخاب دیسک سرور', 'انتخاب دیسک سرور'),
    ]))
    levels.append(_sub('۱.۵ تغذیه', [
        ('محاسبه توان PSU', 'محاسبه توان PSU'),
        ('80Plus و راندمان', '80Plus و راندمان'),
        ('ریل\u200cهای برق', 'ریل\u200cهای برق'),
        ('UPS آنلاین', 'UPS آنلاین'),
        ('PDU رک', 'PDU رک'),
        ('توزیع برق اتاق سرور', 'توزیع برق اتاق سرور'),
    ]))
    C.append((1, 'فصل ۰۱: مبانی IT و معماری کامپیوتر', 'Ch01 Architecture', levels))

    levels = []
    levels.append(_sub('۲.۱ اسمبل دسکتاپ', [
        ('ESD و ایمنی', 'ESD و ایمنی'),
        ('نصب CPU و خمیر حرارتی', 'نصب CPU و خمیر حرارتی'),
        ('نصب خنک\u200cکننده', 'نصب خنک\u200cکننده'),
        ('نصب RAM', 'نصب RAM'),
        ('نصب NVMe و SSD', 'نصب NVMe و SSD'),
        ('نصب کارت توسعه', 'نصب کارت توسعه'),
        ('کابل\u200cکشی مدیریت\u200cشده', 'کابل\u200cکشی مدیریت\u200cشده'),
        ('اولین روشن شدن', 'اولین روشن شدن'),
    ]))
    levels.append(_sub('۲.۲ POST و عیب\u200cیابی', [
        ('Beep Codes', 'Beep Codes'),
        ('Q-Code و LED', 'Q-Code و LED'),
        ('No Power', 'No Power'),
        ('No POST', 'No POST'),
        ('ریستارت مکرر', 'ریستارت مکرر'),
        ('گرمای بیش از حد', 'گرمای بیش از حد'),
        ('BSOD سخت\u200cافزاری', 'BSOD سخت\u200cافزاری'),
        ('دیسک خراب', 'دیسک خراب'),
    ]))
    levels.append(_sub('۲.۳ نگهداری', [
        ('تمیزکاری سیستم', 'تمیزکاری سیستم'),
        ('تعویض خمیر', 'تعویض خمیر'),
        ('بروزرسانی فریمور', 'بروزرسانی فریمور'),
        ('برنامه نگهداری پیشگیرانه', 'برنامه نگهداری پیشگیرانه'),
    ]))
    levels.append(_sub('۲.۴ سرور HP', [
        ('خانواده ProLiant', 'خانواده ProLiant'),
        ('نسل\u200cهای Gen', 'نسل\u200cهای Gen'),
        ('iLO نصب و دسترسی', 'iLO نصب و دسترسی'),
        ('iLO کاربران و Directory', 'iLO کاربران و Directory'),
        ('Smart Array کنترلر', 'Smart Array کنترلر'),
        ('آرایه\u200cهای RAID در HP', 'آرایه\u200cهای RAID در HP'),
        ('HPE OneView مبانی', 'HPE OneView مبانی'),
        ('عیب\u200cیابی سخت\u200cافزار سرور', 'عیب\u200cیابی سخت\u200cافزار سرور'),
    ]))
    C.append((2, 'فصل ۰۲: اسمبل، عیب\u200cیابی و سرورهای سازمانی', 'Ch02 Assembly HW', levels))

    levels = []
    levels.append(_sub('۳.۱ فریمور', [
        ('BIOS سنتی', 'BIOS سنتی'),
        ('UEFI ساختار', 'UEFI ساختار'),
        ('Secure Boot', 'Secure Boot'),
        ('CSM', 'CSM'),
        ('TPM در فریمور', 'TPM در فریمور'),
        ('Virtualization VT-x AMD-V', 'Virtualization VT-x AMD-V'),
        ('SATA Mode AHCI RAID', 'SATA Mode AHCI RAID'),
    ]))
    levels.append(_sub('۳.۲ فرآیند بوت', [
        ('زنجیره POST تا OS', 'زنجیره POST تا OS'),
        ('Boot Order', 'Boot Order'),
        ('PXE Boot', 'PXE Boot'),
        ('MBR محدودیت', 'MBR محدودیت'),
        ('GPT و ESP', 'GPT و ESP'),
        ('Windows BCD', 'Windows BCD'),
        ('GRUB2', 'GRUB2'),
        ('systemd-boot', 'systemd-boot'),
        ('بازیابی بوت خراب', 'بازیابی بوت خراب'),
    ]))
    C.append((3, 'فصل ۰۳: BIOS UEFI و بوت', 'Ch03 Boot', levels))

    levels = []
    levels.append(_sub('۴.۱ مفاهیم OS', [
        ('Kernel', 'Kernel'),
        ('User Space', 'User Space'),
        ('Process', 'Process'),
        ('Thread', 'Thread'),
        ('Scheduler', 'Scheduler'),
        ('Service Daemon', 'Service Daemon'),
        ('Syscall', 'Syscall'),
    ]))
    levels.append(_sub('۴.۲ ویندوز پایه', [
        ('Registry', 'Registry'),
        ('Services.msc', 'Services.msc'),
        ('Event Viewer', 'Event Viewer'),
        ('Task Manager', 'Task Manager'),
        ('Resource Monitor', 'Resource Monitor'),
        ('Safe Mode', 'Safe Mode'),
    ]))
    levels.append(_sub('۴.۳ لینوکس پایه', [
        ('سلسله\u200cمراتب FS', 'سلسله\u200cمراتب FS'),
        ('Permission chmod', 'Permission chmod'),
        ('Process ps top', 'Process ps top'),
        ('journalctl پایه', 'journalctl پایه'),
    ]))
    levels.append(_sub('۴.۴ عیب\u200cیابی منابع', [
        ('CPU بالا', 'CPU بالا'),
        ('RAM پر', 'RAM پر'),
        ('Disk IO', 'Disk IO'),
        ('Network Bottleneck', 'Network Bottleneck'),
    ]))
    C.append((4, 'فصل ۰۴: سیستم\u200cعامل پایه', 'Ch04 OS', levels))

    levels = []
    levels.append(_sub('۵.۱ ویندوز FS', [
        ('FAT32 exFAT', 'FAT32 exFAT'),
        ('NTFS ساختار', 'NTFS ساختار'),
        ('ACL و Permission', 'ACL و Permission'),
        ('Compression EFS', 'Compression EFS'),
        ('ReFS', 'ReFS'),
    ]))
    levels.append(_sub('۵.۲ لینوکس FS', [
        ('ext4', 'ext4'),
        ('XFS', 'XFS'),
        ('Btrfs Snapshot', 'Btrfs Snapshot'),
        ('ZFS مبانی', 'ZFS مبانی'),
        ('Swap', 'Swap'),
    ]))
    levels.append(_sub('۵.۳ پارتیشن', [
        ('MBR GPT', 'MBR GPT'),
        ('diskpart', 'diskpart'),
        ('fdisk parted', 'fdisk parted'),
        ('LVM PV VG LV', 'LVM PV VG LV'),
        ('Mount fstab', 'Mount fstab'),
    ]))
    levels.append(_sub('۵.۴ RAID', [
        ('RAID 0', 'RAID 0'),
        ('RAID 1', 'RAID 1'),
        ('RAID 5', 'RAID 5'),
        ('RAID 6', 'RAID 6'),
        ('RAID 10', 'RAID 10'),
        ('انتخاب RAID سازمانی', 'انتخاب RAID سازمانی'),
    ]))
    C.append((5, 'فصل ۰۵: فایل\u200cسیستم و Storage پایه', 'Ch05 FS', levels))

    levels = []
    levels.append(_sub('۶.۱ انواع شبکه', [
        ('LAN', 'LAN'),
        ('WAN', 'WAN'),
        ('MAN', 'MAN'),
        ('PAN', 'PAN'),
        ('Internet', 'Internet'),
        ('Intranet Extranet', 'Intranet Extranet'),
        ('SDN مفهوم', 'SDN مفهوم'),
    ]))
    levels.append(_sub('۶.۲ مدل OSI', [
        ('لایه فیزیکی', 'لایه فیزیکی'),
        ('لایه پیوند داده', 'لایه پیوند داده'),
        ('لایه شبکه', 'لایه شبکه'),
        ('لایه انتقال', 'لایه انتقال'),
        ('لایه نشست', 'لایه نشست'),
        ('لایه ارائه', 'لایه ارائه'),
        ('لایه کاربرد', 'لایه کاربرد'),
        ('مقایسه OSI و TCP/IP', 'مقایسه OSI و TCP/IP'),
    ]))
    levels.append(_sub('۶.۳ TCP/IP', [
        ('مدل چهار لایه', 'مدل چهار لایه'),
        ('Encapsulation Decapsulation', 'Encapsulation Decapsulation'),
        ('PDU در هر لایه', 'PDU در هر لایه'),
    ]))
    levels.append(_sub('۶.۴ آدرس و ترافیک', [
        ('MAC Address', 'MAC Address'),
        ('IPv4 مقدمه', 'IPv4 مقدمه'),
        ('IPv6 مقدمه', 'IPv6 مقدمه'),
        ('Unicast', 'Unicast'),
        ('Broadcast', 'Broadcast'),
        ('Multicast', 'Multicast'),
        ('Anycast', 'Anycast'),
    ]))
    levels.append(_sub('۶.۵ Packet Journey', [
        ('مسیر بسته از App تا کابل', 'مسیر بسته از App تا کابل'),
        ('مسیر برگشت', 'مسیر برگشت'),
        ('نقاط شکست رایج', 'نقاط شکست رایج'),
    ]))
    C.append((6, 'فصل ۰۶: مبانی شبکه', 'Ch06 Net Fund', levels))

    levels = []
    levels.append(_sub('۷.۱ فریم', [
        ('ساختار فریم اترنت', 'ساختار فریم اترنت'),
        ('EtherType', 'EtherType'),
        ('FCS', 'FCS'),
        ('Jumbo Frame', 'Jumbo Frame'),
    ]))
    levels.append(_sub('۷.۲ MAC Table', [
        ('Learning', 'Learning'),
        ('Aging', 'Aging'),
        ('Forwarding', 'Forwarding'),
        ('Flooding', 'Flooding'),
        ('CAM Overflow', 'CAM Overflow'),
    ]))
    levels.append(_sub('۷.۳ سوییچ', [
        ('Store-and-Forward', 'Store-and-Forward'),
        ('Cut-Through', 'Cut-Through'),
        ('Collision Domain', 'Collision Domain'),
        ('Broadcast Domain', 'Broadcast Domain'),
    ]))
    levels.append(_sub('۷.۴ سرعت و استاندارد', [
        ('100M 1G 10G', '100M 1G 10G'),
        ('25G 40G 100G', '25G 40G 100G'),
        ('Auto Negotiation', 'Auto Negotiation'),
        ('Speed Duplex', 'Speed Duplex'),
    ]))
    C.append((7, 'فصل ۰۷: اترنت و سوییچینگ پایه', 'Ch07 Ethernet', levels))

    levels = []
    levels.append(_sub('۸.۱ IPv4', [
        ('ساختار آدرس', 'ساختار آدرس'),
        ('کلاس\u200cها و چرا منسوخ', 'کلاس\u200cها و چرا منسوخ'),
        ('Network Broadcast Host', 'Network Broadcast Host'),
        ('Private RFC1918', 'Private RFC1918'),
        ('APIPA', 'APIPA'),
    ]))
    levels.append(_sub('۸.۲ ساب\u200cنتینگ', [
        ('Subnet Mask', 'Subnet Mask'),
        ('CIDR', 'CIDR'),
        ('VLSM', 'VLSM'),
        ('FLSM', 'FLSM'),
        ('Summarization', 'Summarization'),
        ('تمرین طرح آدرس', 'تمرین طرح آدرس'),
    ]))
    levels.append(_sub('۸.۳ IPv6', [
        ('ساختار 128 بیتی', 'ساختار 128 بیتی'),
        ('Global Unicast', 'Global Unicast'),
        ('Link-Local', 'Link-Local'),
        ('ULA', 'ULA'),
        ('Multicast IPv6', 'Multicast IPv6'),
        ('SLAAC', 'SLAAC'),
        ('DHCPv6', 'DHCPv6'),
        ('NDP', 'NDP'),
    ]))
    levels.append(_sub('۸.۴ طرح سازمانی', [
        ('سگمنت Users', 'سگمنت Users'),
        ('Servers', 'Servers'),
        ('Voice', 'Voice'),
        ('CCTV', 'CCTV'),
        ('Management', 'Management'),
        ('Guest', 'Guest'),
        ('IoT', 'IoT'),
        ('Security DMZ', 'Security DMZ'),
    ]))
    C.append((8, 'فصل ۰۸: IPv4 IPv6 ساب\u200cنتینگ', 'Ch08 IP', levels))

    levels = []
    levels.append(_sub('۹.۱ ARP', [
        ('Request Reply', 'Request Reply'),
        ('Cache', 'Cache'),
        ('Gratuitous ARP', 'Gratuitous ARP'),
        ('Proxy ARP', 'Proxy ARP'),
        ('ARP Spoofing', 'ARP Spoofing'),
    ]))
    levels.append(_sub('۹.۲ ICMP', [
        ('Echo', 'Echo'),
        ('Destination Unreachable', 'Destination Unreachable'),
        ('TTL Exceeded', 'TTL Exceeded'),
        ('Path MTU Discovery', 'Path MTU Discovery'),
        ('Traceroute', 'Traceroute'),
    ]))
    levels.append(_sub('۹.۳ TCP', [
        ('Three-way Handshake', 'Three-way Handshake'),
        ('Four-way Termination', 'Four-way Termination'),
        ('Sequence ACK', 'Sequence ACK'),
        ('Window Size', 'Window Size'),
        ('Retransmission', 'Retransmission'),
        ('Congestion', 'Congestion'),
        ('SYN Flood', 'SYN Flood'),
        ('RST', 'RST'),
    ]))
    levels.append(_sub('۹.۴ UDP', [
        ('ویژگی\u200cها', 'ویژگی\u200cها'),
        ('DNS روی UDP', 'DNS روی UDP'),
        ('DHCP', 'DHCP'),
        ('VoIP RTP', 'VoIP RTP'),
        ('مقایسه TCP UDP', 'مقایسه TCP UDP'),
    ]))
    C.append((9, 'فصل ۰۹: ARP ICMP TCP UDP', 'Ch09 Protocols', levels))

    levels = []
    levels.append(_sub('۱۰.۱ مبانی', [
        ('Resolver', 'Resolver'),
        ('Recursive Query', 'Recursive Query'),
        ('Iterative', 'Iterative'),
        ('Authoritative', 'Authoritative'),
        ('Root TLD', 'Root TLD'),
    ]))
    levels.append(_sub('۱۰.۲ رکوردها', [
        ('A AAAA', 'A AAAA'),
        ('CNAME', 'CNAME'),
        ('MX', 'MX'),
        ('NS', 'NS'),
        ('PTR', 'PTR'),
        ('TXT', 'TXT'),
        ('SRV', 'SRV'),
        ('SOA', 'SOA'),
        ('CAA', 'CAA'),
    ]))
    levels.append(_sub('۱۰.۳ سازمانی', [
        ('Split-Horizon DNS', 'Split-Horizon DNS'),
        ('Conditional Forwarder', 'Conditional Forwarder'),
        ('Delegation', 'Delegation'),
        ('Stub Zone', 'Stub Zone'),
        ('Cache', 'Cache'),
    ]))
    levels.append(_sub('۱۰.۴ امنیت', [
        ('DNSSEC', 'DNSSEC'),
        ('DNS Filtering', 'DNS Filtering'),
        ('DNS Tunneling', 'DNS Tunneling'),
        ('DDoS روی DNS', 'DDoS روی DNS'),
    ]))
    C.append((10, 'فصل ۱۰: DNS', 'Ch10 DNS', levels))

    levels = []
    levels.append(_sub('۱۱.۱ DHCP', [
        ('DORA', 'DORA'),
        ('Lease', 'Lease'),
        ('Renewal', 'Renewal'),
        ('Reservation', 'Reservation'),
    ]))
    levels.append(_sub('۱۱.۲ Options', [
        ('Router Option', 'Router Option'),
        ('DNS Option', 'DNS Option'),
        ('Domain', 'Domain'),
        ('NTP', 'NTP'),
        ('PXE Options', 'PXE Options'),
    ]))
    levels.append(_sub('۱۱.۳ سازمانی', [
        ('DHCP Relay', 'DHCP Relay'),
        ('Failover', 'Failover'),
        ('Superscope', 'Superscope'),
        ('Conflict Detection', 'Conflict Detection'),
    ]))
    levels.append(_sub('۱۱.۴ IPAM', [
        ('مفهوم IPAM', 'مفهوم IPAM'),
        ('یکپارچگی DHCP DNS', 'یکپارچگی DHCP DNS'),
        ('ابزارهای IPAM', 'ابزارهای IPAM'),
    ]))
    C.append((11, 'فصل ۱۱: DHCP و IPAM', 'Ch11 DHCP', levels))

    levels = []
    levels.append(_sub('۱۲.۱ مسی', [
        ('Cat5e Cat6 Cat6A', 'Cat5e Cat6 Cat6A'),
        ('T568A T568B', 'T568A T568B'),
        ('Straight Crossover', 'Straight Crossover'),
        ('Patch Panel Keystone', 'Patch Panel Keystone'),
    ]))
    levels.append(_sub('۱۲.۲ فیبر', [
        ('OM1 تا OM5', 'OM1 تا OM5'),
        ('OS2 Single Mode', 'OS2 Single Mode'),
        ('SFP SFP+ QSFP', 'SFP SFP+ QSFP'),
        ('LC SC Connectors', 'LC SC Connectors'),
    ]))
    levels.append(_sub('۱۲.۳ رک', [
        ('واحد U', 'واحد U'),
        ('آرایش جلو عقب', 'آرایش جلو عقب'),
        ('PDU', 'PDU'),
        ('مدیریت کابل', 'مدیریت کابل'),
        ('جریان هوا', 'جریان هوا'),
    ]))
    levels.append(_sub('۱۲.۴ فیزیک DC', [
        ('برق دو مسیر', 'برق دو مسیر'),
        ('سرمایش', 'سرمایش'),
        ('ارت', 'ارت'),
        ('اطفاء', 'اطفاء'),
        ('حفاظت ESD', 'حفاظت ESD'),
    ]))
    levels.append(_sub('۱۲.۵ تست', [
        ('Wiremap', 'Wiremap'),
        ('NEXT Attenuation', 'NEXT Attenuation'),
        ('OTDR', 'OTDR'),
        ('Certifier', 'Certifier'),
    ]))
    C.append((12, 'فصل ۱۲: کابل\u200cکشی فیبر رک', 'Ch12 Physical', levels))

    levels = []
    levels.append(_sub('۱۳.۱ VLAN', [
        ('مفهوم VLAN', 'مفهوم VLAN'),
        ('Access Port', 'Access Port'),
        ('Trunk 802.1Q', 'Trunk 802.1Q'),
        ('Native VLAN', 'Native VLAN'),
        ('Voice VLAN', 'Voice VLAN'),
        ('VLAN Hopping', 'VLAN Hopping'),
    ]))
    levels.append(_sub('۱۳.۲ STP', [
        ('مشکل Loop', 'مشکل Loop'),
        ('STP 802.1D', 'STP 802.1D'),
        ('RSTP', 'RSTP'),
        ('MSTP', 'MSTP'),
        ('PVST+', 'PVST+'),
        ('Root Bridge', 'Root Bridge'),
        ('PortFast', 'PortFast'),
        ('BPDU Guard', 'BPDU Guard'),
        ('Root Guard', 'Root Guard'),
        ('Loop Guard', 'Loop Guard'),
    ]))
    levels.append(_sub('۱۳.۳ EtherChannel', [
        ('LACP', 'LACP'),
        ('PAgP', 'PAgP'),
        ('Load Balancing Modes', 'Load Balancing Modes'),
    ]))
    levels.append(_sub('۱۳.۴ امنیت L2', [
        ('Port Security', 'Port Security'),
        ('DHCP Snooping', 'DHCP Snooping'),
        ('DAI', 'DAI'),
        ('IP Source Guard', 'IP Source Guard'),
        ('Storm Control', 'Storm Control'),
        ('Protected Port', 'Protected Port'),
    ]))
    levels.append(_sub('۱۳.۵ 802.1X', [
        ('EAP', 'EAP'),
        ('MAB', 'MAB'),
        ('RADIUS Integration', 'RADIUS Integration'),
        ('NAC مقدماتی', 'NAC مقدماتی'),
    ]))
    C.append((13, 'فصل ۱۳: سوییچینگ سیسکو', 'Ch13 Cisco SW', levels))

    levels = []
    levels.append(_sub('۱۴.۱ Static', [
        ('Static Route', 'Static Route'),
        ('Default Route', 'Default Route'),
        ('Floating Static', 'Floating Static'),
        ('Administrative Distance', 'Administrative Distance'),
    ]))
    levels.append(_sub('۱۴.۲ OSPF', [
        ('Link-State مفهوم', 'Link-State مفهوم'),
        ('Area', 'Area'),
        ('Router ID', 'Router ID'),
        ('LSA Types', 'LSA Types'),
        ('DR BDR', 'DR BDR'),
        ('Network Types', 'Network Types'),
        ('Multi-Area', 'Multi-Area'),
        ('Stub NSSA', 'Stub NSSA'),
        ('Summarization OSPF', 'Summarization OSPF'),
    ]))
    levels.append(_sub('۱۴.۳ EIGRP', [
        ('Metric مرکب', 'Metric مرکب'),
        ('DUAL', 'DUAL'),
        ('Successor Feasible', 'Successor Feasible'),
        ('Query SIA', 'Query SIA'),
    ]))
    levels.append(_sub('۱۴.۴ BGP', [
        ('AS Number', 'AS Number'),
        ('eBGP iBGP', 'eBGP iBGP'),
        ('Path Attributes', 'Path Attributes'),
        ('Best Path', 'Best Path'),
        ('Communities', 'Communities'),
        ('Route Reflector', 'Route Reflector'),
    ]))
    levels.append(_sub('۱۴.۵ Policy', [
        ('Prefix-list', 'Prefix-list'),
        ('Route-map', 'Route-map'),
        ('Redistribution', 'Redistribution'),
        ('PBR', 'PBR'),
        ('Local Pref MED', 'Local Pref MED'),
    ]))
    C.append((14, 'فصل ۱۴: مسیریابی پیشرفته', 'Ch14 Routing', levels))

    levels = []
    levels.append(_sub('۱۵.۱ VRF', [
        ('VRF مفهوم', 'VRF مفهوم'),
        ('VRF-Lite', 'VRF-Lite'),
        ('Route Distinguisher', 'Route Distinguisher'),
        ('Route Leaking', 'Route Leaking'),
    ]))
    levels.append(_sub('۱۵.۲ MPLS', [
        ('Label Switching', 'Label Switching'),
        ('LDP', 'LDP'),
        ('LSR LER', 'LSR LER'),
        ('Penultimate Hop', 'Penultimate Hop'),
    ]))
    levels.append(_sub('۱۵.۳ L3VPN', [
        ('PE P CE', 'PE P CE'),
        ('MP-BGP VPNV4', 'MP-BGP VPNV4'),
        ('طراحی Multi-Tenant', 'طراحی Multi-Tenant'),
    ]))
    C.append((15, 'فصل ۱۵: MPLS VRF L3VPN', 'Ch15 MPLS', levels))

    levels = []
    levels.append(_sub('۱۶.۱ مبانی', [
        ('چرا Multicast', 'چرا Multicast'),
        ('IGMPv2', 'IGMPv2'),
        ('IGMPv3', 'IGMPv3'),
        ('IGMP Snooping', 'IGMP Snooping'),
    ]))
    levels.append(_sub('۱۶.۲ مسیریابی', [
        ('PIM Dense', 'PIM Dense'),
        ('PIM Sparse', 'PIM Sparse'),
        ('Rendezvous Point', 'Rendezvous Point'),
        ('Bidir PIM', 'Bidir PIM'),
    ]))
    levels.append(_sub('۱۶.۳ کاربرد', [
        ('IPTV سازمانی', 'IPTV سازمانی'),
        ('Video Distribution', 'Video Distribution'),
        ('Market Data', 'Market Data'),
    ]))
    C.append((16, 'فصل ۱۶: Multicast', 'Ch16 Multicast', levels))

    levels = []
    levels.append(_sub('۱۷.۱ VXLAN', [
        ('Overlay مفهوم', 'Overlay مفهوم'),
        ('VNI', 'VNI'),
        ('VTEP', 'VTEP'),
        ('Encapsulation', 'Encapsulation'),
    ]))
    levels.append(_sub('۱۷.۲ EVPN', [
        ('Control Plane', 'Control Plane'),
        ('Route Type 2 3 5', 'Route Type 2 3 5'),
        ('Multi-Homing', 'Multi-Homing'),
    ]))
    levels.append(_sub('۱۷.۳ Leaf-Spine', [
        ('Underlay طراحی', 'Underlay طراحی'),
        ('Anycast Gateway', 'Anycast Gateway'),
        ('Multi-Tenancy DC', 'Multi-Tenancy DC'),
    ]))
    C.append((17, 'فصل ۱۷: EVPN VXLAN', 'Ch17 EVPN', levels))

    levels = []
    levels.append(_sub('۱۸.۱ SDN', [
        ('Control Data Plane جدا', 'Control Data Plane جدا'),
        ('Controller', 'Controller'),
        ('Southbound Northbound', 'Southbound Northbound'),
        ('OpenFlow مفهوم', 'OpenFlow مفهوم'),
    ]))
    levels.append(_sub('۱۸.۲ SD-WAN', [
        ('Underlay Overlay', 'Underlay Overlay'),
        ('Orchestrator', 'Orchestrator'),
        ('Application Policy', 'Application Policy'),
        ('Path Selection', 'Path Selection'),
    ]))
    levels.append(_sub('۱۸.۳ SASE', [
        ('ZTNA', 'ZTNA'),
        ('SWG', 'SWG'),
        ('CASB', 'CASB'),
        ('FWaaS', 'FWaaS'),
        ('معماری SASE', 'معماری SASE'),
    ]))
    C.append((18, 'فصل ۱۸: SDN SD-WAN SASE', 'Ch18 SDWAN', levels))

    levels = []
    levels.append(_sub('۱۹.۱ RouterOS', [
        ('معماری RouterOS', 'معماری RouterOS'),
        ('Package', 'Package'),
        ('Upgrade', 'Upgrade'),
        ('Downgrade', 'Downgrade'),
        ('Backup Export', 'Backup Export'),
        ('CHR', 'CHR'),
    ]))
    levels.append(_sub('۱۹.۲ دسترسی', [
        ('WinBox', 'WinBox'),
        ('WebFig', 'WebFig'),
        ('SSH', 'SSH'),
        ('API REST', 'API REST'),
        ('Safe Mode', 'Safe Mode'),
    ]))
    levels.append(_sub('۱۹.۳ اینترفیس', [
        ('Ethernet', 'Ethernet'),
        ('VLAN Interface', 'VLAN Interface'),
        ('Bridge', 'Bridge'),
        ('Bridge VLAN Filtering', 'Bridge VLAN Filtering'),
        ('Bonding', 'Bonding'),
        ('VRRP Interface', 'VRRP Interface'),
    ]))
    levels.append(_sub('۱۹.۴ مدیریت', [
        ('Users Groups', 'Users Groups'),
        ('Services', 'Services'),
        ('Certificates', 'Certificates'),
        ('Scheduler مقدماتی', 'Scheduler مقدماتی'),
    ]))
    C.append((19, 'فصل ۱۹: MikroTik مبانی', 'Ch19 MT Base', levels))

    levels = []
    levels.append(_sub('۲۰.۱ Routing', [
        ('Static Route', 'Static Route'),
        ('ECMP', 'ECMP'),
        ('OSPF در MT', 'OSPF در MT'),
        ('BGP در MT', 'BGP در MT'),
        ('Policy Routing', 'Policy Routing'),
        ('VRF در MT', 'VRF در MT'),
    ]))
    levels.append(_sub('۲۰.۲ Firewall Filter', [
        ('Chain Input Forward Output', 'Chain Input Forward Output'),
        ('Action Accept Drop Reject', 'Action Accept Drop Reject'),
        ('Address-list', 'Address-list'),
        ('Connection State', 'Connection State'),
        ('Raw NoTrack', 'Raw NoTrack'),
    ]))
    levels.append(_sub('۲۰.۳ NAT', [
        ('masquerade', 'masquerade'),
        ('srcnat', 'srcnat'),
        ('dstnat', 'dstnat'),
        ('netmap', 'netmap'),
        ('Hairpin NAT', 'Hairpin NAT'),
    ]))
    levels.append(_sub('۲۰.۴ Mangle', [
        ('Mark Connection', 'Mark Connection'),
        ('Mark Packet', 'Mark Packet'),
        ('Mark Routing', 'Mark Routing'),
        ('Use Case QoS و Policy', 'Use Case QoS و Policy'),
    ]))
    C.append((20, 'فصل ۲۰: MikroTik Routing Firewall NAT', 'Ch20 MT FW', levels))

    levels = []
    levels.append(_sub('۲۱.۱ QoS', [
        ('Simple Queue', 'Simple Queue'),
        ('Queue Tree', 'Queue Tree'),
        ('PCQ', 'PCQ'),
        ('HTB', 'HTB'),
        ('اولویت\u200cبندی ترافیک', 'اولویت\u200cبندی ترافیک'),
    ]))
    levels.append(_sub('۲۱.۲ VPN', [
        ('WireGuard', 'WireGuard'),
        ('IPsec', 'IPsec'),
        ('L2TP/IPsec', 'L2TP/IPsec'),
        ('SSTP', 'SSTP'),
        ('GRE', 'GRE'),
        ('EoIP', 'EoIP'),
        ('VXLAN MT', 'VXLAN MT'),
    ]))
    levels.append(_sub('۲۱.۳ HA', [
        ('VRRP', 'VRRP'),
        ('Failover Script', 'Failover Script'),
        ('Backup Sync', 'Backup Sync'),
    ]))
    levels.append(_sub('۲۱.۴ اتوماسیون مانیتور', [
        ('Scheduler', 'Scheduler'),
        ('Netwatch', 'Netwatch'),
        ('Script', 'Script'),
        ('API Automation', 'API Automation'),
        ('SNMP', 'SNMP'),
        ('Traffic Flow', 'Traffic Flow'),
        ('Graphing', 'Graphing'),
    ]))
    C.append((21, 'فصل ۲۱: MikroTik QoS VPN HA', 'Ch21 MT Adv', levels))

    levels = []
    levels.append(_sub('۲۲.۱ RF', [
        ('فرکانس 2.4 5 6', 'فرکانس 2.4 5 6'),
        ('Channel Width', 'Channel Width'),
        ('RSSI SNR', 'RSSI SNR'),
        ('Noise Floor', 'Noise Floor'),
        ('Interference', 'Interference'),
        ('Propagation', 'Propagation'),
    ]))
    levels.append(_sub('۲۲.۲ استاندارد', [
        ('802.11n', '802.11n'),
        ('802.11ac', '802.11ac'),
        ('802.11ax WiFi6', '802.11ax WiFi6'),
        ('WiFi 6E', 'WiFi 6E'),
        ('802.11be WiFi7', '802.11be WiFi7'),
        ('MCS Rates', 'MCS Rates'),
    ]))
    levels.append(_sub('۲۲.۳ امنیت', [
        ('WPA2-PSK', 'WPA2-PSK'),
        ('WPA3', 'WPA3'),
        ('Enterprise 802.1X', 'Enterprise 802.1X'),
        ('Guest Isolation', 'Guest Isolation'),
    ]))
    levels.append(_sub('۲۲.۴ طراحی', [
        ('Site Survey', 'Site Survey'),
        ('AP Placement', 'AP Placement'),
        ('Controller vs Cloud', 'Controller vs Cloud'),
        ('Roaming 802.11kvr', 'Roaming 802.11kvr'),
        ('High Density', 'High Density'),
    ]))
    C.append((22, 'فصل ۲۲: وایرلس سازمانی', 'Ch22 WiFi', levels))

    levels = []
    levels.append(_sub('۲۳.۱ لینک', [
        ('Fresnel Zone', 'Fresnel Zone'),
        ('LOS NLOS', 'LOS NLOS'),
        ('EIRP', 'EIRP'),
        ('Budget Link', 'Budget Link'),
    ]))
    levels.append(_sub('۲۳.۲ توپولوژی', [
        ('Point to Point', 'Point to Point'),
        ('Point to Multipoint', 'Point to Multipoint'),
        ('Sector Antenna', 'Sector Antenna'),
        ('Dish', 'Dish'),
    ]))
    levels.append(_sub('۲۳.۳ عیب\u200cیابی', [
        ('Alignment', 'Alignment'),
        ('Interference', 'Interference'),
        ('Capacity Planning', 'Capacity Planning'),
        ('Failover لینک', 'Failover لینک'),
    ]))
    C.append((23, 'فصل ۲۳: PtP PtMP', 'Ch23 Wireless Links', levels))

    levels = []
    levels.append(_sub('۲۴.۱ معماری', [
        ('FortiOS', 'FortiOS'),
        ('Interface Mode', 'Interface Mode'),
        ('Zone', 'Zone'),
        ('VDOM', 'VDOM'),
        ('Hardware Acceleration', 'Hardware Acceleration'),
    ]))
    levels.append(_sub('۲۴.۲ Policy NAT', [
        ('Firewall Policy', 'Firewall Policy'),
        ('Address Objects', 'Address Objects'),
        ('Service Schedule', 'Service Schedule'),
        ('VIP DNAT', 'VIP DNAT'),
        ('IP Pool SNAT', 'IP Pool SNAT'),
        ('Central SNAT', 'Central SNAT'),
    ]))
    levels.append(_sub('۲۴.۳ UTM', [
        ('IPS', 'IPS'),
        ('Antivirus', 'Antivirus'),
        ('Web Filter', 'Web Filter'),
        ('Application Control', 'Application Control'),
        ('SSL Inspection', 'SSL Inspection'),
    ]))
    levels.append(_sub('۲۴.۴ VPN', [
        ('IPsec Site-to-Site', 'IPsec Site-to-Site'),
        ('SSL VPN Portal', 'SSL VPN Portal'),
        ('Dial-up', 'Dial-up'),
        ('Overlapping Subnets', 'Overlapping Subnets'),
    ]))
    levels.append(_sub('۲۴.۵ HA SD-WAN', [
        ('HA Active-Passive', 'HA Active-Passive'),
        ('Session Sync', 'Session Sync'),
        ('FGSP', 'FGSP'),
        ('SD-WAN Members', 'SD-WAN Members'),
        ('SLA Health Check', 'SLA Health Check'),
        ('SD-WAN Rules', 'SD-WAN Rules'),
    ]))
    C.append((24, 'فصل ۲۴: FortiGate', 'Ch24 FortiGate', levels))

    levels = []
    levels.append(_sub('۲۵.۱ معماری FW', [
        ('Stateful Firewall', 'Stateful Firewall'),
        ('NGFW مفهوم', 'NGFW مفهوم'),
        ('Packet Filter', 'Packet Filter'),
    ]))
    levels.append(_sub('۲۵.۲ pfSense', [
        ('نصب', 'نصب'),
        ('Rules', 'Rules'),
        ('NAT', 'NAT'),
        ('OpenVPN', 'OpenVPN'),
        ('Packages Snort', 'Packages Snort'),
    ]))
    levels.append(_sub('۲۵.۳ OPNsense', [
        ('تفاوت با pfSense', 'تفاوت با pfSense'),
        ('Plugins', 'Plugins'),
        ('WireGuard', 'WireGuard'),
    ]))
    levels.append(_sub('۲۵.۴ Sophos و مقایسه', [
        ('Sophos XG مبانی', 'Sophos XG مبانی'),
        ('مقایسه FG pfSense Sophos', 'مقایسه FG pfSense Sophos'),
    ]))
    C.append((25, 'فصل ۲۵: pfSense OPNsense Sophos', 'Ch25 Alt FW', levels))

    levels = []
    levels.append(_sub('۲۶.۱ رمزنگاری', [
        ('Symmetric AES', 'Symmetric AES'),
        ('Asymmetric RSA ECC', 'Asymmetric RSA ECC'),
        ('Hash SHA', 'Hash SHA'),
        ('HMAC', 'HMAC'),
        ('DH ECDH', 'DH ECDH'),
    ]))
    levels.append(_sub('۲۶.۲ PKI', [
        ('CA', 'CA'),
        ('Root CA', 'Root CA'),
        ('Intermediate', 'Intermediate'),
        ('CRL OCSP', 'CRL OCSP'),
        ('Trust Chain', 'Trust Chain'),
    ]))
    levels.append(_sub('۲۶.۳ گواهی TLS', [
        ('CSR', 'CSR'),
        ('SAN', 'SAN'),
        ('Wildcard', 'Wildcard'),
        ('EKU', 'EKU'),
        ('TLS Handshake', 'TLS Handshake'),
        ('Cipher Suites', 'Cipher Suites'),
    ]))
    levels.append(_sub('۲۶.۴ سازمانی', [
        ('AD CS', 'AD CS'),
        ('Autoenrollment', 'Autoenrollment'),
        ('Internal HTTPS', 'Internal HTTPS'),
        ('LDAPS', 'LDAPS'),
    ]))
    C.append((26, 'فصل ۲۶: PKI TLS', 'Ch26 PKI', levels))

    levels = []
    levels.append(_sub('۲۷.۱ AAA', [
        ('Authentication', 'Authentication'),
        ('Authorization', 'Authorization'),
        ('Accounting', 'Accounting'),
    ]))
    levels.append(_sub('۲۷.۲ RADIUS TACACS+', [
        ('RADIUS جریان', 'RADIUS جریان'),
        ('TACACS+ تفاوت', 'TACACS+ تفاوت'),
        ('Attribute', 'Attribute'),
    ]))
    levels.append(_sub('۲۷.۳ 802.1X NAC', [
        ('EAP Methods', 'EAP Methods'),
        ('MAB', 'MAB'),
        ('NAC Posture', 'NAC Posture'),
        ('Guest Flow', 'Guest Flow'),
    ]))
    levels.append(_sub('۲۷.۴ MFA PAM', [
        ('MFA روش\u200cها', 'MFA روش\u200cها'),
        ('Privileged Access Management', 'Privileged Access Management'),
    ]))
    C.append((27, 'فصل ۲۷: AAA NAC', 'Ch27 AAA', levels))

    levels = []
    levels.append(_sub('۲۸.۱ نصب', [
        ('نسخه\u200cها Edition', 'نسخه\u200cها Edition'),
        ('Server Core vs GUI', 'Server Core vs GUI'),
        ('Roles Features', 'Roles Features'),
        ('Server Manager', 'Server Manager'),
    ]))
    levels.append(_sub('۲۸.۲ مدیریت', [
        ('Windows Admin Center', 'Windows Admin Center'),
        ('Remote Management', 'Remote Management'),
        ('WinRM', 'WinRM'),
        ('سرویس\u200cهای حیاتی', 'سرویس\u200cهای حیاتی'),
    ]))
    C.append((28, 'فصل ۲۸: Windows Server Core', 'Ch28 WinServer', levels))

    levels = []
    levels.append(_sub('۲۹.۱ ساختار', [
        ('Forest Domain Tree', 'Forest Domain Tree'),
        ('OU طراحی', 'OU طراحی'),
        ('Object Types', 'Object Types'),
        ('Schema', 'Schema'),
    ]))
    levels.append(_sub('۲۹.۲ DC', [
        ('Domain Controller', 'Domain Controller'),
        ('Global Catalog', 'Global Catalog'),
        ('FSMO Roles', 'FSMO Roles'),
        ('Read-Only DC', 'Read-Only DC'),
    ]))
    levels.append(_sub('۲۹.۳ Sites Replication', [
        ('Site Subnet', 'Site Subnet'),
        ('Replication Intra Inter', 'Replication Intra Inter'),
        ('SYSVOL', 'SYSVOL'),
    ]))
    levels.append(_sub('۲۹.۴ GPO', [
        ('GPO ساختار', 'GPO ساختار'),
        ('Inheritance', 'Inheritance'),
        ('Filtering', 'Filtering'),
        ('Loopback', 'Loopback'),
        ('عیب\u200cیابی GPO', 'عیب\u200cیابی GPO'),
    ]))
    levels.append(_sub('۲۹.۵ امنیت AD', [
        ('Tier 0 1 2', 'Tier 0 1 2'),
        ('Protected Users', 'Protected Users'),
        ('LAPS', 'LAPS'),
        ('Kerberos', 'Kerberos'),
        ('Credential Theft Mitigation', 'Credential Theft Mitigation'),
    ]))
    C.append((29, 'فصل ۲۹: Active Directory', 'Ch29 AD', levels))

    levels = []
    levels.append(_sub('۳۰.۱ MS DNS', [
        ('AD-Integrated Zone', 'AD-Integrated Zone'),
        ('Aging Scavenging', 'Aging Scavenging'),
        ('Conditional Forwarder', 'Conditional Forwarder'),
        ('DNS Policies', 'DNS Policies'),
    ]))
    levels.append(_sub('۳۰.۲ MS DHCP', [
        ('Scope Options', 'Scope Options'),
        ('Reservation', 'Reservation'),
        ('Failover', 'Failover'),
        ('Filter', 'Filter'),
    ]))
    levels.append(_sub('۳۰.۳ NPS', [
        ('RADIUS Client', 'RADIUS Client'),
        ('Network Policy', 'Network Policy'),
        ('802.1X با NPS', '802.1X با NPS'),
    ]))
    C.append((30, 'فصل ۳۰: Windows DNS DHCP NPS', 'Ch30 MS Net Services', levels))

    levels = []
    levels.append(_sub('۳۱.۱ SMB', [
        ('SMB نسخه', 'SMB نسخه'),
        ('Share Permission', 'Share Permission'),
        ('NTFS Permission', 'NTFS Permission'),
        ('Effective Access', 'Effective Access'),
    ]))
    levels.append(_sub('۳۱.۲ DFS', [
        ('Namespace', 'Namespace'),
        ('Replication DFSR', 'Replication DFSR'),
        ('Topology', 'Topology'),
    ]))
    levels.append(_sub('۳۱.۳ چاپ', [
        ('Print Server', 'Print Server'),
        ('Driver Deployment', 'Driver Deployment'),
        ('Queue مدیریت', 'Queue مدیریت'),
    ]))
    C.append((31, 'فصل ۳۱: فایل چاپ DFS', 'Ch31 File DFS', levels))

    levels = []
    levels.append(_sub('۳۲.۱ حفاظت', [
        ('Microsoft Defender', 'Microsoft Defender'),
        ('BitLocker', 'BitLocker'),
        ('Windows Firewall', 'Windows Firewall'),
        ('AppLocker مقدماتی', 'AppLocker مقدماتی'),
    ]))
    levels.append(_sub('۳۲.۲ Baseline EDR', [
        ('CIS Baseline', 'CIS Baseline'),
        ('LAPS', 'LAPS'),
        ('Event Log Security', 'Event Log Security'),
        ('EDR مفهوم', 'EDR مفهوم'),
    ]))
    C.append((32, 'فصل ۳۲: امنیت Endpoint ویندوز', 'Ch32 Win Endpoint', levels))

    levels = []
    levels.append(_sub('۳۳.۱ Entra ID', [
        ('Tenant', 'Tenant'),
        ('Users Groups', 'Users Groups'),
        ('App Registration', 'App Registration'),
        ('Roles', 'Roles'),
    ]))
    levels.append(_sub('۳۳.۲ Hybrid', [
        ('Azure AD Connect', 'Azure AD Connect'),
        ('Password Hash Sync', 'Password Hash Sync'),
        ('Pass-through Auth', 'Pass-through Auth'),
        ('Federation ADFS', 'Federation ADFS'),
        ('SSO', 'SSO'),
        ('MFA Conditional Access', 'MFA Conditional Access'),
    ]))
    C.append((33, 'فصل ۳۳: Entra ID Hybrid', 'Ch33 Entra', levels))

    levels = []
    levels.append(_sub('۳۴.۱ Intune', [
        ('Enrollment', 'Enrollment'),
        ('Compliance', 'Compliance'),
        ('Configuration Profiles', 'Configuration Profiles'),
        ('App Deployment', 'App Deployment'),
    ]))
    levels.append(_sub('۳۴.۲ Conditional Access', [
        ('CA Policies', 'CA Policies'),
        ('Named Locations', 'Named Locations'),
        ('Risk-based', 'Risk-based'),
    ]))
    levels.append(_sub('۳۴.۳ ایمیل سازمانی', [
        ('Exchange Online', 'Exchange Online'),
        ('Mail Flow Rules', 'Mail Flow Rules'),
        ('Connector', 'Connector'),
        ('Anti-Spam Anti-Phish', 'Anti-Spam Anti-Phish'),
        ('DNS برای ایمیل MX SPF DKIM DMARC', 'DNS برای ایمیل MX SPF DKIM DMARC'),
    ]))
    C.append((34, 'فصل ۳۴: M365 Intune ایمیل', 'Ch34 M365', levels))

    levels = []
    levels.append(_sub('۳۵.۱ CMD شبکه', [
        ('ipconfig', 'ipconfig'),
        ('ping pathping', 'ping pathping'),
        ('tracert', 'tracert'),
        ('nslookup', 'nslookup'),
        ('netsh', 'netsh'),
        ('arp route', 'arp route'),
    ]))
    levels.append(_sub('۳۵.۲ PowerShell پایه', [
        ('Cmdlets', 'Cmdlets'),
        ('Pipeline', 'Pipeline'),
        ('Objects', 'Objects'),
        ('Providers', 'Providers'),
    ]))
    levels.append(_sub('۳۵.۳ اتوماسیون', [
        ('Remoting', 'Remoting'),
        ('AD Module', 'AD Module'),
        ('Network Scripts', 'Network Scripts'),
        ('Scheduled Jobs', 'Scheduled Jobs'),
        ('DSC مقدماتی', 'DSC مقدماتی'),
    ]))
    C.append((35, 'فصل ۳۵: PowerShell CMD', 'Ch35 PowerShell', levels))

    levels = []
    levels.append(_sub('۳۶.۱ پایه', [
        ('توزیع\u200cها RHEL Ubuntu Debian', 'توزیع\u200cها RHEL Ubuntu Debian'),
        ('Filesystem Hierarchy', 'Filesystem Hierarchy'),
        ('Users Groups', 'Users Groups'),
        ('sudo', 'sudo'),
        ('Permissions ACL', 'Permissions ACL'),
    ]))
    levels.append(_sub('۳۶.۲ فرآیند و سرویس', [
        ('systemd Units', 'systemd Units'),
        ('journalctl', 'journalctl'),
        ('Target Runlevel', 'Target Runlevel'),
        ('Package Managers', 'Package Managers'),
    ]))
    C.append((36, 'فصل ۳۶: مدیریت لینوکس', 'Ch36 Linux Admin', levels))

    levels = []
    levels.append(_sub('۳۷.۱ پیکربندی', [
        ('ip addr route', 'ip addr route'),
        ('nmcli', 'nmcli'),
        ('Netplan', 'Netplan'),
        ('Bridge', 'Bridge'),
        ('VLAN', 'VLAN'),
        ('Bonding', 'Bonding'),
    ]))
    levels.append(_sub('۳۷.۲ سرویس', [
        ('systemd-resolved', 'systemd-resolved'),
        ('DHCP Client Server', 'DHCP Client Server'),
        ('nftables firewalld مقدماتی', 'nftables firewalld مقدماتی'),
    ]))
    C.append((37, 'فصل ۳۷: شبکه لینوکس', 'Ch37 Linux Net', levels))

    levels = []
    levels.append(_sub('۳۸.۱ دسترسی', [
        ('SSH Hardening پایه', 'SSH Hardening پایه'),
        ('Key Auth', 'Key Auth'),
        ('Jump Host', 'Jump Host'),
    ]))
    levels.append(_sub('۳۸.۲ وب', [
        ('Nginx', 'Nginx'),
        ('Apache', 'Apache'),
        ('Reverse Proxy', 'Reverse Proxy'),
        ('TLS Certificates', 'TLS Certificates'),
        ('Load Balancing با Nginx', 'Load Balancing با Nginx'),
    ]))
    C.append((38, 'فصل ۳۸: سرویس لینوکس وب', 'Ch38 Linux Services', levels))

    levels = []
    levels.append(_sub('۳۹.۱ MAC Firewall', [
        ('SELinux Modes', 'SELinux Modes'),
        ('AppArmor', 'AppArmor'),
        ('nftables پیشرفته', 'nftables پیشرفته'),
        ('firewalld', 'firewalld'),
    ]))
    levels.append(_sub('۳۹.۲ Hardening', [
        ('SSH Advanced', 'SSH Advanced'),
        ('Auditd', 'Auditd'),
        ('Fail2ban', 'Fail2ban'),
        ('AIDE', 'AIDE'),
        ('Kernel Sysctl', 'Kernel Sysctl'),
    ]))
    C.append((39, 'فصل ۳۹: امنیت لینوکس', 'Ch39 Linux Sec', levels))

    levels = []
    levels.append(_sub('۴۰.۱ ESXi', [
        ('نصب ESXi', 'نصب ESXi'),
        ('Networking vSwitch', 'Networking vSwitch'),
        ('Datastore', 'Datastore'),
        ('VM Hardware', 'VM Hardware'),
    ]))
    levels.append(_sub('۴۰.۲ vCenter', [
        ('Inventory', 'Inventory'),
        ('vMotion', 'vMotion'),
        ('Storage vMotion', 'Storage vMotion'),
        ('DRS', 'DRS'),
        ('HA', 'HA'),
        ('FT', 'FT'),
    ]))
    levels.append(_sub('۴۰.۳ Hyper-V', [
        ('Hyper-V Role', 'Hyper-V Role'),
        ('Virtual Switch', 'Virtual Switch'),
        ('Replica', 'Replica'),
        ('Failover Cluster', 'Failover Cluster'),
    ]))
    C.append((40, 'فصل ۴۰: VMware Hyper-V', 'Ch40 Virtualization', levels))

    levels = []
    levels.append(_sub('۴۱.۱ Proxmox', [
        ('نصب', 'نصب'),
        ('Cluster', 'Cluster'),
        ('ZFS Storage', 'ZFS Storage'),
        ('KVM VM', 'KVM VM'),
        ('LXC', 'LXC'),
        ('Backup Replication', 'Backup Replication'),
    ]))
    levels.append(_sub('۴۱.۲ Docker', [
        ('Image Container', 'Image Container'),
        ('Network Modes', 'Network Modes'),
        ('Volume', 'Volume'),
        ('Compose', 'Compose'),
        ('Registry', 'Registry'),
    ]))
    C.append((41, 'فصل ۴۱: Proxmox Docker', 'Ch41 Proxmox Docker', levels))

    levels = []
    levels.append(_sub('۴۲.۱ مبانی', [
        ('Pod', 'Pod'),
        ('Deployment', 'Deployment'),
        ('Service', 'Service'),
        ('Namespace', 'Namespace'),
        ('ConfigMap Secret', 'ConfigMap Secret'),
    ]))
    levels.append(_sub('۴۲.۲ شبکه امنیت', [
        ('CNI', 'CNI'),
        ('Ingress', 'Ingress'),
        ('NetworkPolicy', 'NetworkPolicy'),
        ('RBAC', 'RBAC'),
        ('ServiceAccount', 'ServiceAccount'),
    ]))
    levels.append(_sub('۴۲.۳ عملیات', [
        ('Helm', 'Helm'),
        ('Monitoring Stack', 'Monitoring Stack'),
        ('Upgrade Strategy', 'Upgrade Strategy'),
    ]))
    C.append((42, 'فصل ۴۲: Kubernetes', 'Ch42 K8s', levels))

    levels = []
    levels.append(_sub('۴۳.۱ AWS', [
        ('VPC', 'VPC'),
        ('Subnet Public Private', 'Subnet Public Private'),
        ('Route Table', 'Route Table'),
        ('IGW NAT GW', 'IGW NAT GW'),
        ('Security Group', 'Security Group'),
        ('NACL', 'NACL'),
        ('TGW', 'TGW'),
    ]))
    levels.append(_sub('۴۳.۲ Azure', [
        ('VNet', 'VNet'),
        ('NSG', 'NSG'),
        ('Azure Firewall مبانی', 'Azure Firewall مبانی'),
        ('Load Balancer', 'Load Balancer'),
        ('Private Endpoint', 'Private Endpoint'),
    ]))
    levels.append(_sub('۴۳.۳ Hybrid', [
        ('Site-to-Site VPN', 'Site-to-Site VPN'),
        ('ExpressRoute', 'ExpressRoute'),
        ('Direct Connect', 'Direct Connect'),
        ('DNS Hybrid', 'DNS Hybrid'),
    ]))
    C.append((43, 'فصل ۴۳: شبکه ابری', 'Ch43 Cloud Net', levels))

    levels = []
    levels.append(_sub('۴۴.۱ هویت ابر', [
        ('IAM AWS', 'IAM AWS'),
        ('Azure RBAC', 'Azure RBAC'),
        ('Secrets Manager', 'Secrets Manager'),
        ('Key Vault', 'Key Vault'),
    ]))
    levels.append(_sub('۴۴.۲ CSPM FinOps', [
        ('CSPM', 'CSPM'),
        ('Logging CloudTrail', 'Logging CloudTrail'),
        ('Backup ابر', 'Backup ابر'),
        ('Cost Management', 'Cost Management'),
        ('Policies Governance', 'Policies Governance'),
    ]))
    C.append((44, 'فصل ۴۴: امنیت ابر Governance', 'Ch44 Cloud Sec', levels))

    levels = []
    levels.append(_sub('۴۵.۱ انواع', [
        ('DAS NAS SAN', 'DAS NAS SAN'),
        ('iSCSI', 'iSCSI'),
        ('Fibre Channel', 'Fibre Channel'),
        ('NVMe-oF', 'NVMe-oF'),
    ]))
    levels.append(_sub('۴۵.۲ پروتکل نرم\u200cافزار', [
        ('NFS', 'NFS'),
        ('SMB', 'SMB'),
        ('Ceph', 'Ceph'),
        ('ZFS Enterprise', 'ZFS Enterprise'),
        ('Thin Provisioning Dedup', 'Thin Provisioning Dedup'),
    ]))
    C.append((45, 'فصل ۴۵: Storage سازمانی', 'Ch45 Storage', levels))

    levels = []
    levels.append(_sub('۴۶.۱ Backup', [
        ('Full Incremental Differential', 'Full Incremental Differential'),
        ('3-2-1-1-0', '3-2-1-1-0'),
        ('Immutable Backup', 'Immutable Backup'),
        ('Catalog', 'Catalog'),
    ]))
    levels.append(_sub('۴۶.۲ DR', [
        ('RPO RTO', 'RPO RTO'),
        ('Veeam مبانی', 'Veeam مبانی'),
        ('DR Site', 'DR Site'),
        ('تست بازیابی', 'تست بازیابی'),
        ('Ransomware Recovery', 'Ransomware Recovery'),
    ]))
    C.append((46, 'فصل ۴۶: Backup DR', 'Ch46 Backup', levels))

    levels = []
    levels.append(_sub('۴۷.۱ فیزیکی', [
        ('Tier Classification', 'Tier Classification'),
        ('Power Design', 'Power Design'),
        ('Cooling', 'Cooling'),
        ('Hot Cold Aisle', 'Hot Cold Aisle'),
    ]))
    levels.append(_sub('۴۷.۲ شبکه و عملیات', [
        ('Leaf-Spine مرور', 'Leaf-Spine مرور'),
        ('DCIM', 'DCIM'),
        ('Capacity Planning', 'Capacity Planning'),
        ('Environmental Monitoring', 'Environmental Monitoring'),
    ]))
    C.append((47, 'فصل ۴۷: Data Center', 'Ch47 DC', levels))

    levels = []
    levels.append(_sub('۴۸.۱ HA', [
        ('Active Passive', 'Active Passive'),
        ('Active Active', 'Active Active'),
        ('Quorum', 'Quorum'),
        ('Failover Clustering', 'Failover Clustering'),
        ('No SPOF Design', 'No SPOF Design'),
    ]))
    levels.append(_sub('۴۸.۲ LB', [
        ('L4 vs L7', 'L4 vs L7'),
        ('HAProxy', 'HAProxy'),
        ('Nginx LB', 'Nginx LB'),
        ('Keepalived VRRP', 'Keepalived VRRP'),
        ('Health Check', 'Health Check'),
    ]))
    C.append((48, 'فصل ۴۸: HA و Load Balancing', 'Ch48 HA', levels))

    levels = []
    levels.append(_sub('۴۹.۱ پروتکل', [
        ('SNMPv2c v3', 'SNMPv2c v3'),
        ('Syslog', 'Syslog'),
        ('NetFlow', 'NetFlow'),
        ('IPFIX', 'IPFIX'),
        ('sFlow', 'sFlow'),
    ]))
    levels.append(_sub('۴۹.۲ NMS', [
        ('Zabbix', 'Zabbix'),
        ('PRTG', 'PRTG'),
        ('LibreNMS', 'LibreNMS'),
        ('Alerting', 'Alerting'),
    ]))
    levels.append(_sub('۴۹.۳ Observability', [
        ('Prometheus', 'Prometheus'),
        ('Grafana', 'Grafana'),
        ('OpenTelemetry', 'OpenTelemetry'),
        ('Metrics Logs Traces', 'Metrics Logs Traces'),
    ]))
    C.append((49, 'فصل ۴۹: مانیتورینگ', 'Ch49 Monitoring', levels))

    levels = []
    levels.append(_sub('۵۰.۱ ELK', [
        ('Elasticsearch', 'Elasticsearch'),
        ('Logstash', 'Logstash'),
        ('Kibana', 'Kibana'),
        ('Beats', 'Beats'),
        ('Index Lifecycle', 'Index Lifecycle'),
    ]))
    levels.append(_sub('۵۰.۲ SIEM', [
        ('Correlation Rules', 'Correlation Rules'),
        ('Use Cases', 'Use Cases'),
        ('Alert Tuning', 'Alert Tuning'),
        ('SOAR مقدماتی', 'SOAR مقدماتی'),
    ]))
    C.append((50, 'فصل ۵۰: SIEM ELK', 'Ch50 SIEM', levels))

    levels = []
    levels.append(_sub('۵۱.۱ Python شبکه', [
        ('Paramiko', 'Paramiko'),
        ('Netmiko', 'Netmiko'),
        ('NAPALM', 'NAPALM'),
        ('Scrapli', 'Scrapli'),
        ('Requests API', 'Requests API'),
    ]))
    levels.append(_sub('۵۱.۲ IaC', [
        ('Ansible Playbook', 'Ansible Playbook'),
        ('Inventory', 'Inventory'),
        ('Terraform State', 'Terraform State'),
        ('Git Workflow', 'Git Workflow'),
        ('CI برای شبکه', 'CI برای شبکه'),
    ]))
    levels.append(_sub('۵۱.۳ AI در IT', [
        ('ChatOps', 'ChatOps'),
        ('RAG روی مستندات', 'RAG روی مستندات'),
        ('Ollama محلی', 'Ollama محلی'),
        ('Anomaly Detection مانیتورینگ', 'Anomaly Detection مانیتورینگ'),
        ('تولید Runbook با AI', 'تولید Runbook با AI'),
    ]))
    C.append((51, 'فصل ۵۱: اتوماسیون و AI در IT', 'Ch51 Automation', levels))

    levels = []
    levels.append(_sub('۵۲.۱ تجاری', [
        ('SQL Server معماری', 'SQL Server معماری'),
        ('Always On', 'Always On'),
        ('Oracle Instance', 'Oracle Instance'),
        ('Data Guard', 'Data Guard'),
    ]))
    levels.append(_sub('۵۲.۲ متن\u200cباز', [
        ('PostgreSQL', 'PostgreSQL'),
        ('Replication PG', 'Replication PG'),
        ('MySQL MariaDB', 'MySQL MariaDB'),
        ('InnoDB', 'InnoDB'),
    ]))
    levels.append(_sub('۵۲.۳ NoSQL HA', [
        ('MongoDB', 'MongoDB'),
        ('Redis', 'Redis'),
        ('Backup Strategy DB', 'Backup Strategy DB'),
        ('Performance Basics', 'Performance Basics'),
    ]))
    C.append((52, 'فصل ۵۲: مدیریت دیتابیس', 'Ch52 DBA', levels))

    levels = []
    levels.append(_sub('۵۳.۱ کنترل', [
        ('Authentication', 'Authentication'),
        ('Authorization Roles', 'Authorization Roles'),
        ('Encryption TDE', 'Encryption TDE'),
        ('TLS به DB', 'TLS به DB'),
        ('Audit', 'Audit'),
    ]))
    levels.append(_sub('۵۳.۲ حمله Hardening', [
        ('SQL Injection', 'SQL Injection'),
        ('Least Privilege', 'Least Privilege'),
        ('Patching', 'Patching'),
        ('Secrets در App', 'Secrets در App'),
    ]))
    C.append((53, 'فصل ۵۳: امنیت دیتابیس', 'Ch53 DB Sec', levels))

    levels = []
    levels.append(_sub('۵۴.۱ مبانی', [
        ('SIP', 'SIP'),
        ('SDP', 'SDP'),
        ('RTP RTCP', 'RTP RTCP'),
        ('Codecs', 'Codecs'),
        ('QoS برای صوت', 'QoS برای صوت'),
        ('NAT و SIP ALG', 'NAT و SIP ALG'),
    ]))
    levels.append(_sub('۵۴.۲ Issabel Asterisk', [
        ('Extension', 'Extension'),
        ('Trunk', 'Trunk'),
        ('IVR', 'IVR'),
        ('Queue', 'Queue'),
        ('CDR', 'CDR'),
        ('Recording', 'Recording'),
    ]))
    levels.append(_sub('۵۴.۳ پاناسونیک', [
        ('مدل\u200cهای KX-NS TDA', 'مدل\u200cهای KX-NS TDA'),
        ('برنامه\u200cریزی Extension', 'برنامه\u200cریزی Extension'),
        ('Trunk PRI SIP', 'Trunk PRI SIP'),
        ('Gateway', 'Gateway'),
        ('عیب\u200cیابی سانترال', 'عیب\u200cیابی سانترال'),
    ]))
    C.append((54, 'فصل ۵۴: VoIP سانترال', 'Ch54 VoIP', levels))

    levels = []
    levels.append(_sub('۵۵.۱ CCTV', [
        ('IP Camera', 'IP Camera'),
        ('NVR VMS', 'NVR VMS'),
        ('ONVIF', 'ONVIF'),
        ('PoE Budget', 'PoE Budget'),
        ('VLAN دوربین', 'VLAN دوربین'),
        ('Bandwidth محاسبه', 'Bandwidth محاسبه'),
    ]))
    levels.append(_sub('۵۵.۲ Access BMS', [
        ('کنترل تردد', 'کنترل تردد'),
        ('بیومتریک', 'بیومتریک'),
        ('Alarm', 'Alarm'),
        ('BMS پروتکل\u200cها', 'BMS پروتکل\u200cها'),
    ]))
    levels.append(_sub('۵۵.۳ IoT', [
        ('IoT VLAN', 'IoT VLAN'),
        ('Segmentation', 'Segmentation'),
        ('پروتکل\u200cهای سبک', 'پروتکل\u200cهای سبک'),
        ('امنیت IoT', 'امنیت IoT'),
    ]))
    C.append((55, 'فصل ۵۵: CCTV Access BMS IoT', 'Ch55 Physical IoT', levels))

    levels = []
    levels.append(_sub('۵۶.۱ مفاهیم', [
        ('CIA Triad', 'CIA Triad'),
        ('AAA Security', 'AAA Security'),
        ('Risk Threat Vulnerability', 'Risk Threat Vulnerability'),
        ('Asset Classification', 'Asset Classification'),
    ]))
    levels.append(_sub('۵۶.۲ معماری', [
        ('Defense in Depth', 'Defense in Depth'),
        ('Zero Trust اصول', 'Zero Trust اصول'),
        ('NIST CSF', 'NIST CSF'),
        ('ISO 27001', 'ISO 27001'),
        ('CIS Controls', 'CIS Controls'),
    ]))
    levels.append(_sub('۵۶.۳ ITIL', [
        ('Incident Management', 'Incident Management'),
        ('Problem Management', 'Problem Management'),
        ('Change Management', 'Change Management'),
        ('CMDB', 'CMDB'),
        ('Service Desk', 'Service Desk'),
    ]))
    C.append((56, 'فصل ۵۶: امنیت پایه Zero Trust ITIL', 'Ch56 Sec Fund ITIL', levels))

    levels = []
    levels.append(_sub('۵۷.۱ لایه\u200cها', [
        ('امنیت L2', 'امنیت L2'),
        ('امنیت L3 uRPF', 'امنیت L3 uRPF'),
        ('امنیت L4', 'امنیت L4'),
        ('Segmentation', 'Segmentation'),
    ]))
    levels.append(_sub('۵۷.۲ کنترل\u200cها', [
        ('Firewall Policy Design', 'Firewall Policy Design'),
        ('IDS IPS', 'IDS IPS'),
        ('VPN امن', 'VPN امن'),
        ('DDoS Mitigation', 'DDoS Mitigation'),
        ('Remote Access ZTNA', 'Remote Access ZTNA'),
    ]))
    C.append((57, 'فصل ۵۷: امنیت شبکه', 'Ch57 NetSec', levels))

    levels = []
    levels.append(_sub('۵۸.۱ Endpoint', [
        ('EDR', 'EDR'),
        ('XDR', 'XDR'),
        ('Hardening Endpoint', 'Hardening Endpoint'),
    ]))
    levels.append(_sub('۵۸.۲ Application', [
        ('OWASP Top 10', 'OWASP Top 10'),
        ('Secure Coding', 'Secure Coding'),
        ('WAF', 'WAF'),
        ('API Security', 'API Security'),
    ]))
    levels.append(_sub('۵۸.۳ DevSecOps', [
        ('CI/CD Security', 'CI/CD Security'),
        ('Container Scanning', 'Container Scanning'),
        ('Supply Chain', 'Supply Chain'),
        ('Secrets Management', 'Secrets Management'),
    ]))
    C.append((58, 'فصل ۵۸: Endpoint AppSec DevSecOps', 'Ch58 AppSec', levels))

    levels = []
    levels.append(_sub('۵۹.۱ SOC', [
        ('SOC مدل\u200cها', 'SOC مدل\u200cها'),
        ('SIEM Use Cases', 'SIEM Use Cases'),
        ('SOAR Playbook', 'SOAR Playbook'),
        ('Shift Scheduling', 'Shift Scheduling'),
    ]))
    levels.append(_sub('۵۹.۲ IR', [
        ('Preparation', 'Preparation'),
        ('Detection', 'Detection'),
        ('Containment', 'Containment'),
        ('Eradication', 'Eradication'),
        ('Recovery', 'Recovery'),
        ('Lessons Learned', 'Lessons Learned'),
    ]))
    levels.append(_sub('۵۹.۳ Hunting Forensics', [
        ('MITRE ATT&CK', 'MITRE ATT&CK'),
        ('Hypothesis Hunting', 'Hypothesis Hunting'),
        ('Disk Memory Forensics', 'Disk Memory Forensics'),
        ('Evidence Handling', 'Evidence Handling'),
    ]))
    C.append((59, 'فصل ۵۹: SOC IR Hunting', 'Ch59 SOC', levels))

    levels = []
    levels.append(_sub('۶۰.۱ روش\u200cشناسی', [
        ('Symptom to Root Cause', 'Symptom to Root Cause'),
        ('Bottom-Up', 'Bottom-Up'),
        ('Top-Down', 'Top-Down'),
        ('Divide and Conquer', 'Divide and Conquer'),
        ('Follow the Path', 'Follow the Path'),
        ('Compare Known-Good', 'Compare Known-Good'),
        ('Baseline', 'Baseline'),
        ('Change History', 'Change History'),
    ]))
    levels.append(_sub('۶۰.۲ عیب\u200cیابی عملی', [
        ('Network TS Tools', 'Network TS Tools'),
        ('Windows TS', 'Windows TS'),
        ('Linux TS', 'Linux TS'),
        ('Wireshark Capture', 'Wireshark Capture'),
        ('Filter و TCP Stream', 'Filter و TCP Stream'),
        ('DNS DHCP ARP TS', 'DNS DHCP ARP TS'),
    ]))
    levels.append(_sub('۶۰.۳ هک اخلاقی Lab', [
        ('قوانین Authorized Only', 'قوانین Authorized Only'),
        ('Reconnaissance', 'Reconnaissance'),
        ('Scanning', 'Scanning'),
        ('Enumeration', 'Enumeration'),
        ('VA', 'VA'),
        ('Exploitation در Lab', 'Exploitation در Lab'),
        ('PrivEsc مفهوم', 'PrivEsc مفهوم'),
        ('Reporting', 'Reporting'),
    ]))
    levels.append(_sub('۶۰.۴ ابزار Lab', [
        ('Nmap', 'Nmap'),
        ('Wireshark', 'Wireshark'),
        ('Burp Suite', 'Burp Suite'),
        ('Metasploit Lab', 'Metasploit Lab'),
        ('Nessus OpenVAS', 'Nessus OpenVAS'),
        ('BloodHound Lab', 'BloodHound Lab'),
    ]))
    levels.append(_sub('۶۰.۵ لاب سازمانی', [
        ('LAB-01 دفتر ۵۰ کاربر', 'LAB-01 دفتر ۵۰ کاربر'),
        ('LAB-02 سازمان ۳۰۰ کاربر', 'LAB-02 سازمان ۳۰۰ کاربر'),
        ('LAB-03 سازمان ۱۰۰۰ کاربر', 'LAB-03 سازمان ۱۰۰۰ کاربر'),
        ('LAB-04 چندسایت ۳۰۰۰ کاربر', 'LAB-04 چندسایت ۳۰۰۰ کاربر'),
        ('LAB-05 Data Center EVPN', 'LAB-05 Data Center EVPN'),
        ('LAB-06 Hybrid Cloud', 'LAB-06 Hybrid Cloud'),
        ('LAB-07 SOC Detection', 'LAB-07 SOC Detection'),
        ('LAB-08 Ransomware Response', 'LAB-08 Ransomware Response'),
        ('LAB-09 قطع لینک Core', 'LAB-09 قطع لینک Core'),
        ('LAB-10 DNS Disaster', 'LAB-10 DNS Disaster'),
        ('LAB-11 AD Disaster', 'LAB-11 AD Disaster'),
        ('LAB-12 VoIP Quality', 'LAB-12 VoIP Quality'),
        ('LAB-13 Wireless Capacity', 'LAB-13 Wireless Capacity'),
        ('LAB-14 Storage Failure', 'LAB-14 Storage Failure'),
        ('LAB-15 Capstone کامل', 'LAB-15 Capstone کامل'),
        ('LAB-16 Dual ISP FortiGate HA', 'LAB-16 Dual ISP FortiGate HA'),
        ('LAB-17 MikroTik QoS 500 User', 'LAB-17 MikroTik QoS 500 User'),
        ('LAB-18 Cisco Campus 802.1X', 'LAB-18 Cisco Campus 802.1X'),
        ('LAB-19 VMware Cluster HA', 'LAB-19 VMware Cluster HA'),
        ('LAB-20 Backup Immutable DR', 'LAB-20 Backup Immutable DR'),
    ]))
    C.append((60, 'فصل ۶۰: عیب\u200cیابی هک اخلاقی لاب سازمانی', 'Ch60 Labs', levels))

    # ========== فاز A: Operations & Architecture ==========
    levels = []
    levels.append(_sub("۶۱.۱ مهندسی نیازمندی و معماری", [
        ("Business Requirements", "Business Requirements"),
        ("Technical Requirements", "Technical Requirements"),
        ("HLD طراحی سطح بالا", "HLD"),
        ("LLD طراحی سطح پایین", "LLD"),
        ("Reference Architecture", "Reference Architecture"),
        ("BOM و BoQ", "BOM BoQ"),
        ("انتخاب Vendor و Technology", "Vendor Selection"),
        ("Migration Planning", "Migration Planning"),
    ]))
    levels.append(_sub("۶۱.۲ مفاهیم قابلیت اطمینان", [
        ("SPOF", "SPOF"),
        ("Failure Domain و Blast Radius", "Failure Domain"),
        ("RTO و RPO", "RTO RPO"),
        ("SLA SLO SLI", "SLA SLO SLI"),
        ("MTBF و MTTR", "MTBF MTTR"),
        ("Redundancy و Resilience", "Redundancy"),
        ("Availability و Reliability", "Availability"),
        ("Scalability و Headroom", "Scalability"),
    ]))
    levels.append(_sub("۶۱.۳ معماری دامنهها", [
        ("Network Architecture", "Network Architecture"),
        ("Server Architecture", "Server Architecture"),
        ("Storage Architecture", "Storage Architecture"),
        ("Security Architecture", "Security Architecture"),
        ("Cloud و Hybrid Architecture", "Hybrid Architecture"),
        ("Multi-Site Architecture", "Multi-Site Architecture"),
        ("Cost Estimation و Licensing", "Cost Licensing"),
    ]))
    levels.append(_sub("۶۱.۴ ظرفیت و عملکرد", [
        ("Capacity Planning کاربران و پورت", "Capacity Ports"),
        ("Bandwidth و PoE Budget", "Capacity Bandwidth"),
        ("Performance Baseline", "Performance Baseline"),
        ("Bottleneck Analysis", "Bottleneck"),
        ("Percentile 95 99", "Percentiles"),
        ("سناریو ARCH-3000-USER", "Scenario ARCH-3000"),
    ]))
    C.append((61, "فصل ۶۱: معماری سازمانی Enterprise Architecture", "Ch61 Enterprise Architecture", levels))

    levels = []
    levels.append(_sub("۶۲.۱ عملیات روزانه", [
        ("Daily Operations", "Daily Operations"),
        ("Shift Handover", "Shift Handover"),
        ("Health Check روتین", "Health Check"),
        ("Alert Handling", "Alert Handling"),
        ("Monitoring Review", "Monitoring Review"),
        ("Backup Verification روزانه", "Backup Verification"),
        ("Certificate Expiration Review", "Cert Review"),
        ("License و Support Review", "License Review"),
    ]))
    levels.append(_sub("۶۲.۲ Incident و Change", [
        ("Incident Handling عملیاتی", "Incident Ops"),
        ("Escalation Path", "Escalation"),
        ("Change Request تا Closure", "Change Lifecycle"),
        ("Risk و Impact Assessment", "Change Risk"),
        ("Maintenance Window", "Maintenance Window"),
        ("Validation و Rollback", "Change Validation"),
        ("Post-Implementation Review", "PIR"),
    ]))
    levels.append(_sub("۶۲.۳ نگهداری و انطباق", [
        ("Patch و Firmware عملیاتی", "Patch Ops"),
        ("Configuration Review", "Config Review"),
        ("Account و Access Review", "Access Review"),
        ("Capacity Review دوره‌ای", "Capacity Review"),
        ("سناریو OPS-NOC-DAY-SHIFT", "Scenario NOC Shift"),
    ]))
    C.append((62, "فصل ۶۲: عملیات IT و NOC", "Ch62 IT Operations", levels))

    levels = []
    levels.append(_sub("۶۳.۱ انواع مستند عملیاتی", [
        ("Runbook چیست و ساختار آن", "Runbook Structure"),
        ("MOP Method of Procedure", "MOP"),
        ("SOP Standard Operating Procedure", "SOP"),
        ("EOP Emergency Operating Procedure", "EOP"),
        ("Preconditions و Backup قبل از تغییر", "Preconditions"),
        ("Validation Evidence و Rollback", "Validation Rollback"),
        ("Escalation در مستند", "Doc Escalation"),
    ]))
    levels.append(_sub("۶۳.۲ Configuration و Compliance", [
        ("Golden Configuration", "Golden Config"),
        ("Config Backup و Versioning", "Config Versioning"),
        ("Config Diff و Drift Detection", "Config Drift"),
        ("Configuration Compliance Checks", "Config Compliance"),
        ("Baseline در برابر Current", "Config Baseline"),
    ]))
    levels.append(_sub("۶۳.۳ دارایی و CMDB", [
        ("IT Asset Inventory", "Asset Inventory"),
        ("CMDB و Relationship", "CMDB"),
        ("Serial Asset ID Location Owner", "Asset Fields"),
        ("Dependency Mapping سرویس", "Service Dependency"),
        ("سناریو DISC-UNKNOWN-NETWORK", "Scenario Discovery"),
    ]))
    levels.append(_sub("۶۳.۴ الگوهای Runbook نمونه", [
        ("RUNBOOK-WAN-DOWN", "Runbook WAN Down"),
        ("RUNBOOK-AD-AUTH-FAILURE", "Runbook AD Auth"),
        ("RUNBOOK-FIREWALL-HA-FAILOVER", "Runbook FW HA"),
        ("MOP-CORE-SWITCH-UPGRADE", "MOP Core Upgrade"),
        ("EOP-RANSOMWARE-ISOLATION", "EOP Ransomware"),
    ]))
    C.append((63, "فصل ۶۳: مستندسازی Runbook و CMDB", "Ch63 Documentation CMDB", levels))


    return C

def _chapter_number(title):
    if not title:
        return None
    m = re.search(r"فصل\s*۰*(\d+)|فصل\s*(\d+)|Ch0*(\d+)", str(title), re.I)
    if not m:
        return None
    for g in m.groups():
        if g:
            return int(g)
    return None

def _normalize_title(s):
    if not s:
        return ""
    return re.sub(r"\s+", " ", str(s).replace("\u200c", " ")).strip().lower()

def seed_from_full_curriculum(db):
    cur = get_full_curriculum()
    existing = db.fetchall("SELECT * FROM chapters ORDER BY order_index, id")
    by_number = {}
    for ch in existing:
        num = _chapter_number(ch["title_fa"]) or ch["order_index"]
        if num is not None and num not in by_number:
            by_number[num] = ch
    added = {"chapters": 0, "levels": 0, "lessons": 0}
    for order, title_fa, title_en, levels in cur:
        ch = by_number.get(order)
        if ch is None:
            ch_id = db.add_chapter(title_fa, title_en, order_index=order)
            added["chapters"] += 1
        else:
            ch_id = ch["id"]
            db.execute(
                "UPDATE chapters SET title_fa=?, title_en=?, order_index=?, is_active=1 WHERE id=?",
                (title_fa, title_en, order, ch_id),
            )
        existing_levels = {_normalize_title(lv["title_fa"]): lv["id"] for lv in db.get_levels(ch_id)}
        for li, (lv_title, lessons) in enumerate(levels, 1):
            key = _normalize_title(lv_title)
            lv_id = existing_levels.get(key)
            if lv_id is None:
                lv_id = db.add_level(ch_id, lv_title, order_index=li)
                added["levels"] += 1
                existing_levels[key] = lv_id
            else:
                try:
                    db.execute(
                        "UPDATE levels SET title_fa=?, order_index=?, is_active=1 WHERE id=?",
                        (lv_title, li, lv_id),
                    )
                except Exception:
                    pass
            existing_lessons = {_normalize_title(x["title_fa"]): x["id"] for x in db.get_lessons(lv_id)}
            for oi, (lfa, len_) in enumerate(lessons, 1):
                if _normalize_title(lfa) not in existing_lessons:
                    tag = lfa[1:3] if lfa.startswith("[L") else "L0"
                    db.add_lesson(lv_id, lfa, len_, order_index=oi, tags=tag)
                    added["lessons"] += 1
    try:
        db.execute("UPDATE chapters SET is_active=1")
    except Exception:
        pass
    return added

def rebuild_curriculum_from_scratch(db):
    db.execute("DELETE FROM lesson_history")
    try:
        db.execute("DELETE FROM lessons_fts")
    except Exception:
        pass
    db.execute("DELETE FROM lessons")
    db.execute("DELETE FROM levels")
    db.execute("DELETE FROM chapters")
    return seed_from_full_curriculum(db)

def get_meta_template(title_fa, level_code="L2", chapter="", vendors=None):
    """قالب Meta برای هر درس — مرحله بعد موتور محتوا"""
    return {
        "title": title_fa,
        "level": level_code,
        "chapter": chapter,
        "description": f"آموزش «{title_fa}» در سطح {level_code} برای مهندس شبکه/سیستم/امنیت.",
        "learning_objectives": [
            f"درک مفهومی {title_fa}",
            "پیاده‌سازی عملی",
            "عیب‌یابی و Hardening",
        ],
        "keywords_fa": [title_fa],
        "keywords_en": [],
        "vendors": vendors or [],
        "command_categories": ["show", "config", "troubleshoot", "security", "automation"],
        "ai_teaching_prompt": (
            f"موضوع را در سطح {level_code} آموزش بده. شامل مفهوم، معماری، پیکربندی، "
            f"دستورات با توضیح آرگومان، مثال سازمانی، عیب‌یابی و امنیت."
        ),
        "ai_search_prompt": (
            f"جستجو فقط از منابع معتبر Vendor/RFC برای: {title_fa} سطح {level_code}"
        ),
    }
