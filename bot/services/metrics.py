import time
from dataclasses import dataclass, field

@dataclass
class Metrics:
    started_at: float = field(default_factory=time.time)
    scans: int = 0
    hits: int = 0
    notifications: int = 0

    def uptime(self) -> float:
        return time.time() - self.started_at

metrics = Metrics()
