import llm
import asyncio
from Z3Problem import Z3Problem
from Z3Solver import Z3Solver
## This is the main file for the project which initializes the application.

async def main():
    print("Application has started.")
    problem_question = "Finde zwei ganze Zahlen x und y, so dass x + y = 10 und x - y = 4."
    await solve_problem(problem_question)

    print("\nEin weiteres einfaches Problem:")
    problem_question = "„Finde Werte für a, b, c, sodass a + b + c = 12, a > b, b = 2 * c und alle Variablen natürliche Zahlen sind."
    await solve_problem(problem_question)

    print("\nKomplexeres Problem mit int:")
    problem_question="Suche Werte für m, n, p mit m + n + p = 15, m > n > p, m ist gerade, n ist ungerade und p ≥ 2."
    await solve_problem(problem_question)

    # print("\nSehr komplexes Problem mit BitVectoren und speziellen Operationen:")
    # problem_question="Finde zwei 32-Bit-Ganzzahlen (Bitvektoren), x und y. Diese Zahlen müssen mehrere Bedingungen erfüllen: Erstens, wenn x um 5 Bits nach links rotiert wird, muss das Ergebnis, bitweise XOR-verknüpft mit y, gleich dem Hexadezimalwert 0xABCDEF12 sein. Zweitens muss x selbst ein Palindrom in seiner Binärdarstellung sein (d.h., das erste Bit ist gleich dem 32. Bit, das zweite gleich dem 31., usw.). Drittens muss y eine Zweierpotenz sein (also y > 0 und die bitweise AND-Verknüpfung von y und y-1 muss 0 ergeben) und gleichzeitig muss y größer als 1.000.000 sein. Viertens muss die Anzahl der gesetzten Bits (Population Count) in x ODER y (aber nicht in beiden) größer als 15 sein."
    # await solve_problem(problem_question)

    # print("\nSehr komplexes Problem mit Real-Zahlen, Bit-Vektoren und komplexer eingabe:")
    # problem_question="Suche einen 16-Bit-Bitvektor config und eine reelle Zahl ratio. Diese müssen folgende Bedingungen erfüllen: Der Bitvektor config muss in seinen oberen 8 Bits (dem 'high byte') genau 3 gesetzte Bits haben (Population Count = 3). Gleichzeitig müssen die unteren 8 Bits (das 'low byte') von config, wenn sie bitweise AND-verknüpft werden mit dem Hexadezimalwert 0x0F (binär 00001111), gleich 0x0A (binär 00001010) sein.Die reelle Zahl ratio muss positiv, aber kleiner als 5.0 sein. Außerdem muss das Quadrat von ratio (ratio * ratio) größer als 12.0 sein.Die Verbindung zwischen beiden ist: Der als vorzeichenlose Ganzzahl interpretierte Wert des gesamten 16-Bit-Bitvektors config (nennen wir ihn config_val) muss, wenn er zu einer reellen Zahl umgewandelt wird, gleich dem Produkt aus ratio und 1000.0 sein (also muss die Gleichung (to_real config_val) = ratio * 1000.0 gelten)."
    # await solve_problem(problem_question)

async def solve_problem(problem_question: str):
    modelSolver = llm.LLM(model_name="ollama/qwen3:4b")
    
    solver_result = await modelSolver.generate_response(
        prompt=problem_question,
        instruct=Z3Problem,)
    
    print(f"Problem vom LLM erhalten: {solver_result}")

    result = Z3Solver(solver_result).solve()
    print(f"Solver Ergebnis: {result}")


if __name__ == "__main__":
    asyncio.run(main())