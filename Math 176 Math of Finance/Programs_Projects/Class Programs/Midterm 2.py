import math
import numpy as np
from scipy.stats import norm

"""

Sample code:

black_scholes(S, X, T, t, r, sigma, option_type="call")
mode_of_ST(S, T, t, mu, sigma)
option_delta(S, strike, r, sigma, T, t, option_type = 'call')
print(option_behavior)

"""


#   solving for price of option

def black_scholes(S, X, T, t, r, sigma, option_type="call"):
    """
    Solve Black-Scholes equations for European call/put options.
    
    :param S: Current stock price
    :param X: Strike price
    :param T: Time to expiration
    :param t: Current time
    :param r: Risk-free interest rate
    :param sigma: Volatility of the underlying asset
    :param option_type: "call" for call option, "put" for put option
    :return: Option price
    """
    tau = T - t
    d1 = (np.log(S / X) + (r + 0.5 * sigma ** 2) * tau) / (sigma * np.sqrt(tau))
    d2 = d1 - sigma * np.sqrt(tau)
    
    if option_type == "call":
        price = S * norm.cdf(d1) - np.exp(-r * tau) * X * norm.cdf(d2)
        delta = norm.cdf(d1)
    elif option_type == "put":
        price = np.exp(-r * tau) * X * norm.cdf(-d2) - S * norm.cdf(-d1)
        delta = -norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")
    
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(tau))
    vega = S * norm.pdf(d1) * np.sqrt(tau)
    theta = - (S * norm.pdf(d1) * sigma) / (2 * np.sqrt(tau)) - r * X * np.exp(-r * tau) * norm.cdf(d2 if option_type == "call" else -d2)
    rho = X * tau * np.exp(-r * tau) * norm.cdf(d2 if option_type == "call" else -d2)
    
    return {
        "price": price,
        "delta": delta,
        "gamma": gamma,
        "vega": vega,
        "theta": theta,
        "rho": rho
    }

    """
    if option_type == "call":
        price = S * norm.cdf(d1) - np.exp(-r * tau) * X * norm.cdf(d2)
    elif option_type == "put":
        price = np.exp(-r * tau) * X * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put' -lowercase-")

    return price
"""
#           Mode of S(T)


def mode_of_ST(S, T, t, mu, sigma):
    """
    Compute the mode of the lognormal distribution of S(T)
    
    :param S: Current stock price
    :param T: Time to expiration
    :param t: Current time
    :param mu: Drift (expected return)
    :param sigma: Volatility of the underlying asset
    :return: Mode of S(T)
    """
    tau = T - t
    mu_1 = np.log(S) + (mu - 0.5 * sigma**2) * tau
    sigma_1_squared = sigma**2 * tau
    mode_ST = np.exp(mu_1 - sigma_1_squared)
    return mode_ST


#           Solving for delta


def option_delta(S, strike, r, sigma, T, t, option_type = 'call'):
    """
    Compute optimal delta to elimate stochastic process

    :param S:       Current stock price
    :param T:       Time to expiration
    :param strike:  option strike price
    :param r:       risk free rate
    :param sigma:   Volatility of the underlying asset
    """
    
    
    tau = T-t
    d1 = (np.log(S / strike) + (r + 0.5 * sigma ** 2) * tau) / (sigma * np.sqrt(tau))

    if option_type == "call":
        delta = norm.cdf(d1)
    elif option_type == "put":
        delta = norm.cdf(d1)-1
    else:
        raise ValueError("option_type must be 'call' or 'put' -lowercase-")

    return delta

option_behavior = """
Call Option Behavior:
- As S -> 0, the call option price approaches 0.
- As S -> ∞, the call option price approaches S - X * exp(-r * (T - t)).
- As T -> t, the call price is max(S - X, 0).
- As T -> ∞, the call price approaches S.
- As r -> ∞, the call price approaches S.
- As r -> 0, the call price follows Black-Scholes with r = 0.
- As σ -> ∞, the call price approaches S.
- As σ -> 0, the call price is max(S - X * exp(-r * (T - t)), 0).

Put Option Behavior:
- As S -> 0, the put option price approaches X * exp(-r * (T - t)).
- As S -> ∞, the put option price approaches 0.
- As T -> t, the put price is max(X - S, 0).
- As T -> ∞, the put price approaches 0.
- As r -> ∞, the put price approaches 0.
- As r -> 0, the put price follows Black-Scholes with r = 0.
- As σ -> ∞, the put price approaches X * exp(-r * (T - t)).
- As σ -> 0, the put price is max(X * exp(-r * (T - t)) - S, 0).
"""
"""

cumulative cdf of lognormal dist
realized volatility
hedging solve for alpha
at the money problems

"""

def american_arb(S, strike, r, sigma, T, t, option_type = 'call'):
    european_value = black_scholes(S, strike, r, sigma, T, t, option_type)
    early_excercise = 