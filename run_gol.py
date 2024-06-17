import subprocess
from typing import List
from tqdm import tqdm
import multiprocessing as mp

from gol import GOLState, GOLGame


def run_gol(initial_state: GOLState, T=1000, out_file="artifacts/run.gif") -> GOLGame:
    in_file = "artifacts/initial_state.txt"
    initial_state.to_txt(in_file)
    command = f"""\
life \
--in {in_file} \
--max-gen {T} \
--out {out_file} \
"""
    subprocess.run(command, shell=True)
    gol_game = GOLGame.from_gif(out_file)
    return gol_game


def batched_run_gol(initial_states: List[GOLState], T=1000, num_procs=24) -> List[GOLGame]:
    num_batches = (len(initial_states) + num_procs - 1) // num_procs
    batched_states = [initial_states[i*num_procs:(i+1)*num_procs] for i in range(num_batches)]
    gol_games = []
    for batch in tqdm(batched_states):
        procs = []
        for i, initial_state in enumerate(batch):
            out_file = f"artifacts/run_{i}.gif"
            p = mp.Process(target=run_gol, args=(initial_state, T, out_file))
            procs.append(p)
            p.start()
        for i, p in enumerate(procs):
            p.join()
            gol_games.append(GOLGame.from_gif(f"artifacts/run_{i}.gif"))
    return gol_games


if __name__ == "__main__":
    p = [0.3, 0.7]
    initial_state = GOLState.random_init(p=p)
    run_gol(initial_state)