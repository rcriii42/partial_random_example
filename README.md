# partial_random_example

Ever want to inject randomness in your Python program, but unsure what random function to use? As an example, I am writing simulation software and want to randomly vary the length of the agent tasks. However, I want to pass in the random parameters so that I don't have to continually update the underlying code. 

[functools.partial](https://docs.python.org/3/library/functools.html#functools.partial) and [random](https://docs.python.org/3/library/random.html) to the rescue:

```
In [2]: import random
In [3]: import functools
In [4]: var_high = 1.25
In [5]: var_low = 0.5
In [6]: var_mode = 0.9
In [7]: random_func = functools.partial(random.triangular, low=var_low, high=var_high, mode=var_mode)
In [8]: print(f'{random_func=}')
random_func=functools.partial(<bound method Random.triangular of <random.Random object at 0x000001FD600A6800>>, low=0.5, high=1.25, mode=0.9)
In [9]: random_func()
Out[9]: 0.9645202174961249
In [10]: random_func()
Out[10]: 1.1161735490673275
```

`functools.partial` creates a wrapper around the given function with certain parameters already filled in. The result is a function that you only have to call with any remaining parameters. Since I've provided all the parameters for `random.triangular`, random_func is has no parameters, so the call is simply `random_func()`. Notice how `print(random_func)` gives a nice summary with the random method and parameters. If I decide later that I don't like the triangular distribution, I can redefine random_func:

`random_func = functools.partial(random.uniform, a=var_low, b=var_high)`

For example, I have an agent in the Python [Mesa](https://mesa.readthedocs.io/en/latest/tutorials/intro_tutorial.html) framework:

```
class ProductionAgent(mesa.Agent):
    """An agent that does work."""
    def __init__(self, unique_id, model, production=10, random_function=None):
        # Pass the parameters to the parent class.
        super().__init__(unique_id, model)
        self.randfunc = random_function
        self.production = production
        self.work_to_date = 0
        print(f'Production agent initialized with {self.unique_id=}, {self.randfunc=}, {self.production=}')

    def step(self):
        """Step function called by the model at each timestep.

        Do work and track the result"""
        if self.randfunc is None:
            self.work_to_date += self.production
        else:
            self.work_to_date += self.production * self.randfunc()
```

To change the parameters of the random function, I only need redefine random_func once at the top level and pass it into the underlying Model and Agents. Otherwise, I would have to change the Agent code to change the random function and the passed in parameters everywhere they are used.
