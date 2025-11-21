import instructor
import llm
import asyncio
from Z3Problem import Z3Problem
from Z3Solver import Z3Solver

async def solve_batch(questions, hosts):
    if not hosts:
        for question in questions:
            await solve_problem(question)
        return

    queue = asyncio.Queue()
    for question in questions:
        queue.put_nowait(question)

    async def worker(host):
        while True:
            try:
                question = queue.get_nowait()
            except asyncio.QueueEmpty:
                break
            await solve_problem(question, host_config=host)

    tasks = [asyncio.create_task(worker(host)) for host in hosts]
    await asyncio.gather(*tasks)

async def main():
    print("Application has started.")
    hosts = [
        # {
        #     "url": "http://localhost:11434",
        # },
        {
            "url": "http://192.168.178.128:11434",
        },
        ]

    ## Integer Probleme
    problem_question = []
    problem_question.append("Find two integers x and y such that x + y = 10 and x - y = 4.")
        # Possible Expected solution: x=7, y=3
    problem_question.append("Find three positive integers x, y and z. The product of x and y should be 72. z should be the remainder when x is divided by y. The sum of all three numbers (x, y, z) must be less than 30 and x must be greater than y.")
        # Possible Expected solution: x=9, y=8, z=1
    problem_question.append("I am looking for four integers a, b, c and d. The sum of a and b is 15. c is three times d. b must be greater than c. All numbers must be positive, and the sum of all four numbers must not exceed 40.")
        # Possible Expected solution: a=11, b=4, c=3, d=1
    problem_question.append("We are looking for two integers k and m. k must be an even number between 10 and 50 (inclusive). m must be an odd number. k must be equal to 4 times m plus 6.")
        # Possible Expected solution: k=10, m=1

    # Real Number Probleme
    problem_question_real = []
    problem_question_real.append("Find two real numbers x and y. Their sum should be 12.5. If you multiply x by 2.0 and add y, the result should be 20.0.")
        # Possible Expected solution: x=7.5, y=5.0
    problem_question_real.append("Find three real numbers a, b and c. a must be between 1.1 and 5.5. b must be greater than twice a. c is the sum of a and b, and c must be less than 15.0.")
        # Possible Expected solution: a=2.1, b=5.2, c=7.3
    problem_question_real.append("Find a positive real number z. The square of z (z multiplied by itself) must be greater than 10.0 but less than 50.0. Furthermore, 3.0 times z must be greater than 7.5.")
        # Possible Expected solution: z=7.0

    # Mixed Probleme
    problem_question_mixed = []
    problem_question_mixed.append("Find an integer quantity and a real number price. quantity must be between 5 and 20. price must be greater than 9.99. The product of quantity (as a real number) and price must be less than 150.75.")
        # Possible Expected solution: quantity=11, price=10.99
    problem_question_mixed.append("Find an interger count and a real number rate. count must be an even number between 2 and 30. rate must be greater than 1.5. The sum of count and rate must be less than 40.0, and the product of count (as a real number) and rate must be greater than 50.0.")
        # Possible Expected solution: count=22, rate=3.0

    # Not solvable problem
    not_solvable_problem = []
    not_solvable_problem.append("Find two integers x and y such that x + y = 5 and x + y = 10.")
        # Expected solution: No solution
    not_solvable_problem.append("Find three integers p, q and r such that p + q + r = 12, p > 10, q > 10 and r > 10.")
        # Expected solution: No solution
    
    problem_question.extend(problem_question_real)
    problem_question.extend(problem_question_mixed)
    problem_question.extend(not_solvable_problem)
    await solve_batch(problem_question, hosts)

async def solve_problem(problem_question: str, host_config= None):
    """
    Solves a Z3 problem generated from a natural language question using LLMs.
    :param problem_question: The natural language description of the problem.
    """

    default_host = "http://localhost:11434"

    if isinstance(host_config, dict):
        host = host_config.get("url", default_host)
    elif isinstance(host_config, str):
        host = host_config
    elif host_config is None:
        host = default_host
    else:
        raise TypeError("host_config must be a dict, str, or None.")


    # modelSolver = llm.LLM(model_name="ollama/qwen3:1.7b")
    modelSolver = llm.LLM(model_name="qwen3:1.7b", mode=instructor.Mode.TOOLS, host=host)
    answerModel = llm.LLM(model_name="qwen3:0.6b", host=host)

    solver_input = await modelSolver.generate_z3_problem_string(
        prompt=problem_question,
        instruct=Z3Problem)
    
    print(f"\n--- LLM Problem description for z3 Solver: {solver_input} ---")
    loop = asyncio.get_running_loop()
    solver_result = await loop.run_in_executor(None, lambda: Z3Solver(solver_input).solve())

    solution_human_readable = await answerModel.response_model( 
        solution=str(solver_result),
        original_problem=problem_question
    )    
    print(solution_human_readable)

if __name__ == "__main__":
    asyncio.run(main())