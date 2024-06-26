from llm.config import *
from llm.engine import chat
from llm.tools import *


def referee_clarifier_agent(a1, a2, choice):
    prompt = [
        {'role': 'system', 'content': LLAMA3_SYS_PROMPT},
        {'role': 'user',
         'content': "My assistant made a choice between 2 answers, but he didn't enter his choice in the right format."
                    f"\nHere is answer n°1: {a1}"
                    f"\nHere is answer n°2: {a2}"
                    f"\nHere's his choice: {choice}"
                    f"\nWhich answer did he choose? Please answer with the answer number."}
    ]
    assistant_prefix = (f"No problem, I'll clear it up.\n\n"
                        f"Your assistant replied \"{choice}\"\n"
                        f"Given that \"{a1}\" is the first answer and \"{a2}\" is the second answer, your assistant "
                        f"chose answer number ...")

    if VERBOSE:
        print("Clarifier agent answer: ", end="")
    output = chat(prompt, assistant_prefix=assistant_prefix)
    for c in output:
        if c.isdigit():
            return c

    redlog("Clarifier agent did not answer correctly")



def number_clarifier_agent(number):

    prompt = [
        {'role': 'system', 'content': LLAMA3_SYS_PROMPT},
        {'role': 'user',
         'content': "My assistant has entered data in the wrong format. I just want a numbers and here's his answer:"
                    "\n“““Response n°0”””\nWhat's the number?"},
        {'role': 'assistant', 'content': "0"},
        {'role': 'user', 'content': "Awesome! And what's the number here:\n“““The second response is better.”””"},
        {'role': 'assistant', 'content': "2"},
        {'role': 'user', 'content': f"Amazing! And what's the number here:\n“““{number}”””"},
    ]

    if VERBOSE:
        print("Clarifier agent answer: ", end="")
    output = chat(prompt)
    return output


def price_clarifier_agent(price):

    prompt = [
        {'role': 'system', 'content': LLAMA3_SYS_PROMPT},
        {'role': 'user',
         'content': "My assistant has entered data in the wrong format. I just want a tuple with "
                    "the number and the currency. Here's his answer:\n“““500 millions d'euros”””\nWhat's the price in "
                    "the tuple format? (answer only with a tuple)"},
        {'role': 'assistant', 'content': "('500000000', 'euro')"},
        {'role': 'user', 'content': "Great! And what's the price here:\n“““2.5k $”””"},
        {'role': 'assistant', 'content': "('2500', 'dollar')"},
        {'role': 'user', 'content': f"Fantastic! And what's the price here:\n“““{price}”””"},
    ]

    if VERBOSE:
        print(f"""Price clarifier agent answer of "{price}": """, end="")
    output = chat(prompt)
    return output
