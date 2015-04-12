## Yeasty: Simulating Multicellular Growth of Yeast

The yeast *Saccharomyces cerevisiae* can evolve a simple form of multicellularity in lab conditions which gravity-select for larger clumps ([1][mcell2],[2][mcell2]). A analysis of this growth suggests that the geometry of this growth has important evolutionary consequences, and can explain why an initial division of reproductive labour arises ([3][geometry]). The division of labour exhibits itself as an increased cell-death rate within the clump. Dead cells provides weak points, allowing the clusters to split, increasing the space for further replication. So increased cell death actually increases the overall reproductive rate of cells and clusters.

This aim of this simulation it to provide a simple *in-silico* visual laboratory for exploring the parameters that control cluster growth and splitting (there is no selection in this model, yet). The simulation uses simple physics to model two-dimensional cluster growth, and provides an optional visual display. Simple configuration files can provide different sets of parameters, multiple replicates can be run, and the results can be recorded for analysis. This is a work in progress, and more work is needed to capture some of the more interesting dynamics.

<!-- <a href="http://www.youtube.com/watch?feature=player_embedded&v=YOUTUBE_VIDEO_ID_HERE -->
<!-- " target="_blank"><img src="http://img.youtube.com/vi/YOUTUBE_VIDEO_ID_HERE/0.jpg"  -->
<!-- alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a> -->

### Installation

To run this code, you'll need to install [pymunk][pymunk]. To see the visualisations, you'll need to install [pygame][pygame]. The simulations will work fine without pygame (indeed, things will run faster), but you don't get any visual feedback.

### Running the Code

To run a simulation, you need to invoke `python run_simulation.py`, and point it at a configuration file. Some example configuration files are in the `./experiments` folder. Here is the contents of `simple.cfg`:

```python
p = parameters()
p.max_steps = 2000
p.max_joint_distortion = 30
p.max_dead_joint_distortion = 5
p.life_expectancy = 5000
p.max_cells = 400
add_treatment('distort_10', p, replicates=10)
```
This runs 10 simulations with the parameter settings shown. To run this:

```
$ python run_simulation experiments/simple.cfg 
```

If you want to see some graphics, add the -g flag:

```
$ python run_simulation -g experiments/simple.cfg 
```

To control the frequency you get updates, use the `-u <N>` option:

```
$ python run_simulation -g -u 10 experiments/simple.cfg 
```

If you invoke the graphics, you can hit `<space>` to pause the simulation, and `<enter>` to take a snapshot of the simulation.

### Writing Experiments and Collecting Results

To really play with this simulation, and write your own experiments, you're going to have to dig into the code. The `./yeasty/parameters.py` file is a good place to start. The `Parameters` class provides a bunch of defaults, which can be overridden. Here is a snippet of that file:

```python
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
```

A configuration file allows you to create different "treatments" which vary these parameters, and this run multiple related simulations from one configuration file. To collect the results, you need to load an "analysis" plugin. A few examples are currently provided, such as one that records the final number of clusters produced at the end of each simulation in a `.csv` file.

### Contact

Contact me (Brett Calcott) with any questions: brett.calcott@gmail.com

### Credits

The programming was done in [python][python] by [Brett Calcott][brettc], in consultation with [Ben Kerr][kerrlab]. The simulation uses [pymunk][pymunk], the python version of the 2d physics library [chipmunk][chipmunk], and the visualisations use [pygame][pygame].

### References

* [Libby E, Ratcliff W, Travisano M, Kerr B (2014) Geometry Shapes Evolution of Early Multicellularity. PLoS Comput Biol 10:e1003803. doi: 10.1371/journal.pcbi.1003803][geometry]

* [Ratcliff WC, Denison RF, Borrello M, Travisano M (2012) Experimental evolution of multicellularity. PNAS 109:1595–1600. doi: 10.1073/pnas.1115323109][mcell1]

* [Ratcliff WC, Fankhauser JD, Rogers DW, et al (2015) Origins of multicellular evolvability in snowflake yeast. Nat Commun. doi: 10.1038/ncomms7102][mcell2]

[pygame]: http://pygame.org

[pymunk]: http://pymunk.readthedocs.org/en/latest/ 

[kerrlab]: http://kerrlab.org/Public/BenKerr 

[geometry]: http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003803

[mcell1]: http://www.pnas.org/content/109/5/1595.abstract

[mcell2]: http://www.nature.com/ncomms/2015/150120/ncomms7102/full/ncomms7102.html
