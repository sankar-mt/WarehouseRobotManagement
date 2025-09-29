# CP1_Skynet: Cade Lueker, Mani Sankar Thirugana Muthuvelan, Aaron Pineda
ROBO5000 Challenge Problem 1: Warehouse Robot Management

This project will showcase a scalable and robust warehouse robot navigation algorithm that is capable of managing 2*n robots within an nxn sized grid. The basis for the algorithm will be a greedy shortest path algorithm that avoids any sort of robotic collisions

# Directions for Running the Program

- the environment tool we used is called `uv` and serves as a pip / conda replacement
- this environment is located in our `warehouse/` directory where packages and versions are specified
- the project requirements are specified below, copied from "warehouse/pyproject.toml"

```
[project]
name = "warehouse"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "matplotlib>=3.10.6",
    "numpy>=2.3.3",
    "pyright>=1.1.404",
]
```

- if these are installed on your machine simply `python warehouse/src/main.py` will run our project
    - it will start a prompt asking for grid size
    - once grid size is entered it will execute the animation
    - if for whatever reason this doesn't work (which it should) try running from the `warehouse/` directory
        - ie `python src/main.py`
- if you happen to be using `uv` you can `uv run src/main.py` from the `warehouse/` directory
## Animation might take a lot of RAM:
- If your system is low on RAM, the animation might take time to show or maybe slow down your system. If it seems to hang, try running the program again by closing all other heavy applications. Sometimes due to the inbuilt functions of the animation libraries, it tends to not open quick enough, especially for n size >= 10. Try running the program again, it should display the animation. 
