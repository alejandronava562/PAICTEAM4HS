from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
import json
import os
from prompts import USER_TEMPLATE, SYSTEM_PROMPT, IDEA_SCHEMA, USER_PLAN, CHOSEN_PLAN_SCEMA

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# Alejandro


def call_api(system_prompt, user_prompt, schema):
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "user", "content": user_prompt},
            {"role": "system", "content": system_prompt},
        ],
        response_format={"type": "json_schema", "json_schema": schema},
    )
    text = response.choices[0].message.content
    return json.loads(text)  # type: ignore


def main():
    print("app")

    user_project = input("Describe the project.").strip()
    user_context = input(
        "Describe the context of the project that you will be working on."
    ).strip()

    # Stage 1: Generate Ideas
    print("Generating possible ideas...\n")
    ideas = call_api(
        SYSTEM_PROMPT,
        USER_TEMPLATE.format(project=user_project, context=user_context),
        IDEA_SCHEMA,
    )
    print("Summary:")
    print(ideas["summary"])
    print()
    print("IDEAS:\n")
    for idea in ideas["directions"]:
        idea_num = idea["idea_num"]
        title = idea["label"]
        description = idea["description"]
        print(f"{idea_num}. {title}")
        print(description)
    chosen_idea_num = input("Pick an option by number")
    # To do: add error handling for variable
    chosen_idea = (
        next(idea for idea in ideas["directions"] if idea["id"] == chosen_idea_num),
        None,
    )
    if not chosen_idea:
        print("ERROR")
        return
    
    # Stage 2: Generate Plan
    print("Generating step by step plan")
    chosen_json = json.dumps(chosen_idea, ensure_ascii=False)
    # TODO: CHANGE STRING PROMPTS BELOW
    plan = call_api(
        SYSTEM_PROMPT,
        USER_TEMPLATE.format(project=user_project, context=user_context),
        CHOSEN_PLAN_SCEMA,
    )

if __name__ == "__main__":
    main()
