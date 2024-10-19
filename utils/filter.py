from openai import OpenAI


API_KEY = "sk-pPx-KnrZIlCapTuNaZex0GAhSH9u0GKnTGIZAsM4_bT3BlbkFJFJu3jZ7kQ53CBfguDqDB1u377oXM95DypE--siwGMA"


client = OpenAI(api_key=API_KEY)


def filter_text(input: str):
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=input,
    )

    return response.to_dict()["results"][0]["flagged"]
