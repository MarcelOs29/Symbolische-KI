import time
import instructor
import inspect

from openai import AsyncOpenAI
from typing import Any, Dict, Optional


class LLM:
    """
    Wrapper class for LLM interactions and prompt engineering.
    """

    client: instructor.AsyncInstructor

    def __init__(self, model_name: str, mode: instructor.Mode = instructor.Mode.MD_JSON, host: str = "http://localhost:11434"):
        self.model_name = model_name

        self.openai_client = AsyncOpenAI(
            base_url=f"{host}/v1", 
            api_key="ollama"
        )
        self.client = instructor.from_openai(self.openai_client, mode=mode)

    async def response_model(self, solution: str, original_problem: str) -> str:
        """
        Formulates a human-readable answer based on the solution for a Z3 problem.
        :param solution: The solution obtained from Z3.
        :return: A human-readable string summarizing the solution.
        """
        print(f"\nFormulating human-readable answer for solution: {solution} on host {self.client.base_url}")
        start_time = round(time.time_ns() / 1_000_000)

        request: Dict[str, Any] = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": 
                        "You will get a solution for a given problem which was solved by Z3.\n"
                        "Your task is to print the solution in a human-readable format in one sentence.\n"
                        "Example output: 'The values are varaible_name1=5, varaible_name2=10, varaible_name3=3 which satisfy all constraints.' or 'The problem is unsatisfiable.' or 'There was an error during solving or parsing to z3 problem.'\n\n"
                        f"Z3 Solution: {solution}\n"    
                }
            ],
            "response_model": None,
            "max_retries": 1,
        }
        
        result = self.client.chat.completions.create(**request)

        if inspect.isawaitable(result):
            result = await result

        result = result.choices[0].message.content

        end_time = round(time.time_ns() / 1_000_000)
        processing_time = (end_time - start_time) / 1000.0
        print(f"LLM finished on host {self.client.base_url} with response time {processing_time} seconds")
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
        print(f"\n\nStart LLM with prompt: {prompt} on host {self.client.base_url}")
        start_time = round(time.time_ns() / 1_000_000)
        request: Dict[str, Any] = {
            "model": self.model_name,
            "messages": [
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
            "response_model": instruct,
            "max_retries": max_retries,
        }

        result = self.client.chat.completions.create(**request)
        if inspect.isawaitable(result):
            result = await result
        end_time = round(time.time_ns() / 1_000_000)
        processing_time = (end_time - start_time) / 1000.0
        print(f"LLM finished on host {self.client.base_url} with response time {processing_time} seconds.")
        return result