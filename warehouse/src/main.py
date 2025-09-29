from grid import Grid
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D
import numpy as np
DRONE = 0
HUMANOID = 1
def main():
    GridSizeN = int(input("Please enter the grid size n: "))
    grid = Grid(gridSizeN = GridSizeN)
    # Set of all robot indexes
    OpenList = list(range(GridSizeN*2))
    # While all robots haven't reached their goal
    while OpenList:
        OpenList = grid.roboMove(OpenList)
    paths = []    
    # Now we use the paths of all the robots, to later plot the grid
    for i in range(0,GridSizeN*2):
        print("Robot", i+1,"Type: QuadRotor" if grid.robots[i].robo_type == 0
                            else "Type: Humanoid" if grid.robots[i].robo_type == 1
                            else "Type: DiffDrive")
        print("<--- Path Taken: --->", grid.robots[i].path)
        paths.append(grid.robots[i].path)

    figure, axes = plt.subplots(figsize=(GridSizeN+5, GridSizeN))
    cellColor = np.ones((GridSizeN, GridSizeN, 3))  # White grid

    # Displays the grid in a neat manner
    def display(frame, grid):
        axes.clear()

        # White color grid
        cellColor[:, :] = [1, 1, 1]  # white for all cells
        LabelText = [[[] for _ in range(GridSizeN)] for _ in range(GridSizeN)]

        for index, path in enumerate(paths):
            if frame < len(path):
                row, col = path[frame]
                # Turqoise if waiting
                if (row,col) == path[frame - 1]:
                        cellColor[row, col] = [0, 1, 1]
                else: # Color code the robots based on their type
                    if  grid.robots[index].robo_type == DRONE: 
                        cellColor[row, col] = [0.56, 0.56,  0.93]  
                    elif grid.robots[index].robo_type == HUMANOID:   
                         cellColor[row, col] = [0.93, 0.56, 0.56]
                    else:
                         cellColor[row, col] = [0.56, 0.93, 0.56]
                if  grid.robots[index].robo_type == 0: 
                    LabelText[row][col].append(f'Q{index + 1}')  # Append robot index (R1, R2, etc.)
                elif grid.robots[index].robo_type == 1:   
                    LabelText[row][col].append(f'H{index + 1}')
                else:
                    LabelText[row][col].append(f'D{index + 1}')
                
                cell = path[-1]
                Finalrow, Finalcol = cell

                # Top border 
                axes.plot([Finalcol - 0.5, Finalcol + 0.5], [Finalrow - 0.5, Finalrow - 0.5], color='red', lw=3)

                # Bottom border 
                axes.plot([Finalcol - 0.5, Finalcol + 0.5], [Finalrow + 0.5, Finalrow + 0.5], color='red', lw=3)

                # Left border 
                axes.plot([Finalcol - 0.5, Finalcol - 0.5], [Finalrow - 0.5, Finalrow + 0.5], color='red', lw=3)

                # Right border 
                axes.plot([Finalcol + 0.5, Finalcol + 0.5], [Finalrow - 0.5, Finalrow + 0.5], color='red', lw=3)
                
                axes.annotate('', xy=(Finalcol, Finalrow), xytext=(col,row),
                       arrowprops=dict(facecolor='blue', edgecolor='green',linestyle=':', arrowstyle='->', lw=1))
        # show grid
        axes.imshow(cellColor, origin='upper')

        # grid lines
        for i in range(GridSizeN + 1):
            axes.axhline(y=i-0.5, color='black', linewidth=1)
            axes.axvline(x=i-0.5, color='black', linewidth=1)
        
        # Labels
        for row in range(GridSizeN):
          for col in range(GridSizeN):
            # Print Robot names
            if LabelText[row][col]:
                label = ', '.join(LabelText[row][col])  # Combine robot labels (e.g., "R1, R2")
                axes.text(col, row + 0.3, label, ha='center', va='center', fontsize=10, color='black', fontweight='bold')

            # Coordinates
            axes.text(col, row, f'({row},{col})', ha='center', va='center', fontsize=8, fontweight='bold')
        
            # Create custom legend proxy items (just colored patches without text)
            legend_elements = [
                Line2D([0], [0], marker='o', color='w', markerfacecolor=(0.56, 0.56, 0.93), markersize=10, label='Q: QuadRotor'),
                Line2D([0], [0], marker='o', color='w', markerfacecolor=(0.93, 0.56, 0.93), markersize=10, label='H: Humanoid'),
                Line2D([0], [0], marker='o', color='w', markerfacecolor=(0.56, 0.93, 0.56), markersize=10, label='D: DiffDrive'),
                Line2D([0], [0], marker='o', color='w', markerfacecolor=(0,1,1), markersize=10, label='Skip Turn')
            ]

        # Add legend
        axes.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.3, 1), draggable = True)
        # Current Frame
        axes.set_title(f"Frame {frame + 1}/{max(len(path) for path in paths)}, at TimeStep Interval = 3000", fontsize=10, pad=20, fontweight='bold')

    # Create the animation, showing each path in the paths list
    anim = FuncAnimation(figure, display, frames=max(len(path) for path in paths),fargs=(grid,), interval=3000, repeat=True)

    plt.show()

if __name__ == "__main__":
    main()