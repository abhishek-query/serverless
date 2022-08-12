import Packs.ApiModules.Scripts.DemistoClassApiModule.DemistoClassApiModule as orig
from queryai.logging import logger

class Demisto(orig.Demisto):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.integration_context = {}

    def __do(self, cmd):
        self.__not_implemented()

    def __do_no_res(self, cmd):
        self.__not_implemented()

    def __not_implemented(self):
        import inspect
        caller = inspect.currentframe()

        while caller:
            path, line, func, _, _ = inspect.getframeinfo(caller)
            caller                 = caller.f_back

            if path.endswith('DemistoClassApiModule.py'):
                caller = caller and caller.f_back
                raise RuntimeError(f'{__file__} must override `{func}`, called from {func} in {path}, line {line}')

        raise RuntimeError('__do or __do_no_res should not be called')

    def info(self, *args):
        logger.info(*args)

    def error(self, *args):
        logger.error(*args)

    def exception(self, ex):
        logger.error(ex)

    def debug(self, *args):
        logger.debug(*args)

    def getIntegrationContext(self):
        return self.integration_context

    def setIntegrationContext(self, context):
        self.integration_context = context

    def results(self, data):
        res = []

        if self.is_integration:
            converted = self.__convert(data)
        else:
            converted = self.convert(data)

        if type(converted) is list:
            res = converted
        else:
            res.append(converted)

        self.output = data
