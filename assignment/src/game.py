#!/usr/bin/env python3
"""
Game Module - Iterated Prisoner's Dilemma Game Engine
======================================================

This module defines the Game class for running iterated Prisoner's Dilemma
games between two FSA-based agents.

Game Rules:
-----------
- Two players repeatedly play Prisoner's Dilemma
- Each player is represented by a finite state machine (FSA)
- Payoff matrix: CC=(3,3), CD=(0,5), DC=(5,0), DD=(1,1)
- 5% chance of noise (action flips) on each move
"""

import random
from typing import Tuple, Optional
from agent import Agent

# Game constants
ERROR_PROB = 0.05  # 5% chance of action flip (noise)


class Game:
    """
    Manages an iterated Prisoner's Dilemma game between two agents.
    
    Attributes:
        agent1: First agent
        agent2: Second agent
        num_rounds: Number of rounds to play
        verbose: Whether to print detailed output
        score1: Current score for agent 1
        score2: Current score for agent 2
    
    Examples:
        >>> from agent import Agent
        >>> agent1 = Agent(1, ["0: 1.0 0 0 0 0"])  # Always cooperate
        >>> agent2 = Agent(2, ["0: 0.0 0 0 0 0"])  # Always defect
        >>> game = Game(agent1, agent2, num_rounds=10, verbose=False)
        >>> score1, score2 = game.run()
        >>> score1 < score2  # Defector beats cooperator
        True
    """
    
    def __init__(self, agent1: Agent, agent2: Agent, num_rounds: int = 20, 
                 verbose: bool = True):
        """
        Initialize a game.
        
        Args:
            agent1: First agent
            agent2: Second agent
            num_rounds: Number of rounds to play (default: 20)
            verbose: Whether to print detailed output (default: True)
        """
        self.agent1 = agent1
        self.agent2 = agent2
        self.num_rounds = num_rounds
        self.verbose = verbose
        self.score1 = 0
        self.score2 = 0
    
    def reset(self) -> None:
        """
        Reset the game state.
        
        Resets both agents to their initial states and clears scores.
        """
        self.agent1.reset()
        self.agent2.reset()
        self.score1 = 0
        self.score2 = 0
    
    @staticmethod
    def add_noise(move: bool) -> bool:
        """
        Add noise to a move with ERROR_PROB probability.
        
        Simulates observation error - with 5% probability, the observed
        move is flipped from what was actually played.
        
        Args:
            move: The actual move (True=cooperate, False=defect)
        
        Returns:
            The observed move (possibly flipped)
        
        Examples:
            >>> random.seed(42)
            >>> Game.add_noise(True)  # Usually returns True
            True
            >>> Game.add_noise(False)  # Usually returns False
            False
        """
        if random.random() < ERROR_PROB:
            return not move
        return move
    
    @staticmethod
    def get_payoff(move1: bool, move2: bool) -> Tuple[int, int]:
        """
        Calculate payoffs for both players based on their moves.
        
        Payoff matrix:
            CC (both cooperate): (3, 3)
            CD (p1 cooperates, p2 defects): (0, 5)
            DC (p1 defects, p2 cooperates): (5, 0)
            DD (both defect): (1, 1)
        
        Args:
            move1: Agent 1's move (True=cooperate, False=defect)
            move2: Agent 2's move (True=cooperate, False=defect)
        
        Returns:
            Tuple of (agent1_payoff, agent2_payoff)
        
        Examples:
            >>> Game.get_payoff(True, True)   # Both cooperate
            (3, 3)
            >>> Game.get_payoff(True, False)  # A1 cooperates, A2 defects
            (0, 5)
            >>> Game.get_payoff(False, True)  # A1 defects, A2 cooperates
            (5, 0)
            >>> Game.get_payoff(False, False) # Both defect
            (1, 1)
        """
        if move1 and move2:  # CC
            return (3, 3)
        elif move1 and not move2:  # CD
            return (0, 5)
        elif not move1 and move2:  # DC
            return (5, 0)
        else:  # DD
            return (1, 1)
    
    @staticmethod
    def move_to_string(move: bool) -> str:
        """
        Convert a move to string representation.
        
        Args:
            move: True for cooperate, False for defect
        
        Returns:
            'C' for cooperate, 'D' for defect
        
        Examples:
            >>> Game.move_to_string(True)
            'C'
            >>> Game.move_to_string(False)
            'D'
        """
        return "C" if move else "D"
    
    def run(self) -> Tuple[int, int]:
        """
        Run the game for the specified number of rounds.
        
        Returns:
            Tuple of (agent1_total_score, agent2_total_score)
        
        Examples:
            >>> random.seed(42)
            >>> from agent import Agent
            >>> a1 = Agent(1, ["0: 1.0 0 0 0 0"])  # Always cooperate
            >>> a2 = Agent(2, ["0: 0.0 0 0 0 0"])  # Always defect
            >>> game = Game(a1, a2, 10, verbose=False)
            >>> score1, score2 = game.run()
            >>> score1 < score2  # Defector beats cooperator
            True
        """
        self.reset()
        
        if self.verbose:
            self._print_header()
        
        for round_num in range(self.num_rounds):
            # Get moves
            move1 = self.agent1.move()
            move2 = self.agent2.move()
            
            # Add noise to observations
            obs1 = self.add_noise(move2)  # Agent 1 observes Agent 2's move (with noise)
            obs2 = self.add_noise(move1)  # Agent 2 observes Agent 1's move (with noise)
            
            # Calculate payoffs based on ACTUAL moves
            pay1, pay2 = self.get_payoff(move1, move2)
            self.score1 += pay1
            self.score2 += pay2
            
            if self.verbose:
                self._print_round(round_num + 1, move1, move2, obs1, obs2, pay1, pay2)
            
            # Update states based on OBSERVED moves
            self.agent1.update(move1, obs1)
            self.agent2.update(move2, obs2)
        
        if self.verbose:
            self._print_footer()
        
        return self.score1, self.score2
    
    def _print_header(self) -> None:
        """Print game header."""
        print("\n" + "="*70)
        print(f"Starting game: {self.num_rounds} rounds")
        if self.agent1.name:
            print(f"Agent 1: {self.agent1.name}")
        if self.agent2.name:
            print(f"Agent 2: {self.agent2.name}")
        print("="*70)
        print(f"{'Round':<6} {'A1 Move':<8} {'A2 Move':<8} {'A1 Obs':<7} "
              f"{'A2 Obs':<7} {'Payoff':<12} {'Score':<12} {'States':<10}")
        print("-"*70)
    
    def _print_round(self, round_num: int, move1: bool, move2: bool, 
                     obs1: bool, obs2: bool, pay1: int, pay2: int) -> None:
        """Print information for a single round."""
        print(f"{round_num:<6} {self.move_to_string(move1):<8} "
              f"{self.move_to_string(move2):<8} "
              f"{self.move_to_string(obs1):<7} {self.move_to_string(obs2):<7} "
              f"({pay1},{pay2}){'':<7} ({self.score1},{self.score2}){'':<6} "
              f"({self.agent1.current_state},{self.agent2.current_state})")
    
    def _print_footer(self) -> None:
        """Print game footer with final results."""
        print("="*70)
        print(f"Final Score: Agent 1 = {self.score1}, Agent 2 = {self.score2}")
        print("="*70)


# Compatibility function for backward compatibility
def run_game(player1: Agent, player2: Agent, num_rounds: int, 
             verbose: bool = True) -> Tuple[int, int]:
    """
    Run an iterated Prisoner's Dilemma game between two agents.
    
    This is a compatibility function that creates a Game instance and runs it.
    For new code, prefer using the Game class directly.
    
    Args:
        player1: First agent
        player2: Second agent
        num_rounds: Number of rounds to play
        verbose: If True, print each round's outcome
    
    Returns:
        Tuple of (agent1_total_score, agent2_total_score)
    
    Examples:
        >>> random.seed(42)
        >>> from agent import Agent
        >>> p1 = Agent(1, ["0: 1.0 0 0 0 0"])  # Always cooperate
        >>> p2 = Agent(2, ["0: 0.0 0 0 0 0"])  # Always defect
        >>> score1, score2 = run_game(p1, p2, 10, verbose=False)
        >>> score1 < score2  # Defector beats cooperator
        True
    """
    game = Game(player1, player2, num_rounds, verbose)
    return game.run()
