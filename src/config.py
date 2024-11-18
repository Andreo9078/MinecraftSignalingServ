import os

from src.exceptions import MissingEnvVar

DEBUG = os.getenv("DEBUG", True)

if DEBUG:
    from dotenv import load_dotenv

    load_dotenv()


def get_env_var_or_exc(var_name: str, default_value: str = None) -> str:
    result = os.getenv(var_name, default_value)
    if not result:
        raise MissingEnvVar(var_name)

    return result


DB_NAME = get_env_var_or_exc("DB_NAME")
JWT_LIFETIME = int(get_env_var_or_exc("JWT_LIFETIME"))
SECRET_KEY = get_env_var_or_exc("SECRET_KEY")
