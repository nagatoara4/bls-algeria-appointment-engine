import time
from dataclasses import dataclass, field

@dataclass
class Metrics:
    started_at: float = field(default_factory=time.time)
    scans: int = 0
    hits: int = 0
    claims_attempted: int = 0
    claims_success: int = 0

    def uptime(self) -> float:
        return time.time() - self.started_at

    @property
    def success_rate(self) -> float:
        if self.claims_attempted == 0:
            return 0.0
        return round(100.0 * self.claims_success / self.claims_attempted, 1)

metrics = Metrics()
