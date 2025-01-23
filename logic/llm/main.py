import json
import sys
import time
import random
from rag import load_chunks, retrieve
from conversational_llm import prompt_llm
from rich.console import Console

console = Console()


def simulate_typing(text, min_delay=0.02, max_delay=0.1):
    """Simulates typing text with random delays.
    :param text: The text to be typed.
    :param min_delay: The minimum delay between characters.
    :param max_delay: The maximum delay between characters.
    """

    for char in text:
        print(char, end='', flush=True)
        time.sleep(random.uniform(min_delay, max_delay))
    print()  # For final newline


def boldify(text):
    """Formats text enclosed in ** ** as bold.
    :param text: The text to be formatted.
    :return: The formatted text."""
    parts = text.split("**")
    formatted = ""
    for i, part in enumerate(parts):
        if i % 2 == 1:
            formatted += f"\033[1m{part}\033[0m"  # ANSI escape for bold
        else:
            formatted += part
    return formatted


def main():
    while True:
        try:
            console.print("[bold green]Prompt AI Assistant:[/bold green] ", end="")
            input_query = input()
            if input_query.lower() in {"exit", "quit"}:
                console.print("[bold red]Exiting... Goodbye![/bold red]")
                break

            r = prompt_llm(
                user_prompt=input_query,
            )

            lines = r.split("\n")
            for line in lines:
                formatted_line = boldify(line)
                simulate_typing(formatted_line, min_delay=0.001, max_delay=0.01)
        except Exception as e:
            console.print(f"[bold red]An error occurred: {e}[/bold red]")


if __name__ == "__main__":
    main()
