import re

def _format_code(code):
    return f"\n\n```python\n{code}\n```"

def _detect_language(text):
    if "javascript" in text or "js" in text:
        return "javascript"
    if "java" in text:
        return "java"
    return "python"

def think(message, memory):
    message = (message or "").strip()
    low = message.lower()

    if not low:
        return "You sent an empty message."

    if "hello" in low or "hi" in low:
        return "Hey there! I'm Dexa — your coding assistant."

    if "loop" in low or "for loop" in low:
        return ("Example — Python for loop:" +
                _format_code("for i in range(5):\n    print(i)"))

    if "function" in low:
        return ("Python function example:" +
                _format_code("def greet(name):\n    return f'Hello {name}'"))

    if "read file" in low:
        return ("Read a file in Python:" +
                _format_code("with open('file.txt','r') as f:\n    print(f.read())"))

    if any(token in low for token in ("error", "exception", "traceback")):
        return "Please share the full error message wrapped in triple backticks."

    if low in ("show memory", "memory", "history"):
        if not memory:
            return "Memory is empty."
        lines = []
        for e in memory[-6:]:
            lines.append(f"U: {e.get('user')}\nB: {e.get('bot')}")
        return "Recent memory:\n\n" + "\n\n".join(lines)

    if low in ("clear memory", "forget", "reset memory"):
        return "Use the /clear endpoint to clear memory."

    return ("I didn't fully understand. Try asking for an example, debugging help, "
            "or explanation. For example: 'python: example read file'.")
