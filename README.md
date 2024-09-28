# Drone Simulation and Image Capture in Unreal Engine with AirSim and Model Prediction

This documentation outlines the steps required to reproduce a drone simulation and image capture environment using Unreal Engine 4.27 and AirSim, followed by image processing with Python scripts. This setup is useful for testing and evaluating depth estimation models in a controlled virtual environment.

## Prerequisites

Before proceeding, ensure that your system meets the following requirements:

- **Operating System**: Windows 10 or later, or a Linux distribution that supports Unreal Engine.
- **Hardware**: A computer with at least 8GB of RAM and a dedicated graphics card.

## Installation Guide

### Step 1: Install Unreal Engine 4.27
- **Download**: Visit the [Unreal Engine download page](https://www.unrealengine.com/download) and download the Epic Games Launcher.
- **Installation**: Install Unreal Engine 4.27 through the Epic Games Launcher. Select the version from the library section and choose 'Install'.

### Step 2: Install AirSim
AirSim is a simulator for drones, cars, and more, built on Unreal Engine. It is open-source and cross-platform.

- **Clone or Download**: Obtain the AirSim repository from [GitHub](https://github.com/microsoft/AirSim).
- **Setup**: Follow the detailed setup instructions provided in the [AirSim documentation](https://microsoft.github.io/AirSim/) to integrate AirSim with Unreal Engine. This usually involves running `build.cmd` on Windows or `./setup.sh` and `./build.sh` on Linux.

### Step 3: Install Python
Ensure Python version 3.8 or higher is installed on your system.

- **Download**: Visit the [official Python website](https://www.python.org/downloads/) to download and install Python.

### Step 4: Open the Unreal Engine Project
- **Location**: Navigate to the `AirSim/Unreal/Environments/Blocks` directory inside the downloaded AirSim repository.
- **Project File**: Double-click on the `blocks.uproject` file to open the project in Unreal Engine.

### Step 5: Initial Setup in Unreal Engine
- **Launch**: Press the 'Play' button in Unreal Engine. A drone should appear idle on the ground within the Blocks environment.

## Running Python Scripts

### Step 6: Install AirSim Python Package
- **Command**: Open a command prompt or terminal and run `pip install airsim` to install the AirSim client Python package.

### Step 7: Script Execution
- **Location**: Navigate to the `py_scripts` directory where the Python scripts are stored.
- **Terminals**: Open two separate terminal windows for running different scripts simultaneously.

#### Terminal 1: Run `motion_controller.py`
- **Execution**: Type `python motion_controller.py` in the terminal. This script controls the drone's movement along a predefined path.

#### Terminal 2: Run `capture_images.py`
- **Execution**: Immediately after starting the motion controller script, run `python capture_images.py` in the second terminal. This script captures stereo images (left and right) and depth maps while the drone is moving. The images are saved in the `output_data` folder for a duration of 22 seconds.

## Model Execution and Evaluation

### Step 8: Install Model Requirements and Run Models
- For each depth estimation model (Dispnet, Monodepth, PSMNet):
  - Navigate to the respective model's folder.
  - Run `pip install -r requirements.txt` to install dependencies.
  - Execute the main script of the model to process images in `output_data` and store results in model-specific output directories.

### Step 9: Analyze Model Performance
- **Script**: Return to the main folder and execute `models_eval.py`. This script analyzes the performance of each model and generates three types of graphs:
  - Model Comparison Chart
  - Average Depth Prediction Chart
  - Error Map (highlighting areas with significant depth prediction errors)

## Conclusion
By following these steps and ensuring all components are correctly installed and scripts properly executed, you can achieve reproducibility in your drone simulation and image capture project. This setup enables the evaluation of various depth estimation models in a consistent and controlled environment.
