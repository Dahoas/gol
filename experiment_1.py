from experiment import *
from gol import GOLState, GOLGame, batched_run_gol


hypothesis = Hypothesis(
    text="Increasing the initial density of live cells in a 100x100 Game of Life board increases the average number of live cells after 1000 time steps."
)


import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Union

@dataclass
class IndependentVariable:
    value: Union[bool, int, float]
    description: str

@dataclass
class DependentVariable:
    value: Union[bool, int, float]
    description: str

@dataclass
class Results:
    results: List[Tuple[IndependentVariable, DependentVariable]]

class Experiment:
    def __init__(self, hypothesis: Hypothesis):
        self.hypothesis = hypothesis

    def __call__(self) -> Results:
        densities = [0.1, 0.2, 0.3, 0.4, 0.5]
        results = []
        for density in densities:
            avg_live_cells = self.run_simulations(density)
            indep_var = IndependentVariable(value=density, description="Initial density of live cells")
            dep_var = DependentVariable(value=avg_live_cells, description="Average number of live cells after 1000 steps")
            results.append((indep_var, dep_var))
        return Results(results=results)

    def run_simulations(self, density):
        initial_states = [GOLState.random_init(p=[1-density, density]) for _ in range(50)]
        games = batched_run_gol(initial_states)
        live_cells_counts = [np.sum(game.trajectory[-1].state) for game in games]
        return np.mean(live_cells_counts)


class HypothesisTest:
    def __init__(self):
        pass

    def __call__(self, results: Results) -> bool:
        densities = [result[0].value for result in results.results]
        avg_live_cells = [result[1].value for result in results.results]
        return all(x <= y for x, y in zip(avg_live_cells, avg_live_cells[1:]))  # Check if avg_live_cells is non-decreasing

def e1():
    experiment = Experiment(hypothesis=hypothesis)
    hypothesis_test = HypothesisTest()


    # Run the experiment
    results = experiment()

    # Test the hypothesis
    hypothesis_result = hypothesis_test(results)

    # Print results
    print(f"Hypothesis: {hypothesis.text}")
    print("Results:")
    for indep_var, dep_var in results.results:
        print(f"Initial density: {indep_var.value}, Average live cells: {dep_var.value}")
    print(f"Hypothesis is {'supported' if hypothesis_result else 'not supported'} by the results.")


class NewExperiment(Experiment):
        def __call__(self) -> Results:
            densities = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
            results = []
            for density in densities:
                avg_live_cells = self.run_simulations(density)
                indep_var = IndependentVariable(value=density, description="Initial density of live cells")
                dep_var = DependentVariable(value=avg_live_cells, description="Average number of live cells after 1000 steps")
                results.append((indep_var, dep_var))
            return Results(results=results)

def e2():
    # Define new hypothesis
    new_hypothesis = Hypothesis(
        text="There exists an optimal initial density of live cells that maximizes the average number of live cells after 1000 time steps on a 100x100 Game of Life board."
    )

    # Run the new experiment
    new_experiment = NewExperiment(hypothesis=new_hypothesis)
    new_results = new_experiment()

    # Print new results
    print(f"New Hypothesis: {new_hypothesis.text}")
    print("Results:")
    for indep_var, dep_var in new_results.results:
        print(f"Initial density: {indep_var.value}, Average live cells: {dep_var.value}")


class FurtherRefinementExperiment(Experiment):
    def __call__(self) -> Results:
        densities = [0.38, 0.39, 0.4, 0.41, 0.42]
        results = []
        for density in densities:
            avg_live_cells = self.run_simulations(density)
            indep_var = IndependentVariable(value=density, description="Initial density of live cells")
            dep_var = DependentVariable(value=avg_live_cells, description="Average number of live cells after 1000 steps")
            results.append((indep_var, dep_var))
        return Results(results=results)


def e3():
    # Define further refinement hypothesis
    further_refinement_hypothesis = Hypothesis(
        text="There exists a precise optimal initial density of live cells around 0.4 that maximizes the average number of live cells after 1000 time steps on a 100x100 Game of Life board."
    )

    # Run the further refinement experiment
    further_refinement_experiment = FurtherRefinementExperiment(hypothesis=further_refinement_hypothesis)
    further_refinement_results = further_refinement_experiment()

    # Print further refinement results
    print(f"Further Refinement Hypothesis: {further_refinement_hypothesis.text}")
    print("Results:")
    for indep_var, dep_var in further_refinement_results.results:
        print(f"Initial density: {indep_var.value}, Average live cells: {dep_var.value}")


class StabilityExperiment(Experiment):
    def __call__(self) -> Results:
        patterns = ['random', 'glider', 'still_life', 'oscillator']
        results = []
        for pattern in patterns:
            stability = self.run_simulations(pattern)
            indep_var = IndependentVariable(value=pattern, description="Initial pattern of live cells")
            dep_var = DependentVariable(value=stability, description="Stability after 1000 steps")
            results.append((indep_var, dep_var))
        return Results(results=results)

    def run_simulations(self, pattern):
        if pattern == 'random':
            initial_states = [GOLState.random_init() for _ in range(50)]
        elif pattern == 'glider':
            initial_states = [self.create_glider() for _ in range(50)]
        elif pattern == 'still_life':
            initial_states = [self.create_still_life() for _ in range(50)]
        elif pattern == 'oscillator':
            initial_states = [self.create_oscillator() for _ in range(50)]
        games = batched_run_gol(initial_states)
        stability_counts = [self.calculate_stability(game) for game in games]
        return np.mean(stability_counts)

    def calculate_stability(self, game):
        initial_state = game.trajectory[0].state
        final_state = game.trajectory[-1].state
        unchanged_cells = np.sum(initial_state == final_state)
        total_cells = initial_state.size
        return unchanged_cells / total_cells

    def create_glider(self):
        state = np.zeros((100, 100), dtype=int)
        state[1, 2] = state[2, 3] = state[3, 1] = state[3, 2] = state[3, 3] = 1
        return GOLState(state)

    def create_still_life(self):
        state = np.zeros((100, 100), dtype=int)
        state[1, 1] = state[1, 2] = state[2, 1] = state[2, 2] = 1
        return GOLState(state)

    def create_oscillator(self):
        state = np.zeros((100, 100), dtype=int)
        state[1, 2] = state[2, 2] = state[3, 2] = 1
        return GOLState(state)

def e4():
    # Define stability hypothesis
    stability_hypothesis = Hypothesis(
        text="Certain initial patterns (random, glider, still life, oscillator) maintain their structure and stability better over 1000 time steps."
    )

    # Run the stability experiment
    stability_experiment = StabilityExperiment(hypothesis=stability_hypothesis)
    stability_results = stability_experiment()

    # Print stability results
    print(f"Stability Hypothesis: {stability_hypothesis.text}")
    print("Results:")
    for indep_var, dep_var in stability_results.results:
        print(f"Initial pattern: {indep_var.value}, Stability: {dep_var.value}")

    class StabilityHypothesisTest(HypothesisTest):
        def __call__(self, results: Results) -> bool:
            pattern_stability = {result[0].value: result[1].value for result in results.results}
            still_life_stability = pattern_stability['still_life']
            oscillator_stability = pattern_stability['oscillator']
            random_stability = pattern_stability['random']
            glider_stability = pattern_stability['glider']
            return still_life_stability > random_stability and still_life_stability > glider_stability and oscillator_stability > random_stability and oscillator_stability > glider_stability

    # Define the hypothesis test
    stability_hypothesis_test = StabilityHypothesisTest()

    # Test the hypothesis
    hypothesis_result = stability_hypothesis_test(stability_results)

    # Print the test result
    print(f"Hypothesis is {'supported' if hypothesis_result else 'not supported'} by the results.")


class InteractionExperiment(Experiment):
    def __call__(self) -> Results:
        configurations = ['single_random', 'single_glider', 'single_still_life', 'single_oscillator', 'multiple']
        results = []
        for config in configurations:
            stability = self.run_simulations(config)
            indep_var = IndependentVariable(value=config, description="Initial configuration of patterns")
            dep_var = DependentVariable(value=stability, description="Stability after 1000 steps")
            results.append((indep_var, dep_var))
        return Results(results=results)

    def run_simulations(self, config):
        if config == 'single_random':
            initial_states = [GOLState.random_init() for _ in range(50)]
        elif config == 'single_glider':
            initial_states = [self.create_glider() for _ in range(50)]
        elif config == 'single_still_life':
            initial_states = [self.create_still_life() for _ in range(50)]
        elif config == 'single_oscillator':
            initial_states = [self.create_oscillator() for _ in range(50)]
        elif config == 'multiple':
            initial_states = [self.create_multiple() for _ in range(50)]
        games = batched_run_gol(initial_states)
        stability_counts = [self.calculate_stability(game) for game in games]
        return np.mean(stability_counts)

    def calculate_stability(self, game):
        initial_state = game.trajectory[0].state
        final_state = game.trajectory[-1].state
        unchanged_cells = np.sum(initial_state == final_state)
        total_cells = initial_state.size
        return unchanged_cells / total_cells

    def create_glider(self):
        state = np.zeros((100, 100), dtype=int)
        state[1, 2] = state[2, 3] = state[3, 1] = state[3, 2] = state[3, 3] = 1
        return GOLState(state)

    def create_still_life(self):
        state = np.zeros((100, 100), dtype=int)
        state[1, 1] = state[1, 2] = state[2, 1] = state[2, 2] = 1
        return GOLState(state)

    def create_oscillator(self):
        state = np.zeros((100, 100), dtype=int)
        state[1, 2] = state[2, 2] = state[3, 2] = 1
        return GOLState(state)

    def create_multiple(self):
        state = np.zeros((100, 100), dtype=int)
        # Place a glider
        state[1, 2] = state[2, 3] = state[3, 1] = state[3, 2] = state[3, 3] = 1
        # Place a still life (block)
        state[10, 10] = state[10, 11] = state[11, 10] = state[11, 11] = 1
        # Place an oscillator (blinker)
        state[20, 21] = state[21, 21] = state[22, 21] = 1
        return GOLState(state)

def e5():
    # Define interaction hypothesis
    interaction_hypothesis = Hypothesis(
        text="The interaction between different initial patterns (e.g., gliders, still lifes, oscillators) on the same board significantly impacts the average stability and structure after 1000 time steps compared to when patterns evolve independently."
    )

    # Run the interaction experiment
    interaction_experiment = InteractionExperiment(hypothesis=interaction_hypothesis)
    interaction_results = interaction_experiment()

    # Print interaction results
    print(f"Interaction Hypothesis: {interaction_hypothesis.text}")
    print("Results:")
    for indep_var, dep_var in interaction_results.results:
        print(f"Initial configuration: {indep_var.value}, Stability: {dep_var.value}")

    class InteractionHypothesisTest(HypothesisTest):
        def __call__(self, results: Results) -> bool:
            single_pattern_stabilities = [result[1].value for result in results.results if 'single' in result[0].value]
            multiple_pattern_stability = next(result[1].value for result in results.results if result[0].value == 'multiple')
            avg_single_stability = np.mean(single_pattern_stabilities)
            return multiple_pattern_stability != avg_single_stability

    # Define the hypothesis test
    interaction_hypothesis_test = InteractionHypothesisTest()

    # Test the hypothesis
    hypothesis_result = interaction_hypothesis_test(interaction_results)

    # Print the test result
    print(f"Hypothesis is {'supported' if hypothesis_result else 'not supported'} by the results.")


class ClusteringExperiment(Experiment):
    def __call__(self) -> Results:
        clustering_degrees = ['low', 'medium', 'high']
        results = []
        for degree in clustering_degrees:
            stability, longevity = self.run_simulations(degree)
            indep_var = IndependentVariable(value=degree, description="Degree of clustering of initial live cells")
            dep_var_stability = DependentVariable(value=stability, description="Stability after 1000 steps")
            dep_var_longevity = DependentVariable(value=longevity, description="Longevity (average number of live cells) over 1000 steps")
            results.append((indep_var, dep_var_stability, dep_var_longevity))
        return Results(results=results)

    def run_simulations(self, degree):
        if degree == 'low':
            initial_states = [self.create_clustered_state(cluster_size=1) for _ in range(50)]
        elif degree == 'medium':
            initial_states = [self.create_clustered_state(cluster_size=3) for _ in range(50)]
        elif degree == 'high':
            initial_states = [self.create_clustered_state(cluster_size=5) for _ in range(50)]
        games = batched_run_gol(initial_states)
        stability_counts = [self.calculate_stability(game) for game in games]
        longevity_counts = [self.calculate_longevity(game) for game in games]
        return np.mean(stability_counts), np.mean(longevity_counts)

    def calculate_stability(self, game):
        initial_state = game.trajectory[0].state
        final_state = game.trajectory[-1].state
        unchanged_cells = np.sum(initial_state == final_state)
        total_cells = initial_state.size
        return unchanged_cells / total_cells

    def calculate_longevity(self, game):
        live_cells_counts = [np.sum(state.state) for state in game.trajectory]
        return np.mean(live_cells_counts)

    def create_clustered_state(self, cluster_size):
        state = np.zeros((100, 100), dtype=int)
        for _ in range(100):  # Creating 100 clusters
            x, y = np.random.randint(0, 100-cluster_size), np.random.randint(0, 100-cluster_size)
            state[x:x+cluster_size, y:y+cluster_size] = 1
        return GOLState(state)


def e6():
    # Define clustering hypothesis
    clustering_hypothesis = Hypothesis(
        text="Initial clustering of live cells significantly impacts the longevity and stability of patterns in the Game of Life over 1000 time steps."
    )

    # Run the clustering experiment
    clustering_experiment = ClusteringExperiment(hypothesis=clustering_hypothesis)
    clustering_results = clustering_experiment()

    # Print clustering results
    print(f"Clustering Hypothesis: {clustering_hypothesis.text}")
    print("Results:")
    for indep_var, dep_var_stability, dep_var_longevity in clustering_results.results:
        print(f"Degree of clustering: {indep_var.value}, Stability: {dep_var_stability.value}, Longevity: {dep_var_longevity.value}")


    class ClusteringHypothesisTest(HypothesisTest):
        def __call__(self, results: Results) -> bool:
            stability_values = {result[0].value: result[1].value for result in results.results}
            longevity_values = {result[0].value: result[2].value for result in results.results}
            
            # We assume that higher clustering should lead to higher stability and longevity
            return (stability_values['high'] > stability_values['medium'] > stability_values['low']) and \
                (longevity_values['high'] > longevity_values['medium'] > longevity_values['low'])

    # Define the hypothesis test
    clustering_hypothesis_test = ClusteringHypothesisTest()

    # Test the hypothesis
    hypothesis_result = clustering_hypothesis_test(clustering_results)

    # Print the test result
    print(f"Hypothesis is {'supported' if hypothesis_result else 'not supported'} by the results.")



if __name__ == "__main__":
    e6()