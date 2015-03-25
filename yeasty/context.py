import logging
log = logging.getLogger("context")

import experiment, simulation, parameters, analysis

def scripted(method):
    # Don't wrap the function, just record it
    # print method.func_name, method.func_globals
    # print dir(method)
    # script_functions.append(method.func_name)
    method.scripted = True
    return method

class Context(object):
    def __init__(self, config):
        self.config = config
        self.namespace = {}

        # Initialise a namespace dictionary for loading the script. Keys in
        # this dictionary will be available in the namespace of the
        # configuration file
        for name in dir(self):
            attr = getattr(self, name)
            # if type(attr) is types.MethodType and hasattr(attr, 'scripted'):
            # TODO should warn about collisions
            if hasattr(attr, 'scripted'):
                self.namespace[name] =  attr

        self.namespace['parameters'] = parameters.Parameters

        # We need to add the agent classes too...
        for cls in analysis.analyses:
            self.namespace[cls.__name__] = cls

        self.defaults = {}

    def init(self, pth):
        self.config.init_from_script(pth)

    # -------------------------------------------------
    # Scripted functions available to config file
    @scripted
    def set_defaults(self, **kwargs):
        for k, v in kwargs.items():
            log.info("setting default of '%s' to %s", k, v)
            self.defaults[k] = v

    @scripted
    def add_treatment(self, name, p, replicates):
        # Duplicate the parameters so that they can't be changed
        self.config.experiment.add_treatment(name, replicates, p.freeze())
        
    @scripted
    def add_analysis(self, cls):
        if cls not in analysis.analyses:
            log.error("Ignoring unknown analysis %s", str(cls))
        else:
            self.config.experiment.add_analysis(cls)

    # -------------------------------------------------
    # Scripted functions available to settings 
    # @scripted
    # def set_random_seed(self, seed=None):
        # self.config.random_seed = seed
    # 
    # @scripted
    # def add_dimensions(self, size, how_many):
        # self.config.dimensions.add_dimensions(size, how_many)

    # @scripted
    # def set_K(self, K):
        # self.config.K = K

    # @scripted
    # def add_agents(self, kind, number):
        # self.config.add_agents(kind, number)

    # @scripted
    # def run_for(self, cycles):
        # self.config.cycles = cycles

    # @scripted
    # def report_peaks(self, b=True):
        # self.config.report_peaks = b

