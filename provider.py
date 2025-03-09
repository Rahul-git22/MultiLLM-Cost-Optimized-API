import requests
import tiktoken
import logging
from logger import log_usage_data
import time

class all_Provider:
    """
    A class representing a provider for generating text using an API.
    """
    def __init__(self, config):
        """
        Initializes the provider with configuration parameters.

        Args:
            config (dict): A dictionary containing configuration parameters, including:
                - api_key (str): The API key for authentication.
                - model (str): The model to use for text generation.
                - cost_per_1k_tokens (float): The cost per 1000 tokens.
                - endpoint (str): The API endpoint.
                - priority (int): The priority of the provider.
        """
        self.api_key = config['api_key']
        self.model = config['model']
        self.cost_per_1k = config['cost_per_1k_tokens']
        self.endpoint = config['endpoint']
        self.priority = config['priority']

    async def generate(self, prompt):
        """
        Generates text based on the given prompt using the provider's API.

        Args:
            prompt (str): The prompt for text generation.

        Returns:
            dict: A dictionary containing the generated text, model used, tokens used and cost.

        Raises:
            Exception: If an error occurs during the API call or processing.
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": None  # Consider adding max_tokens from config if needed.
            }
            start_time = time.time()
            response = requests.post(self.endpoint, headers=headers, json=data)
            end_time = time.time()
            time_taken = end_time - start_time

            if response.status_code == 200:
                response_data = response.json()
                generated_text = response_data['choices'][0]['message']['content']
                tokens_used = len(tiktoken.get_encoding("cl100k_base").encode(generated_text))
                cost = (tokens_used / 1000) * self.cost_per_1k
                log_usage_data(self.model, tokens_used, cost, time_taken, True)
                return {
                    "modelUsed": self.model,
                    "tokens": tokens_used,
                    "cost": cost,
                    "response": generated_text
                }
            else:
                log_usage_data(self.model, 0, 0, time_taken, False)
                logging.error(f"{self.model} error: {response.status_code} - {response.text}")
                raise Exception(f"{self.model} failed with status code {response.status_code}")

        except requests.exceptions.Timeout:
            time_taken = time.time() - start_time
            log_usage_data(self.model, 0, 0, time_taken, False)
            logging.error(f"{self.model} request timed out")
            raise Exception(f"{self.model} timed out")

        except Exception as e:
            time_taken = time.time() - start_time
            log_usage_data(self.model, 0, 0, time_taken, False)
            logging.error(f"{self.model} error: {e}")
            raise Exception(f"{self.model} failed")