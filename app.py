"""Simple command-line chat assistant for Trexovia.

The assistant responds to a small set of fixed prompts, tracks the conversation
history, and persists that history to disk using the memory module. It is a
minimal rule-based bot intended for local experimentation rather than a
production chat system.
"""

from memory import add_message, load_history, save_history
from typing import List, Dict, Optional


RESPONSES = {
    "hello": "Hello, Obinna!",
    "hi": "Hi, Obinna!",
    "help": (
        "I understand hello, hi, help, history, and exit."
    ),
}


def find_last_user_message(
    history: List[Dict[str, str]],
) -> Optional[str]:
    """Return the most recent user message from the conversation history.

    The chat history is expected to contain dictionaries with at least two keys:
    "role" and "content". The function scans the history from newest to oldest,
    returning the first message whose role is "user".

    Args:
        history: Ordered list of chat messages previously loaded from storage.

    Returns:
        The content of the latest user message, or None when no user message is
        present in the history.
    """
    for message in reversed(history):
        if message["role"] == "user":
            return message["content"]

    return None


def generate_reply(
    message: str,
    history: Optional[List[Dict[str, str]]] = None,
) -> str:
    """Create a reply for the provided user input.

    The response logic is intentionally simple and deterministic. It handles
    blank input, known canned responses, a few "history" queries, and a default
    fallback message for everything else.

    Args:
        message: The raw text entered by the user.
        history: Optional conversation history used to answer history-related
            prompts. When omitted, an empty list is assumed.

    Returns:
        A string response that should be printed to the user.
    """
    if history is None:
        history = []

    cleaned_message = message.strip()
    normalized_message = cleaned_message.lower()

    if not cleaned_message:
        return "Please enter a message."

    if normalized_message in RESPONSES:
        return RESPONSES[normalized_message]

    history_commands = {
        "history",
        "what did i say",
        "what did i say?",
    }

    if normalized_message in history_commands:
        last_message = find_last_user_message(history)

        if last_message:
            return f'Your last message was: "{last_message}"'

        return "You have not sent any previous messages."

    return f"You said: {cleaned_message}"


def run() -> None:
    """Start the interactive chat loop in the terminal.

    This function loads prior conversation data, prints a startup banner, and then
    repeatedly accepts input until the user types "exit". Each turn stores both
    the user message and the assistant reply so the session can be reconstructed
    later from saved history.
    """
    history = load_history()

    print("Trexovia Assistant")
    print(f"Loaded {len(history)} previous messages.")
    print("Type 'help' for instructions or 'exit' to stop.\n")

    while True:
        user_message = input("You: ").strip()

        if user_message.lower() == "exit":
            print("Assistant: Goodbye!")
            break

        reply = generate_reply(user_message, history)
        print(f"Assistant: {reply}")

        add_message(history, "user", user_message)
        add_message(history, "assistant", reply)
        save_history(history)


if __name__ == "__main__":
    run()