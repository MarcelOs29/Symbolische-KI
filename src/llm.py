import instructor
import inspect


class LLM:
    """
    Wrapper class for LLM interactions and prompt engineering.
    """

    client: instructor.AsyncInstructor

    def __init__(self, model_name: str, mode: instructor.Mode = instructor.Mode.MD_JSON):
        self.model_name = model_name

        self.client = instructor.from_provider(
            model_name,
            mode=mode
        )

    async def response_model(self, solution: str, original_problem: str) -> str:
        """
        Formulates a human-readable answer based on the solution and original problem.
        :param solution: The solution obtained from Z3.
        :param original_problem: The original natural language problem description.
        :return: A human-readable string summarizing the solution.
        """
        print(f"\nFormulating human-readable answer for solution: {solution}")
        result = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": 
                        "You will get a solution for a given problem which was solved by Z3.\n"
                        "Your task is to print the solution in a human-readable format in one sentence.\n"
                        "Example output: 'The values are varaible_name1=5, varaible_name2=10, varaible_name3=3 which satisfy all constraints.' or 'The problem is unsatisfiable.' or 'There was an error during solving or parsing to z3 problem.'\n\n"
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
        """
        Generates a Z3 problem representation from a natural language prompt.
        :param prompt: The natural language description of the problem.
        :param instruct: The Pydantic model class to parse the response into.
        :param max_retries: Maximum number of retries for the LLM call.
        :return: The Z3 problem representation as a String
        """
        print(f"\n\nStart LLM with prompt: {prompt}")
        result = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": (
                        "You are an expert in Z3 and translate user queries into formal constraints.\n"
                        "Target format: Extract variables (list), constraints (list) and types (object). types: Only specify types for Real or Bool. The default type is Int and does not need to be listed.\n\n"
                        "Four Strict rules which all must be followed: \n"
                        "1. Permitted types & functions: Bool, Real, And, Or, Not, Xor, Implies, If, Distinct. "
                        "2. Permitted operators: +, -, *, /, %, &, |, ^, ==, !=, <, <=, >, >=.\n"
                        "3. No chaining: Always convert chained constraints to atomic ones. Examples: [a < b < c] becomes [“a < b”, “b < c”] and [x And y == 4] becomes [“x == 4”, “y == 4”].\n"                        
                        "4. Variables: Only use variables that you derive yourself from the query.\n\n"
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