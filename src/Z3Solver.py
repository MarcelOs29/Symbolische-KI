import re
from typing import Optional
from Z3Problem import Z3Problem
from z3 import And, Or, Not, Implies, If, Distinct, Xor
from z3 import Int, Bool, Real
from z3 import sat, Solver

# Restrict the eval environment to allowed symbols only
ALLOWED_SYMBOLS = {
    "and": And,
    "or": Or,
    "not": Not,
    "xor": Xor,
    "implies": Implies,
    "if": If,
    "distinct": Distinct,
    "true": True,
    "false": False,
}

DEFAULT_BITVEC_WIDTH = 32

class Z3Solver:
    """
    A class to solve Z3 problems defined by Z3Problem instances.
    """

    z3_problem: Z3Problem

    def __init__(self, z3_problem: Z3Problem):
        self.z3_problem = z3_problem

    def make_var(self, name: str, type_hint: Optional[str]):
        """
        Creates a Z3 variable based on the provided name and optional type hint.
        :param name: The name of the variable.
        :param type_hint: The optional type hint for the variable. Default is Int.
        :return: A Z3 variable of the appropriate type.
        """
        if type_hint:
            normalized = type_hint.strip().lower()
            if normalized == "int":
                return Int(name)
            if normalized == "bool":
                return Bool(name)
            if normalized == "real":
                return Real(name)
            if normalized.startswith("bitvec"):
                raise ValueError("BitVec type is not supported due to LLM limitations.")
            raise ValueError(f"Unknown Z3 type for variable '{name}': {type_hint}")
        return Int(name)

    def solve(self):
        """
        Solves the given Z3 problem.

        :return: A solution to the problem or None if no solution is found.
        """

        print(f"\n--- Z3-Solver is starting ---")
        print(f"Variables: {self.z3_problem.variables}")
        print(f"Constraints: {self.z3_problem.constraints}")
        print(f"Types: {self.z3_problem.types}")

        s = Solver()

        try:
            type_from_llm = self.z3_problem.types or {}
            z3_vars = {
                var: self.make_var(var, type_from_llm.get(var))
                for var in self.z3_problem.variables
            }
            eval_env = {**z3_vars, **ALLOWED_SYMBOLS}
            for const_str in self.z3_problem.constraints:
                const_str = const_str.lower()
                const_str_eval = (
                    const_str.replace("&&", "&")
                             .replace("||", "|")
                             .replace("->", "implies")
                             .replace("=>", "implies")
                             .replace("→", "implies")
                )

                expr = eval(const_str_eval, {"__builtins__": {}}, eval_env)
                s.add(expr)
            
            # The actual solving step
            check = s.check()

            if check == sat:
                model = s.model()
                result = {
                    "status": "satisfiable",
                    "model": {str(d): model[d] for d in model.decls()}
                }
            else:
                result = {
                    "status": "unsatisfiable",
                    "model": None
                }

        except Exception as e:
            print(f"[Z3-Error] Could not parse constraints: {e}")
            result = {
                "status": "error",
                "message": str(e)
            }
        
        print(f"--- Z3-Solver finished ---")
        return result
