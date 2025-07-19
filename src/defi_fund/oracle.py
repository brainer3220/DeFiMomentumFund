from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

from web3 import Web3

from .config import settings

# Minimal Chainlink AggregatorV3 interface
AGGREGATOR_ABI = [
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {"internalType": "uint8", "name": "", "type": "uint8"}
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "latestRoundData",
        "outputs": [
            {"internalType": "uint80", "name": "roundId", "type": "uint80"},
            {"internalType": "int256", "name": "answer", "type": "int256"},
            {"internalType": "uint256", "name": "startedAt", "type": "uint256"},
            {"internalType": "uint256", "name": "updatedAt", "type": "uint256"},
            {"internalType": "uint80", "name": "answeredInRound", "type": "uint80"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
]


@lru_cache(maxsize=None)
def _w3() -> Web3:
    return Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER_URI))


def _price_from_chainlink(feed: str) -> float:
    """Return latest price from a Chainlink aggregator."""
    contract = _w3().eth.contract(address=feed, abi=AGGREGATOR_ABI)
    answer = contract.functions.latestRoundData().call()[1]
    decimals = contract.functions.decimals().call()
    return float(answer) / 10 ** decimals


def get_price(symbol: str, feed: Optional[str] = None) -> float:
    """Get USD price for a token symbol."""
    env_key = f"MOCK_PRICE_{symbol.upper()}"
    if env_key in os.environ:
        return float(os.environ[env_key])
    feed = feed or settings.PRICE_FEED
    if feed:
        try:
            return _price_from_chainlink(feed)
        except Exception:
            pass
    # default to 1.0 if no feed or fetch fails
    return 1.0
