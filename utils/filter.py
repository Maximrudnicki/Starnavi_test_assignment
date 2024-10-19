from openai import OpenAI

# from config.config import API_KEY

API_KEY = "sk-DeS1lGRmEmQKk-L1BNKIPLTn3IARJLXsyxQeZ0qm84T3BlbkFJiYQ_GQw3ygABpNoNZiH0svWYfeidfSuNvREFVTJksA"


client = OpenAI(api_key=API_KEY)


def filter_text(input: str):
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=input,
    )

    return response.to_dict()["results"][0]["flagged"]
