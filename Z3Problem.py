from typing import Dict, List, Optional

from pydantic import BaseModel, Field

class Z3Problem(BaseModel):
    """
    Ein Modell zur Definition eines Constraint-Problems für den Z3-Solver.
    """
    variables: List[str] = Field(
        ..., 
        description="Eine Liste aller eindeutigen Variablennamen im Problem, z.B. ['x', 'y', 'z']"
    )
    constraints: List[str] = Field(
        ...,
        description="Eine Liste von logischen oder arithmetischen Constraints als Strings, z.B. ['x > 10', 'y < 20', 'x + y == 25']"
    )
    types: Optional[Dict[str, str]] = Field(
        default=None,
        description="Optionale Zuordnung von Variablennamen zu Z3-Typen, z.B. {'x': 'Int', 'y': 'BitVec32'}"
    )