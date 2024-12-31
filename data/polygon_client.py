from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pytz
from config.db_manager import get_engine
from polygon import RESTClient
from models.models import AggregateData, OptionData, session_scope
import yfinance as yf
from services.black_scholes_service import calculate_greeks

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

    def fetch_option_greeks_yfinance(self, ticker, option_type="call"):
        """
        Fetch option data from yfinance and calculate Greeks using Black-Scholes.
        """
        try:
            # Fetch the option chain
            stock = yf.Ticker(ticker)
            options = stock.options

            # For simplicity, we'll use the nearest expiration date
            expiration = options[0]
            opt_chain = stock.option_chain(expiration)

            # Choose call or put options
            options_data = opt_chain.calls if option_type == "call" else opt_chain.puts

            # Iterate over options to calculate Greeks
            greeks_list = []
            for idx, option in options_data.iterrows():
                S = stock.history(period="1d")["Close"].iloc[-1]
                K = option["strike"]
                T = (
                    datetime.strptime(expiration, "%Y-%m-%d") - datetime.utcnow()
                ).days / 365.0
                r = 0.01  # Assume 1% risk-free rate; you might want to fetch current rates
                sigma = option["impliedVolatility"]

                greeks = calculate_greeks(S, K, T, r, sigma, option_type)
                greeks["ticker"] = option["contractSymbol"]
                greeks["date"] = datetime.utcnow()
                greeks_list.append(greeks)

                # Store in database
                with session_scope() as session:
                    new_record = OptionData(
                        ticker=option["contractSymbol"],
                        date=datetime.utcnow(),
                        delta=greeks["delta"],
                        gamma=greeks["gamma"],
                        theta=greeks["theta"],
                        vega=greeks["vega"],
                        rho=greeks["rho"],
                    )
                    session.add(new_record)

            return greeks_list

        except Exception as e:
            print(f"Failed to fetch option Greeks from yfinance: {e}")
            return None


# Don't forget to close the session
session.close()
