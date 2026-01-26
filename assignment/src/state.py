#!/usr/bin/env python3
"""
State Module - Finite State Automaton State
============================================

This module defines the State class used in FSA-based agents for the
Prisoner's Dilemma game.

A State represents a single node in a finite state automaton, defining:
- The probability of cooperation in this state
- Transitions to other states based on game outcomes
"""

from typing import Optional

# Game outcome constants
CC = 0  # Both cooperate
CD = 1  # Self cooperates, opponent defects
DC = 2  # Self defects, opponent cooperates
DD = 3  # Both defect


class State:
    """
    Represents a single state in a finite state automaton agent.
    
    Each state defines:
    - Probability of cooperation
    - Transition rules for all four possible outcomes (CC, CD, DC, DD)
    
    Attributes:
        num: State number (0 to MAX_STATES-1)
        prob_coop: Probability of cooperating in this state [0.0, 1.0]
        on_cc: Next state if both players cooperate
        on_cd: Next state if self cooperates, opponent defects
        on_dc: Next state if self defects, opponent cooperates
        on_dd: Next state if both players defect
    
    Examples:
        >>> # Always cooperate state
        >>> s = State(0, 1.0, 0, 0, 0, 0)
        >>> s.prob_coop
        1.0
        >>> s.check(1)  # Validate transitions for 1-state agent
    """
    
    def __init__(self, num: int, prob_coop: float, on_cc: int, on_cd: int, 
                 on_dc: int, on_dd: int):
        """
        Initialize a state.
        
        Args:
            num: State number
            prob_coop: Probability of cooperation [0.0, 1.0]
            on_cc: Next state on mutual cooperation
            on_cd: Next state on unilateral cooperation
            on_dc: Next state on unilateral defection
            on_dd: Next state on mutual defection
        
        Raises:
            Exception: If prob_coop is not in [0, 1]
        """
        self.num = num
        if prob_coop < 0.0 or prob_coop > 1.000001:
            raise Exception("prob_coop %f for state %d must be in [0,1]" % (
                prob_coop, num))
        self.prob_coop = prob_coop
        self.on_cc = on_cc
        self.on_cd = on_cd
        self.on_dc = on_dc
        self.on_dd = on_dd
        
    def check(self, n: int) -> None:
        """
        Validate that all state transitions are valid.
        
        Args:
            n: Total number of states in the agent
        
        Raises:
            Exception: If any transition points to invalid state
        
        Examples:
            >>> s = State(0, 1.0, 0, 0, 0, 0)
            >>> s.check(1)  # Valid - all transitions to state 0
            >>> s2 = State(0, 1.0, 2, 0, 0, 0)
            >>> s2.check(1)  # Raises - transition to non-existent state 2
            Traceback (most recent call last):
                ...
            Exception: invalid jump from state 0 on on_cc: 2
        """
        if self.num >= n:
            raise Exception("invalid state number %d" % self.num)
        if self.on_cc >= n:
            raise Exception("invalid jump from state %d on on_cc: %d" % (
                self.num, self.on_cc))
        if self.on_cd >= n:
            raise Exception("invalid jump from state %d on on_cd: %d" % (
                self.num, self.on_cd))
        if self.on_dc >= n:
            raise Exception("invalid jump from state %d on on_dc: %d" % (
                self.num, self.on_dc))
        if self.on_dd >= n:
            raise Exception("invalid jump from state %d on on_dd: %d" % (
                self.num, self.on_dd))

    def __repr__(self) -> str:
        """String representation of the state for debugging."""
        return "State(id=%d, prob_c=%0.2f, on_cc=%d, on_cd=%d, on_dc=%d, on_dd=%d)" % (
            self.num, self.prob_coop, self.on_cc, self.on_cd, self.on_dc, self.on_dd)
