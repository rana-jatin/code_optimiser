import os
from typing import Optional

try:
    import groq
except ImportError:  # pragma: no cover - library may not be installed
    groq = None

try:
    from pyflakes import api as pyflakes_api
    from pyflakes.reporter import Reporter
except Exception:  # pragma: no cover - optional dependency
    pyflakes_api = None


class Debugger:
    """Simple debugger to check Python code for errors.

    It performs a basic syntax check and, if a Groq API key is available,
    uses the Groq LLM to provide additional feedback.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "llama3-8b-8192") -> None:
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model
        self.client = None
        if self.api_key and groq is not None:
            self.client = groq.Groq(api_key=self.api_key)

    def _static_analysis(self, code: str) -> str:
        """Run pyflakes on the code if available and return the output."""
        if pyflakes_api is None:
            return "Pyflakes not installed; skipping static analysis."
        from io import StringIO

        out = StringIO()
        reporter = Reporter(out, out)
        warnings = pyflakes_api.check(code, filename="<string>", reporter=reporter)
        output = out.getvalue().strip()
        if warnings == 0 and not output:
            return "Pyflakes: no issues found."
        return f"Pyflakes issues:\n{output}"

    def check(self, code: str) -> str:
        """Check the given code for errors and return a report."""
        try:
            compile(code, "<string>", "exec")
            syntax_result = "No syntax errors detected."
        except SyntaxError as exc:
            syntax_result = f"Syntax error: {exc}"

        static_result = self._static_analysis(code)

        llm_result = ""
        if self.client is not None:
            prompt = (
                "You are a Python code debugger. Analyze the following code "
                "and describe any potential issues or improvements."
            )
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": f"{prompt}\n\n{code}"}],
                    temperature=0,
                )
                llm_result = response.choices[0].message.content.strip()
            except Exception as exc:  # pragma: no cover - network errors
                llm_result = f"Error contacting Groq: {exc}"
        return "\n".join(filter(None, [syntax_result, static_result, llm_result]))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Check Python code for errors.")
    parser.add_argument("file", help="Path to the Python file to check")
    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        source_code = f.read()

    debugger = Debugger()
    print(debugger.check(source_code))
