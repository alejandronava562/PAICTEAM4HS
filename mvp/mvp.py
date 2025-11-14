from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import json
import os
from prompts import USER_TEMPLATE, SYSTEM_PROMPT, IDEA_SCHEMA

api_key=os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def call_api(system_prompt, user_prompt, schema):
    response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[
        {"role": "user", "content": user_prompt},
        {"role": "system", "content": system_prompt}
    ],
    response_format={"type": "json_schema", "json_schema": schema}
    )
    text = response.choices[0].message.content
    return json.loads(text) # type: ignore


def main():
    print("app")
    
    user_project = input("Describe the project.").strip()
    user_context = input("Describe the context of the project that you will be working on.").strip()

    print("Generating possible ideas...\n")
    ideas = call_api(SYSTEM_PROMPT, 
                     USER_TEMPLATE.format(project=user_project, context= user_context), 
                     IDEA_SCHEMA)
    print(ideas["summary"])
    print("IDEAS:\n")
    for idea in ideas["direction"]:
        


if __name__ == "__main__":
    main()
