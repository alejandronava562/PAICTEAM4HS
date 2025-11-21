SYSTEM_PROMPT = """
You are a supportive writing and planning coach. Keep langauge brief and concrete. Avoid filler.
"""

USER_TEMPLATE = """
User profile:
- project : {project}
- context : {context}

Task:
1) Identify the main issue of the project
2) Propose 5 distinct ideas that could help the user start
3) Each idea must have:
{{
    "ID": "ID_NUMBER",
    "LABEL": "SHORT_READABLE_NAME", 
    "TIMELINE": "SIMPLE_TIMELINE",
}}
Return only a JSON that matches the template
"""

IDEA_SCHEMA = {
    "name": "writers_ideation_output",
    "schema": {
        "type": "object",
        "properties": {
            "summary": {"type": "string"},
            "directions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "idea_num": {"type": "string"},
                        "label": {"type": "string"},
                        "description": {"type": "string"},
                        "sample_prompt": {"type": "string"},
                        "sample_outline": {"type": "string"},
                    },
                    "required": [
                        "idea_num",
                        "label",
                        "description",
                        "sample_prompt",
                        "sample_outline",
                    ],
                    "additionalProperties": False,
                },
            },
        },
        "required": ["summary", "directions"],
        "additionalProperties": False,
    },
    "strict": True,
}

USER_PLAN = """
User project: {project} 
User context: {context}
Chosen idea: {chosen_idea}

Task:
1) Use the chosen idea to define end goal
2) Create a realistic plan based on the chosen idea with ordered steps
Return only JSON that matches the schema
"""

CHOSEN_PLAN_SCEMA = {
    "name": "writers_plan_output",
    "schema": {
        "type": "object",
        "properties": {
            "chosen_direction_id" : {"type": "string"},
            "goal": {"type": "string"},
            "timeline_days": {"type": "int", "minimum": 1},
            "steps": {
                "type": "array",
                "items": "object",
                "properties": {
                    "step_number": {"type": "int"},
                    "label": {"type": "string"},
                    "instructions": {"type": "string"},
                },
                "required": ["step_number", "label", "instructions"],
                "additionalProperties": False,
            },
        },
        "required": ["goal", "chosen_direction_id", "timeline_days", "steps"],
        "additionalProperties": False,
    },
    "strict": True
}
