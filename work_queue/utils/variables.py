import os


def get_env_variable(variable_name, log, expected_type=str):
    log.info(f"Obtaining environment variable {variable_name}")
    try:
        value = os.environ[variable_name]
        log.debug(f"{variable_name}: {value}")
        return expected_type(value)
    except KeyError:
        raise KeyError(f"The environment variable '{variable_name}' is not set.")
    except ValueError:
        raise ValueError(
            f"The value of environment variable '{variable_name}' is not of expected type {expected_type.__name__}.")
