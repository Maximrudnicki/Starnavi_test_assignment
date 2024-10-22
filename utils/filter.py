from openai import OpenAI

# from config.config import API_KEY

API_KEY = "sk-DeS1lGRmEmQKk-L1BNKIPLTn3IARJLXsyxQeZ0qm84T3BlbkFJiYQ_GQw3ygABpNoNZiH0svWYfeidfSuNvREFVTJksA"
# API_KEY = "sk-kOwNDwK_myUP65G7fq9029JXuycJ2kZ2VSdv3pxh9ZT3BlbkFJozm1x8OzQEJYIEZq0X4Ri_ZadWAEh4eyeMymxVkZIA"


client = OpenAI(api_key=API_KEY)


def filter_text(input: str):
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=input,
    )

    return response.to_dict()["results"][0]["flagged"]
