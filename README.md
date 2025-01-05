# Movable Cellular Automaton for Disease Spread Prediction

This project is a simulation of a movable cellular automaton designed to predict disease spread. The cells can move randomly, collide with each other, and some cells can be infected, allowing for interaction between infected and non-infected cells.

## Features

- Highly customizable simulation parameters, grouped into:
    - Basic simulation parameters: Adjust the total number of cells, cycles per day, and more.
    - Infection parameters: Configure the infection probability, death probability.
    - Cell parameters: Define movement speed, cell infection radius.
    - Multiple runs: Ability to run the simulation multiple times for representative results.
- Cells move randomly in one of three distinct 2D spaces: Office, Open Area, or Trench.
- Infected cells can infect other cells upon collision.
- Cells bounce off the walls and each other.

## Prerequisites

Make sure you have Python installed on your system. This project is built using Python and Pygame.

## Installation

1. Clone the repository (or download the zip file) to your local machine using Git:

   ```bash
   git clone https://github.com/Fllugel/Movable-Automa-Disease-Spread-Simulation
   cd repository-name

2. Install the required packages using pip:
   ```bash
   pip install -r requirements.txt

## Usage

Run the main.py file to start the simulation:

   ```bash
   python main.py
   ```

After running the script, an interface window will open, where you can choose the 2D space for the simulation: Office, Open Area, or Trench. 

Once you select a space, you can start the simulation, showing cells interacting dynamically in the chosen environment. Additionally, you can save the simulation's acquired data to your device for analysis.