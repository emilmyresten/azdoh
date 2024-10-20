from dataclasses import dataclass


@dataclass(frozen=True)
class AzdohContext:
    file: str = None
