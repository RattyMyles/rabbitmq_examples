import json
from utils.exceptions import JSONException


def parse_json(body, log):
    try:
        parsed_data = json.loads(body)
        return parsed_data
    except ValueError:
        # Handle JSON decoding errors
        error_message = "Error: Invalid JSON format"
        log.error(error_message)
        raise JSONException(error_message)
    except KeyError:
        # Handle key errors if accessing a non-existent key in the JSON
        error_message = "Error: Key not found"
        log.error(error_message)
        raise JSONException(error_message)
    except TypeError:
        # Handle type errors if the input is not a string
        error_message = "Error: Input is not a valid JSON string"
        log.error(error_message)
        raise JSONException(error_message)
    except json.JSONDecodeError as e:
        # Handle other JSON decoding errors
        error_message = f"Error decoding JSON: {e}"
        log.error(error_message)
        raise JSONException(error_message)
