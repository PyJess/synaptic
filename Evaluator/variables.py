import os
from docx import Document
from langchain_openai import ChatOpenAI
import json
import asyncio
from pathlib import Path

## This script is used to extract all the possible variables in the input word file.

process_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "process"))

for root, dirs, files in os.walk(process_dir):
        for file in files:
          if file.endswith(".docx"):
              print(f"Processing file: {file}")
              file_path = os.path.join(root, file)
              input_data = ""
              doc=Document(file_path)
              for para in doc.paragraphs:
                  if para.text:
                      input_data += str(para.text) + "\n"


gpt=ChatOpenAI(model='gpt-4.1').bind(
            temperature=0.7,
            frequency_penalty=0,
            presence_penalty=0,
            logprobs=True,
            top_logprobs=10,
        )

messages=[
    {"role": "system", "content": """You are an expert assistant. Given an input text, you must identify all possible variables it contains. For each variable, extract its specific value and store the results in a JSON structure, where each entry includes the variable name and its corresponding value. The purpose of this JSON is to clearly map which variables exist with their fixed values, ensuring that these values cannot be changed. example of output: {
  "population": 2344,
  "age": 43,
  "country": "Italy"
}"""},
    {"role": "user", "content": "This is the input text:" + input_data}
]

print(f"MESSAGES:{messages}")


async def a_invoke_model(gpt, msgs):
    return await gpt.ainvoke(msgs)


async def main():
    response = await a_invoke_model(gpt, messages)

    if hasattr(response, "content"):
        clean_response = response.content
    elif isinstance(response, list):
        clean_response = [msg.content for msg in response]

    if isinstance(clean_response, str):
        try:
 
            clean_response = json.loads(clean_response)
        except json.JSONDecodeError:

            clean_response = {"text": clean_response}

    output_file = Path("variables.json")
    with output_file.open("w", encoding="utf-8") as f:
        json.dump(clean_response, f, ensure_ascii=False, indent=4)


asyncio.run(main())


with open("variables.json", "r", encoding="utf-8") as f:
    data = json.load(f)


def extract_keys(obj, prefix=""):
    keys = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            full_key = f"{prefix}.{k}" if prefix else k
            keys.append(full_key)
            keys.extend(extract_keys(v, prefix=full_key))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            full_key = f"{prefix}[{i}]"
            keys.extend(extract_keys(item, prefix=full_key))
    return keys

all_keys = extract_keys(data)

for key in all_keys:
    print(key)
