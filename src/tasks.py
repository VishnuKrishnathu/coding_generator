from textwrap import dedent
from crewai import Task
from pydantic import BaseModel


class TestCase(BaseModel):
    input: str
    output: str


class CodingTestcases(BaseModel):
    total_testcases: str
    testcases: list[TestCase]


class CodingQuestion(BaseModel):
    description: str
    function_signature: str
    sample_input: str
    sample_output: str
    example: str
    explanation: str
    constraints: list[str]
    note: str
    difficulty_level: str


class CodingBoilerPlate(BaseModel):
    c: str
    cpp: str
    java: str
    python3: str


class CodingQuestionTasks():
    def coding_description_generation_task(self, agent, coding_title):
        return Task(
            description=dedent(f"""\
For the given coding title, generate a Coding Question description.
Following points should be noted before generatin the description.
1. The boiler plate code given to the user will read input from standard input and output will be displayed using standard output.
2. If the input is an array the first line will contain the array length and the second line will contain the array elements separated by spaces.
3. If the input is a string the first line will contain the string length and the second line will contain the string.
4. If the input is a 2 dimensional array the first line will contain the number of rows and the second line will contain the number of columns and the third line will contain the array elements separated by spaces.
5. Avoid printing unnecessary things in standard output (example: Enter the text)

Coding Question Title: {coding_title}
Give a json output with the following keys
1. description
2. function_signature
3. sample_input
4. sample_output
5. example
6. explanation
7. constraints
8. note
9. difficulty_level
            """),
            expected_output="A description which will help user to understand the coding question in a clear way and also the function signature, sample input, sample output, example, explanation, constraints, note, difficulty level",
            agent=agent,
            async_execution=True,
            output_json=CodingQuestion
        )

    def coding_boilerplate_task(self, agent, coding_description, function_signature, sample_input, sample_output):
        return Task(
            description=dedent(f"""\
For the given coding description, function signature, sample input and sample output generate a boilerplate code.
The code should be generated in 4 languages, which are Python3, Java, C++, and C.
The code should have proper indentations. Spaces should be used for indentations.
Following points should be noted before generating the boiler plate code
1. The boiler plate code given to the user will read input from standard input and output will be displayed using standard output.
2. If the input is an array the first line will contain the array length and the second line will contain the array elements separated by spaces.
3. If the input is a string the first line will contain the string length and the second line will contain the string.
4. If the input is a 2 dimensional array the first line will contain the number of rows and the second line will contain the number of columns and the third line will contain the array elements separated by spaces.
5. Avoid printing unnecessary things in standard output (example: Enter the text)
6. For language C and C++ main function should read from standard input and write to standard output, also it should call the function mentioned in the function signature
7. For language Java class Main should be declared and it should have a main method which should read from standard input and write to standard output, also it should call the function mentioned in the function signature
8. For language Python3 __name__ == "__main__" should be declared and it should read from standard input and write to standard output, also it should call the function mentioned in the function signature
9. The boilerplate code should also read the input and print the output according to the given sample input and sample output
10. The function signature should be empty and shouldn't have any logic.
Coding Description: {coding_description}
Function Signature: {function_signature}
Sample Input: {sample_input}
Sample Output: {sample_output}
Give a json output with the following keys
1. c
2. cpp
3. java
4. python3
"""),
            expected_output="A boilerplate code for the given coding description and function signature",
            agent=agent,
            async_execution=True,
            output_json=CodingBoilerPlate
        )

    def coding_solution_task(self, agent, coding_description, function_signature, sample_input, sample_output):
        return Task(
            description=dedent(f"""\
For the given coding description, function signature, sample input and sample output generate a boilerplate code.
The code should be generated in 4 languages, which are Python3, Java, C++, and C.
The code should have proper indentations. Spaces should be used for indentations.
Following points should be noted before generating the boiler plate code
1. The boiler plate code given to the user will read input from standard input and output will be displayed using standard output.
2. If the input is an array the first line will contain the array length and the second line will contain the array elements separated by spaces.
3. If the input is a string the first line will contain the string length and the second line will contain the string.
4. If the input is a 2 dimensional array the first line will contain the number of rows and the second line will contain the number of columns and the third line will contain the array elements separated by spaces.
5. Avoid printing unnecessary things in standard output (example: Enter the text)
6. For language C and C++ main function should read from standard input and write to standard output, also it should call the function mentioned in the function signature
7. For language Java class Main should be declared and it should have a main method which should read from standard input and write to standard output, also it should call the function mentioned in the function signature
8. For language Python3 __name__ == "__main__" should be declared and it should read from standard input and write to standard output, also it should call the function mentioned in the function signature
9. The boilerplate code should also read the input and print the output according to the given sample input and sample output
Coding Description: {coding_description}
Function Signature: {function_signature}
Sample Input: {sample_input}
Sample Output: {sample_output}
Give a json output with the following keys
1. c
2. cpp
3. java
4. python3
"""),
            expected_output="A boilerplate code for the given coding description and function signature",
            agent=agent,
            async_execution=True,
            output_json=CodingBoilerPlate
        )

    def coding_testcases_task(self, agent, coding_description, sample_input, sample_output):
        return Task(
            description=dedent(f"""\
For the given coding description, sample input and sample output generate 5 testcases.
Following points should be noted before generating the testcases
1. If the input is an array the first line will contain the array length and the second line will contain the array elements separated by spaces.
2. If the input is a string the first line will contain the string length and the second line will contain the string.
3. If the input is a 2 dimensional array the first line will contain the number of rows and the second line will contain the number of columns and the third line will contain the array elements separated by spaces.
Coding Description: {coding_description}
Sample Input: {sample_input}
Sample Output: {sample_output}
Give a json output with the following keys
1. testcases
2. total_testcases
"""),
            expected_output="A list of 5 testcases for the given coding description and sample input and sample output",
            agent=agent,
            async_execution=True,
            output_json=CodingTestcases
        )
