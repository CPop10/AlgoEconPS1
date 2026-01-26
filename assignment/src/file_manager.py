#!/usr/bin/env python3
"""
CS 4501 - File Manager
======================

This module handles all file I/O operations:
- Loading agent files
- Saving results to CSV, TXT, and MD files

This module is independent and doesn't import tournament or agent modules.
"""

import os
import glob
import csv
from typing import List, Tuple, Dict, Any, Optional


def load_agent(filename: str) -> List[str]:
    """
    Load an agent definition from a file.
    
    Args:
        filename: Path to .agent file
    
    Returns:
        List of lines from the file
    
    Raises:
        FileNotFoundError: If file not found
    
    Examples:
        >>> # Assuming 'sample-agents/always_cooperate.agent' exists
        >>> lines = load_agent('sample-agents/always_cooperate.agent')
        >>> len(lines) > 0
        True
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines


def get_agent_files(folder_path: str) -> List[str]:
    """
    Get all .agent file paths from a folder.
    
    Args:
        folder_path: Path to folder containing .agent files
    
    Returns:
        List of absolute paths to .agent files
    
    Examples:
        >>> # Returns list of .agent files
        >>> files = get_agent_files("sample-agents")
        >>> all(f.endswith('.agent') for f in files)
        True
    """
    return glob.glob(os.path.join(folder_path, "*.agent"))


def get_agent_name_from_file(filepath: str) -> str:
    """
    Extract agent name from file path.
    
    Args:
        filepath: Path to .agent file
    
    Returns:
        Agent name (filename without .agent extension)
    
    Examples:
        >>> get_agent_name_from_file("path/to/my_agent.agent")
        'my_agent'
    """
    return os.path.basename(filepath)[:-6]  # Remove .agent extension


def save_csv_results(output_path: str, rankings: List[Tuple[str, float, str]]) -> None:
    """
    Save tournament results to CSV file.
    
    Args:
        output_path: Path to output CSV file
        rankings: List of (name, score, strategy_text) tuples
    
    Examples:
        >>> # Example usage
        >>> rankings = [("agent1", 3.5, "0: 1.0, 0, 0, 0, 0")]
        >>> save_csv_results("test.csv", rankings)
    """
    with open(output_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Name", "Score", "Strategy"])
        
        for name, score, strategy_text in rankings:
            csv_writer.writerow([name, f"{score:.4f}", strategy_text])


def save_text_results(output_path: str, content: str) -> None:
    """
    Save text content to file.
    
    Args:
        output_path: Path to output text file
        content: Text content to write
    """
    with open(output_path, 'w') as f:
        f.write(content)


def save_error_log(failed_agents: List[Tuple[str, str]], output_path: str) -> None:
    """
    Save error log to markdown file.
    
    Args:
        failed_agents: List of (agent_name, error_message) tuples
        output_path: Path to output markdown file
    """
    with open(output_path, 'w') as f:
        f.write("# Failed Agent Submissions\n\n")
        f.write("The following agents failed to load and were excluded from the tournament.\n\n")
        f.write("---\n\n")
        
        for agent_name, error in failed_agents:
            f.write(f"## `{agent_name}.agent`\n\n")
            f.write(f"**Error:** {error}\n\n")
            f.write("---\n\n")


def remove_error_log_if_exists(output_path: str) -> None:
    """Remove error log file if it exists from previous runs."""
    if os.path.exists(output_path):
        os.remove(output_path)


# Example usage
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
