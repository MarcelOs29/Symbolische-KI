import llm
import asyncio
from Z3Problem import Z3Problem
from Z3Solver import Z3Solver
## This is the main file for the project which initializes the application.

async def main():
    print("Application has started.")
    ## Integer Probleme
    problem_question = []
    problem_question.append("Find three positive integers x, y and z. The product of x and y should be 72. z should be the remainder when x is divided by y. The sum of all three numbers (x, y, z) must be less than 30 and x must be greater than y.")
    problem_question.append("I am looking for four integers a, b, c and d. The sum of a and b is 15. c is three times d. b must be greater than c. All numbers must be positive, and the sum of all four numbers must not exceed 40.")
    problem_question.append("We are looking for two integers k and m. k must be an even number between 10 and 50 (inclusive). m must be an odd number. k must be equal to 4 times m plus 6.")

    for question in problem_question:
         await solve_problem(question)

    # Real Number Probleme
    problem_question_real = []
    problem_question_real.append("Find two real numbers x and y. Their sum should be 12.5. If you multiply x by 2.0 and add y, the result should be 20.0.")
    problem_question_real.append("Find three real numbers a, b and c. a must be between 1.1 and 5.5. b must be greater than twice a. c is the sum of a and b, and c must be less than 15.0.")
    problem_question_real.append("Find a positive real number z. The square of z (i.e. z multiplied by itself) must be greater than 10.0 but less than 50.0. Furthermore, 3.0 times z must be greater than 7.5.")

    for question in problem_question_real:
         await solve_problem(question)

    # Mixed Probleme
    problem_question_mixed = []
    problem_question_mixed.append("Find an integer quantity and a real number price. quantity must be between 5 and 20. price must be greater than 9.99. The product of quantity (as a real number) and price must be less than 150.75.")
    problem_question_mixed.append("Find two positive integers x and y. If x is greater than 10, then y must be twice x. Otherwise (if x is less than or equal to 10), y must be equal to x plus 5. In either case, the sum of x and y must be 30.")
    
    for question in problem_question_mixed:
        await solve_problem(question)

async def solve_problem(problem_question: str):
    modelSolver = llm.LLM(model_name="ollama/qwen3:1.7b")
    answerModel = llm.LLM(model_name="ollama/qwen3:0.6b")
    
    solver_input = await modelSolver.generate_z3_problem_string(
        prompt=problem_question,
        instruct=Z3Problem,)
    
    print(f"\n--- LLM Problem description for z3 Solver: {solver_input} ---")
    solver_result = Z3Solver(solver_input).solve()

    solution_human_readable = await answerModel.response_model( 
        solution=str(solver_result),
        original_problem=problem_question
    )    
    print(solution_human_readable)

if __name__ == "__main__":
    asyncio.run(main())