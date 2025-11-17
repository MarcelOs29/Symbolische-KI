import instructor
import inspect

from typer import prompt

class LLM:
    client: instructor.AsyncInstructor

    def __init__(self, model_name: str):
        self.model_name = model_name

        self.client = instructor.from_provider(
            model_name,
        )

    async def response_model(self, solution: str, original_problem: str) -> str:
        print(f"\nFormulating human-readable answer for solution: {solution}")
        result = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": 
                        "You will get a solution for a given problem which was solved by Z3.\n"
                        "Your task is to print the solution in a human-readable format in one sentence.\n"
                        "Example output: 'The values are x=5, y=10, z=3 which satisfy all constraints.' or 'The problem is unsatisfiable.' or 'There was an error during solving or parsing to z3 problem.'\n\n"
                        f"Original Problem: {original_problem}\n"
                        f"Z3 Solution: {solution}\n"    
                },
            ],
            response_model=None,
            max_retries=1,
        )
        if inspect.isawaitable(result):
            result = await result

        result = result.choices[0].message.content
        if isinstance(result, str):
            return result.strip()
        return str(result)

    async def generate_z3_problem_string(self, prompt: str, instruct, max_retries: int = 3):
        print(f"\n\nStart LLM with prompt: {prompt}")
        result = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": (
                        "You are an expert in Z3 and translate user queries into formal constraints.\n"
                        "Target format: Extract variables (list), constraints (list) and types (object). types: Only specify types for BitVec (e.g. BitVec32) or Bool. The default type is Int and does not need to be listed.\n\n"
                        "Five Strict rules which all must be followed: \n"
                        "1. Permitted types & functions: BitVec, Bool, Real, And, Or, Not, Xor, Implies, If, Distinct, RotateLeft, RotateRight, LShR, Extract."
                        "2. Permitted operators: +, -, *, /, %, &, |, ^, ~, <<, >>, ==, !=, <, <=, >, >=.\n"
                        "3. No chaining: Always convert chained constraints to atomic ones. Examples: [a < b < c] becomes [“a < b”, “b < c”] and [x And y == 4] becomes [“x == 4”, “y == 4”].\n"                        
                        "4. Bit access: Access individual bits exclusively with the shift operator. Example: The 3rd bit of x is ((x >> 3) & 1). Never use x[3].\n"
                        "5. Variables: Only use variables that you derive yourself from the query.\n\n"
                        ""
                        f"Content: {prompt}"
                    ),
                },
            ],
            response_model=instruct,
            max_retries=max_retries,
        )
        if inspect.isawaitable(result):
            result = await result
        return result