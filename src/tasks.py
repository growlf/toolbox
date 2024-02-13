from invoke import task
import invoke
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


@task(incrementable=['verbose'])
def dockerinfo(c, verbose=0):
    """Get Docker installation information
    """

    _set_log_level(verbose)

    logger.debug("Looking for Docker installation...")

    try:
        client = docker.from_env()        
    except Exception as e:
        raise invoke.Exit("ERROR: Docker connection failed.", e)
    info = client.info()
    plugins = client.plugins.list()
    client.close()

    print('-'*40)
    print(f"{'System Name':<20}: {info.get('Name')}")
    print(f"{'Árchetecture':<20}: {info.get('Architecture')}")
    print(f"{'OSType':<20}: {info.get('OSType')}")
    print(f"{'Kernel Version':<20}: {info.get('KernelVersion')}")
    print(f"{'Operating System':<20}: {info.get('OperatingSystem')}")
    print(f"{'System Time':<20}: {info.get('SystemTime')}")

    print('-'*40)
    print(f"{'Docker Version':<20}: {info.get('ServerVersion')}")
    print(f"{'Docker Root':<20}: {info.get('DockerRootDir')}")
    print(f"{'Logging Driver':<20}: {info.get('LoggingDriver')}")
    print(f"{'Images':<20}: {info.get('Images')}")
    print(f"{'Containers':<20}: {info.get('Containers')}")
    print(f"{'Containers Running':<20}: {info.get('ContainersRunning')}")
    loki = next((x for x in plugins if x.name == 'loki:latest'), None)
    if loki:
        print(f"{'Loki':<20}: {loki.name}")
        print(f"{' ':<20}: {'enabled' if loki.enabled else 'disabled'}")
        for setting in loki.settings:
            print(f"{' ':<20}: {setting}:{loki.settings.get(setting)}")
    else:
        print(f"{'Loki':<20}: {'Loki not found'}")        

    print('-'*40)
    print(f"{'HttpProxy':<20}: {info.get('HttpProxy')}")
    print(f"{'HttpsProxy':<20}: {info.get('HttpsProxy')}")
    print(f"{'NoProxy':<20}: {info.get('NoProxy')}")
    print('-'*40)

    #from pprint import pprint
    #pprint(ddf['Volumes'])

####TODO: check outbound connections
    print(f"{'verify correct time':<20}: {'TBD'}")        
####TODO: add task to check remaining disk size on host system
    print(f"{'Drive space':<20}: {'TBD'}")        
####TODO: check outbound connections
    print(f"{'Firewall':<20}: {'TBD'}")        
    #declare -a urls=("https://www.google.com 200"
    # "https://arch.archfx.io/api/v1/server/ 200"
    # "https://portainer.overseer.archfx.io 200"
    # "https://portaineredge.overseer.archfx.io 404"
    # "https://ecr.archfx.io 401"
####TODO: get docker-compose version
    
@task(incrementable=['verbose'])
def dockertest(c, verbose=0):
    """Test Docker installation
    """

    _set_log_level(verbose)

    logger.debug("Testing Docker installation...")

    try:
        client = docker.from_env()        
    except Exception as e:
        raise invoke.Exit("ERROR: Docker connection failed.", e)
    info = client.info()
    plugins = client.plugins.list()
    print(client.containers.run('netyeti/toolbox:latest', 'echo hello world'))
    client.images.pull("netyeti/toolbox:latest")

    from pprint import pprint
    pprint(client.swarm.attrs)

    client.close()
