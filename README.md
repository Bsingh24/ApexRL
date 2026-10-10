# ApexRL
The aim of this project is to train an agent to drive a segment of the Automation Test Track successfully in BeamNG.drive. Success here means it can navigate the track segment as quickly as possible while maintaining track rules (going off-course, crashing, etc.). 
# Requirements & How to Run
* In order to run this project, you will first need BeamnNG.tech. This is different from BeamNG.drive as BeamNG.tech works alongside [BeamNGpy](https://documentation.beamng.com/api/beamngpy/master/index.html#). Without, it will make this project not run with the current code seen here. Therefore, first submit a form through [register.beamng.tech](https://register.beamng.tech/) and specify your goal with using their platform, this will help.
* Once you have BeamNG.tech, you will need to create an anaconda environment and download all the supporting libraries in `requirements.txt` using `pip install -r requirements.txt`. Then clone this repo and make sure the directory is in the same location as where you placed BeamNG in your computer.
* Run `Pipeline.ipynb` to run the simulation, you may need to change the path names but it should work afterwards.
* If you prefer to just run the model and not train everything again you can load `best.pt` in the `runs` folder as these contain the best model based on total reward. For easier navigation, the folders are named based on the date so the most recent run will be the most recent date.
# Demo Runs & Results
This project is ongoing so I will be posting new demos and updates as I improve the pipeline.
### Run 1

https://github.com/user-attachments/assets/39dbe1d9-1140-4879-be4f-9678674c29df

For the first run I based my state collection and reward function off of this [paper](https://www.nature.com/articles/s41598-025-27702-6). From this, I based my observation to collect step count, vehicle speed, steering angle, track width, track progress, centerline offset, on track indication (0 or 1), and prior steering, throttle, and brake action. I then based my reward to use the centerline offset, track progress, step count and velocity to train the agent. Lastly, the termination state which would look at whether the vehicle was damaged, off-track and took too many steps (truncated). For this specific training sequence, we ran for about 8 hours (roughly 240,000 steps). Initially, I observed the agent crashing quite frequently but around hour 5, it began to make its way towards the first turn, before failing. You can view the results via this demo. 
Something to note in particular with this run is that the model did not learn what actions to take yet. As seen in the visualizations below, the std remains high throughout training meaning the agent is still exploring and has not factored whether to throttle or brake as it mashes both at the same time when you remove the std factor. This particular demo includes std so it manages to drive but you notice it switches between throttle and brake many times. For the next run, I will update the reward system to penalize the agent if no progress is made while maintaining that same length of training. Stay tuned.

# Credits
This project uses [BeamNG.tech](https://beamng.tech/), a soft-body physics driving simulator by BeamNG GmbH, accessed through an academic license, and [BeamNGpy](https://github.com/BeamNG/BeamNGpy), the official Python API for controlling BeamNG.tech. Thanks to BeamNG GmbH for providing research access to the simulator.
