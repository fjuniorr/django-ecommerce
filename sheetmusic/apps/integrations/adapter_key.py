import re
from dataclasses import dataclass
from typing import List

_KEY_RE = re.compile(
    r'^(?P<provider>[a-z0-9_-]+)\.(?P<api_version>[a-z0-9_-]+)\.(?P<kind>[a-z0-9_-]+)'
    r'(?:\.(?P<channel>[a-z0-9_-]+))?(?:\.(?P<program>[a-z0-9_-]+))?'
    r'(?:@(?P<ingest>[a-z0-9_-]+))?(?:\#(?P<schema_version>[a-z0-9_-]+))?'
    r'(?::(?P<format>[a-z0-9_-]+))?(?P<flags>(?:\+[a-z0-9_-]+)*)$'
)


@dataclass
class AdapterKey:
    provider: str
    api_version: str
    kind: str
    channel: str | None = None
    program: str | None = None
    ingest: str | None = None
    schema_version: str | None = None
    format: str | None = None
    flags: List[str] | None = None

    @classmethod
    def parse(cls, key_str: str) -> "AdapterKey":
        m = _KEY_RE.match(key_str)
        if not m:
            raise ValueError(f"invalid adapter key: {key_str}")
        flags = [f for f in m.group('flags').split('+') if f]
        return cls(**{**m.groupdict(), "flags": flags})

    def fallback_candidates(self) -> List[str]:
        parts = []
        base = f"{self.provider}.{self.api_version}.{self.kind}"
        if self.channel:
            base += f".{self.channel}"
        if self.program:
            base += f".{self.program}"
        if self.ingest:
            base += f"@{self.ingest}"
        if self.schema_version:
            base += f"#{self.schema_version}"
        if self.format:
            base += f":{self.format}"
        full = base
        if self.flags:
            full += "+" + "+".join(self.flags)
        candidates = [full]
        if self.flags:
            candidates.append(base)
        if self.format:
            base_no_format = base.rsplit(":", 1)[0]
            candidates.append(base_no_format)
            base = base_no_format
        if self.schema_version:
            base_no_schema = base.split("#", 1)[0]
            candidates.append(base_no_schema)
            base = base_no_schema
        if self.ingest:
            base_no_ingest = base.split("@", 1)[0]
            candidates.append(base_no_ingest)
            base = base_no_ingest
        if self.program:
            base_no_program = base.rsplit(".", 1)[0]
            candidates.append(base_no_program)
            base = base_no_program
        if self.channel:
            base_no_channel = base.rsplit(".", 1)[0]
            candidates.append(base_no_channel)
            base = base_no_channel
        core = f"{self.provider}.{self.api_version}.{self.kind}"
        candidates.append(core)
        candidates.append(f"{self.provider}.{self.api_version}.*")
        candidates.append(f"{self.provider}.*")
        candidates.append("*")
        return candidates
