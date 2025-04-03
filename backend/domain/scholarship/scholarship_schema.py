from pydantic import BaseModel
from typing import Optional

class ScholarshipName(BaseModel):
    name: Optional[str] = None


class ScholarshipRawText(BaseModel):
    raw_text: Optional[str] = None
