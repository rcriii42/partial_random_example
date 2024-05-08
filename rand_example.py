"""Example script to demonstrate how to generate random numbers using a passed-in random function."""

import functools
import random

import mesa


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


class MyModel(mesa.Model):
    """Example model with random functions."""

    def __init__(self,
                 num_agents=1,
                 default_production=10,
                 production_randomizer=None):
        super().__init__()
        self.num_agents = num_agents
        self.num_steps = 0
        # Create scheduler and assign it to the model
        self.schedule = mesa.time.RandomActivation(self)

        # Create agents
        for i in range(self.num_agents):
            a = ProductionAgent(i, self, default_production, production_randomizer)
            # Add the agent to the scheduler
            self.schedule.add(a)

    def step(self):
        """Advance the model by one step."""
        self.num_steps += 1
        self.schedule.step()  # This polls all the agents
        total_production = sum(a.work_to_date for a in self.schedule.agents)
        print(f'Step {self.num_steps}, Production to date: {total_production:0.0f}')


if __name__ == '__main__':
    var_high = 1.25
    var_low = 0.75
    var_mode = 0.25
    random_func = functools.partial(random.triangular, low=var_low, high=var_high, mode=var_mode)

    my_model = MyModel(num_agents=1, production_randomizer=random_func)
    for i in range(5):
        my_model.step()

    print()

    random_func = functools.partial(random.uniform, a=var_low, b=var_high)

    my_model = MyModel(num_agents=2, production_randomizer=random_func)
    for i in range(5):
        my_model.step()