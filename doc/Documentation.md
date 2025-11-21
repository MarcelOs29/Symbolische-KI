# Symbolische KI - Verknüpfung von LLMs (Subsymbolischer KI) mit symbolischer KI

## Aufgabestellung
Verknüpfung eines logischen Schlussfolgerungssystems (symbolische KI) mit einem großen Sprachmodell (LLM, subsymbolische KI). Ziel ist es, natürliche Sprachprobleme in eine formale Repräsentation zu überführen, diese mit einem logischen Solver zu lösen und die Lösung wieder in natürlicher Sprache auszugeben. Die LLMs sollen dabei lokal ausgeführt werden.

## Lösungsidee
1. **Natürliche Sprache zu formaler Repräsentation**: Ein LLM wird verwendet, um ein natürlichsprachliches Problem in eine formale Repräsentation zu übersetzen, die von einem logischen Solver verstanden wird.
2. **Lösen des Problems**: Ein logischer Solver wird verwendet, um die formale Repräsentation zu verarbeiten und eine Lösung zu finden.
3. **Formulierung der Lösung in natürlicher Sprache**: Ein weiteres LLM wird verwendet, um die Lösung des logischen Solvers in eine verständliche natürliche Sprachantwort zu übersetzen.

## Lösungsarchitektur
### Software und Frameworks
- **Programmierumgebung**: Python 3.12
- **LLM-Integration**: Ollama (https://ollama.com/) für die Nutzung lokaler LLM-Modelle
    - **LLM-Modelle**: Qwen-1.7B und Qwen-0.6B (während der Entwicklung diverse Modelle getestet)
- **Logischer Solver**: Z3 Theorem Prover als Python-Bibliothek (https://github.com/Z3Prover/z3)
- **Z3 Modellierung**: Pydantic (https://docs.pydantic.dev/latest/) zur Definition der Repräsentation von Z3-Problemen
- **LLM Interaktion/Framework**: Instruct (https://python.useinstructor.com/), wobei es die Antworten der LLMs in vordefinierte Pydantic-Modelle parst.

### Module und Komponenten
- **llm.py**: Enthält die `LLM`-Klasse zur Interaktion mit den LLMs, Generierung von Z3-Problemen Pydantic Darstellungen aus den Problemen in natürlicher Sprache. Zudem werden die Antworten aus den Ergebnissen von Z3 formuliert.
- **Z3Problem.py**: Definiert die Pydantic-Modelle zur Repräsentation von Z3-Problemen, einschließlich Variablen, Typen und Constraints.
- **Z3Solver.py**: Enthält die `Z3Solver`-Klasse, welche die Z3-Probleme Pydantic Darstellungen entgegennimmt und die Z3-Variablen und -Constraints erstellt. Anschließend wird das Problem mit Z3 gelöst und die Lösung zurückgegeben.
- **main.py**: Hauptskript, das die Interaktion zwischen den LLMs und dem Z3-Solver koordiniert. Es nimmt eine Frage in natürlicher Sprache entgegen, generiert das Z3-Problem Pydantic-Modell, löst es und formuliert die Antwort.

## Architekturdiagramm
Das Architektur/Komponentendiagramm zeigt die Interaktion zwischen den Modulen und Komponenten des Systems sind in der Datei [`doc/Process-Flow.drawid.pdf`](doc/Process-Flow.drawid.pdf) dokumentiert.


## Beispielablauf
1. **Eingabe**: "Finde zwei Zahlen x und y, so dass x + y = 10 und x - y = 4."
2. **LLM Generierung**: Das LLM generiert die folgende Pydantic-Darstellung des Z3-Problems:
    ```python
    class Z3Problem(BaseModel):
        variables: List[str] = ["x", "y"]
        types: Optional[Dict[str, str]] = {"x": "Int", "y": "Int"}
        constraints: List[str] = [
            "x + y == 10",
            "x - y == 4"
        ]
    ```
3. **Z3 Lösung**: Der Z3-Solver evaluiert die Eingabe und bildet eine Z3 Repräsentation:
    ```python
    x = Int('x')
    y = Int('y')
    s = Solver()
    s.add(x + y == 10)
    s.add(x - y == 4)
    ```
   Nach dem Lösen erhält Z3 die Lösung: `x = 7`, `y = 3`.
4. **LLM Antwortformulierung**: Das zweite LLM formuliert die Antwort basierend auf der Lösung:
   "Die zwei Zahlen sind x = 7 und y = 3."


## Anweisungen zur Ausführung
1. **Voraussetzungen**:
   - Installiere Python 3.12.
   - Installiere die erforderlichen Python-Pakete:
     ```bash
     pip install z3-solver pydantic instructor
     ```
   - Stelle sicher, dass Ollama installiert und konfiguriert ist, um lokale LLM-Modelle zu verwenden.
   - Stelle sicher, dass die gewünschten LLM-Modelle (z.B. Qwen-1.7B) in Ollama verfügbar sind.
2. **Ausführung**:
   - Führe das Hauptskript aus:
     ```bash
     python src/main.py
     ```
3. Optional: Passe die Eingabeprobleme im `main.py`-Skript an, um verschiedene natürliche Sprachprobleme zu testen.

## Anmerkungen
- Aufgrund der nicht deterministischen Natur von LLMs können die generierten Z3-Probleme und die formulierten Antworten variieren. Dadurch kann es passieren, dass einige Probleme nicht korrekt gelöst werden oder das übersetzen der natürlichen Sprache in die Z3 Repräsentation fehlschlägt.
- Insbesondere bei komplexeren Problemen kann es notwendig sein, die Prompts für die LLMs anzupassen, um konsistentere und genauere Ergebnisse zu erzielen.
- Probleme, die BitVectoren Datentypen und die damit verbundenen Operationen erfordern, werden von dem LLM sehr häufig nicht korrekt in die Z3 Repräsentation übersetzt. Daher wurden dieses Feature in der finalen Lösung nicht berücksichtigt.
- Die Erstellung der menschenlesbaren Antworten könnte durch die Verwendung von LLms auch wieder zu Problemen führen. Zum Teil lieferte das Modell andere antworten, wie das Z3 Modell bereitgestellt hatte, insbesondere dann, wenn die Lösung von Z3 ein Fehler ausgab. Hier könnte in zukünftigen Versionen eine Validierung der Antwort erfolgen, um sicherzustellen, dass die Antwort mit der Z3 Lösung übereinstimmt. Ich habe vorerst entschieden, in den Prompt der Antwortformulierung, das Originalproblem nicht mit aufzunehmen, um die Komplexität zu reduzieren und die Konsistenz der Antworten zu erhöhen.
### LLM Größen
- Bei der Erstellung der Menschenlesbaren Antworten aus den Z3 Lösungen konnte festgestellt werden, dass kleinere Modelle (z.B. Qwen-0.6B) oft bessere und konsistentere Antworten lieferten als größere Modelle (z.B. Qwen-1.7B). Möglicherweise liegt dies daran, dass kleinere Modelle weniger "kreativ" sind und sich stärker an die vorgegebenen Strukturen halten.
- Bei der Generierung der Z3-Probleme aus den natürlichen Sprachproblemen lieferten größere Modelle tendenziell bessere Ergebnisse, da sie komplexere Zusammenhänge besser erfassen können. Daher wurde für diesen Schritt das größere Modell (Qwen-1.7B) verwendet.
    - Das kleinere Modell (Qwen-0.6B) wurde jedoch auch hier getestet und lieferte in einigen Fällen ebenfalls zufriedenstellende Ergebnisse.
    - Das größere Modell (Qwen-4B) benötigt deutlich mehr Ressourcen und Zeit, lieferte jedoch keine signifikant besseren Ergebnisse im Vergleich zum 1.7B Modell.


## Ausblick
- Während des testen und der Entwicklung ist aufgefallen, dass spezielle Coder-Modelle (z.B. qwen2.5-coder:3b) bessere Ergebnisse bei der Generierung der Z3-Probleme liefern könnten, da diese Modelle besser im Umgang mit formalen Sprachen und Strukturen sind und die Z3 Syntax eher einer Programmiersprache ähnelt. Daher könnten zukünftige Versionen dieses Projekts die Verwendung solcher Modelle in Betracht ziehen.
Die aktuelle implementation ist jedoch auf die allgemeinen Modelle fokussiert, um eine breitere Anwendbarkeit zu gewährleisten. Coder-Modelle antworten in der Regel in einer anderen Repräsentation wie JSON, wodurch die Ergebnisse mit Coder-Modellen aktuell eher schlechter ausfallen.
- Die Nutzung von Pydantic zur Definition der Z3-Probleme hat sich als vorteilhaft erwiesen, da es eine klare Struktur und Validierung der Probleme ermöglicht. In zukünftigen Versionen sollten weitere Features von Pydantic erkundet werden, um die Robustheit und Flexibilität der Problemdefinitionen zu erhöhen. Bereits in der Problemdefinition könnten Validierungen eingebaut werden, um sicherzustellen, dass die generierten Probleme den Anforderungen von Z3 entsprechen. (Sofern dies von Pydantic unterstützt wird.)
- BitVectoren und deren Operationen könnten in zukünftigen Versionen besser unterstützt werden, indem die Prompts weiter verfeinert oder spezialisierte Modelle verwendet werden. Zum Beispiel könnten Coder-Modelle eingesetzt werden, die besser mit solchen Datentypen umgehen können.
- Falls die LLM generierte Z3-Repräsentation des Problems nicht gelöst werden kann, könnte eine Rückmeldungsschleife implementiert werden, bei der das LLM gebeten wird, die Repräsentation zu überarbeiten oder zu korrigieren. Dies könnte die Erfolgsrate bei der Problemlösung erhöhen.

## Fazit
Die Verknüpfung von LLMs mit einem logischen Solver wie Z3 ermöglicht es, natürliche Sprachprobleme in formale Repräsentationen zu überführen und diese zu lösen. Trotz einiger Herausforderungen bei der Genauigkeit der LLM-Ausgaben zeigt dieses Projekt das Potenzial solcher hybriden Ansätze in der KI. Mit weiteren Verbesserungen in den Prompts und der Modellauswahl können die Ergebnisse weiter optimiert werden.
Es wird jedoch auch deutlich, dass die nicht-deterministische Natur von LLMs und deren Verständnis für formale Sprachen noch Herausforderungen mit sich bringt, die es zu adressieren gilt. Der Determinismus von logischen Solvern bieten hingegen eine Sicherheit, der vertraut werden kann, sobald die formale Repräsentation korrekt erstellt wurde.
Insbesondere bei Problemen, die nicht lösbar sind, sind die Stärken von logischen Solvern wie Z3 deutlich erkennbar, da diese zuverlässig angeben können, wenn ein Problem unlösbar ist, während LLMs in solchen Fällen oft ungenaue oder irreführende Antworten liefern können.
