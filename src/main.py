# from textwrap import dedent
from agents import CodingQuestionAgents
from crewai import Crew
from langtrace_python_sdk import langtrace
from os import path, environ
from tasks import CodingQuestionTasks
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
import json

langtrace.init(api_key=environ.get("LANGTRACE"))

def coding_description(tasks, agents, coding_title_name):
    coding_desciption_genrating_agent = agents.coding_desciption_genrating_agent()

    # create tasks
    description_task = tasks.coding_description_generation_task(
        coding_desciption_genrating_agent,
        coding_title_name
    )

    crew = Crew(
        agents=[coding_desciption_genrating_agent],
        tasks=[description_task],
    )

    result = crew.kickoff()

    return result.json_dict


def coding_boilerplate(tasks, agents, coding_description, function_signature, sample_input, sample_output):
    coding_boilerplate_agent = agents.coding_boilerplate_agent()

    coding_boilerplate_task = tasks.coding_boilerplate_task(
        coding_boilerplate_agent,
        coding_description,
        function_signature,
        sample_input,
        sample_output
    )

    crew = Crew(
        agents=[coding_boilerplate_agent],
        tasks=[coding_boilerplate_task],
    )

    result = crew.kickoff()

    return result.json_dict


def coding_solution(tasks, agents, coding_description, function_signature, sample_input, sample_output):
    coding_boilerplate_agent = agents.coding_boilerplate_agent()

    coding_solution_task = tasks.coding_solution_task(
        coding_boilerplate_agent,
        coding_description,
        function_signature,
        sample_input,
        sample_output
    )

    crew = Crew(
        agents=[coding_boilerplate_agent],
        tasks=[coding_solution_task],
    )

    result = crew.kickoff()

    return result.json_dict


def coding_testcases(tasks, agents, coding_description, sample_input, sample_output):
    coding_testcases_agent = agents.coding_testcases_agent()

    coding_testcases_task = tasks.coding_testcases_task(
        coding_testcases_agent,
        coding_description,
        sample_input,
        sample_output
    )

    crew = Crew(
        agents=[coding_testcases_agent],
        tasks=[coding_testcases_task],
    )

    result = crew.kickoff()
    return result.json_dict


def main(coding_title_name):

    update_data = {}

    description_data = coding_description(tasks, agents, coding_title_name)
    boilerplate_data = coding_boilerplate(
        tasks, agents,
        description_data["description"],
        description_data["function_signature"],
        description_data["sample_input"],
        description_data["sample_output"],
    )

    solution_data = coding_solution(
        tasks, agents,
        description_data["description"],
        description_data["function_signature"],
        description_data["sample_input"],
        description_data["sample_output"],
    )

    testcases_data = coding_testcases(
        tasks, agents,
        description_data["description"],
        description_data["sample_input"],
        description_data["sample_output"],
    )

    question_code = []
    solutions = []

    for val in boilerplate_data.keys():
        question_code.append({
            "langauge": val,
            "code": boilerplate_data[val]
        })

    for val in solution_data.keys():
        solutions.append({
            "langauge": val,
            "code": solution_data[val]
        })

    update_data["description"] = description_data["description"]
    update_data["exlpanation"] = description_data["explanation"]
    update_data["constraints"] = description_data["constraints"]
    update_data["note"] = description_data["note"]
    update_data["function_signature"] = description_data["function_signature"]
    update_data["questionCode"] = question_code
    update_data["solutions"] = solutions
    update_data["test_cases"] = testcases_data["testcases"]
    update_data["private_test_cases"] = testcases_data["private_testcases"]
    update_data["sanitized"] = True

    return update_data


# create agents

if __name__ == "__main__":
    tasks = CodingQuestionTasks()
    agents = CodingQuestionAgents()
    MONGO_URI = environ.get("MONGO_URI")
    DATABASE_NAME = environ.get("DATABASE_NAME")
    COLLECTION_NAME = environ.get("COLLECTION_NAME")
    output = open("output.json", "w")

    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    try:
        updated_data = main("4 Sum")
        print(updated_data)
        json.dump(updated_data, output)

    finally:
        # Close the connection
        client.close()
