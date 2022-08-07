from typing import cast, Optional, Tuple
from DemistoClassApiModule.DemistoClassApiModule import Demisto

import logging, json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# This is the common interface each driver implements. Since drivers are modules, there
# is no way for the type checker to ensure they have `main`. But this interface is here
# to document what we expect to be true, and to make the type checker happy when we call
# `driver.main()`
class Driver:
    def main(self) -> None:
        pass

def load_driver(name, context) -> Optional[Tuple[Driver, Demisto]]:
    driver = None

    # This must be setup before any drivers are loaded
    import demistomock as demisto
    demisto.setup(context)

    # Drivers are in 'Packs/{name}/Integrations/{name}/{name}.py'. We *could*
    # read the source code, use `compile()`, then use `exec()`, but that has
    # a non-zero risk of an attacker being able to make us run a Python script
    # which we didn't intend to do. This also serves to validate the input.
    if name == 'CrowdStrikeFalcon':
        import Packs.CrowdStrikeFalcon.Integrations.CrowdStrikeFalcon.CrowdStrikeFalcon as driver
    if name == 'SplunkPy':
        import Packs.SplunkPy.Integrations.SplunkPy.SplunkPy as driver

    if driver is not None:
        return (cast(Driver, driver), demisto)

def lambda_handler(event, _):
    body     = event.get('body')
    payload  = json.loads(body)
    cmd      = payload.get('command')
    args     = payload.get('args')
    params   = payload.get('params')
    platform = payload.get('connection')

    #tx = {'command': cmd, 'args': event.get('args'), 'params': {'host': 'splunk.query.ai', 'port': '8089', 'authentication': {'identifier': 'admin', 'password': '#Irisiris20'}}, 'integration': True, 'IsDebug': False}
    ctx = {'command': cmd, 'args': args, 'params': params, 'integration': True, 'IsDebug': False, 'context': {'IntegrationInstance': None}}

    driver = load_driver(platform, ctx)
    if driver is None:
        return {'result': 'error'}

    (driver, demisto) = driver
    driver.main()

    # Demisto drivers use CommonServerPython.return_results, which eventually
    # ends up writing the output to demistomock.output
    return {'result': demisto.output}

if __name__ == '__main__':
    event = {
        'body': json.dumps({
            'command': 'cs-falcon-search-device',
            'args':    {},
            'params':  {
                'client_id': '9f85fa0134374edea917c822caeeb507',
                'secret':    'asFJot8V0rUPfT2l97mNkw1Z6iqhn3x5bOdW4gvX',
                'url':       'https://api.crowdstrike.com'
            },
            'connection': 'CrowdStrikeFalcon'
        })
    }

    result = lambda_handler(event, None)
    print(result)
