import numpy as np
from collections import defaultdict
import json
from tqdm import tqdm

from run_gol import run_gol, batched_run_gol
from gol import GOLState, GOLGame


def compute_entropy(grid):
    """
    Compute the Shannon entropy of a grid for Conway's Game of Life.
    
    Parameters:
    - grid (numpy array): A 2D numpy array where cells are either 1 (alive) or 0 (dead).
    
    Returns:
    - entropy (float): The Shannon entropy of the grid.
    """
    # Flatten the grid to a 1D array for easier computation
    flat_grid = grid.flatten()
    
    # Calculate the probability of a cell being alive or dead
    p_alive = np.mean(flat_grid)
    p_dead = 1 - p_alive
    
    # Handle the log(0) case by defining 0*log(0) as 0
    entropy = 0
    if p_alive > 0:
        entropy -= p_alive * np.log2(p_alive)
    if p_dead > 0:
        entropy -= p_dead * np.log2(p_dead)
    
    return entropy


def detect_still_life(gol_game: GOLGame):
    # Assuming grid is a 2D numpy array
    prev_state = None
    is_still = False
    for gol_state in gol_game:
        if prev_state is None:
            prev_state = gol_state
        else:
            is_still = is_still or (prev_state == gol_state)
    return is_still


def detect_oscillators(gol_game: GOLGame):
    seen_states = set()
    is_oscillator = False
    for i, state in enumerate(gol_game):
        state_hash = hash(str(state))
        is_oscillator = is_oscillator or (state_hash in seen_states)
        seen_states.add(state_hash)
    return is_oscillator


def get_stats(gol_game):
    return {
            "is_still": detect_still_life(gol_game), 
            "is_oscillator": detect_oscillators(gol_game),
           }


def run_experiment():
    # run experiment to compare complexity vs. initial entropy levels
    num_trials = 500
    batch_size = 100
    horizon = 5000
    num_batches = (num_trials + batch_size - 1) // batch_size
    init_ps = [0.1 * i for i in range(1, 10)]  # prob. of any cell starting with life
    exp_stats = dict()
    for init_p in init_ps:
        trials_stats = defaultdict(list)
        # dispatching multiple batches to avoid accumulating GOLGames in memory
        for _ in tqdm(range(num_batches)):
            init_states = [GOLState.random_init(p=[1-init_p, init_p]) for i in range(batch_size)]
            gol_games = batched_run_gol(init_states, T=horizon)
            for gol_game in gol_games:
                trial_stats = get_stats(gol_game)
                for k, v in trial_stats.items():
                    trials_stats[k].append(v)
        # average results over trials
        for k, v in trials_stats.items():
            trials_stats[k] = np.mean(v)
        exp_stats[init_p] = trials_stats
    return exp_stats


if __name__ == "__main__":
    stats = run_experiment()
    print(json.dumps(stats, indent=2))