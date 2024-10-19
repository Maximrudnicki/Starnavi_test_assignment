from openai import OpenAI

from config.config import API_KEY


client = OpenAI(api_key=API_KEY)


def filter_text(input: str):
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=input,
    )

    return response.to_dict()["results"][0]["flagged"]
