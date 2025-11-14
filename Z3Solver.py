import re
from typing import Optional

from Z3Problem import Z3Problem
from z3 import And, Bool, BoolVal, Int, IntVal, Not, Or, Real, RealVal, Solver, Xor, BitVec, BitVecVal, RotateLeft, sat

ALLOWED_SYMBOLS = {
    "And": And,
    "Or": Or,
    "Not": Not,
    "Xor": Xor,
    "IntVal": IntVal,
    "BoolVal": BoolVal,
    "Bool": Bool,
    "RealVal": RealVal,
    "True": True,
    "False": False,
    "BitVecVal": BitVecVal,
    "RotateLeft": RotateLeft,
}

DEFAULT_BITVEC_WIDTH = 32

class Z3Solver:
    """
    Eine Klasse zur Interaktion mit dem Z3-Solver.
    """

    z3_problem: Z3Problem
    def __init__(self, z3_problem: Z3Problem):
        self.z3_problem = z3_problem

    @staticmethod
    def _make_var(name: str, type_hint: Optional[str]):
        if type_hint:
            normalized = type_hint.strip().lower()
            if normalized == "int":
                return Int(name)
            if normalized == "bool":
                return Bool(name)
            if normalized == "real":
                return Real(name)
            if normalized.startswith("bitvec"):
                digits = re.findall(r"\d+", type_hint)
                width = int(digits[0]) if digits else DEFAULT_BITVEC_WIDTH
                return BitVec(name, width)
            raise ValueError(f"Unbekannter Z3-Typ für Variable '{name}': {type_hint}")
        return Int(name)

    def solve(self):
        """
        Löst das gegebene Z3-Problem.

        :return: Eine Lösung des Problems oder None, wenn keine Lösung gefunden wurde.
        """

        print(f"\n--- Z3-Solver wird gestartet ---")
        print(f"Variablen: {self.z3_problem.variables}")
        print(f"Constraints: {self.z3_problem.constraints}")
        print(f"Typen: {self.z3_problem.types}")

        s = Solver()

        try:
            type_from_llm = self.z3_problem.types or {}
            z3_vars = {
                var: self._make_var(var, type_from_llm.get(var))
                for var in self.z3_problem.variables
            }
            eval_env = {**z3_vars, **ALLOWED_SYMBOLS}
            for const_str in self.z3_problem.constraints:
                # Überstezte die Strings in Z3-Ausdrücke und füge sie dem Solver hinzu.
                expr = eval(const_str, {"__builtins__": {}}, eval_env)
                s.add(expr)

            check = s.check()

            if check == sat:
                model = s.model()
                result = {
                    "status": "lösbar",
                    "modell": {str(d): model[d] for d in model.decls()}
                }
            else:
                result = {
                    "status": "unlösbar",
                    "modell": None
                }

        except Exception as e:
            print(f"[Z3-Fehler] Konnte Constraints nicht parsen: {e}")
            result = {
                "status": "fehler",
                "message": str(e)
            }
        
        print(f"Ergebnis: {result}")
        print(f"--- Z3-Solver beendet ---")
        return result
