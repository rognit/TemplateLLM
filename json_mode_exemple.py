from llm.tools import *
from llm.engine import *

with open("questions_test.json", "r", encoding="utf-8") as file:
    data = json.load(file)


def main():
    for row in data:
        paragraph, question, exp_answer = row["paragraph"], row["question"], row["response"]
        question_with_context = json_extractor_question(paragraph, question[:1].lower() + question[1:])
        prompt = basic_prompt(question_with_context)
        if VERBOSE:
            print(f"\n\nParagraph: {paragraph}")
            print(f"Question: {question}\nExpected answer: {exp_answer}\nAnswer:", end="")
        answer = chat(prompt, json_format=True)
        bluelog(f"{question}\n{answer}\n\n")


if __name__ == '__main__':
    main()
