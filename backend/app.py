from pathlib import Path

from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

from prompts import USER_TEMPLATE, SYSTEM_PROMPT, IDEA_SCHEMA, USER_PLAN, CHOSEN_PLAN_SCEMA

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
app = Flask(__name__, template_folder=str(BASE_DIR / "templates"))
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


@app.route("/")
def index():
    return render_template("index.html")

@app.post("/ideas")
def ideas():
    data = request.json
    project = data.get("project", "")
    context = data.get("context", "")
    ideas = call_api(
        SYSTEM_PROMPT,
        USER_TEMPLATE.format(project=project, context=context),
        IDEA_SCHEMA,
    )

    return jsonify(ideas)


@app.route("/plan")
def plan():
    data = request.json
    project = data.get("project", "")
    context = data.get("context", "")
    chosen_id = data.get("chosen_idea_num", "")
    chosen_label = data.get("chosen_label", "")
    chosen_idea = {"id": chosen_id, "label":chosen_label}


    # Plan Only
    plan = call_api(
        SYSTEM_PROMPT,
        USER_PLAN.format(project=project, context=context, chosen_idea=chosen_idea),
        CHOSEN_PLAN_SCEMA,
    )

    return jsonify({ "plan": plan, "chosen_idea" : chosen_idea})


if __name__ == "__main__":
    app.run(debug=True)
