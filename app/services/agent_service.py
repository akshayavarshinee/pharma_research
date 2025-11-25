"""
Agent service layer for integrating CrewAI pharmaceutical research agents.
"""
import sys
import os
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class AgentExecutionError(Exception):
    """Custom exception for agent execution failures."""
    pass

def get_agents_path():
    """Get the path to the agents module."""
    # Get the project root (parent of app directory)
    current_dir = Path(__file__).resolve()
    project_root = current_dir.parent.parent.parent
    agents_src_path = project_root / "agents" / "src"
    
    # Add agents path to Python path if not already there
    agents_src_str = str(agents_src_path)
    if agents_src_str not in sys.path:
        sys.path.insert(0, agents_src_str)
    
    return agents_src_path

def run_pharma_research(query: str, user_id: int) -> tuple[str, str]:
    """
    Execute the CrewAI pharmaceutical research agents with the given query.
    
    Args:
        query: The research question from the user
        user_id: The ID of the user making the request
        
    Returns:
        tuple: (title, report_text) - The generated report title and content
        
    Raises:
        AgentExecutionError: If agent execution fails
    """
    logger.info(f"Starting pharma research for user {user_id}: {query[:100]}...")
    
    try:
        # Ensure agents module is in path
        get_agents_path()
        
        # Import CrewAI components
        from pharma_researcher.crew import PharmaResearcher
        
        # Prepare inputs for the crew
        inputs = {
            'query': query,
            'current_year': str(datetime.now().year)
        }
        
        logger.info("Initializing PharmaResearcher crew...")
        crew_instance = PharmaResearcher()
        
        logger.info("Executing crew with query...")
        result = crew_instance.crew().kickoff(inputs=inputs)
        
        # Extract the report content
        if hasattr(result, 'raw'):
            report_text = result.raw
        elif isinstance(result, str):
            report_text = result
        else:
            report_text = str(result)
        
        # Generate title from query
        title = generate_title_from_query(query)
        
        logger.info(f"Research completed successfully. Report length: {len(report_text)} characters")
        
        return title, report_text
        
    except ImportError as e:
        logger.error(f"Failed to import pharma_researcher module: {e}")
        raise AgentExecutionError(
            f"Agent module not found. Please ensure the agents package is properly installed. Error: {e}"
        )
    except Exception as e:
        logger.error(f"Agent execution failed: {e}", exc_info=True)
        raise AgentExecutionError(f"Failed to execute research agents: {str(e)}")

def generate_title_from_query(query: str, max_length: int = 100) -> str:
    """
    Generate a report title from the user's query.
    
    Args:
        query: The user's research question
        max_length: Maximum length of the title
        
    Returns:
        str: A formatted title
    """
    # Clean up the query
    title = query.strip()
    
    # Add prefix if not already a question
    if not title.endswith('?'):
        title = f"Research Report: {title}"
    else:
        title = f"Analysis: {title}"
    
    # Truncate if too long
    if len(title) > max_length:
        title = title[:max_length - 3] + "..."
    
    return title

def validate_query(query: str) -> bool:
    """
    Validate that the query is suitable for agent processing.
    
    Args:
        query: The user's research question
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not query or not query.strip():
        return False
    
    # Minimum length check
    if len(query.strip()) < 10:
        return False
    
    # Maximum length check (to prevent abuse)
    if len(query) > 1000:
        return False
    
    return True
