from invoke import task
import subprocess
import os
import logging
import docker
import pyfiglet 
import urllib
import portscan


# Create a logger object 
logger = logging.getLogger(__name__)
def _set_log_level(verbose=0) -> None:
    """Set the logging level

    Args:
        verbose (int, optional): verbosity level [0-4]. Defaults to 0.
    """

    log_levels = ["CRITICAL", "ERROR",  "WARNING", "INFO", "DEBUG"]

    # Ensure verbosity stays within the tollerances
    verbose = 4 if verbose > 4 else verbose

    # Actually set the logging level
    logging.basicConfig(level=log_levels[verbose])
 

@task(
    default=True, 
    incrementable=["verbose"]
    )
def help(c, verbose=0):
    """Shows the help screen.

    Args:
        c (_type_): _description_
        verbose (int, optional): _description_. Defaults to 0.
    """
    _set_log_level(verbose)

    ascii_banner = pyfiglet.figlet_format("Tool Box")
    print(ascii_banner)

    print("Try running `inv --help` for more information or `inv --list` to see a list of subcommands.")


@task(
    help={'name': "Name of the person to say hi to.",
          'verbose': "Logging and verbosity level"
          }, 
    optional=['name'],
    incrementable=['verbose']
    )
def hello(c, name="world", verbose=0):
    """Say hello
    
    Args:
        c (_type_): _description_
        name (str, optional): _description_. Defaults to "world".
        verbose (int, optional): _description_. Defaults to 0.
    """
    _set_log_level(verbose)
    logger.debug("Set loglevel.")

    print("Hello {}!".format(name))
    logger.debug("Said hello.")


@task(
    help={'host': "Host to test against"},
    incrementable=['verbose']
    )
def ping(c, host, verbose=0):
    """Ping a remote systems

    Args:
        c (_type_): _description_
        host (_type_): address to ping
        verbose (int, optional): logging and response level. Defaults to 0.
    """

    _set_log_level(verbose)

    try:
        output = subprocess.check_output(['ping', '-c', '1', host])
        logger.debug("PING checked Google")
    except subprocess.CalledProcessError:
        logger.info("Ping command failed")




