# Overview

A fun, interactive Connect 4 game implemented in Python, where a human player competes against an intelligent AI agent. The AI uses Minimax with Alpha–Beta pruning to choose strong moves efficiently under limited computation.

## Problem

Connect 4 is a competitive, turn-based game that requires strategic planning. Building an AI agent for this game is a great way to study adversarial search, depth-limited decision-making, and how increasing lookahead improves gameplay strategy.

## Solution

This project implements a Connect 4 AI that:

Evaluates game states using Minimax

Uses Alpha–Beta pruning to reduce unnecessary computations

Allows testing different search depths (1–5) to observe performance changes

Provides a graphical interface to visualize gameplay and AI decisions

## Key Features

Human vs AI gameplay

AI agent using Minimax + Alpha–Beta pruning

Adjustable search depth (1–5)

Graphical interface using Pygame

Demonstrates the trade-off between decision quality and computation cost

## Technologies Used

Python

Pygame

NumPy

Minimax

Alpha–Beta Pruning

## Experimental Summary

Conducted 35 gameplay experiments across search depths 1 to 5

Tested move selection across all columns (1–7)

Observed improved strategic capability and winning consistency with deeper search

Highlighted increasing computation cost with higher depth

## How to run the project
1) Clone the repository
git clone https://github.com/hanshitha818/connect-4.git
cd connect-4

2) Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

3) Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

4) Run the game
python Connect-4.py


If your file name is different, replace Connect-4.py with your actual Python file name.

requirements.txt

Create a file named requirements.txt (if you don’t already have it) and add:

pygame
numpy

Notes (macOS users)

If you see a Tkinter error like:
ModuleNotFoundError: No module named '_tkinter'

install Tk support:

brew install python-tk@3.11
