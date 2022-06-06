
from abc import ABC, abstractmethod


class ReleaseMetric(ABC):
    @abstractmethod
    def measure(self, release):
        pass

class Cycle(ReleaseMetric):
    def measure(self, release):
        pass
