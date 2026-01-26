# Iterated Prisoner's Dilemma

## Instructions

- You should aim to work in a team of two, but you are allowed to work alone or in a team of three. Your team should submit a single writeup. You should also submit a single code solution and a PDF with your writings answering the prompts in Part 2.
- We will run a class tournament where each student agent plays against each other student agent.
- You are allowed to engage with other teams over Perusall (e.g., use the chat feature to create a general discussion) or in person (but this is neither encouraged nor discouraged). If this is part of your strategy, you should discuss what you did and why you did it in your writeup. You are allowed to coordinate with other teams, or trick other teams. You are not allowed to promise other teams favors (e.g. monetary rewards) or threaten punishment outside the scope of this assignment. For example, you are allowed to promise ''if your code does X, our code will do Y.'' You are not allowed to promise ''if your code does X, I will buy you a cookie.'' If this is part of your strategy, your justification should explain why it will help you on this assignment.
- Please reference the course collaboration policy.
- Please reference the grading instructions for these assignments.
- This assignment is open-ended, please ask questions to clarify expectations as needed.

### Background

The Prisoners’ Dilemma is a classic problem in game theory that is often used to explore behaviors in a situation of strategic interdependence.

The usual presentation of the problem is that two suspects are being interrogated separately by a detective. The detective has insufficient evidence to make an arrest, depending on a plea bargain to make a convincing case.

The detective offers each suspect the following deal: "defect" and admit to the crime in exchange for early parole, or "cooperate" (with the other prisoner) and refuse to admit the crime. Neither suspect is told of the other's choice. If both cooperate (C, C) (=don't admit), then both are found guilty of a minor charge (for a payoff of 3 each). If one defects while the other cooperates, (D, C) or (C, D), then the person who defects (=admits) is released (payoff 5) while the other serves a long sentence (payoff 0). If both defect (D, D) (=admit), they both go to prison but with early parole (payoff 1).

|          |     | Player 2 |      |
| -------- | --- | -------- | ---- |
|          |     | C        | D    |
| Player 1 | C   | 3, 3     | 0, 5 |
|          | D   | 5, 0     | 1, 1 |

When played once, only one equilibrium exists: both suspects defect, and both face prison time with early parole. This is a dominant strategy equilibrium.  However, if both suspects had cooperated then both would have gone free. This is the dilemma!

When played once, the prisoners make their choices confident in the knowledge that their opponent would never know of a betrayal. In the iterated prisoners’ dilemma (IPD), the game is repeated and the suspects can make their decisions based on knowledge of previous betrayals. Cooperation can occur because a player can punish a treacherous opponent.

In his 1984 book The Evolution of Cooperation, Robert Axelrod describes the results of a tournament that he organized for academics to submit IPD strategies for a fixed number of rounds. The winner was the strategy "tit-for-tat" ---play the same move as was chosen by the opponent in the previous round.

In general, Axelrod found that altruistic strategies triumphed over greedy ones. At the 20th anniversary of the competition, a new strategy from the University of Southampton, UK, outperformed even tit-for-tat. U. Southampton made multiple entries into the competition. At each game, an entry would recognize if its opponent was another U. Southampton entry or an enemy. Some of the entries were self-sacrificing, continuously cooperating with another U. Southampton entry (which would defect), allowing those entries to take the top rankings. If a U. Southampton entry did not recognize its opponent as one of its own, it would continuously defect to minimize its opponent's score. Interestingly enough, Richard Dawkins had already predicted the success of such a strategy in his book The Selfish Gene.

You can check out the Wikipedia article for more information on the [Prisoners’ Dilemma](https://en.wikipedia.org/wiki/Prisoner%27s_dilemma) (and the iterated prisoners’ dilemma)[.](https://en.wikipedia.org/wiki/Prisoner%27s_dilemma#The_iterated_prisoner.27s_dilemma)

For this problem set, you will create a submission to an IPD tournament similar to the one Axelrod set up in 1984 but with a twist.

In particular, the information your player receives about its opponent's previous action is noisy. With a probability of 0.05, your player receives incorrect information about the last action of the other player. (Note: the payoffs are for the correct action, but you don't learn the payoff.) Tit-for-tat is not reliable in noisy environments. To understand why, imagine that Alice is told that her opponent Bob defected, when in fact, Bob cooperated. Alice would then defect, falsely punishing Bob, and the mistaken defections will echo until someone gets the wrong information once again. What do you think would be the best strategy to overcome a noisy environment for IPD? In discussing the complications that noise adds to his tournament, Axelrod said that "Noise calls for forgiveness, but too much forgiveness invites exploitation." How will you design a winning agent for such an environment?

### Part 1: Making your Agents

#### The game

Your task is to create an agent for the iterated noisy prisoner's dilemma described above. In each round, there will be a 5% probability of mis-detecting your opponent's move. The scores for each round are as follows: 

|     | C   | D   |
| --- | --- | --- |
| C   | 3,3 | 0,5 |
| D   | 5,0 | 1,1 |
This means that:

- If both players cooperate (CC), they both get a score of 3.
- If player #1 defects, but player #2 cooperates (DC), then player #1 gets a score of 5, while player #2 gets 0.
- If player #1 cooperates, but player #2 defects (CD), then player #1 gets a score of 0, while player #2 gets 5.
- If both players defect (DD), then both players get a score of 1.

The scores are computed using the actual joint action of the two agents, even if the 5% noise leads one or both agents to get the wrong information about the other's action.

#### Planning

You will be modeling a game strategy using an automaton machine, following the description in Chapter 4. The difference is that your machines can specify a probability of action C in each state and need not just emit an action deterministically. Along with the probability of cooperating in a state, your machine will specify the transition to a new state, based on the observed joint action, which may have a mistaken observation of the other player's action, as described above. Of course, your observation of your own actions is always correct.

Here are a few examples that introduce how you'll specify your agents. The first is a simple automaton that has one state and thus always stays in it. This would look something like this:

0: 0.4 0 0 0 0

The first number represents the index of the current state, the second number the probability of cooperation in the state, and the last four numbers represent transitions to make in response to whether you and your opponent defect or cooperate (explained in more detail in the next section). In this case, there is only one state, so the transitions all have to remain in the same state, and the only interesting part of the design is the probability of cooperation, which is 0.4 in this case.

A slightly more complicated automaton might have two states with different cooperation probabilities and switch between them based on what the opponent does. It might look something like this:

0: 0.6 1 0 0 1

1: 0.8 1 0 0 1

There are two states (0 is always the initial state). When in state 0, the automaton will cooperate with probability 0.6. In two situations (if both players cooperated or both players defected -- explained in more detail below), it will move to state 1. In state 1, it will cooperate with probability 0.8 and return to state 0 if the players acted differently (one defected and one cooperated).

In this assignment, you can have between 1 and 5 states (where state 0 will always be the initial state, and the following states are numbered 1, 2, 3, and 4). Your goal is to define probabilities and transitions for each of the states in the format below. You need not use all five states.

#### Format

Each agent should have the following format. This agent is composed of three states, so it is written on three lines.  

0: 0.1 1 0 0 1

1: 0.7 1 1 0 2

2: 0.4 2 2 1 0

Your agent should have between 1 and 5 lines of text for five maximum states. Each line has format: state_id: prob_of_cooperate state_on_cc state_on_cd state_on_dc state_on_dd Where:

- *state_id* is the id of the state. These must be 0,1,2,3,4 in that order.

- *prob_of_cooperate* is the probability of cooperating when in this state (and thus, one minus this value is the probability of defecting).

- *state_on_cc* is the state to move to on information that both agents cooperated in this round.

- *state_on_cd* is the state to move to on information that your agent cooperated and the other agent defected in this round.

- *state_on_dc* is the state to move to on information that your agent defected, and the other agent cooperated in this round.

- *state_on_dd* is the state to move to on information that both agents defected in this round.

Remember that your automata gets noisy information about the play of the other agent. With probability 0.05, the transition will be based on wrong information about the other agent's action.

### Part 2: Analysis

Submit a writeup of your agent as a PDF file. The writeup should include the following answers:

1. **Automata Description:** Provide a diagram or a clear written description of your automaton. Include the cooperation probability for each state and the transition rules for all outcomes (CC, CD, DC, DD). Explain the specific purpose of each state (e.g., "State 0 is the initial cooperative state," "State 1 is for retaliation").
2. **Strategy Philosophy:** Describe the core philosophy of your agent. Is it aggressive, forgiving, or random? How does it attempt to maximize score in a noisy environment?
3. **Noise Resilience:** Explain specifically how your agent handles the 5% noise. If your agent accidentally defects (or perceives a defection that didn't happen), how does it recover cooperation? Or does it not care?
4. **Opponent Analysis:**
    - How does your agent fare against a pure "Always Defect" strategy? Does it get exploited, or does it protect itself?
    - How does it fare against "Tit-for-Tat" in a noisy environment?
5. **Self-Play:** What happens when your agent plays against itself? Do they cooperate effectively, or do they spiral into mutual defection due to noise?
6. **Tournament Prediction:** If the class consists mostly of "Tit-for-Tat" variants, how will your agent perform? What if the class is mostly "Always Defect"?
7. **Exploitation:** Design a theoretical 'Anti-MyAgent' that would perfectly exploit your strategy. What would it do?
8. **Parameter Tuning:** If you used probabilistic transitions (e.g., 0.8), how did you tune these numbers? What happens if you change them?

## Grading

For each prompt, you will get graded based on your explanation of your strategy on a scale of 0, 1, 2 -- where 0 is an unsatisfactory explanation, 1 is a weak explanation, and 2 is a well-written explanation.
We only expect a maximum of two paragraphs of explanation for each prompt and you can choose to plot the results of experiments to support your explanations (but that is not required).
There will be a small bonus for agents that perform well in the class tournament.

## Collaboration policy

While you are permitted to discuss your agent designs with each other as much as you like, you must submit your agent and explanation for that agent (submission instructions below).

## Instructions

### Prerequisites

- **Python 3.7 or higher** (check with `python3 --version`)
- Basic terminal/command line knowledge

### Installation

1. **Download the assignment files** to your computer
2. **Open a terminal** in the assignment folder
3. **Verify installation** by running a test game:
   ```bash
   python3 src/game_runner.py sample-agents/tit_for_tat.agent sample-agents/always_cooperate.agent 5
   ```

   You should see a 5-round game simulation with detailed output.
---

## Creating Your Agent

### File Format

Create your agent in a file named `STUDENT_ID.agent` (replace STUDENT_ID with your actual ID).

Each line defines a state:
```
state_id: prob_cooperate state_on_cc state_on_cd state_on_dc state_on_dd
```

**Rules:**
- States numbered 0, 1, 2, 3, 4 in order (0 is always the starting state)
- Probability between 0 and 1 (e.g., `0.5`, `0`, `1`)
- Transitions must reference valid state numbers
- Maximum 5 states (you can use fewer)
- Lines starting with `#` are comments (ignored)

### Example Agents

Study the sample agents in `sample-agents/`:

**Always cooperate:**
```
0: 1.0 0 0 0 0
```

**Always defect:**
```
0: 0.0 0 0 0 0
```

**Random (50/50):**
```
0: 0.5 0 0 0 0
```

**Tit-for-Tat:**
```
0: 1.0 0 1 0 1
1: 0.0 0 1 0 1
```

---

## Testing Your Agent

### Basic Test
```bash
python3 src/game_runner.py STUDENT_ID.agent sample-agents/tit_for_tat.agent 100
```

### Test Against Different Opponents
```bash
python3 src/game_runner.py STUDENT_ID.agent sample-agents/always_defect.agent 100
python3 src/game_runner.py STUDENT_ID.agent sample-agents/always_cooperate.agent 100
python3 src/game_runner.py STUDENT_ID.agent sample-agents/random.agent 100
```

### Understanding the Output

The game displays:
- **Round**: Current round number
- **P1 Move / P2 Move**: What each agent actually did (C=Cooperate, D=Defect)
- **P1 Obs / P2 Obs**: What each agent *observed* (may be wrong due to 5% noise!)
- **Payoff**: Points earned this round
- **Score**: Cumulative score
- **States**: Current state of each agent

---

## Common Errors & Solutions

### "Line does not have the right pattern"
- Make sure you have exactly 6 values per line (one state ID + five numbers)
- Check that probabilities are valid numbers between 0 and 1
- Ensure state transitions are integers

### "invalid jump from state X"
- You're trying to transition to a state that doesn't exist
- Example: If you only define states 0 and 1, you can only transition to 0 or 1

### "Was expecting state X. Saw Y"
- States must be defined in order starting from 0
- Don't skip state numbers (can't go 0, 2, 3 - must be 0, 1, 2)

### "Agent has too many states"
- Maximum 5 states allowed (0 through 4)

---

## Pre-submission Checklist

- [ ] My agent file is named `STUDENT_ID.agent`
- [ ] My agent has between 1 and 5 states
- [ ] I have tested my agent against the sample agents using `src/game_runner.py`
- [ ] I have created a PDF writeup explaining my strategy

## Submission

Submit your `STUDENT_ID.agent` file together with your writeup (as a PDF) into a zip file named `STUDENT_ID.zip`
