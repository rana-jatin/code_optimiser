import os
from typing import Optional, TypedDict

try:
    import groq
except ImportError:  # pragma: no cover - library may not be installed
    groq = None

try:
    from black import format_str, FileMode
except Exception:  # pragma: no cover - optional dependency
    format_str = None


class Agent:
    """Base class for optimisation agents."""

    def run(self, code: str, query: str) -> str:  # pragma: no cover - interface
        return code


class GroqOptimiserAgent(Agent):
    """Use the Groq LLM to rewrite code according to a query."""

    def __init__(self, api_key: Optional[str], model: str) -> None:
        self.client = None
        if api_key and groq is not None:
            self.client = groq.Groq(api_key=api_key)
        self.model = model

    def run(self, code: str, query: str) -> str:
        if self.client is None:
            return code
        prompt = (
            "You are a helpful Python code optimiser. Modify the following code "
            f"according to this user request: {query!r}. "
            "Return only the modified code."
        )
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": f"{prompt}\n\n{code}"}],
                temperature=0,
            )
            return response.choices[0].message.content.strip()
        except Exception as exc:  # pragma: no cover - network errors
            return code + f"\n# Error contacting Groq: {exc}"


class BlackFormatterAgent(Agent):
    """Format code using the Black formatter."""

    def run(self, code: str, query: str) -> str:  # pragma: no cover - formatting
        if format_str is None:
            return code
        try:
            return format_str(code, mode=FileMode())
        except Exception:
            return code


class CodeOptimiser:
    """Optimise Python code according to a user query using LangGraph."""

    class _State(TypedDict):
        code: str
        query: str

    def __init__(self, api_key: Optional[str] = None, model: str = "llama3-8b-8192") -> None:
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model

        self._groq_agent = GroqOptimiserAgent(self.api_key, self.model)
        self._formatter_agent = BlackFormatterAgent()

        self.graph = self._build_graph()

    def _build_graph(self):
        from langgraph.graph import StateGraph, START, END

        graph = StateGraph(self._State)

        def groq_node(state: self._State) -> dict[str, str]:
            return {"code": self._groq_agent.run(state["code"], state["query"])}

        def format_node(state: self._State) -> dict[str, str]:
            return {"code": self._formatter_agent.run(state["code"], state["query"])}

        graph.add_node("groq", groq_node)
        graph.add_node("format", format_node)
        graph.add_edge(START, "groq")
        graph.add_edge("groq", "format")
        graph.add_edge("format", END)

        return graph.compile()

    def optimise(self, code: str, query: str) -> str:
        """Run the optimisation graph on the code."""
        result = self.graph.invoke({"code": code, "query": query})
        return result["code"]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Optimise Python code with a user-supplied query"
    )
    parser.add_argument("file", help="Path to the Python file to optimise")
    parser.add_argument("query", help="Optimisation request")
    parser.add_argument(
        "-o",
        "--output",
        help="File to write optimised code to (defaults to stdout)",
    )
    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        source_code = f.read()

    optimiser = CodeOptimiser()
    result = optimiser.optimise(source_code, args.query)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
    else:
        print(result)
