import logging
log = logging.getLogger("main")

import sys
from optparse import OptionParser
from yeasty import config, script, context, simulation
from yeasty.visual_progress import Progress as VisualProgress


def configure_options():
    usage = """usage: python %prog [options] <foldername>"""
    parser = OptionParser(usage)
    parser.add_option(
        "-v", "--verbose",
        action="store_true", dest="verbose",
        help="show verbose (debug) output")
    parser.add_option(
        "-c", "--clean",
        action="store_true", dest="clean",
        help="Clean any previous output")
    parser.add_option(
        "-g", "--graphics=",
        action="store_true", dest="graphics", 
        help="show graphics")
    parser.add_option(
        "-u", "--updates",
        type="int", dest="updates", default=100, metavar="N",
        help="show updates every N steps")

    return parser


def configure_logging():
    # TODO Add additional logger in the output folder
    handler = logging.StreamHandler(sys.stdout)
    # format = "%(name)-15s | %(levelname)-8s | %(asctime)s | %(message)s"
    format = "%(name)-15s | %(levelname)-8s | %(message)s"
    formatter = logging.Formatter(format)
    handler.setFormatter(formatter)
    root = logging.getLogger("")
    root.addHandler(handler)
    root.setLevel(logging.INFO)

class TextProgress(object):
    def __init__(self, every=100):
        self.every = every
        self.running = True
        self.paused = False

    def begin(self, sim):
        log.info("Begin {0.treatment.name}, {0.replicate} -----------".format(sim))
        self.count = 0

    def update(self, sim):
        if self.count % self.every == 0:
            text = "\tTreat:{0.treatment.name}, Rep:{0.replicate}, Step:{0.time_step}, Cell Count:{0.cell_count}".format(sim)
            log.info(text)
        self.count += 1

    def interact(self, sim):
        pass

    def end(self, sim):
        log.info("----------------------")

def main():
    configure_logging()
    parser = configure_options()
    options, args = parser.parse_args()

    # We should have one argument: the folder to read the configuration from
    if not args:
        # Otherwise exit, printing the help
        parser.print_help()
        return 2

    script_path = args[0]
    log.info("Starting up...")

    # Load, using the first argument as the folder
    cfg = config.Configuration(options.clean)
    ctx = context.Context(cfg)
    spt = script.Script(ctx)

    # For now, we just turn on debugging
    if options.verbose:
        logging.getLogger("").setLevel(logging.DEBUG)

    # This loads the script using the given context, which puts stuff into the
    # config
    if spt.load(script_path):
        # TODO cfg.validate()
        # Override settings
        progress = [TextProgress(options.updates)]
        if options.graphics:
            progress.append(VisualProgress(options.updates))

        try:
            cfg.experiment.run(progress)
            return 0

        except KeyboardInterrupt:
            log.error("User interrupted the Program")
        except simulation.SimulationInterrupt:
            pass

    return 1

if __name__ == "__main__":
    # Well behaved unix programs exits with 0 on success...
    sys.exit(main())
