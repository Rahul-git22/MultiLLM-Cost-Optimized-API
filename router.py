import logging
from provider import all_Provider

class RouteManager:
    """
    Manages and routes requests to different providers based on priority and cost.
    """
    def __init__(self, config):
        """
        Initializes the RouteManager with a configuration.

        Args:
            config (dict): A dictionary containing provider configurations.
        """
        self.providers = self._initialize_providers(config)

    def _initialize_providers(self, config):
        """
        Initializes and sorts providers based on priority and cost.

        Args:
            config (dict): A dictionary containing provider configurations.

        Returns:
            list: A sorted list of provider instances.
        """
        providers_list = []
        for p in config['providers']:
            providers_list.append(all_Provider(p))
        # Sort providers: lower priority numbers are higher priority, then lower cost.
        providers_list.sort(key=lambda x: (x.priority, x.cost_per_1k))
        return providers_list

    async def route_request(self, prompt):
        """
        Routes a request to the first available provider based on priority and cost.

        Args:
            prompt (str): The prompt to send to the provider.

        Returns:
            dict: The response from the successful provider.

        Raises:
            Exception: If all providers fail to process the request.
        """
        for provider in self.providers:
            try:
                return await provider.generate(prompt)
            except Exception as e:
                logging.error(f"Provider {provider.model} failed: {e}")
        raise Exception("All providers failed")
