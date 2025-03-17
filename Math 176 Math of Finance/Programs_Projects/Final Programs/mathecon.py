import math
import numpy as np
from scipy.stats import norm

def calculate_optimal_bets(odds, total_money):

    # Convert odds to numpy array for easier calculations
    odds = np.array(odds)

    # Calculate the denominator for optimal bets formula
    denominator = np.sum(1 / (1 + odds))

    # Calculate optimal bets for each outcome
    optimal_bets = total_money / denominator * (1 / (1 + odds))

    # Calculate the guaranteed profit
    profit = total_money * (np.prod(1 + odds) / np.sum(np.prod(1 + odds) / (1 + odds)) - 1)

    return optimal_bets, profit

def p_to_odds(p):
    return (1 - p) / p

def odds_to_p(odds):
    return 1 / (odds + 1)

# calculate expected value for finite list of events
def expected_value(prob_list, value_list):
    p_sum = 0
    v_sum = 0
    for i in range(len(prob_list)):
        p_sum += prob_list[i]
        v_sum += prob_list[i] * value_list[i]
    if abs(p_sum - 1) > .0001:
        raise ValueError
    else:
        return v_sum
    
def variance(prob_list, value_list):
    v2_sum = 0
    for i in range(len(prob_list)):
        v2_sum += prob_list[i] * value_list[i] ** 2
    return v2_sum - expected_value(prob_list, value_list) ** 2

def find_p(s, c, E, r, t):
    return c + E * math.e ** (-r * t)  - s

def find_c(s, p, E, r, t):
    return s + p - E * math.e ** (-r * t)

def find_e(s, p, c, r, t):
    return (s + p - c) / (math.e ** (-r * t))

def find_s(p, c, E, r, t):
    return c + E * math.e ** (-r * t)  - p

def find_r(s, p, c, E, t):
    return math.log((s + p - c) / E) / -t

def find_t(s, p, c, E, r):
    return math.log((s + p - c) / E) / -r

def fact(x):
    if x == 0:
        return 1
    p = 1
    for i in range(1, x+1):
        p *= i
    return p

def derivative(x, y):
    return (-1) **  (x // 2) * ((-1)** x + 1) / 2

def taylor(x, n, deriv=derivative):
    s = 0
    for j in range(n + 1):
        s += -deriv(j) * (x - math.pi) ** j / (fact(j))
    return s

def c(n, k):
    p = 1
    for i in range(n - k + 1, n + 1):
        p *= i
    for i in range(1, k + 1):
        p //= i
    return p

# probability that variable with 
#   mean = mu
#   var = sigma
#   n samples
#   has sum less than x
def clt_sum(mu, sigma, n, x):
    return norm.cdf(x, loc=mu * n, scale=sigma * (n ** .5))

# probability that variable with 
#   mean = mu
#   var = sigma
#   n samples
#   has sum less than x
def clt_avg(mu, sigma, n, x):
    return norm.cdf(x, loc=mu, scale=sigma / (n ** .5))

# hw specific
def e6():
    good = 0
    total = 0
    for x in range(0, 101):
        for y in range(0, 101 - x):
            pos = c(100, x) * c(100 - x, y)
            if (4 * x + 5 * y >= 310):
                good += pos
            total += pos
    return (good, total)
# returns (171790031178624005677722517960457649367012027599,
#   515377520732011331036461129765621272702107522001)
