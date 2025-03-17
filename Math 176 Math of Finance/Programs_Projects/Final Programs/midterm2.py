import math
import numpy as np
from scipy.stats import norm

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
    elif option_type == "put":
        price = np.exp(-r * tau) * X * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put' -lowercase-")

    return price

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

def option_delta(S, strike, r, sigma, time, option_type = 'call'):
    """
    Compute optimal delta to elimate stochastic process

    :param S:       Current stock price
    :param T:       Time to expiration
    :param strike:  option strike price
    :param r:       risk free rate
    :param sigma:   Volatility of the underlying asset
    """
    
    
    tau = time
    d1 = (np.log(S / strike) + (r + 0.5 * sigma ** 2) * tau) / (sigma * np.sqrt(tau))

    if option_type == "call":
        delta = norm.cdf(d1)
    elif option_type == "put":
        delta = norm.cdf(-d1)-1
    else:
        raise ValueError("option_type must be 'call' or 'put' -lowercase-")

    return delta

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
        
def find_inverse(o: Option, func, target: float, change_param: str, eps:float=.0001, lower_bound=-300, upper_bound=300, max_iters=30):
    mid = (upper_bound + lower_bound) / 2
    setattr(o, change_param, mid)
    delta = func() - target
    print(mid, delta)
    if abs(delta) < eps or max_iters <= 0:
        return getattr(o, change_param)
    else:
        if delta > 0:
            return find_inverse(o, func, target, change_param, eps, lower_bound, mid, max_iters-1)
        else:
            return find_inverse(o, func, target, change_param, eps, mid, upper_bound, max_iters-1)



def taylor_option_approx(o: Option, ds: float):
    return o.price() + o.delta() * ds + o.gamma() / 2 * ds ** 2

