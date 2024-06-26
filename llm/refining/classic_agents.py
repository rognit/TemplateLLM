from llm.engine import chat
from llm.config import *


def reviewer_agent(question, answer):
    prompt = [
        {'role': 'system', 'content': LLAMA3_SYS_PROMPT},
        {'role': 'user',
         'content': f"You're there to make sure that answers to questions are correct and concise, and both aspects"
                    f" are equally important. As far as conciseness is concerned, the answer should never be a "
                    f"sentence, but rather the pure answer to the question.\n\nInitial question is below.\n"
                    f"---------------------\n"
                    f"How many people does Apple employ?\n"
                    f"---------------------\n\n"
                    f"Candidate answer is below.\n"
                    f"---------------------\n"
                    f"Apple employs 161,000 people around the world\n"
                    f"---------------------\n\n"
                    f"Please list the default of the candidate answer to the initial question. If correctness and "
                    f"conciseness are good, just answer “The answer is sufficiently correct and concise”."},
        {'role': 'assistant', 'content': "The answer is not sufficiently concise"},
        {'role': 'user',
         'content': f"Great, thanks for your feedback!\nDo exactly the same thing again on the following question & "
                    f"answer pair:\n\nInitial question is below.\n"
                    f"---------------------\n"
                    f"For which product is Meta most well-known?\n"
                    f"---------------------\n\n"
                    f"Candidate answer is below.\n"
                    f"---------------------\n"
                    f"Facebook\n"
                    f"---------------------\n\n"
                    f"Please list the default of the candidate answer to the initial question. If correctness and "
                    f"conciseness are good, just answer “The answer is sufficiently correct and concise”."},
        {'role': 'assistant', 'content': "The answer is sufficiently correct and concise"},
        {'role': 'user',
         'content': f"Wonderful, thanks again for your feedback!\nDo exactly the same thing again on the following "
                    f"question & answer pair:\n\nInitial question is below.\n"
                    f"---------------------\n"
                    f"{question}\n"
                    f"---------------------\n\n"
                    f"Candidate answer is below.\n"
                    f"---------------------\n"
                    f"{answer}\n"
                    f"---------------------\n\n"
                    f"Please list the default of the candidate answer to the initial question. If correctness and "
                    f"conciseness are good, just answer “The answer is sufficiently correct and concise”."}



    ]

    if VERBOSE:
        print("Reviewer agent answer: ", end="")
    output = chat(prompt)

    return output


def enhancer_agent(question, answer, defaults):
    system_prompt = (f"{LLAMA3_SYS_PROMPT} You're there to get feedback from a reviewer to improve the answer to a "
                     f"question. If no flaws are present, you will repeat the given answer back to the user exactly as "
                     f"it is.")


    prompt = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user',
         'content': f"Initial question is below.\n"
                    f"---------------------\n"
                    f"{question}\n"
                    f"---------------------\n\n"
                    f"Candidate answer is below.\n"
                    f"---------------------\n"
                    f"{answer}\n"
                    f"---------------------\n\n"
                    f"Answer defaults are below.\n"
                    f"---------------------\n"
                    f"{defaults}\n"
                    f"---------------------\n\n"
                    f"The candidate answer to the initial question is not optimal because of the provided defaults."
                    f" Please refine the answer regarding the aforementioned flaw. You should provide nothing but "
                    f"the answer"}
    ]

    if VERBOSE:
        print("Enhancer agent answer: ", end="")
    output = chat(prompt)
    return output


def referee_agent(question, answer1, answer2):
    prompt = [
        {'role': 'system', 'content': LLAMA3_SYS_PROMPT},
        {'role': 'user',
         'content': f"You are there to determine the best answer to a question.\n\n"
                    f"Initial query is below.\n"
                    f"---------------------\n"
                    f"{question}\n"
                    f"---------------------\n\n"
                    f"Answer n°1: “{answer1}”\n\n"
                    f"Answer n°2: “{answer2}”\n\n"
                    f"The expected conciseness of the answer is that of a single answer, without sentence or "
                    f"additional details. Which answer is the best in terms of accuracy and conciseness?"}
    ]

    if VERBOSE:
        print("Referee agent answer: ", end="")
    output = chat(prompt)
    return output






# price_clarifier_agent("3 millions of yens")
# price_clarifier_agent("12 milliers d'euros")
# price_clarifier_agent("23k dollars")
# price_clarifier_agent("195 thousand £")
