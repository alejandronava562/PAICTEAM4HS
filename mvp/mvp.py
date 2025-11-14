from openai import OpenAI
import json
import os
from prompts import USER_TEMPLATE, SYSTEM_PROMPT

# API_KEY = os.getenv("OPENAI_API_KEY")

# client = OpenAI(
#      api_key = API_KEY
# )

def main():
    print("app")
    
    user_context = input("Describe the context project that you will be working on.")
    user_project = input("Describe the project.")  

if __name__ == "__main__":
    main()