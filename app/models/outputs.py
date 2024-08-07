from typing import List, Optional

from pydantic import BaseModel


class ValidationOutput(BaseModel):
    reason: str
    verdict: str
    missing_tables: Optional[List[str]] = None
