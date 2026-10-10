# Schema رکورد دستور

```json
{
  "uid": "cmd:cisco:vlan:show-vlan-brief",
  "vendor": "cisco|mikrotik|fortigate|issabel|powershell|firewall_generic",
  "platform": "IOS-XE|ROS7|FortiOS|Asterisk|Windows",
  "category": "switching|routing|firewall|vpn|voice|identity|monitor|troubleshoot",
  "subcategory": "vlan",
  "level": "L0|L1|L2|L3|L4",
  "title_fa": "نمایش وضعیت VLAN",
  "title_en": "show vlan brief",
  "command": "show vlan brief",
  "aliases": ["sh vlan br"],
  "syntax": "show vlan [brief | id <vlan-id>]",
  "arguments": [
    {"name": "brief", "required": false, "meaning_fa": "خروجی فشرده", "example": "show vlan brief"}
  ],
  "when_to_use_fa": "دیدن VLANها و پورت‌های عضو",
  "prerequisites_fa": ["enable"],
  "steps_fa": ["enable", "اجرای دستور", "خواندن Status و Ports"],
  "sample_output": "...",
  "output_fields_fa": [{"field": "Status", "meaning": "active/act/lshut"}],
  "related_commands": ["show interfaces status"],
  "common_mistakes_fa": ["اشتباه access با trunk"],
  "lab_hint_fa": "دو سوییچ GNS3 و یک VLAN",
  "security_notes_fa": "خروجی توپولوژی را فاش می‌کند",
  "search_keywords": ["vlan", "show vlan", "عضویت پورت"],
  "flashcards": [
    {"front": "عضویت پورت در VLAN؟", "back": "show vlan brief"}
  ],
  "assessment": {
    "questions": [{
      "id": "q1",
      "prompt": "کدام دستور عضویت VLAN را سریع نشان می‌دهد؟",
      "options": ["show vlan brief", "show ip route", "ping", "show version"],
      "type": "mcq"
    }],
    "answer_key": [{"id": "q1", "correct_index": 0, "explain_fa": "مخصوص membership"}]
  }
}
```

بسته:
```json
{
  "package_schema_version": 1,
  "project": "ENGINEER JOKAR / NetworkEncyclopedia",
  "purpose": "commands encyclopedia",
  "chapter_order": 68,
  "chapter_title_fa": "دانشنامه جامع دستورات",
  "commands": []
}
```
