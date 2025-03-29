def main():
    print("starting abot")
    # start_abot()


if __name__ == '__main__':
    main()

    # ~ / PycharmProjects / ABOT
    # git: [main]
    # ├── README.md
    # ├── connectors
    # │   ├── binance.py
    # │   ├── coindcx.py
    # │   ├── csx.py
    # │   └── kucoin.py
    # ├── database
    # │   ├── db.py
    # │   ├── schema.sql
    # │   └── migrations /
    # ├── main.py
    # ├── manager
    # │   ├── arbitrage_manager.py        -- Core logic for identifying arbitrage between various exchanges
    # │   ├── config_manager.py           -- Handles configuration loading and validation
    # ├── models
    # │   ├── arbitrage_opportunity.py -- Defines data model for arbitrage opportunities
    # │   └── exchange.py              -- Stores exchange-specific metadata.
    # ├── poetry.lock
    # ├── pyproject.toml
    # ├── service
    # │   ├── fetcher.py
    # │   ├── processor.py
    # │   ├── notifier.py (not required now)
    # │   └── executor.py (not required now)
    # ├── utils
    # │   ├── logger.py
    # │   ├── metrics.py
    # │   ├── config_loader.py
    # │   └── helper.py
