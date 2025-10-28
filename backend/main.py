def think(message, memory):
    msg = message.lower().strip()

    # Simple intent-based responses
    if "hello" in msg or "hi" in msg:
        return "Hey there! I'm Dexa, your coding assistant."
    elif "python" in msg:
        return "Python is great for beginners. Want an example of loops or functions?"
    elif "javascript" in msg:
        return "JavaScript runs in browsers and servers. I can show you a simple DOM example."
    elif "loop" in msg:
        return "In Python, a for loop looks like:\nfor i in range(5):\n    print(i)"
    elif "function" in msg:
        return "In Python:\ndef greet(name):\n    return f'Hello {name}'"
    elif "help" in msg:
        return "Sure. Ask me any coding question — I can explain syntax, examples, or logic."
    else:
        return "Hmm... I don't know that yet, but I’ll learn soon."

