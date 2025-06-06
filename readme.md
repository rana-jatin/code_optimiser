## Debugger

This repository includes a simple `debugger.py` script that checks Python files for syntax errors, runs static analysis with Pyflakes, and can optionally query the Groq language model for additional feedback.

## Optimiser

`optimiser.py` now builds its optimisation pipeline using LangGraph. The graph
first sends code and the user query to a Groq LLM agent and then formats the
result with Black. If a `GROQ_API_KEY` is available, the Groq step rewrites the
code according to the request before formatting.

## JSON Optimiser

`json_optimiser.py` loads a JSON file that must contain `code` and `query` fields. It prints analysis from `debugger.py`, runs the optimiser pipeline from `optimiser.py`, then prints a second analysis of the optimised code and outputs the final result.
