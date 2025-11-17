from typing import Dict, List, Optional

from pydantic import BaseModel, Field

class Z3Problem(BaseModel):
    """
    A class representing a Z3 problem with variables, constraints, and optional types.
    """
    variables: List[str] = Field(
        ..., 
        description="A list of all unique variable names in the problem, e.g., ['x', 'y', 'z']"
    )
    constraints: List[str] = Field(
        ...,
        description="A list of logical or arithmetic constraints as strings, e.g., ['x > 10', 'y < 20', 'x + y == 25']"
    )
    types: Optional[Dict[str, str]] = Field(
        default=None,
        description="Optional mapping of variable names to Z3 types, e.g., {'x': 'Int', 'y': 'BitVec32'}"
    )