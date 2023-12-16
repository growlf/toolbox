from invoke import task
import logging
import docker
import pyfiglet 
import speedtest



###########################################
# Library functions

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
    
    

###########################################
# Tasks

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
    incrementable=['verbose']
    )
def netspeed(c, verbose=0):
    """Run an internet speedtest
    """

    _set_log_level(verbose)

    servers = []
    # If you want to test against a specific server
    # servers = [1234]

    threads = None
    # If you want to use a single threaded test
    # threads = 1

    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.get_best_server()
    s.download(threads=threads)
    s.upload(threads=threads)

    results_dict = s.results.dict()
    
    logger.debug(results_dict)
    logger.debug(s.results.server)
    logger.info(f"PING: {int(s.results.ping)}ms")
    logger.info(f"UPLOAD: {int(s.results.upload / 1024 / 1024)}Mbps")
    logger.info(f"DOWNLOAD: {int(s.results.download / 1024 / 1024)}Mbps")
    