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
            "sample_outline": {"type": "string"}
          },
          "required": ["idea_num", "label", "description", "sample_prompt", "sample_outline"],
          "additionalProperties": False
        }
      }
    },
    "required": ["summary", "directions"],
    "additionalProperties": False
  },
  "strict": True
}
