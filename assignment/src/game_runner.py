#!/usr/bin/env python3
"""
CS 4501 - Prisoner's Dilemma Game Runner
=========================================

This module provides a command-line interface for running iterated
Prisoner's Dilemma games between FSA-based agents.

Game Rules:
-----------
- Two players repeatedly play Prisoner's Dilemma
- Each player is represented by a finite state machine (FSA)
- Payoff matrix: CC=(3,3), CD=(0,5), DC=(5,0), DD=(1,1)
- 5% chance of noise (action flips) on each move
- Maximum of 5 states per agent

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

Usage:
------
As a standalone script:
    python3 game_runner.py <agent1_file> <agent2_file> [number_of_rounds]

As a module (imported by tournament.py):
    from game_runner import Agent, Game, load_agent
    
    lines = load_agent("agent.agent")
    agent1 = Agent(1, lines, name="Agent1")
    agent2 = Agent(2, lines, name="Agent2")
    game = Game(agent1, agent2, num_rounds=100)
    score1, score2 = game.run()

Examples:
---------
    # Run game between two agents for 20 rounds (default)
    python3 game_runner.py answer.agent opponent.agent
    
    # Run game for 100 rounds
    python3 game_runner.py answer.agent opponent.agent 100
    
    # Run agent against itself
    python3 game_runner.py answer.agent answer.agent 50

Module Structure:
-----------------
This module now imports from:
    - state.py: State class for FSA states
    - agent.py: Agent class (FSA-based player) and load_agent function
    - game.py: Game class for running matches

For backward compatibility, we re-export commonly used items:
    - Agent (formerly Player)
    - Game (new class-based interface)
    - run_game (compatibility function)
    - load_agent (file loading)
"""

import sys
from agent import Agent
from game import Game, run_game

# Note: load_agent imported from file_manager when needed to avoid circular imports


# ============================================================================
# COMMAND-LINE INTERFACE
# ============================================================================

def main():
    """Main entry point for command-line usage."""
    # Import here to avoid circular dependency
    from file_manager import load_agent
    
    # Parse command line arguments
    if len(sys.argv) < 3:
        print("Usage: python3 game_runner.py <agent1_file> <agent2_file> [number_of_rounds]")
        print("\nExamples:")
        print("  python3 game_runner.py answer.agent opponent.agent")
        print("  python3 game_runner.py answer.agent opponent.agent 100")
        sys.exit(1)
    
    agent1_file = sys.argv[1]
    agent2_file = sys.argv[2]
    num_rounds = 20  # Default
    
    if len(sys.argv) > 3:
        try:
            num_rounds = int(sys.argv[3])
        except ValueError:
            print("Error: number of rounds must be an integer")
            sys.exit(1)
    
    # Load agents
    print(f"Loading Agent 1 from '{agent1_file}'...")
    try:
        agent1_lines = load_agent(agent1_file)
    except FileNotFoundError:
        print(f"Error: Could not find file '{agent1_file}'")
        print(f"\nPlease create a file called '{agent1_file}' with your agent definition.")
        print("\nExample agent format:")
        print("0: 0.5 0 0 0 0")
        print("\nThis is a simple agent with one state that cooperates 50% of the time.")
        print("\nMake sure your file has the .agent extension!")
        sys.exit(1)
    
    print(f"Loading Agent 2 from '{agent2_file}'...")
    try:
        agent2_lines = load_agent(agent2_file)
    except FileNotFoundError:
        print(f"Error: Could not find file '{agent2_file}'")
        sys.exit(1)
    
    # Create agents
    try:
        agent1 = Agent(1, agent1_lines, name=agent1_file)
        agent2 = Agent(2, agent2_lines, name=agent2_file)
        print("✓ Both agents loaded successfully!")
    except Exception as e:
        print(f"\n❌ Error loading agent: {e}")
        sys.exit(1)
    
    # Run the game
    game = Game(agent1, agent2, num_rounds)
    game.run()


if __name__ == "__main__":
    main()
