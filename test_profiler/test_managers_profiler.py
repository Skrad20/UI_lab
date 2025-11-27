from test_profiler.profiler import profiler
from code_app.managers import ManagerUtilities
import pandas as pd


class TestProfilerManager:
    def __init__(self) -> None:
        self.manager_utilites = ManagerUtilities()

    def run_profiler(self):
        self.test_delit()

    @profiler("TestProfilerManager")
    def test_delit(self):
        data = pd.DataFrame(
            data=["23/34" for i in range(100000)],
            columns=["data"]
        )
        self.manager_utilites.delit(data, "/", "data")


if __name__ == "__main__":
    test = TestProfilerManager()
    test.run_profiler()
