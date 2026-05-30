from dataclasses import dataclass
from typing import Optional


@dataclass
class AuthResult:
    success: bool
    username: Optional[str] = None