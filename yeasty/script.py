import logging
log = logging.getLogger("script")

import traceback, sys, cStringIO

class Script(object):
    def __init__(self, context):
        self.context = context

    def load(self, pth):
        self.context.init(pth)
        try:
            log.info("Loading Script '%s'", pth)
            execfile('%s' % pth, self.context.namespace)

        # TODO This is WAY too complex. Make it nicer
        except SyntaxError, err:
            log.error("Syntax error in loading script '%s'", pth)
            log.error("Line %d", err.lineno)
            log.error("%s", err.text[:-1])
            if err.offset > 1:
                log.error("%s^", (' ' * (err.offset-1)))
            else:
                log.error("^")
        except Exception, err:
            # Stolen from logging. It's rubbish. But it will do for now.
            ei = sys.exc_info()
            sio = cStringIO.StringIO()
            traceback.print_exception(ei[0], ei[1], ei[2], None, sio)
            s = sio.getvalue()
            sio.close()
            if s[-1:] == "\n":
                s = s[:-1]
            log.error("Unhandled exception in loading script: '%s'", pth)
            log.error(s)
        else:
            log.info("Finished loading Script '%s'", pth)
            return True

        return False

