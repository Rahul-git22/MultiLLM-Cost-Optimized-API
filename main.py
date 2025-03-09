from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from router import RouteManager
from config import load_config
import logging
from logger import setup_logger, log_usage_data

# Initialize the logger using the custom setup_logger function.
logger = setup_logger()

# Create a FastAPI application instance.
app = FastAPI()

# Load configuration from the 'providers.yaml' file.
config = load_config("providers.yaml")

# Initialize the RouteManager with the loaded configuration.
route_manager = RouteManager(config)

# Re-obtain the logger with the correct name. This is generally redundant
# since setup_logger already does this, but it's kept here for clarity.
logger = logging.getLogger(__name__)

# Define a Pydantic model for the incoming prompt request.
class PromptRequest(BaseModel):
    prompt: str  # The prompt string provided by the user.

# Define the endpoint for generating responses.
@app.post("/generate")
async def generate(request: PromptRequest):
    """
    Endpoint to process prompt requests and generate responses.

    Args:
        request (PromptRequest): The incoming request containing the prompt.

    Returns:
        dict: The generated response data.

    Raises:
        HTTPException: If an error occurs during processing.
    """
    try:
        # Route the request to the appropriate provider using the RouteManager.
        response_data = await route_manager.route_request(request.prompt)

        # Log successful request processing.
        logger.info(f"Request processed successfully: {response_data}")

        # Return the generated response data.
        return response_data

    except Exception as e:
        # Log any errors that occur during request processing.
        logger.error(f"Error processing request: {e}")

        # Raise an HTTPException with a 500 status code and the error details.
        raise HTTPException(status_code=500, detail=str(e))

