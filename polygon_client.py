from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pytz
from db_manager import get_engine
from polygon import RESTClient
from models import AggregateData, OptionData, session_scope

engine = get_engine()
Session = sessionmaker(bind=engine)
session = Session()


class PolygonClient:
    def __init__(self, api_key):
        self.client = RESTClient(api_key)

    def fetch_aggregates(self, ticker, multiplier, timespan, start_date, end_date):
        with session_scope() as session:
            cached_data = (
                session.query(AggregateData)
                .filter(
                    AggregateData.ticker == ticker,
                    AggregateData.date
                    >= datetime.strptime(start_date, "%Y-%m-%d").replace(
                        tzinfo=pytz.UTC
                    ),
                    AggregateData.date
                    <= datetime.strptime(end_date, "%Y-%m-%d").replace(tzinfo=pytz.UTC),
                )
                .all()
            )

            if cached_data:
                return cached_data

            aggs = self.client.list_aggs(
                ticker=ticker,
                multiplier=multiplier,
                timespan=timespan,
                from_=start_date,
                to=end_date,
            )
            for agg in aggs:
                new_record = AggregateData(
                    ticker=ticker,
                    date=datetime.fromtimestamp(agg.timestamp / 1000, tz=pytz.UTC),
                    open=agg.open,
                    high=agg.high,
                    low=agg.low,
                    close=agg.close,
                    volume=agg.volume,
                )
                session.add(new_record)
            return aggs

    def fetch_option_greeks(self, option_ticker):
        try:
            # Use the Universal Snapshot endpoint to fetch option details
            response = self.client.get(
                f"/v3/snapshot?ticker.any_of={option_ticker}&limit=1"
            )
            option_details = response.json()
            greeks = option_details["results"][0]["greeks"]
            with session_scope() as session:
                new_record = OptionData(
                    ticker=option_ticker,
                    date=datetime.utcnow(),
                    delta=greeks["delta"],
                    gamma=greeks["gamma"],
                    theta=greeks["theta"],
                    vega=greeks["vega"],
                    rho=greeks.get(
                        "rho", None
                    ),  # Some responses might not include all greeks
                )
                session.add(new_record)
            return greeks
        except Exception as e:
            print(f"Failed to fetch Greeks: {e}")
            return None


# Don't forget to close the session
session.close()
