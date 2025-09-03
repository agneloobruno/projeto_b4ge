from __future__ import annotations
import csv
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Any, Dict, Iterable, List, Optional

# ---------- parsing numérico ----------
def to_decimal(x: Any, default: Optional[Decimal] = None) -> Optional[Decimal]:
    if x is None:
        return default
    if isinstance(x, Decimal):
        return x
    s = str(x).strip().replace(",", ".")
    if s == "" or s.lower() in {"na", "n/a", "none", "null", "-"}:
        return default
    try:
        return Decimal(s)
    except (InvalidOperation, ValueError):
        return default

# ---------- normalização de unidade ----------
_UNIT_ALIASES = {
    "kg": "kg", "quilo": "kg", "kilo": "kg",
    "g": "g",  "t": "t",
    "m3": "m3", "m^3": "m3", "m³": "m3",
    "m2": "m2", "m^2": "m2", "m²": "m2",
    "un": "un", "unid": "un", "unidade": "un",
    "mj": "MJ", "gj": "GJ",
}
def norm_unit(u: Any) -> Optional[str]:
    if not u:
        return None
    key = str(u).strip().lower()
    return _UNIT_ALIASES.get(key, key)

# ---------- CSV ----------
def read_csv(path: str, delimiter: str = None, encoding: str = "utf-8") -> Iterable[Dict[str, str]]:
    with open(path, "r", encoding=encoding, newline="") as f:
        sample = f.read(4096)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=[",", ";", "\t"])
            delim = delimiter or dialect.delimiter
        except csv.Error:
            delim = delimiter or ";"
        reader = csv.DictReader(f, delimiter=delim)
        for row in reader:
            yield { (k or "").strip(): (v or "").strip() for k, v in row.items() }

@dataclass
class ImportResult:
    created: int = 0
    updated: int = 0
    skipped: int = 0
    errors: List[str] = None
    def __post_init__(self):
        if self.errors is None:
            self.errors = []

# ---------- helpers simples ----------
def pick(row: Dict[str, str], *aliases: str, default: Any = None) -> Any:
    for a in aliases:
        if a in row and row[a] != "":
            return row[a]
    return default
