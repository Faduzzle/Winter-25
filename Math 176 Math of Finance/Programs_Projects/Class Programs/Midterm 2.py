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
gbm_lognormal_stats(x=100, X_t=100, mu=0.05, sigma=0.2, T_minus_t=1)


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

d1_values = ["d1 -> -∞", "d1 -> -∞", "d1 -> ∞", "d1 -> -∞", "d1 finite", "d1 finite", "d1 -> 0", "d1 -> 0",
             "d1 -> ∞", "d1 -> ∞", "d1 -> -∞", "d1 -> -∞", "d1 -> finite", "d1 -> finite", "d1 -> -∞", "d1 -> ∞"]

d2_values = ["d2 -> -∞", "d2 -> -∞", "d2 -> ∞", "d2 -> -∞", "d2 finite", "d2 finite", "d2 -> 0", "d2 -> 0",
             "d2 -> -∞", "d2 -> -∞", "d2 -> -∞", "d2 -> -∞", "d2 -> finite", "d2 -> finite", "d2 -> -∞", "d2 -> ∞"]

N_d1_values = ["0", "0", "1", "0", "Finite", "Finite", "0.5", "0.5", "1", "1", "0", "0", "Finite", "Finite", "0", "1"]

N_d2_values = ["0", "0", "1", "0", "Finite", "Finite", "0.5", "0.5", "0", "0", "Finite", "Finite", "0", "1", "0", "1"]

deltas = ["0", "-1", "1", "0", "Finite", "Finite", "0.5", "-0.5", "1", "-1", "0", "0", "Finite", "Finite", "0", "1"]

gammas = ["0", "0", "0", "0", "Finite", "Finite", "High", "High", "0", "0", "0", "0", "Finite", "Finite", "0", "1"]

vegas = ["0", "0", "0", "0", "Finite", "Finite", "0", "0", "High", "High", "0", "0", "Finite", "Finite", "0", "1"]

thetas = ["0", "0", "0", "0", "Finite", "Finite", "-High", "-High", "0", "0", "0", "0", "Finite", "Finite", "0", "1"]

rhos = ["0", "0", "0", "0", "Finite", "Finite", "Finite", "Finite", "0", "0", "0", "0", "Finite", "Finite", "0", "1"]

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

df_boundaries = pd.DataFrame(data).set_index("Boundary Condition")

def gbm_lognormal_stats(x, X_t, mu, sigma, T_minus_t):
    """
    Calculate various statistics for a lognormal variable arising from a 
    geometric Brownian motion (GBM) process at a future time.
    
    Parameters:
        x (float or array-like): The value(s) at which to evaluate the CDF and PDF.
        X_t (float): The value of the process at time t.
        mu (float): Drift coefficient of the GBM process.
        sigma (float): Volatility coefficient of the GBM process.
        T_minus_t (float): Time difference between the future time T and current time t.
        
    Returns:
        dict: A dictionary containing:
            'cdf'      : Cumulative Distribution Function evaluated at x.
            'pdf'      : Probability Density Function evaluated at x.
            'mean'     : Mean of the lognormal distribution.
            'median'   : Median of the lognormal distribution.
            'mode'     : Mode of the lognormal distribution.
            'variance' : Variance of the lognormal distribution.
    """
    # Update the parameters for the lognormal distribution
    mu_1 = np.log(X_t) + (mu - 0.5 * sigma**2) * T_minus_t
    sigma_1 = sigma * np.sqrt(T_minus_t)
    
    # Calculate the CDF and PDF at x
    # Note: For x > 0; x can be a scalar or an array.
    cdf = norm.cdf(np.log(x), loc=mu_1, scale=sigma_1)
    pdf = norm.pdf(np.log(x), loc=mu_1, scale=sigma_1) / x  # Adjusted for lognormal
    
    # Compute moments of the lognormal distribution
    mean = np.exp(mu_1 + 0.5 * sigma_1**2)
    median = np.exp(mu_1)
    mode = np.exp(mu_1 - sigma_1**2)
    variance = (np.exp(sigma_1**2) - 1) * np.exp(2 * mu_1 + sigma_1**2)
    
    stats= {
        'cdf': cdf,
        'pdf': pdf,
        'mean': mean,
        'median': median,
        'mode': mode,
        'variance': variance
    }
    for key, value in stats.items():
        print(f"{key.capitalize()}: {value:.4f}" if np.isscalar(value) else f"{key.capitalize()}: {value}")
"""


cumulative cdf of lognormal dist
realized volatility
hedging solve for alpha
at the money problems

"""
