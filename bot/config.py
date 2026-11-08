from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    bot_token: str
    admin_ids: str = ""
    log_level: str = "INFO"

    @property
    def admin_id_list(self) -> List[int]:
        if not self.admin_ids.strip():
            return []
        return [int(x.strip()) for x in self.admin_ids.split(",") if x.strip().isdigit()]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
