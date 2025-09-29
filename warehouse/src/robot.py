from dataclasses import dataclass, field

DRONE = 0
HUMANOID = 1
DIFFDRIVE = 2

@dataclass
class Robot():
    """
    base class for robots that provides non unique methods and fields
    """
    pos: tuple[int, int]
    goal: tuple[int, int]
    distance: float = field(init=False)
    desired_moves: list[int, int] = field(default_factory=list, init=False)  # List of desired move indexes
    path: list[tuple[int,int]] = field(init=False)
    robo_type : int = field(init=False)

    def __post_init__(self):
        self.path = [self.pos]
        self.distance = self.calc_distance()

    def calc_distance(self):
        (c_x, c_y) = self.pos
        (g_x, g_y) = self.goal
        return abs(c_x - g_x) + abs(c_y - g_y)

    def desired_move(self):
        """
        return the list of desired moves of the robot. Can have a maximum
        of two desired moves at every iteration.
        """
        (c_x, c_y) = self.pos
        (g_x, g_y) = self.goal
        x_diff = g_x - c_x
        y_diff = g_y - c_y

        # Possible moves: Up, Down, Left, Right
        possible_moves = []

        # Check move to the left (if applicable)
        if x_diff < 0:
            possible_moves.append((c_x - 1, c_y))
        # Check move to the right (if applicable)
        if x_diff > 0:
            possible_moves.append((c_x + 1, c_y))
        # Check move upwards (if applicable)
        if y_diff < 0:
            possible_moves.append((c_x, c_y - 1))
        # Check move downwards (if applicable)
        if y_diff > 0:
            possible_moves.append((c_x, c_y + 1))
        
        # If the robot is already at its goal, return DONE
        if (c_x, c_y) == (g_x, g_y):
            return []
        return possible_moves

class Drone(Robot):
    """
    Drone subclass
    """
    def __init__(self, pos, goal):
        super().__init__(pos, goal)
        self.robo_type = DRONE

    def __str__(self):
        return "Drone"

class Humanoid(Robot):
    """
    Humanoid subclass
    """
    def __init__(self, pos, goal):
        super().__init__(pos, goal)
        self.robo_type = HUMANOID

    def __str__(self):
        return "Humanoid"

class DiffDrive(Robot):
    """
    DiffDrive subclass
    """
    def __init__(self, pos, goal):
        super().__init__(pos, goal)
        self.robo_type = DIFFDRIVE

    def __str__(self):
        return "DifferentialDrive"
