#!/usr/bin/env python

import json
import logging
import requests
import subprocess


# setup the logging
CAMP_LOG="camping_alert_log.txt"
logging.basicConfig(
    filename=CAMP_LOG, format="%(asctime)s %(message)s", filemode="a"
)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# Slack urls
SLACK_HOOKS = "https://hooks.slack.com/services"
CAMP_URL = SLACK_HOOKS+"/<your>/<slack>/<info>"



def send_slack_msg(msg_template, channel_url=CAMP_URL):
    # Example curl command
    #curl -X POST -H 'Content-type: application/json' --data '{"text":"Hello, World!"}' https://hooks.slack.com/services/<your>/<slack>/<info>
    # Slack urls

    headers = {"content-type": "application/json"}
    data = {"text": msg_template}
    requests.post(url=channel_url, data=json.dumps(data), headers=headers)


def send_sites_found_message(campsite_data):
    SLACK_SITES_FOUND_MSG = """We got ourselves some campin' sites!"""
    send_slack_msg(SLACK_SITES_FOUND_MSG)
    send_slack_msg(campsite_data)


def send_sites_not_found_message(days_of_week):
    SLACK_NO_SITES_MSG = f"Sorry partner - no sites found for any:{days_of_week}"
    send_slack_msg(SLACK_NO_SITES_MSG)


def run_cmd(args, **kwargs):
    if isinstance(args, str):
        kwargs["shell"] = True
    logger.info("about to run this command")
    logger.info(args)
    p = subprocess.run(args, check=True, capture_output=True, **kwargs)
    output = p.stdout.decode()
    errOutput = p.stderr.decode()
    logger.info("output from the command is below:")
    logger.info(output)
    # if the errOutput is not null then log it
    if errOutput:
        logger.info("error output is below: ")
        logger.info(errOutput)
    p.check_returncode()
    return str(output)



def check_avail(campsite, days_of_week, api="reserve_ca", nights=1):
    # Note: the only other api option is: recreation_gov
    # If you want to test a command that has results try: check_avail(campsite=231958,  days_of_week="mon", nights=1, api="recreation_gov")
    
    # If any of the days of week are wrong just quit
    allowed_days_of_week = {"mon", "tue", "wed", "thu", "fri", "sat", "sun"}
    days_of_week = set(days_of_week)
    diff = days_of_week.difference(allowed_days_of_week)
    if len(diff) != 0:
        logger.debug('Error: day of week not recognized')
        quit()
    
    sites_avail = []
    for day in days_of_week:
        cmd=["find-campsite", "--api", api, "-c", str(campsite), "-n", str(nights), "--day", day]
        output=run_cmd(cmd)
        if "No sites found" not in output:
            logger.info('sites found!!!!')
            sites_avail.append(output)
        else:
            logger.info("no sites found")
    if len(sites_avail) != 0:
        send_sites_found_message(output)
    else:
        send_sites_not_found_message(days_of_week)


# Run the script
check_avail("766", days_of_week=["thu", "fri", "sat"])
