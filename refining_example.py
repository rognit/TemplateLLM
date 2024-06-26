from llm.refining.refiner import refine
from llm.engine import chat
from llm.tools import *

paragraph_test = ("TechNova, founded in 2012, has quickly become a leader in the field of artificial intelligence "
                  "applied to renewable energy. In 2023, it recorded a revenue of 500 million euros, with an annual "
                  "growth rate of 15%. Its headquarters are located in Lyon, France, and it currently employs 2,"
                  "500 people across its 10 international offices. TechNova recently launched a revolutionary "
                  "product, the SolarOptimizer 3.0, which has increased the efficiency of solar panels by 20%. The "
                  "company also invested 50 million euros in research and development last year, representing 10% of "
                  "its total revenue. Additionally, it collaborates with several prestigious universities to support "
                  "innovation in the energy sector.")

question_test = ["when was TechNova founded?",
                 "in what field is TechNova a leader?",
                 "what was TechNova's revenue in 2023?",
                 "what was TechNova's annual growth rate in 2023?",
                 "where are TechNova's headquarters located?",
                 "how many people does TechNova currently employ?",
                 "what is the name of the recently launched product by TechNova?",
                 "by how much has the SolarOptimizer 3.0 increased the efficiency of solar panels?",
                 "how much did TechNova invest in research and development last year?",
                 "what percentage of total revenue does this investment represent?",
                 "with whom does TechNova collaborate to support innovation in the energy sector?"]


def main():
    for question in question_test:
        question_with_context = extractor_question(paragraph_test, question)
        prompt = basic_prompt(question_with_context)
        if VERBOSE:
            print("Initial answer: ", end="")
        init_answer = chat(prompt)
        refined_answer = refine(question_with_context, init_answer, refinements_number=1)
        bluelog(f"{question}\n{refined_answer}\n\n")


if __name__ == '__main__':
    main()
