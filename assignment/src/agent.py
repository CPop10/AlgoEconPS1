#!/usr/bin/env python3
"""
Agent Module - Finite State Automaton Agent
============================================

This module defines the Agent class used to represent players in the
Prisoner's Dilemma game. Each agent is a finite state automaton that
decides whether to cooperate or defect based on its current state.

Agent File Format:
------------------
Each line represents a state in the FSA:
    state_num: prob_coop on_cc on_cd on_dc on_dd

Where:
    - state_num: State number (0 to 4)
    - prob_coop: Probability of cooperating (0.0 to 1.0)
    - on_cc: Next state if both cooperate
    - on_cd: Next state if self cooperates, opponent defects
    - on_dc: Next state if self defects, opponent cooperates
    - on_dd: Next state if both defect

Example Agent (Tit-for-Tat):
    0: 1.0 0 1 0 1
    1: 0.0 0 1 0 1
"""

import random
import re
from typing import List, Optional
from state import State, CC, CD, DC, DD

# Maximum number of states per agent
MAX_STATES = 5


class Agent:
    """
    Represents an agent in the Prisoner's Dilemma game.
    
    An agent is a finite state automaton with:
    - A collection of states
    - A current state (starting at 0)
    - Logic for deciding whether to cooperate and transitioning states
    
    Attributes:
        id: Agent identifier (typically 1 or 2)
        current_state: Index of current state
        states: List of State objects defining the FSA
        name: Optional name for the agent (e.g., filename)
    
    Examples:
        >>> # Create a simple always-cooperate agent
        >>> lines = ["0: 1.0 0 0 0 0"]
        >>> agent = Agent(1, lines)
        >>> agent.states[0].prob_coop
        1.0
        >>> agent.current_state
        0
    """
    
    def __init__(self, agent_id: int, lines: List[str], name: Optional[str] = None):
        """
        Initialize an agent from strategy lines.
        
        Args:
            agent_id: Agent identifier (typically 1 or 2)
            lines: List of state definition strings
            name: Optional name for the agent
        
        Raises:
            Exception: If agent format is invalid
        
        Examples:
            >>> agent = Agent(1, ["0: 1.0 0 0 0 0", "1: 0.5 1 0 1 0"])
            >>> len(agent.states)
            2
        """
        self.id = agent_id
        self.name = name
        self.current_state = 0
        self.states = []
        
        # Accept both integer and decimal probability formats
        pattern = r"^\d:\s+([01](\.\d+)?|0?\.\d+)(\s+\d){4}"
        
        k = 0  # Which state we're expecting to see next
        for line in lines:
            line = line.strip()
            if len(line) == 0 or line[0] == '#':
                continue  # skip empty lines and comments
            if not re.match(pattern, line):
                raise Exception("Line does not have the right pattern: '%s'" % line)
            (num, prob, on1, on2, on3, on4) = line.split()
            num = int(num[:-1])  # pull off the ':'
            if k != num:
                raise Exception("Was expecting state %d. Saw %d" % (k, num))
            k += 1
            prob = float(prob)
            on_cc = int(on1)
            on_cd = int(on2)
            on_dc = int(on3)
            on_dd = int(on4)
            state = State(num, prob, on_cc, on_cd, on_dc, on_dd)
            self.states.append(state)
        
        # Validate the agent's FSA
        self._validate()
    
    def _validate(self) -> None:
        """
        Validate the agent's FSA structure.
        
        Checks:
        - Agent has at least one state
        - Agent doesn't exceed MAX_STATES
        - All state transitions are valid
        
        Raises:
            Exception: If validation fails
        """
        n = len(self.states)
        
        # Check state count
        if n == 0:
            raise Exception("Agent %d has no states" % self.id)
        if n > MAX_STATES:
            raise Exception("Agent %d has too many states: %d" % (self.id, n))
        
        # Validate each state's transitions
        for state in self.states:
            state.check(n)
    
    def reset(self) -> None:
        """
        Reset agent to initial state.
        
        Examples:
            >>> agent = Agent(1, ["0: 1.0 0 1 0 1", "1: 0.5 1 0 1 0"])
            >>> agent.current_state = 1
            >>> agent.reset()
            >>> agent.current_state
            0
        """
        self.current_state = 0
    
    def move(self) -> bool:
        """
        Decide whether to cooperate based on current state.
        
        Returns:
            True if cooperating, False if defecting
        
        Examples:
            >>> random.seed(42)
            >>> agent = Agent(1, ["0: 1.0 0 0 0 0"])  # Always cooperate
            >>> agent.move()
            True
            >>> agent2 = Agent(2, ["0: 0.0 0 0 0 0"])  # Always defect
            >>> agent2.move()
            False
        """
        if random.random() < self.states[self.current_state].prob_coop:
            return True  # Cooperate
        else:
            return False  # Defect
    
    def update(self, my_move: bool, opp_move: bool) -> None:
        """
        Update current state based on the outcome of moves.
        
        Args:
            my_move: True if self cooperated, False if defected
            opp_move: True if opponent cooperated, False if defected
        
        Examples:
            >>> agent = Agent(1, ["0: 1.0 0 1 1 1", "1: 0.5 1 0 1 0"])
            >>> agent.current_state
            0
            >>> agent.update(True, False)  # I cooperated, opponent defected (CD)
            >>> agent.current_state
            1
        """
        if my_move and opp_move:
            action = CC
        elif my_move and not opp_move:
            action = CD
        elif not my_move and opp_move:
            action = DC
        else:
            action = DD
        
        # Transition to next state
        if action == CC:
            self.current_state = self.states[self.current_state].on_cc
        elif action == CD:
            self.current_state = self.states[self.current_state].on_cd
        elif action == DC:
            self.current_state = self.states[self.current_state].on_dc
        else:  # DD
            self.current_state = self.states[self.current_state].on_dd
    
    def __repr__(self) -> str:
        """String representation of the agent for debugging."""
        name_str = f" '{self.name}'" if self.name else ""
        return f"Agent(id={self.id}{name_str}, states={len(self.states)}, current_state={self.current_state})"
