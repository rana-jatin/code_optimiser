import argparse
import json

from debugger import Debugger
from optimiser import CodeOptimiser


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Optimise Python code from a JSON file containing 'code' and 'query' fields"
    )
    parser.add_argument("json_file", help="Path to the JSON input file")
    parser.add_argument(
        "-o", "--output", help="File to write optimised code to (defaults to stdout)"
    )
    args = parser.parse_args()

    with open(args.json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    code = data.get("code")
    query = data.get("query")
    if code is None or query is None:
        raise ValueError("JSON must contain 'code' and 'query' fields")

    debugger = Debugger()
    print("Initial code analysis:\n" + debugger.check(code))

    optimiser = CodeOptimiser()
    optimised = optimiser.optimise(code, query)

    print("\nOptimised code analysis:\n" + debugger.check(optimised))

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(optimised)
    else:
        print("\nOptimised code:\n" + optimised)


if __name__ == "__main__":
    main()
