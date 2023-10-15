from typing import Callable
from stock_trader.reporting.visualizer import (
    ExponentialMovingAverageVisualizer,
    MACDVisualizer,
    RSIVisualizer,
    SimpleMovingAverageVisualizer,
    Visualizer,
)

VisualizerFactory = Callable[[], Visualizer]


def visualizer_factory() -> Visualizer:
    return RSIVisualizer(MACDVisualizer(SimpleMovingAverageVisualizer(ExponentialMovingAverageVisualizer())))
