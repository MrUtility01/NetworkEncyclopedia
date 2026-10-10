# محل ذخیره JSONهای تولیدشده

هر بستهٔ محتوایی که از ChatGPT می‌گیری اینجا بگذار:

```text
tools/packs/<نام_بسته>/<نام>_pack.json
```

مثال:
```text
tools/packs/ch14_routing_deep/routing_ospf_bgp_pack.json
tools/packs/ch67_vpn_enterprise/vpn_ipsec_ssl_pack.json
tools/packs/firewall_practical/firewall_practical_pack.json
tools/packs/ch60_troubleshooting/network_rca_pack.json
```

واردسازی:
```bash
python tools/apply_any_pack.py --db server/data/encyclopedia.db --pack tools/packs/.../file.json --apply
```
