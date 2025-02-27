import math
import numpy as np
import pandas as pd
from scipy.stats import norm

"""

Sample code:

black_scholes(S, X, T, t, r, sigma)
mode_of_ST(S, T, t, mu, sigma)
option_delta(S, strike, r, sigma, T, t, option_type = 'call')
print(option_behavior)

"""


#   solving for price of option

def black_scholes(S, X, T, t, r, sigma):
    """
    Solve Black-Scholes equations for European call and put options.
    blac
    :param S: Current stock price
    :param X: Strike price
    :param T: Time to expiration
    :param t: Current time
    :param r: Risk-free interest rate
    :param sigma: Volatility of the underlying asset
    :return: Dictionary with call and put option values
    """
    tau = T - t
    d1 = (np.log(S / X) + (r + 0.5 * sigma ** 2) * tau) / (sigma * np.sqrt(tau))
    d2 = d1 - sigma * np.sqrt(tau)
    
    call_price = S * norm.cdf(d1) - np.exp(-r * tau) * X * norm.cdf(d2)
    put_price = np.exp(-r * tau) * X * norm.cdf(-d2) - S * norm.cdf(-d1)
    
    call_delta = norm.cdf(d1)
    put_delta = -norm.cdf(-d1)
    
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(tau))
    vega = S * norm.pdf(d1) * np.sqrt(tau)
    theta_call = - (S * norm.pdf(d1) * sigma) / (2 * np.sqrt(tau)) - r * X * np.exp(-r * tau) * norm.cdf(d2)
    theta_put = - (S * norm.pdf(d1) * sigma) / (2 * np.sqrt(tau)) + r * X * np.exp(-r * tau) * norm.cdf(-d2)
    rho_call = X * tau * np.exp(-r * tau) * norm.cdf(d2)
    rho_put = -X * tau * np.exp(-r * tau) * norm.cdf(-d2)
    
    data = {
        "Metric": ["Price", "Delta", "Gamma", "Vega", "Theta", "Rho"],
        "Call": [call_price, call_delta, gamma, vega, theta_call, rho_call],
        "Put": [put_price, put_delta, gamma, vega, theta_put, rho_put]
    }
    

    return pd.DataFrame(data)


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

conditions = [
        "S -> 0 (Call)", "S -> 0 (Put)", "S -> ∞ (Call)", "S -> ∞ (Put)",
        "T -> 0 (Call)", "T -> 0 (Put)", "T -> ∞ (Call)", "T -> ∞ (Put)",
        "σ -> 0 (Call)", "σ -> 0 (Put)", "σ -> ∞ (Call)", "σ -> ∞ (Put)",
        "r -> 0 (Call)", "r -> 0 (Put)", "r -> ∞ (Call)", "r -> ∞ (Put)"
    ]
    
behaviors = [
    "C -> 0", "P -> X * exp(-rT)", "C -> S - X * exp(-rT)", "P -> 0",
    "C -> max(S - X, 0)", "P -> max(X - S, 0)", "C -> S - X * exp(-rT)", "P -> X * exp(-rT) - S",
    "C -> Black-Scholes with zero volatility", "P -> Black-Scholes with zero volatility",
    "C increases with σ", "P increases with σ", "C -> Black-Scholes with r = 0", "P -> Black-Scholes with r = 0",
    "C decreases with high r", "P increases with high r"
]

d1_values = [
    "d1 -> -∞", "d1 -> -∞", "d1 -> ∞", "d1 -> -∞",
    "d1 finite", "d1 finite", "d1 -> 0", "d1 -> 0",
    "d1 -> ∞", "d1 -> ∞", "d1 -> -∞", "d1 -> -∞",
    "d1 -> finite", "d1 -> finite"
]

d2_values = [
    "d2 -> -∞", "d2 -> -∞", "d2 -> ∞", "d2 -> -∞",
    "d2 finite", "d2 finite", "d2 -> 0", "d2 -> 0",
    "d2 -> -∞", "d2 -> -∞", "d2 -> -∞", "d2 -> -∞",
    "d2 -> finite", "d2 -> finite"
]

N_d1_values = [
    "0", "0", "1", "0", "Finite", "Finite", "0.5", "0.5",
    "1", "1", "0", "0", "Finite", "Finite"
]

N_d2_values = [
    "0", "0", "1", "0", "Finite", "Finite", "0.5", "0.5",
    "0", "0", "Finite", "Finite"
]

deltas = [
    "0", "-1", "1", "0", "Finite", "Finite", "0.5", "-0.5",
    "1", "-1", "0", "0", "Finite", "Finite"
]

gammas = [
    "0", "0", "0", "0", "Finite", "Finite", "High", "High",
    "0", "0", "0", "0", "Finite", "Finite"
]

vegas = [
    "0", "0", "0", "0", "Finite", "Finite", "0", "0",
    "High", "High", "0", "0", "Finite", "Finite"
]

thetas = [
    "0", "0", "0", "0", "Finite", "Finite", "-High", "-High",
    "0", "0", "0", "0", "Finite", "Finite"
]

rhos = [
    "0", "0", "0", "0", "Finite", "Finite", "Finite", "Finite",
    "0", "0", "0", "0", "Finite", "Finite"
]

data = {
    "Boundary Condition": conditions,
    "Option Price Behavior": behaviors,
    "d1 Behavior": d1_values,
    "d2 Behavior": d2_values,
    "N(d1) Value": N_d1_values,
    "N(d2) Value": N_d2_values,
    "Delta": deltas,
    "Gamma": gammas,
    "Vega": vegas,
    "Theta": thetas,
    "Rho": rhos
}

limits = pd.DataFrame(data)

"""

cumulative cdf of lognormal dist
realized volatility
hedging solve for alpha
at the money problems

"""
