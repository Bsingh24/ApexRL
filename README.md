# ApexRL
The aim of this project is to train a reinforcement learning agent to drive a segment of the Automation Test Track in BeamNG.tech. Success means navigating the segment as quickly as possible while following track rules (staying on course, avoiding crashes, etc.).
# Requirements & How to Run
* **Get BeamNG.tech.** This project requires BeamNG.tech, not the regular BeamNG.drive. BeamNG.tech is the research version of the simulator, and it's the only version that works with [BeamNGpy](https://documentation.beamng.com/api/beamngpy/master/index.html#), the Python API this project uses to control the car. To request access, submit a form at [register.beamng.tech](https://register.beamng.tech/) describing how you plan to use the platform.
* **Clone this repo and set up the environment.** Clone the repo, create an Anaconda environment, then install the dependencies from inside the repo folder with `pip install -r requirements.txt`.
* **Point the code to your BeamNG.tech install.** In `Pipeline.ipynb`, set `PATH` to the folder where BeamNG.tech is installed on your computer, and update any other file paths as needed.
* Run `Pipeline.ipynb` to start the simulation and training.
* To run a trained model without retraining, load `best.pt` from a folder in `runs`. Run folders are named by date and time, so the most recent run has the latest date. `best.pt` is the model with the highest average return during that run.

# Methodology
The model used is Proximal Policy Optimization (PPO). The actor outputs the mean of three continuous actions (steering, throttle, and brake), with a learned standard deviation for each.

The simulator runs in deterministic mode at 60 Hz and is paused between actions. Each action is applied for 6 steps, so the agent makes 10 decisions per simulated second.

| Hyperparameter | Value |
|---|---|
| Steps per rollout | 2048 |
| Update epochs | 10 |
| Minibatches | 32 |
| Learning rate | 3e-4 |
| Clip coefficient | 0.2 |
| Discount | 0.99 |
| GAE | 0.95 |
| Max gradient norm | 0.5 |

# Demo Runs & Results
This project is ongoing, so I'll be posting new demos and updates as I improve the pipeline.

### Run 1

https://github.com/user-attachments/assets/39dbe1d9-1140-4879-be4f-9678674c29df

For the first run, I based my observations and reward function on this [paper](https://www.nature.com/articles/s41598-025-27702-6). The observation included step count, vehicle speed, steering angle, track width, track progress, centerline offset, an on-track indicator (0 or 1), and the previous steering, throttle, and brake actions. The reward combined centerline offset, track progress, step count, and velocity. Episodes ended when the vehicle took too much damage, went off track, or reached the step limit.

I trained for about 8 hours (roughly 240,000 steps). Early on, the agent crashed frequently, but around hour 5 it began making its way toward the first turn before failing. The demo above shows the agent at the end of this run.

The demo uses sampled actions, where each action is drawn from the actor's output. When run only using the mean action, the car doesn't move at all: the mean applies roughly half throttle and a quarter brake at the same time, which holds the car in place. The driving in the video comes largely from exploration, which is why it switches between throttle and brake so often.

The visualizations below show the policy's standard deviation only fell from 1.0 to ~0.9 over the run, meaning the agent never committed to a clear strategy. This points to a problem with the reward. 

Progress was rewarded by position, not movement. The reward paid out the car's absolute track progress every step, so stopping partway still earned reward. Additionally, centering was rewarded even while stationary. A parked car in the middle of the track earned the full centering bonus, making parking a safe way to collect reward.

For the next run, the reward will only pay for the *change* in track progress each step, so standing still earns nothing. I'll train for the same length to compare. Stay tuned.

<img width="1242" height="470" alt="Results_V1" src="https://github.com/user-attachments/assets/0fc65973-e0a9-45b5-98d6-d6f174969390" />

# Credits
This project uses [BeamNG.tech](https://beamng.tech/), a soft-body physics driving simulator by BeamNG GmbH, accessed through an academic license, and [BeamNGpy](https://github.com/BeamNG/BeamNGpy), the official Python API for controlling BeamNG.tech. Thanks to BeamNG GmbH for providing research access to the simulator.
