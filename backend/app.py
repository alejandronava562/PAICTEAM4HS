from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

from prompts import USER_TEMPLATE, SYSTEM_PROMPT, IDEA_SCHEMA, USER_PLAN, CHOSEN_PLAN_SCEMA

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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
    return json.loads(text)


@app.route("/run", methods=["POST"])
def run():
    data = request.json
    project = data.get("project", "")
    context = data.get("context", "")
    chosen_id = data.get("chosen_idea_num", "")

    # Stage 1: Ideas
    ideas = call_api(
        SYSTEM_PROMPT,
        USER_TEMPLATE.format(project=project, context=context),
        IDEA_SCHEMA,
    )

    # Get chosen idea
    try:
        chosen_idea = next(i for i in ideas["directions"] if i["idea_num"] == chosen_id)
    except StopIteration:
        return jsonify({"error": "Chosen idea not found"}), 400

    # Stage 2: Plan
    plan = call_api(
        SYSTEM_PROMPT,
        USER_PLAN.format(project=project, context=context, chosen_idea=chosen_idea),
        CHOSEN_PLAN_SCEMA,
    )

    return jsonify({
        "ideas": ideas,
        "chosen_idea": chosen_idea,
        "plan": plan
    })


if __name__ == "__main__":
    app.run(debug=True)
