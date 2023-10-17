import json
from pathlib import Path

from stock_trader.acquisition.data_sources.alpha_vantage import AlphaVantageResponse


def test_alpha_vantage_response_can_parse_json_correctly():
    with open(Path(__file__).parent / "test_data/example_alpha_vantage_response.json") as f:
        response = json.load(f)
        AlphaVantageResponse(**response)
    