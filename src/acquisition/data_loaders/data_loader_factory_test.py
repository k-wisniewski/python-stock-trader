from typing import Type
import pytest
import acquisition
from acquisition.data_loaders.data_loader import DataLoader, ParallelDataLoader
from acquisition.data_loaders.data_loader_factory import (
    data_loader_factory,
    Concurrency,
)
from acquisition.data_sources.data_source import DataSource


@pytest.mark.parametrize(
    "concurrency,expected_type",
    [
        (Concurrency.THREADS, ParallelDataLoader),
        (Concurrency.PROCESSESS, ParallelDataLoader),
    ],
)
def test_correctly_typed_loaders_can_be_produced(
    concurrency: Concurrency,
    expected_type: Type[DataLoader],
    fake_data_source: DataSource,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        acquisition.data_loaders.data_loader_factory.APP_SETTINGS,
        "concurrency",
        concurrency,
    )
    data_loader = data_loader_factory(fake_data_source)
    assert isinstance(data_loader, expected_type)
