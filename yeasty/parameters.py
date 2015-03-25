import logging
log = logging.getLogger("parameters")

import copy


class ParametersError(Exception):
    pass


class Parameters(object):

    # Put the default parameters here
    mass_multiplier = .0005
    start_size = 5
    finish_size = 25
    grow_step = .1

    linear_damping = 0
    single_branch_prob = .3
    wait_till_grow = 100
    max_joint_distortion = 30
    max_dead_joint_distortion = 10
    max_cells = 400
    max_steps = 2000
    check_break_every = 1
    life_expectancy = 15000

    max_bias = 15.0

    # 5% every 40th
    error_bias = pow(1.0 - 0.05, 40.0)
    max_force = 0

    attach_width = 10.
    iterations = 10
    dt = 1.0 / 40.0

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                log.info("Setting '%s' to %s", k, v)
                setattr(self, k, v)
            else:
                log.warning("'%s' is not a valid parameter (ignoring)", k)

    def __setattr__(self, k, v):
        if hasattr(self, k):
            log.info("Setting '%s' to %s", k, v)
            object.__setattr__(self, k, v)
        else:
            log.warning("'%s' is not a valid parameter (ignoring)", k)

    def freeze(self):
        # Need to go a bit deeper with agents
        c = copy.copy(self)
        return c
