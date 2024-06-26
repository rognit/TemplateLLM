from llm.refining.classic_agents import referee_agent, enhancer_agent, reviewer_agent
from llm.refining.clarifier_agents import number_clarifier_agent, referee_clarifier_agent
from llm.tools import *


def refine(question, answer, refinements_number=1, clarifier_struggle_limit=3):
    for i in range(refinements_number):

        defaults = reviewer_agent(question, answer)
        new_answer = enhancer_agent(question, answer, defaults)
        best_answer = referee_agent(question, answer, new_answer)
        best_answer_number = referee_clarifier_agent(best_answer, answer, new_answer)

        for j in range(clarifier_struggle_limit):
            match best_answer_number:
                case '0' | '1':
                    if VERBOSE:
                        yellowlog("Useless refining")
                    break
                case '2':
                    if VERBOSE:
                        greenlog("Usefull refining")
                    best_answer = new_answer
                    break
                case _:
                    redlog("Wrong output format")
                    best_answer_number = number_clarifier_agent(best_answer)
            if j == clarifier_struggle_limit - 1:
                redlog("CLARIFIER FAILLURE")

        answer = best_answer

    return answer
