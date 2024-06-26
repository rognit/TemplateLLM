from llm.config import *


def basic_prompt(question):
    return [
        {'role': 'system', 'content': LLAMA3_SYS_PROMPT},
        {'role': 'user', 'content': question},
    ]


def extractor_question(context, question):
    return f"“{context}”\n\nAgainst this backdrop, {question} You should provide nothing but the answer."


def json_extractor_question(context, question):
    return f"“{context}”\n\nAgainst this backdrop, {question} You should provide nothing but the answer in JSON format."


def redlog(string, end='\n'):
    print(f"\033[91m{string}\033[0m", end=end, flush=True)


def greenlog(string):
    print(f"\033[92m{string}\033[0m")


def bluelog(string, end='\n'):
    print(f"\033[94m{string}\033[0m", end=end)


def yellowlog(string):
    print(f"\033[93m{string}\033[0m")


def light_grey(string):
    return f"\033[37m{string}\033[0m"


def dark_grey(string):
    return f"\033[90m{string}\033[0m"


def bold(string):
    return f"\033[1m{string}\033[0m"
