from datetime import datetime
from datetime import timezone
from typing import Any
from typing import List

from redis.client import Pipeline

from collectors import BaseCollector
from config import QUEUE_PREFIX
from config import QUEUES
from config import INTERVAL


class RandomDimensionCollector(BaseCollector):
    dimension_count = 5

    def collect(self, pipeline: Pipeline) -> int:
        for dimension in range(self.dimension_count):
            pipeline.llen(f"random:{dimension + 1}")

        return len(QUEUES)

    def transform(self, result: List[Any]) -> dict:
        now = int(datetime.now(timezone.utc).timestamp())
        for dimension in range(self.dimension_count):
            yield {
                "value": result[dimension],
                "interval": INTERVAL,
                "name": f"lists.random.{dimension + 1}",
                "time": now,
            }
