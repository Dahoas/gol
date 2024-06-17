# GOL 

## Design

Can simply represent as an arbitrarily sized numpy array?

How to design hypothesis function?
- f should take in the experiment and spit out a boolean. It is an evaluation criteria
- The experiment will produce a results object 
- the hypothesis_verifier will take in the results and spit out a bool

GOL format options:
- RLE format: x = 3, y = 3, rule = B3/S23, bo$2bo$3o!
- markdown table

How to represent structure?
- maybe best to examine structures in isolation. Looking at structures in a big soup seems much more difficult

Perhaps each observation is just a function from the state -> value. 
- so then each structure will have a set of properties defined as certain 
e.g. the glider satisfies bounding box == 3,3 and moves right every four ticks

## Observations

List of structures gpt-4 can implement(pass@1, drawing markdown, full context):
- glider
- block
- beehive
- blinker
- toad

Cannot do:
- loaf
- boat
- LWSS (light-weight spaceship)
- Methuselah (r-pentomino)
- gun
- rake
- breeder

## Goals

What do I hope to do with the LLM in gol?

Could also consider fine-tuning llm to model gol world dynamics

Can I use curriculum prompting to implement more complex structures?

Could study gpt-4 on general cellular automata?

"The game of life as a microcosm for scientific discovery with gpt-4"

Things we can do:
- exploration: discovering new trajectories (note: we are defining novelty at the trajectory level. the temporal component is important)
    - modeling the evolution of interest
- scientific discovery:
    - classification (taxonomy of trajectories)
    - prediction (of the higher-level dynamics e.g. what initial configurations tend to result in what state)
        - perhaps both can be thought of as knowledge extraction from the archive (the archive already implicitly does classification)
            - hypothesis testing: what happens when I do "x"?
- applied science/research (goal directed generation):
    - how to set an initial state to achieve a particular dynamic?

Maybe we should make a benchmark of scientific deductions? (what can gpt-4 learn/deduce in an environment?)
- but is the game of life really the best setting for this?
- maybe could take an ensemble of llm exploration to form the benchmark (this is some analgoue of train set coverage?)

Maybe hypothesis generation is a way to solve the grounding issue?
- there should probably be some kind of hypothesis verification step
- what happens if I instruct gpt-4 to be very skeptical?

## Related work

Related work (LLMs + gol):
- https://www.strangeloopcanon.com/p/what-can-llms-never-do
    - neural network seem to struggle to model gol (when trained or in-context)
- https://news.ycombinator.com/item?id=36463564