Hedging: maning bets or investments to eradicate risk

ex: simple sports betting
- 100 dollars to bet on UCLA vs USC game
- UCLA fan offers you 3:1 odds on UCLA winning
- USC fan offers 3:2 odds on USC winning

<br>
<br>

payoff table:
| ODDS | UCLA Wins | USC Wins |
|---|---|---|
| UCLA fan (3:1) |-100 |+300|
| USC fan (3:2)| +150|-100|


<br>
<br>

Is there a way to bet with both ways such that we are guaranteed a win?
-
#### Modeling strategy:
- $ x\ bet\ with\ UCLA\ fan $
- $ (100 - x)\ bet \ with\ USC\ fan $
<br>
### Payoff table:
| ODDS | UCLA Wins | USC Wins |
|---|---|---|
| UCLA fan (3:1) |$-x$ |$+3 * x$|
| USC fan (3:2)| +$\frac{3}{2} * (100 - x)$|-$(100 - x)$|

#### Now to calculate how much to bet on each team

- ##### UCLA wins
    1. set profit > 0 
    1. model payoff for UCLA winning
        <br> $$ -x +\frac{3}{2}(100-x) > 0$$
        <br> $$ x< 60 $$
    1. model payoff for USC winning
        <br> $$ 3x - (100-x) > 0 $$
        <br> $$x>25$$
    1. Choose $25<x<60$ and profit will be postive no matter which event happens
    
![alt text](<../Images/profit plot for sports betting.png>)

$$ x = 38.46 $$
This value will maximize profit
$$ 4(x) - 100 = p$$
$$p = 53.85\quad \text {when}\ x = 38.46$$

<br>
<br>
<br>

### Alternative Hedging Objectives
***
Suppose we want to maximize our profits if UCLA wins but are only willing to lose no more than $10 no matter what happens

1. one option is to bet 10 dollars with the USC fan and pocket the 90 dollars

| ODDS | UCLA Wins | USC Wins |
|---|---|---|
| UCLA fan (3:1) |0 |0|
| USC fan (3:2)| $+15$|$-10$|
|Total Winnings| $+15$| $-10$|
2. Or we can use the model from above and choose an **$x$** with payoffs greater than $-10 \text{ dollars}$
    $$ \text{Profit}_{USC\ wins} =4x - 100>-10 \quad \quad x>22.50$$
    $$\text{Profit}_{UCLA\ wins} = 150-\frac{5}{2}x>-10 \quad \quad x<64$$
    $$\text {Now we choose}\ 22.50<x<64 $$

Now the profit table turns to 
| ODDS | UCLA Wins | USC Wins |
|---|---|---|
| UCLA fan (3:1) |$-22.50$ |$67.50|
| USC fan (3:2)| $116.5$|$-77.50$|
|Total Winnings| $+93.75$| $-10$|

#### New scenario
---
-  UCLA fan offers 1:2 on UCLA winning
- USC fan offers 4:5 odds on USC winning

Does aribitrage still exist?
| ODDS | UCLA Wins | USC Wins |
|---|---|---|
| UCLA fan (1:2) |$-x$ |$\frac{x}{2}$|
| USC fan (4:5)| $\frac{4}{5}(100-x)$|$-(100-x)$|

Setting Profit > 0
$$\text{Profit}_\text{UCLA\ wins} x <44.44$$
$$\text{Profit}_\text{USC\ wins} x>66.67$$

$$\text{These two conditions are impossible to satisfy so arbitrage does not exist}$$


![alt text](<../Images/no arbitrage graph.png>)

<br>
<br>

Formula to calculate sportsbetting arbitrage
---
| ODDS | UCLA Wins | USC Wins |
|---|---|---|
| UCLA fan (1:2) |$-x$ |$O_{A}x$|
| USC fan (4:5)| $O_{B}(n-x)$|$-(n-x)$|

which we can solve by
$$x^* = \frac{n(1+O_B)}{2+O_A+O_B}$$
$$\text{This gives us the solution }x^*\text{ for profit }p^*\text{ given by:}$$
$$p^* = \frac{n(O_AO_B-1)}{2+O_A+O_B}$$
$$\text{Note that in order for }p^*\text{ to be positive we must have}$$
$$O_AO_B>1$$


## Expected Value
$ \text{suppose }X_d\text{ is a discrete random variable that takes on values }\{x_1,x_2, x_3, ..., x_n\} \text{ with probabilities } \{p_1, p_2,p_3, ..., p_n\}$

The probabilities $p_i$ have to sum up to 1 when you are dealing with mutually exculsive events that encompass all possible outcomes
$$ \sum_{i=1}^n{p_i} = 1$$

Then the *Expected Value* of $X_d$ is:
$$ E(X_d) = \sum_{i=1}^n\ x_i \cdot p_i $$
