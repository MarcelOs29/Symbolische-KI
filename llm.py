import instructor
import inspect

class LLM:
    client: instructor.AsyncInstructor

    def __init__(self, model_name: str):
        self.model_name = model_name

        self.client = instructor.from_provider(
            model_name,
            mode=instructor.Mode.TOOLS,
        )

    async def generate_response(self, prompt: str, instruct, max_retries: int = 3):
        print(f"Starte LLM-Anfrage mit Prompt: {prompt}")
        result = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Du bist ein Experte darin, Benutzeranfragen in formale Z3-Constraint-Probleme zu übersetzen. "
                        "Extrahiere NUR die Variablen, Constraints und optional das Feld `types` (z.B. {'x': 'BitVec32'}), wenn spezielle Z3-Typen benötigt werden. "
                        "Die Constraints dürfen keine Verkettung von `<` oder `>` Operatoren enthalten. Wenn nötig, führe Zwischenschritte ein."
                        ##"Die Constraints dürfen nur Z3-kompatible Operatoren und Funktionen verwenden."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            response_model=instruct,
            max_retries=max_retries,
        )
        if inspect.isawaitable(result):
            result = await result
        return result