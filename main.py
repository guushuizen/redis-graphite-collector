from collections import defaultdict
import time
from typing import List

from redis import Redis
import requests

from collectors import BaseCollector
from collectors.random import RandomDimensionCollector
import config

COLLECTORS = [
    RandomDimensionCollector()
]


def collect_all():
    connection = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)

    collected_metrics = collect(connection, COLLECTORS)

    requests.post(
        url=config.GRAPHITE_ENDPOINT,
        auth=(config.GRAPHITE_USER, config.GRAPHITE_AUTH),
        json=collected_metrics
    )

    print(f"Posted {len(collected_metrics)} metrics to Graphite!")


def collect(connection: Redis, collectors: List[BaseCollector]) -> List[dict]:
    pipeline = connection.pipeline()

    collector_tracker = []

    for collector in collectors:
        collector_tracker.extend([collector] * collector.collect(pipeline))

    pipeline_result = pipeline.execute()

    to_transform = defaultdict(list)

    for collector, pipeline_result in zip(collector_tracker, pipeline_result):
        to_transform[collector].append(pipeline_result)

    return [
        transformed_metric
        for collector, metrics in to_transform.items()
        for transformed_metric in collector.transform(list(metrics))
    ]


if __name__ == "__main__":
    start_time = time.time()
    while True:
        collect_all()
        time.sleep(config.INTERVAL - ((time.time() - start_time) % config.INTERVAL))

