#!/usr/bin/env bash
#set -e

DEBUG=${DEBUG:=false}
if $DEBUG; then
    echo "Debug on, all commands will be displayed"
    set -x
fi

# Archfx Broker for linux installation script
#
# See ... for the installation steps
#
# This script is meant for quick and easy setup of your Broker environment via:
#   $ curl -fsSL https://private-sw-downloads.s3.amazonaws.com/archfx_broker/preflight/broker_preflight.sh -o broker_preflight.sh && chmod +x broker_preflight.sh
#   $ ./broker_preflight.sh check
#   $ ./broker_preflight.sh report
#

# Variables
readonly ME=$(basename "$0")

readonly BASE_DIR=${BASE_DIR:-'/opt'}
readonly INST_DIR=${INST_DIR:-$BASE_DIR/archfx}
readonly DEPLOY_DIR=$INST_DIR/broker
readonly DOCKER_CFG_DIR=/etc/docker
OFFLINE=${OFFLINE:=false}


#######################################
#   Output CMDs
#######################################
function _banner_msg () {
    echo -e "\n$(date "+%Y-%m-%d %H:%M:%S") - $@"
}
function _success_msg () {
    echo -e "$(date "+%Y-%m-%d %H:%M:%S") - $@"
}
function _failure_msg () {
    echo -e "$(date "+%Y-%m-%d %H:%M:%S") - FAILURE: $@"
    exit 1
}
function _warning_msg () {
    echo "$(date "+%Y-%m-%d %H:%M:%S") - WARNING: $@"
}
function _done_msg () {
    echo "DONE: $@"
}



#######################################
#   DOCKER COMMANDS
#######################################
function _where_is_docker() {
    ### Get docker insallation location ###
    echo $( which docker )
}


function _docker_root_dir() {
    ### Get docker root dir ###
    root_dir=$(docker info | grep 'Docker Root Dir:' | cut -d " " -f5)
    echo $root_dir
}


function _is_docker_running() {
    echo $(docker --version)
}


function _is_loki_plugin_installed() {
    echo $(docker plugin ls | grep loki)    
}


#######################################
#   Inspect OS
#######################################
function _get_distribution() {
    ### Save distro to logfile ###
	local lsb_dist=""
	# Every system that we officially support has /etc/os-release
	if [ -r /etc/os-release ]; then
		lsb_dist="$(. /etc/os-release && echo "$ID")"
	fi
	echo "$lsb_dist"
}


function _get_distro_version() {
    ### Save distro version ###
	local lsb_dist_id=""
	# Every system that we officially support has /etc/os-release
	if [ -r /etc/os-release ]; then
		lsb_dist_id="$(. /etc/os-release && echo "$VERSION_ID")"
	fi
	echo "$lsb_dist_id"
}


function _get_dir_size() {
    ### Save distro to logfile ###
    dir=$1
    local directory_size=$(df ${dir} | awk 'NR==2 {print $4}')
    echo $directory_size
}


####################
# Other
####################
function _outbound_connections() {
    ### Check if we can get info from the server ###
    url=$1
    expected=$2
    if $OFFLINE;then
        echo -e "no"
    else
        response=$(curl -L -s -o /dev/null -w "%{http_code}" $url)
        if (( $response == $expected )); then
            connect="yes"
        else
            connect="no (response code: $response)"
        fi
    fi
    echo $connect
}


#######################################
#   Verifiy basic requirements
#######################################
function preflight_checks() {
    ### Checks to see everything is as we want
    # Arguments:
    #   log_file = where to save the data
    #
    # Output:
    #   logs_${EPOCH}.txt = formatted output
    ###
    _banner_msg "Running pre-flight checks"
    
    local -ir minute=$(date -u +%s)
    local log_file="$PWD/logs_$minute.txt"
    _success_msg "\tGenerating log file: $log_file"
    
    echo -e "date:" | tee "$log_file"
    echo -e "\tlocal: $(date)" | tee -a "$log_file"
    echo -e "\tutc: $(date -u +%s)" | tee -a "$log_file"

    echo -e "vm:" | tee -a "$log_file"
    echo -e "\thost: $(hostname)" | tee -a "$log_file"
    lsb_dist=$(_get_distribution "$log_file")
    echo -e "\tdistribution: $lsb_dist" | tee -a "$log_file"
    echo -e "\tversion: $(_get_distro_version)" | tee -a "$log_file"
    directory_size=$(_get_dir_size "/")
    echo -e "\troot: /" | tee -a "$log_file"
    echo -e "\t\tsize: $directory_size" | tee -a "$log_file"

    directory_size=$(_get_dir_size "$INST_DIR")
    echo -e "\tarchfx_dir: $INST_DIR" | tee -a "$log_file"
    echo -e "\t\tsize: $directory_size" | tee -a "$log_file"

    echo -e "docker:" | tee -a "$log_file"
    echo -e "\tlocation: $(_where_is_docker)" | tee -a "$log_file"
    echo -e "\trunning: $(_is_docker_running)" | tee -a "$log_file"
    echo -e "\tdata_root: $(_docker_root_dir)" | tee -a "$log_file"


    echo -e "\tloki: $(_is_loki_plugin_installed)" | tee -a "$log_file"

    echo -e "outbound_connections:" | tee -a "$log_file"
    declare -a urls=("https://www.google.com 200"
        "https://arch.archfx.io/api/v1/server/ 200"
        "https://portainer.overseer.archfx.io 200"
        "https://portaineredge.overseer.archfx.io 404"
        "https://ecr.archfx.io 401"
    )
    for url_response in "${urls[@]}"; do
        read -ra url_response <<< "$url_response" # turn url and response into an array
        echo -e "\turl: ${url_response[0]}" | tee -a "$log_file"
        echo -e "\t\tconnected: $(_outbound_connections ${url_response[@]})" | tee -a "$log_file"
    done
}


#######################################
#   Display latest report
#######################################
function latest_report() {
    ls -t logs_* >/dev/null
    if [ $? -eq 0 ]; then
        file=$(ls -t logs_* | head -1)
        echo ${PWD}/$file
        cat $file
    else
        _warning_msg "Log files not yet created. Run:"
        _success_msg "\n./broker_preflight.sh check"
    fi
}


#######################################
#   Command Line Arguments
#######################################
function usage () {
    echo "ArchFX Broker preflight checklist"
    echo ""
    echo "Usage: $ME [options]"
    echo "Options:"
    echo "  $ME check                   : Runs checks and generates report"
    echo "  $ME report                  : Displays last report"
    echo "  $ME help                    : Prints this usage"
    echo ""
}


function do_arguments() {
    if (( $# < 1 )); then
        usage
        exit 0
    fi

    local args="$@"


    if [[ ${args} == 'check' ]]; then
        preflight_checks
    elif [[ ${args} == 'report' ]]; then
        latest_report
    elif [[ ${args} == 'help' ]]; then
        usage
    else
        usage
        _failure_msg "Error: Unknown Command: ${args}"
    fi
    _done_msg "All checks completed"
    exit 0
}
#######################################
# Having this as the last line guarantees that the entire file has been read
do_arguments $@
