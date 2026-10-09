#!/usr/bin/env bash
# یک‌بار اجرا کن تا فایل‌های شلختهٔ ریشه tools مرتب شوند
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

mkdir -p tools/packs/switching_routing
mkdir -p tools/packs/windows_server
mkdir -p tools/packs/git_chapter64
mkdir -p tools/engineer_jokar_wireless_security
mkdir -p tools/engineer_jokar_security_ethical_hacking
mkdir -p tools/engineer_jokar_automation_python

# move loose JSON if present
[ -f tools/switching_routing_curriculum_pack.json ] && mv -f tools/switching_routing_curriculum_pack.json tools/packs/switching_routing/
[ -f tools/windows_server_complete_curriculum_pack.json ] && mv -f tools/windows_server_complete_curriculum_pack.json tools/packs/windows_server/
[ -f tools/wireless_security_pack.json ] && mv -f tools/wireless_security_pack.json tools/engineer_jokar_wireless_security/
[ -f tools/Git_Chapter_64_Full.md ] && mv -f tools/Git_Chapter_64_Full.md tools/packs/git_chapter64/

# optional: keep zips in archive
mkdir -p tools/_archive_zips
for z in tools/*.zip; do
  [ -f "$z" ] && mv -f "$z" tools/_archive_zips/ || true
done

echo "Done. Current tools layout:"
find tools -maxdepth 3 -type f | sort | head -80
