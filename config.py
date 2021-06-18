from pydantic import BaseSettings, Field, SecretStr


class CurrencyConfig(BaseSettings):
    api_url: str = Field(..., env='CURRENCY_API_URL')
    api_key: SecretStr = Field(..., env='CURRENCY_API_KEY')
    secret_api_key: SecretStr = Field(..., env='CURRENCY_SECRET_API_KEY')
