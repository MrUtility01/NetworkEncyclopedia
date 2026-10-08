# -*- coding: utf-8 -*-
from __future__ import annotations
import json
from pathlib import Path
_data = json.loads((Path(__file__).with_name("rich_data.json")).read_text(encoding="utf-8"))
COMMON = [tuple(x) for x in _data["COMMON"]]
BANKS = {k: [tuple(x) for x in v] for k, v in _data["BANKS"].items()}
ERRORS = {k: [tuple(x) for x in v] for k, v in _data["ERRORS"].items()}
