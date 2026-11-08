from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    bot_token: str
    admin_ids: str = ""
    log_level: str = "INFO"
    db_path: str = "data/devil.db"
    max_monitors_per_user: int = 10
    scan_interval_sec: int = 8
    aggression_level: int = 8
    proxy_list: str = ""

    @property
    def admin_id_list(self) -> List[int]:
        if not self.admin_ids.strip():
            return []
        return [int(x.strip()) for x in self.admin_ids.split(",") if x.strip().isdigit()]

    @property
    def proxies(self) -> List[str]:
        if not self.proxy_list.strip():
            return []
        return [p.strip() for p in self.proxy_list.split(",") if p.strip()]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
