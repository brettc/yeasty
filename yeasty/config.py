import logging
log = logging.getLogger("config")
import os, shutil
from experiment import Experiment

class Configuration(object):
    """This holds the user configuration info"""

    def __init__(self, clean=False):
        self.random_seed = None
        self.clean = clean

    def init(self, base_path, name):
        """Call this one if you're doing it programmatically"""
        self.base_path = base_path
        self.output_path = self.make_dir(name+'.output')
        log.info("Setting output folder to '%s'", self.output_path)
        self.init_logger(self.output_path)

        # Creat a cache path
        self.cache_path = self.make_dir('.cache')

        # Make an experiment
        self.experiment = Experiment(self, name)

    def init_from_script(self, script_path):
        """Load using a script file"""

        # Allow for user and environment variables
        script_path = os.path.expanduser(script_path)
        script_path = os.path.expandvars(script_path)
        script_path = os.path.normpath(script_path)

        if not os.path.exists(script_path) or \
           not os.path.isfile(script_path):
            log.error("The script file '%s' does not exist", script_path)
            raise RuntimeError 

        base_path, name = os.path.split(script_path)
        name, ext = os.path.splitext(name)

        self.init(base_path, name)

    def validate(self):
        """Should be called before processing"""
        pass

    def make_dir(self, nm):
        if hasattr(self, 'output_path'):
            start = self.output_path
        else:
            start = self.base_path
        pth = os.path.join(start, nm)

        if os.path.exists(pth):
            if os.path.isdir(pth):
                if self.clean:
                    log.info("Removing existing folder '%s'", pth)
                    shutil.rmtree(pth)
            else:
                log.error("Cannot create folder '%s'", pth)
                raise RuntimeError

        if not os.path.exists(pth):
            os.mkdir(pth)
            log.info("Created folder '%s'", pth)

        return pth

    def init_logger(self, pth):
        log_path = os.path.join(pth, "log.txt")
        handler = logging.FileHandler(log_path, 'a')
        formatter = logging.Formatter(
            "%(levelname)-8s | %(asctime)s | %(name)-15s | %(message)s")
        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)
        logging.getLogger("").addHandler(handler)
        logging.getLogger("analysis").addHandler(handler)

        log.info("Full output log can be found in '%s'", log_path)


