import json
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from openai import OpenAI

# Allow running both via `python app.py` and via Gunicorn/Render.
try:
    from backend.prompts import (
        USER_TEMPLATE,
        SYSTEM_PROMPT,
        IDEA_SCHEMA,
        USER_PLAN,
        CHOSEN_PLAN_SCEMA,
    )
except ImportError:
    from prompts import (  # type: ignore
        USER_TEMPLATE,
        SYSTEM_PROMPT,
        IDEA_SCHEMA,
        USER_PLAN,
        CHOSEN_PLAN_SCEMA,
    )

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__, template_folder=str(BASE_DIR / "templates"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def call_api(system_prompt: str, user_prompt: str, schema: dict) -> dict:
    """Call the ChatGPT API and return parsed JSON."""
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_schema", "json_schema": schema},
    )
    text = response.choices[0].message.content or "{}"
    return json.loads(text)


def require_json():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return None, jsonify({"error": "Expected JSON body"}), 400
    return data, None, None


@app.route("/")
def index():
    return render_template("index.html")

@app.post("/ideas")
def ideas():
    data, error_resp, status = require_json()
    if error_resp:
        return error_resp, status

    project = data.get("project", "").strip()
    context = data.get("context", "").strip()
    if not project:
        return jsonify({"error": "project is required"}), 400

    ideas = call_api(
        SYSTEM_PROMPT,
        USER_TEMPLATE.format(project=project, context=context),
        IDEA_SCHEMA,
    )

    return jsonify(ideas)


@app.post("/plan")
def plan():
    data, error_resp, status = require_json()
    if error_resp:
        return error_resp, status

    project = data.get("project", "").strip()
    context = data.get("context", "").strip()
    chosen_id = data.get("chosen_idea_num", "").strip()
    chosen_label = data.get("chosen_label", "").strip()
    if not (project and chosen_id and chosen_label):
        return (
            jsonify({"error": "project, chosen_idea_num, chosen_label are required"}),
            400,
        )

    chosen_idea = {"idea_num": chosen_id, "label": chosen_label}


    # Plan Only
    plan_response = call_api(
        SYSTEM_PROMPT,
        USER_PLAN.format(
            project=project,
            context=context,
            chosen_idea=json.dumps(chosen_idea, ensure_ascii=False),
        ),
        CHOSEN_PLAN_SCEMA,
    )

    return jsonify({ "plan": plan_response, "chosen_idea" : chosen_idea})


if __name__ == "__main__":
    app.run(debug=True)