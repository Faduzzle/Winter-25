Main Elements of a Game
===
1.
1. strategies
    - the possible strategies are called the strategies space
    - a strategy profile is a list of strategies that each players selects
        - which is also a subset of the strategy space
    - For compactnes, a strategy profile is denoted by 
    $$ s = (s_i, s_{-1}) \quad\text{, where i is the player's strategy and -i is every ther strategy}$$

    1. Payoff function/preferences
        - a game must also list the payoff that every player obtains under each possible strategy
        - we characterize payoffs using utility functions which are a mapping from the strategy functions
        - utility functins only allow ordinal and not cardinal comparisons. Insensity of the like or dislike cannot be inferred, only the rank order
    1. Information
        - the information available to the players is also important for the game
        - complete information: All players know the structure of the game, including the payoffs, strategies, and types of all players, but not necessarily each other's chosen actions
        - perfect informtation: players know all previous moves and utcomes in the game when making their decisions, but may not know the full structure of the game, such as payoffs or types of players
        - incomplete/imperfect information:
            1. incomplete information: players lack knowledge about some aspects of the game such as payoffs or types of other players ( uncertainty of opponent's preferences)
            1. impoerfect information: players do not know the previous moves of the game

Assumptions game theorists make
---
1. Payoffs are known and fixed, people treate expected payoffs the same as certain payoffs (they are risk neutral)
    - ***we can relax this assumptions to capture risk averse behavior***

1. All players behave rationally
    - they understand and seek tho maximize their own profit
    - they do not make mistakes and can calculate which actions maximize their profits

1. The rules of the game are **common knowledge**
    - each player knows the set of players of players, strategies, and payoffs from all possible combinations of strategies: call this information "X"

Two main game forms
---
1. simultaneous move games
    - ex: sealed-bid auctions
    - all players choose their strategy at the same time without the knowledge of other player's strategy
1. sequential move games
    - this type of game has an order of moves

Simultaneous Move Game
--- 
Ex1: Hide and Seek
- two players
- two strategies:
$$ S_1= \{In, Out\},\quad S_2 = \{In, Out\}$$

The payoff functions show us that the seeker's strategy is to try to pick the same option as the hider

<br>

Ex2: Prisoner's DIlemma
- two players
- each player has two strategies:
$$ S_1 = \{Don't\ Confess, Confess\}, \quad S_2 = \{Don't\ Confess, Confess\}$$
