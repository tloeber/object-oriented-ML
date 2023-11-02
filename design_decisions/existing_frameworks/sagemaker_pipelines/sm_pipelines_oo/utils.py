from pathlib import Path
from pydantic import ValidationError
from pydantic_settings import BaseSettings
from loguru import logger


def load_pydantic_config_from_file(config_cls: type[BaseSettings], env_file: str) -> BaseSettings:
    """Load settings from a .env file."""
    try:
        return config_cls(_env_file=env_file)

    except ValidationError as e:
        if not Path(env_file).is_file():
            logger.exception(
                f"Failed to load {config_cls.__name__} because the following file does not exist: {env_file}: {e}"
            )

        raise e