import math
from scipy.stats import norm


def black_scholes(S, K, T, r, sigma, option_type="call"):
    """
    Calculate the Black-Scholes option price.
    """
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    if option_type == "call":
        price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return price


def calculate_greeks(S, K, T, r, sigma, option_type="call"):
    """
    Calculate the Greeks for an option using the Black-Scholes formula.
    """
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    delta = norm.cdf(d1) if option_type == "call" else -norm.cdf(-d1)
    gamma = norm.pdf(d1) / (S * sigma * math.sqrt(T))
    theta = -(S * norm.pdf(d1) * sigma) / (2 * math.sqrt(T)) - r * K * math.exp(
        -r * T
    ) * norm.cdf(d2 if option_type == "call" else -d2)
    vega = S * norm.pdf(d1) * math.sqrt(T)
    rho = K * T * math.exp(-r * T) * norm.cdf(d2 if option_type == "call" else -d2)

    return {
        "delta": delta,
        "gamma": gamma,
        "theta": theta,
        "vega": vega / 100,  # Vega is often represented per 1% change in volatility
        "rho": rho / 100,  # Rho is often represented per 1% change in rates
    }
