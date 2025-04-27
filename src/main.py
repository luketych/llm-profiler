#!/usr/bin/env python3

import os
import logging
import click
from git import Repo
from pathlib import Path
from dotenv import load_dotenv

from . import config

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT,
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def clone_repo(url: str, target_dir: str) -> Repo:
    """
    Clone a repository to the target directory.
    
    Args:
        url (str): Repository URL
        target_dir (str): Target directory path
        
    Returns:
        Repo: GitPython Repo object
    """
    try:
        logger.info(f"Cloning repository: {url}")
        repo = Repo.clone_from(url, target_dir)
        click.echo(f"Successfully cloned repository to {target_dir}")
        return repo
    except Exception as e:
        error_msg = f"Failed to clone repository: {str(e)}"
        logger.error(error_msg)
        click.echo(f"Error: {error_msg}", err=True)
        raise

@click.command()
@click.argument('repo_url', required=True)
@click.option('--target-dir', default=str(config.WORKSPACE_DIR), help='Target directory for cloning')
def main(repo_url: str, target_dir: str):
    """
    Semi-Automated Profiler and Logger Insertion Tool
    
    Arguments:
        REPO_URL    URL of the repository to clone
    """
    try:
        # Create target directory if it doesn't exist
        Path(target_dir).mkdir(parents=True, exist_ok=True)
        
        # Clone repository
        repo = clone_repo(repo_url, target_dir)
        
        logger.info("Initial setup completed successfully")
        click.echo("Initial setup completed successfully")
        
    except Exception as e:
        error_msg = f"Error during execution: {str(e)}"
        logger.error(error_msg)
        click.echo(f"Error: {error_msg}", err=True)
        raise

if __name__ == '__main__':
    main() 