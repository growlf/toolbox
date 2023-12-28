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

    print("Try running `inv --help` for more information or `inv --list` to see a list of subcommands. ")
    print("Some additional commands that are also installed and might be of use:  whois, speedtest, mtr, tcpdump, nmap, nc")

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


@task(incrementable=['verbose'])
def dockerinfo(c, verbose=0):
    """Get Docker installation information
    """

    _set_log_level(verbose)

    logger.debug("Looking for Docker installation...")

    ####TODO: add try/except
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')

    info = client.info()
    client.close()

    print(f"{'Árchetecture':<20}: {info.get('Architecture')}")
    print(f"{'Containers':<20}: {info.get('Containers')}")
    print(f"{'Containers Running':<20}: {info.get('ContainersRunning')}")
    print(f"{'DockerRootDir':<20}: {info.get('DockerRootDir')}")
    print(f"{'HttpProxy':<20}: {info.get('HttpProxy')}")
    print(f"{'HttpsProxy':<20}: {info.get('HttpsProxy')}")
    print(f"{'Images':<20}: {info.get('Images')}")
    print(f"{'KernelVersion':<20}: {info.get('KernelVersion')}")
    print(f"{'LoggingDriver':<20}: {info.get('LoggingDriver')}")
    print(f"{'Name':<20}: {info.get('Name')}")
    print(f"{'NoProxy':<20}: {info.get('NoProxy')}")
    print(f"{'OSType':<20}: {info.get('OSType')}")
    print(f"{'OperatingSystem':<20}: {info.get('OperatingSystem')}")
    print(f"{'ServerVersion':<20}: {info.get('ServerVersion')}")
    print(f"{'SystemTime':<20}: {info.get('SystemTime')}")

    from pprint import pprint
    #pprint(client.df())


@task(incrementable=['verbose'])
def netspeed(c, verbose=0):
    """Run an internet speedtest
    """

    _set_log_level(verbose)

    logger.debug("Checking network speed...")

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
    print(f"{'PING':<20}: {int(s.results.ping)}ms")
    print(f"{'UPLOAD':<20}: {int(s.results.upload / 1024 / 1024)}Mbps")
    print(f"{'DOWNLOAD':<20}: {int(s.results.download / 1024 / 1024)}Mbps")
