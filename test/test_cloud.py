import os
import vertexai
import dotenv
from vertexai.preview import reasoning_engines
from langchain_google_vertexai import HarmBlockThreshold, HarmCategory

dotenv.load_dotenv()
vertexai.init(
    project=os.getenv('GOOGLE_PROJECT_ID'),
    location="us-west1",
    staging_bucket=f"gs://{os.getenv('GOOGLE_BUCKET_NAME')}",
)

model = "gemini-1.0-pro"
safety_settings = {
    HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
}
model_kwargs = {
    # temperature (float): The sampling temperature controls the degree of
    # randomness in token selection.
    "temperature": 0.28,
    # max_output_tokens (int): The token limit determines the maximum amount of
    # text output from one prompt.
    "max_output_tokens": 1000,
    # top_p (float): Tokens are selected from most probable to least until
    # the sum of their probabilities equals the top-p value.
    "top_p": 0.95,
    # top_k (int): The next token is selected from among the top-k most
    # probable tokens.
    "top_k": 40,
    # safety_settings (Dict[HarmCategory, HarmBlockThreshold]): The safety
    # settings to use for generating content.
    "safety_settings": safety_settings,
}


def get_exchange_rate(
        currency_from: str = "USD",
        currency_to: str = "EUR",
        currency_date: str = "latest",
):
    """Retrieves the exchange rate between two currencies on a specified date.

    Uses the Frankfurter API (https://api.frankfurter.app/) to obtain exchange rate data.

    Args:
        currency_from: The base currency (3-letter currency code). Defaults to "USD" (US Dollar).
        currency_to: The target currency (3-letter currency code). Defaults to "EUR" (Euro).
        currency_date: The date for which to retrieve the exchange rate. Defaults to "latest" for the most recent exchange rate data. Can be specified in YYYY-MM-DD format for historical rates.

    Returns:
        dict: A dictionary containing the exchange rate information.
             Example: {"amount": 1.0, "base": "USD", "date": "2023-11-24", "rates": {"EUR": 0.95534}}
    """
    import requests
    response = requests.get(
        f"https://api.frankfurter.app/{currency_date}",
        params={"from": currency_from, "to": currency_to},
    )
    return response.json()


get_exchange_rate(currency_from="USD", currency_to="SEK")
agent = reasoning_engines.LangchainAgent(
    model=model,  # Required.
    tools=[get_exchange_rate],  # Optional.
    model_kwargs=model_kwargs,  # Optional.
)
response = agent.query(
    input="What is the exchange rate from US dollars to Swedish currency?"
)
print(response)