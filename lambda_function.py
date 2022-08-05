# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Purpose

Shows how to implement an AWS Lambda function that handles input from direct
invocation.
"""

import logging, io, json
import importlib, os
from contextlib import redirect_stdout
# import config

from DemistoClassApiModule.DemistoClassApiModule import Demisto

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    :param event: The event dict that contains the parameters sent when the function
                  is invoked.
    :param context: The context in which the function is called.
    :return: The result of the action.
    """
    # print(event)
    body = event.get('body')
    payload_dict = json.loads(body)
    platform = payload_dict.get('connection')
    cmd = payload_dict.get('command')
    # ctx = {'command': cmd, 'args': event.get('args'), 'params': {'host': 'splunk.query.ai', 'port': '8089', 'authentication': {'identifier': 'admin', 'password': '#Irisiris20'}}, 'integration': True, 'IsDebug': False}
    ctx = {'command': cmd, 'args': payload_dict.get('args'), 'params': payload_dict.get('params'), 'integration': True, 'IsDebug': False, 'context': {'IntegrationInstance': None}}
    global demisto
    demisto = Demisto(ctx)
    # mod = importlib.import_module(f'Packs.{platform}.Integrations.{platform}.{platform}')
    # import Packs.CrowdStrikeFalcon.Integrations.CrowdStrikeFalcon.CrowdStrikeFalcon as mod
    # locals().update({'demisto':demisto})
    print('importing Crowdstrike')
    # with open('Packs/Base/Scripts/CommonServerPython/CommonServerPython.py') as csp:
    # with open('Packs/CrowdStrikeFalcon/Integrations/CrowdStrikeFalcon/CrowdStrikeFalcon.py') as cs:
    #   csCode = compile(cs.read(), 'CrowdSrtike.py', 'exec')
    # exec(csCode, {'demisto': demisto, 'demistox': demisto})
    COMMON_SERVER_SCRIPT = 'Packs/Base/Scripts/CommonServerPython/CommonServerPython.py'
    platform_script = 'Packs/CrowdStrikeFalcon/Integrations/CrowdStrikeFalcon/CrowdStrikeFalcon.py'
    with open(COMMON_SERVER_SCRIPT) as cs, open(platform_script) as ps:
      csCode = compile(cs.read(), COMMON_SERVER_SCRIPT, 'exec')
      exec(csCode, globals())
      psCode = compile(ps.read(), platform_script, 'exec')
      exec(psCode, globals())


    result = demisto.output
    print(result)
    # result = None
    # try:
    #     with redirect_stdout(io.StringIO()) as f:
    #         mod.main()
    #     result = f.getvalue()
    #     # logger.info(result)
    #     # result = mod.main(ctx)
    # except SystemExit as se:
    #     logger.error('System Exit Error')
    return {'result': result}

event = {'body': '{"command": "cs-falcon-search-device","args": {},"params": {"client_id": "9f85fa0134374edea917c822caeeb507","secret": "asFJot8V0rUPfT2l97mNkw1Z6iqhn3x5bOdW4gvX","url": "https://api.crowdstrike.com"},"connection": "CrowdStrikeFalcon"}'}
result = lambda_handler(event, None)
print(result)