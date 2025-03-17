import math
import csv
import numpy as np
from scipy.stats import norm
from scipy.optimize import newton

def compute_returns(close_prices: list[float]) -> list[float]:
    returns = []
    for i in range(1, len(close_prices)):
        returns.append((close_prices[i] - close_prices[i-1]) / close_prices[i-1])
    return returns


def compute_mean(returns: list[float], annualized=True):
    s = 0
    for r in returns:
        s += math.log(1 + r)
    return (252 ** .5) * s / len(returns) if annualized else s / len(returns)


def compute_vol(returns: list[float], annualized=True):
    mean = compute_mean(returns, False)
    s = 0
    for r in returns:
        s += (math.log(1 + r) - mean) ** 2
    return (s / (len(returns) - 1)) ** .5 * 252 ** .5 if annualized else (s / (len(returns) - 1)) ** .5

def csv_to_list(rel_filepath, skipfirst=True):
    start = 0 if skipfirst else 1
    l = []
    with open(rel_filepath) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if "$" in row[1]:
                l.append(float(row[1][1:]))
    return l

def csv_to_lists(rel_filepath):
    l1 = []
    l2 = []
    l3 = []
    with open(rel_filepath) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            l1.append(float(row[0]))
            l2.append(float(row[1]))
            l3.append(float(row[2]) / 100)
    return l1, l2, l3

def term_csv_to_lists(rel_filepath):
    T_list = []
    premium_list = []
    with open(rel_filepath) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            T_list.append(float(row[3]))
            premium_list.append(float(row[1]))
    return T_list, premium_list

class Option:
    def __init__(self, S, E, T, r, sigma=None, premium=None, option_type='call'):
        """
        Initialize an Option instance.
        
        Parameters:
            S : float
                Current underlying asset price.
            K : float
                Strike price.
            T : float
                Time to expiration (in years).
            r : float
                Annual risk-free interest rate.
            sigma : float, optional
                Volatility (if known). If not provided, premium must be given.
            premium : float, optional
                Market price of the option (used to back out implied volatility if sigma is not provided).
            option_type : str, default 'call'
                Type of option: 'call' or 'put'.
        """
        self.S = S
        self.K = E
        self.T = T
        self.r = r
        self.option_type = option_type.lower()
        
        if sigma is None and premium is None:
            raise ValueError("Provide either volatility (sigma) or premium (market price).")
        
        # If sigma is not provided, compute implied volatility from the market price.
        if sigma is None:
            self.premium = premium
            self.sigma = self.implied_volatility(premium)
        else:
            self.sigma = sigma
            self.premium = premium if premium is not None else self.price()
    
    def d1(self, sigma=None):
        """
        Calculate the d1 term used in the Black-Scholes formulas.
        """
        sigma = sigma if sigma is not None else self.sigma
        return (np.log(self.S / self.K) + (self.r + 0.5 * sigma ** 2) * self.T) / (sigma * np.sqrt(self.T))
    
    def d2(self, sigma=None):
        """
        Calculate the d2 term used in the Black-Scholes formulas.
        """
        sigma = sigma if sigma is not None else self.sigma
        return self.d1(sigma) - sigma * np.sqrt(self.T)
    
    def price(self, sigma=None):
        """
        Compute the Black-Scholes price for the option.
        """
        sigma = sigma if sigma is not None else self.sigma
        d1 = self.d1(sigma)
        d2 = self.d2(sigma)
        if self.option_type == 'call':
            return self.S * norm.cdf(d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
        elif self.option_type == 'put':
            return self.K * np.exp(-self.r * self.T) * norm.cdf(-d2) - self.S * norm.cdf(-d1)
        else:
            raise ValueError("Invalid option type. Use 'call' or 'put'.")
    
    def delta(self):
        """
        Calculate and return the option's delta.
        """
        d1 = self.d1()
        if self.option_type == 'call':
            return norm.cdf(d1)
        elif self.option_type == 'put':
            return norm.cdf(d1) - 1
    
    def gamma(self):
        """
        Calculate and return the option's gamma.
        """
        d1 = self.d1()
        return norm.pdf(d1) / (self.S * self.sigma * np.sqrt(self.T))
    
    def theta(self):
        """
        Calculate and return the option's theta.
        """
        d1 = self.d1()
        d2 = self.d2()
        term1 = - (self.S * norm.pdf(d1) * self.sigma) / (2 * np.sqrt(self.T))
        if self.option_type == 'call':
            term2 = - self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
            return term1 + term2
        elif self.option_type == 'put':
            term2 = self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-d2)
            return term1 + term2
    
    def vega(self):
        """
        Calculate and return the option's vega.
        """
        d1 = self.d1()
        return self.S * norm.pdf(d1) * np.sqrt(self.T)
    
    def rho(self):
        """
        Calculate and return the option's rho.
        """
        d2 = self.d2()
        if self.option_type == 'call':
            return self.T * self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
        elif self.option_type == 'put':
            return -self.T * self.K * np.exp(-self.r * self.T) * norm.cdf(-d2)
    
    def implied_volatility_objective(self, sigma, market_price):
        """
        The objective function for the Newton-Raphson method to compute implied volatility.
        """
        return self.price(sigma) - market_price
    
    def implied_volatility(self, market_price):
        """
        Calculate the implied volatility given a market price using the Newton-Raphson method.
        """
        sigma_initial_guess = 0.2
        return newton(self.implied_volatility_objective, sigma_initial_guess, args=(market_price,))
