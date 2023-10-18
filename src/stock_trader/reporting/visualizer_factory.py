from typing import Callable
from stock_trader.reporting.visualizer import (
    ExponentialMovingAverageVisualizer,
    MACDVisualizer,
    RSIVisualizer,
    SimpleMovingAverageVisualizer,
    Visualizer,
)
from stock_trader.reporting.visualizer_runner import ChunkedMultiprocessingVisualizerRunner, NaiveMultiprocessingVisualizerRunner, SingleThreadedVisualizerRunner, VisualizerRunner
from stock_trader.settings import APP_SETTINGS, Concurrency

VisualizerFactory = Callable[[], Visualizer]


def visualizer_factory() -> Visualizer:
    return RSIVisualizer(MACDVisualizer(SimpleMovingAverageVisualizer(ExponentialMovingAverageVisualizer())))

def visualizer_runner_factory() -> VisualizerRunner:
    if APP_SETTINGS.visualizer_runner_concurrency == Concurrency.SINGLE_THREADED:
        return SingleThreadedVisualizerRunner(visualizer_factory())
    elif APP_SETTINGS.visualizer_runner_concurrency == Concurrency.PROCESSESS:
       return NaiveMultiprocessingVisualizerRunner(visualizer_factory())
    #   return ChunkedMultiprocessingVisualizerRunner(visualizer_factory())
    raise ValueError(f"Unsupported concurrency: {APP_SETTINGS.visualizer_runner_concurrency}")