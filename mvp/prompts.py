SYSTEM_PROMPT = """
You are a supportive writing and planning coach. Keep langauge brief and concrete. Avoid filler.
"""

USER_TEMPLATE = """
User profile:
- project : {project}
- context : {context}

Chosen idea (from prior options):
{chosen_idea_json}

Task:
1) Identify the main issue of the project
2) Propose 5 distinct ideas that could help the user start
3) Each idea must have:
{
    "ID": "ID_NUMBER",
    "LABEL": "SHORT_READABLE_NAME", 
    "TIMELINE": "SIMPLE_TIMELINE",
}
Return only a JSON that matches the template
"""
