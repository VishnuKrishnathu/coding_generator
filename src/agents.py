from textwrap import dedent
from crewai import Agent
from llms import coding_question
# from tools import ExaSearchToolSet


class CodingQuestionAgents():

    def coding_desciption_genrating_agent(self):
        return Agent(
            llm=coding_question,
            role="Data Structures and Algorithm Expert",
            goal="Generate a description for the given coding title",
            tools=[],
            backstory=dedent(f"""As a Data Structure and Algoritm Expert, your task is to generate a detailed description with examples
and constraintsfor the given coding title."""),
            verbose=True,
        )

    def coding_boilerplate_agent(self):
        return Agent(
            llm=coding_question,
            role="Data Structures and Algorithm Expert",
            goal="For the given coding description, function signature, sample input and sample output generate the boilerplate code",
            tools=[],
            backstory=dedent(f"""As a Data Structure and Algoritm Expert, your task is to generate a boiler plate code
for the given coding description and function signature. The code should be generated in 4 languages, which are Python3, Java, C++, and C."""),
            verbose=True,
        )

    def coding_testcases_agent(self):
        return Agent(
            llm=coding_question,
            role="Data Structures and Algorithm Expert",
            goal="For the given coding description, sample input and sample output generate 5 testcases",
            tools=[],
            backstory=dedent(f"""\
As a Data Structure and Algoritm Expert, your task is to generate 5 test cases
for the given coding description and function signature."""),
            verbose=True,
        )
