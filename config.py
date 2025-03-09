import yaml

def load_config(file_path):
    """
    Loads configuration data from a YAML file.

    Args:
        file_path (str): The path to the YAML configuration file.

    Returns:
        dict: A dictionary containing the configuration data, or None if the file is empty.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        yaml.YAMLError: If there is an error parsing the YAML file.
    """
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file: {file_path}. Error: {e}")

#Example usage and error handling.
if __name__ == "__main__":
    try:
        config = load_config("example.yaml") #replace with your yaml file.
        if config:
            print("Configuration loaded successfully:", config)
        else:
            print("Config file was empty")
    except FileNotFoundError as e:
        print(e)
    except yaml.YAMLError as e:
        print(e)