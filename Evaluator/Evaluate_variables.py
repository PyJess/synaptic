import os
import json
import pandas as pd
import asyncio
from langchain_openai import ChatOpenAI

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "variables"))
print(src_path)


def gen_excel(src_path):
    rows = []
    for filename in os.listdir(src_path):
        if filename.endswith(".json"):
            file_path = os.path.join(src_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            flat_data = {}
            for key, value in data.items():
                if isinstance(value, list):
                    flat_data[key] = "; ".join(str(v) for v in value)
                elif isinstance(value, dict):
                    flat_data[key] = "; ".join(f"{k}: {v}" for k, v in value.items())
                else:
                    flat_data[key] = value

            flat_data["file_name"] = filename
            rows.append(flat_data)

    df = pd.DataFrame(rows)
    cols = ["file_name"] + [c for c in df.columns if c != "file_name"]
    df = df[cols]
    return df


async def check_field_consistency_with_llm(column_name, values_df):
    examples = "\n".join(
        f"{row.file_name}: {str(row[column_name]).replace('“','\"').replace('”','\"')}"
        for _, row in values_df.iterrows()
    )

    gpt = ChatOpenAI(model="gpt-4.1")

    prompt = f"""
    You are a biomedical data auditor.

    Below are the values of the same field (“{column_name}”) 
    extracted from several clinical trial JSON files. 
    Each line shows the file name and the corresponding value.

    Your task:
    - Evaluate whether the values are **consistent** across files.
    - Return a **higher score (close to 1)** when the values are mostly empty or only one non-empty value exists (this is not a real inconsistency).
    - Minor differences in formatting (e.g., slashes, capitalization, multiple sponsors separated by '/', etc.) should NOT lead to a very low score.
    - Return a lower score only when there are clear **differences in meaning or content** (e.g., different sponsors, trial phases, or study types).


    
    Return your result **only** as a JSON object like:
    {{"score": 1, "explanation": "reason here"}}

    ---
    {examples}
    ---
    """

    messages = [
        {"role": "system", "content": "You are an expert data consistency checker for clinical trials."},
        {"role": "user", "content": prompt},
    ]

    response = await gpt.ainvoke(messages)
    content = response.content.strip()
    try:
        parsed = json.loads(content)
        score = parsed.get("score", None)
        explanation = parsed.get("explanation", "")
    except Exception:
        score = None
        explanation = f"⚠️ Parsing error. Raw response: {content}"

    return {"field": column_name, "score": score, "explanation": explanation}


async def evaluate_excel(df):
    tasks = [
        check_field_consistency_with_llm(col, df[["file_name", col]])
        for col in df.columns if col != "file_name"
    ]

    # Esecuzione parallela
    results = await asyncio.gather(*tasks)

    results_df = pd.DataFrame(results)
    results_df = results_df[["field", "score", "explanation"]]
    results_df.to_excel("field_consistency_scores.xlsx", index=False)
    print("✅ Done! Results saved in field_consistency_scores.xlsx")


def main():
    print("Generating Excel...")
    df = gen_excel(src_path)
    output_path = "variables.xlsx"
    df.to_excel(output_path, index=False)
    print(f"✅ Excel file created: {output_path}")

    print("Evaluating Excel...")
    asyncio.run(evaluate_excel(df))


if __name__ == "__main__":
    main()


# ----------------------------------------------------------------------------
