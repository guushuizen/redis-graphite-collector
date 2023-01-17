from abc import ABC
from abc import abstractmethod
from typing import Any

from redis.client import Pipeline
from typing import List


class BaseCollector(ABC):
    @abstractmethod
    def collect(self, pipeline: Pipeline) -> int:
        "Adds commands to the pipeline and returns the commands added"
        ...

    @abstractmethod
    def transform(self, result: List[Any]) -> List[dict]:
        """
        Receives query results passed in the same order as passed previously to the pipline.
        Transforms into a list of dicts ready to send to Graphite.

        Any dict should hold the `name`, `interval`, `value` and `time` key.
        Refer to https://grafana.com/docs/grafana-cloud/data-configuration/metrics/metrics-graphite/http-api/#adding-new-data-posting-to-metrics
            for more information on Graphite and its HTTP API.
        """
        ...



