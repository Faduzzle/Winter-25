## Compounding Interest
$$ P_{t+1} = (1+r)P_t$$
where $(1+r$) is the discounting factor

compounding over N periods we have
$$P_{1+n} = (1+r)^n P_t$$

The final value of investments after 1 year depends on M, the number of times per year compounding, and r the annual percentage rate (APR) 
$$P_{FINAL} = (1+\frac {r}{M})^MP_0$$

The limit as M grows large is $e^r$

## Present Value
Continuous compounding

$$P_{FINAL} = P_0e^{rt}$$

Present value of continuous compounding
$$P_0 = P_{FINAL}e^{-rt}$$

## Put-Call Parity
1. Own the stock and the right to sell it (put option)$$ S + P_E(S,t)$$
    - computing payoff at expiration:
    $$\text{Payoff at expiration}\quad = S+max(0,E-S)
    

1. right to buy the stock and enough cash to buy the right(long call)
$$C_E(S,t)+ Ee^{-r(T-t)}$$
1. for no arbitrage to hold true
$$S + P_E(S,t) = C_E(S,t)+ Ee^{-r(T-t)}$$
