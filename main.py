from argparse import ArgumentParser
from datetime import datetime
import logging

from config_manager import get_api_key
from polygon_client import PolygonClient
from db_manager import get_engine
from models import Base

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def setup_database(engine):
    try:
        Base.metadata.create_all(engine)
        logging.info("Database tables created successfully.")
    except Exception as e:
        logging.error("Failed to create tables: %s", e)


def fetch_and_display_aggregates(
    polygon_client, ticker, multiplier, timespan, start_date, end_date
):
    try:
        aggs = polygon_client.fetch_aggregates(
            ticker, multiplier, timespan, start_date, end_date
        )
        for agg in aggs:
            print(
                f"Ticker: {agg.ticker}, Date: {agg.date}, Open: {agg.open}, High: {agg.high}, Low: {agg.low}, Close: {agg.close}, Volume: {agg.volume}"
            )
    except Exception as e:
        logging.error("Failed to fetch aggregates: %s", e)


def fetch_and_display_greeks(polygon_client, option_ticker):
    greeks = polygon_client.fetch_option_greeks(option_ticker)
    if greeks:
        print(f"Greeks for {option_ticker}: {greeks}")


def main(
    ticker="AAPL",
    start_date=datetime.now().strftime("%Y-%m-%d"),
    end_date=datetime.now().strftime("%Y-%m-%d"),
    option_ticker="AAPL230616C00145000",
):
    engine = get_engine()
    setup_database(engine)

    api_key = get_api_key()
    polygon_client = PolygonClient(api_key)

    fetch_and_display_aggregates(polygon_client, ticker, 1, "day", start_date, end_date)
    fetch_and_display_greeks(polygon_client, option_ticker)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--ticker", type=str, default="AAPL", help="Stock ticker symbol (default: AAPL)"
    )
    parser.add_argument(
        "--start_date",
        type=str,
        default=datetime.now().strftime("%Y-%m-%d"),
        help="Start date (YYYY-MM-DD) (default: today's date)",
    )
    parser.add_argument(
        "--end_date",
        type=str,
        default=datetime.now().strftime("%Y-%m-%d"),
        help="End date (YYYY-MM-DD) (default: today's date)",
    )
    parser.add_argument(
        "--option_ticker",
        type=str,
        default="AAPL230616C00145000",
        help="Option ticker symbol (default: AAPL230616C00145000)",
    )
    args = parser.parse_args()

    main(args.ticker, args.start_date, args.end_date, args.option_ticker)
