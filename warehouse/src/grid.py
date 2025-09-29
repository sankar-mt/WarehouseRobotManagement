from dataclasses import dataclass, field
import random

from robot import DiffDrive, Drone, Humanoid, Robot
DRONE = 0
HUMANOID = 1
DIFFDRIVE = 2
@dataclass
class Grid():
    """
    class for managing the "warehouse" as a Grid
    """
    gridSizeN: int

    robots: list[Robot] = field(default_factory=list)

    def __post_init__(self):
        # list of available positions
        available = [(x,y) for x in range(self.gridSizeN) for y in range(self.gridSizeN)]
        # copy of all cells
        tempAvailable = available.copy()
        # make n*2 random robots
        for _ in range(self.gridSizeN * 2):
            # random robot index
            ri = random.randint(1,3)
            # random start
            rp = random.randint(0, len(available)-1)
            (p_x, p_y) = available[rp]

            # random goal, but not equal to start
            rg = random.randint(0, len(tempAvailable)-1)
            while tempAvailable[rg] ==  available[rp]:
                rg = random.randint(0, len(tempAvailable)-1)
            (g_x, g_y) = tempAvailable[rg]
            
            # Should not be a start cell for next robot
            available.pop(rp)

            match ri:
                case 1:
                    bot = DiffDrive((p_x, p_y), (g_x, g_y))
                case 2:
                    bot = Drone((p_x, p_y), (g_x, g_y))
                case _:
                    bot = Humanoid((p_x, p_y), (g_x, g_y))
            # add robot to "unfinished" robot list
            self.robots.append(bot)
    # Decide the next move of the robots based on certain logics
    def decideMoves(self, OpenList):
        # Let's first create a TargetDictionary of { Target: [[Robot Index, Distance]]}
        TargetDictionary = {}
        for robots in OpenList:
            for moves in self.robots[robots].desired_moves:
                if moves in TargetDictionary.keys():
                   TargetDictionary[moves].append([robots, self.robots[robots].distance])
                else:
                     TargetDictionary[moves] = [[robots, self.robots[robots].distance]]

        # Let's decide which robots will move in the current step
        RobotsMoving = []
       
        # Iterate through the list of keys and values. 
        # Sort in descending order of their distance
        # First entry with highest distance gets to move
        # We can also allow a drone and humanoid (or) a drone and Diffdrive to move to the same cell. 
        for key, values in TargetDictionary.items():
            updatedList = []
            if len(values) > 1:
                TargetDictionary[key] = sorted(values, key=lambda x: x[1], reverse=True) # sort based on their distance
            # Now decide the first one goes. Let's see if others can make it too. 
            RobotTypeList = []
            checkZeroCount = lambda lst: lst.count(0) < 1
            for index in values: # values has (index, distance)
                if ((self.robots[index[0]].robo_type == DRONE)  and (checkZeroCount(RobotTypeList))): # If only one drone
                    if index[0] not in RobotsMoving:
                            RobotTypeList.append(self.robots[index[0]].robo_type)
                            updatedList.append(index)
                            self.robots[index[0]].path.append(key)
                            RobotsMoving.append(index[0])
                elif self.robots[index[0]].robo_type in [HUMANOID, DIFFDRIVE]:
                    if not any(rt in RobotTypeList for rt in [HUMANOID, DIFFDRIVE]):    
                       if index[0] not in RobotsMoving:
                            RobotTypeList.append(self.robots[index[0]].robo_type)
                            updatedList.append(index)
                            self.robots[index[0]].path.append(key)
                            RobotsMoving.append(index[0])
            TargetDictionary[key] = updatedList    

        # Now let's see if any robot is trying to move to (x,y) where a robot is currently skipping a turn
        # If the robot waiting is a drone, then we can allow one humanoid or one diffdrive to move to it's spot
        # Else if it is a humanoid or diffdrive, we can allow one drone to move there
        # for all other cases, we have to wait this turn             
        NewWaitStatesCreated = 1
        while NewWaitStatesCreated == 1: # Do this until we have covered all edge cases
            NewWaitStatesCreated = 0
            for RobotIndex in OpenList:
                deleteKeys = []
                deleteKeys2 = []
                if RobotIndex not in RobotsMoving: # Not moving now
                    self.robots[RobotIndex].path.append(self.robots[RobotIndex].pos) # same postion, must wait
                    found = 0 # Flag to see if we find two robots in same cell
                    
                    # find if already two robots in that cell, if so all robots with this cell as target must wait
                    for RobotI in OpenList: 
                        if RobotI!=RobotIndex:
                            if self.robots[RobotIndex].pos == self.robots[RobotI].pos:
                                found  = 1 # Found two robots in same cell
                                # Looks like already two in cell
                                for key, val in TargetDictionary.items(): # check if that position is a target for another
                                    if key == self.robots[RobotIndex].pos: # if target
                                        for index in val: # Remove all robots from this list
                                            if index[0] in RobotsMoving:
                                                RobotsMoving.remove(index[0])
                                            NewWaitStatesCreated = 1      
                                            self.robots[index[0]].path.append(self.robots[index[0]].pos)
                                            deleteKeys2.append(key)   
                                for key in deleteKeys2: # delete target key, where no robots are moving towards it. 
                                    del TargetDictionary[key]

                    if found == 0:    # Only one robot in current cell, we can check to add another
                        for key, val in TargetDictionary.items(): # check if that position is a target for another
                            if key == self.robots[RobotIndex].pos: # if it is 
                                count = 0
                                allowedRobots = []
                                for index in val: # they also have to wait
                                    if self.robots[RobotIndex].robo_type == DRONE: # if Drone
                                        if self.robots[index[0]].robo_type > DRONE and count == 0:# Allow Hum and DiffD
                                            count+=1 #don't delete
                                            allowedRobots.append(index)
                                        else:
                                            if index[0] in RobotsMoving:
                                                RobotsMoving.remove(index[0])
                                            NewWaitStatesCreated = 1
                                            self.robots[index[0]].path.append(self.robots[index[0]].pos)    
                                    elif self.robots[RobotIndex].robo_type > DRONE and count == 0: # if Hum and DiffD
                                        if self.robots[index[0]].robo_type == DRONE: # allow drone
                                            count+=1
                                            allowedRobots.append(index)
                                        else:
                                            if index[0] in RobotsMoving:
                                                RobotsMoving.remove(index[0])
                                            NewWaitStatesCreated = 1
                                            self.robots[index[0]].path.append(self.robots[index[0]].pos)    
                                    else:   
                                        if index[0] in RobotsMoving:
                                            RobotsMoving.remove(index[0])
                                        NewWaitStatesCreated = 1      
                                        self.robots[index[0]].path.append(self.robots[index[0]].pos)
                                if allowedRobots:
                                    TargetDictionary[key] = allowedRobots
                                else:    
                                    deleteKeys.append(key) # delete that target for now
                        for key in deleteKeys: # delete target key, where no robots are moving towards it. 
                            del TargetDictionary[key]   
        return TargetDictionary # Return the final {(mx,my): [[Robot index, distance]]}
    
    # Execute the robot move
    def makeMoves(self, updatedMoves):
        for key, values in updatedMoves.items():
            for index in values:
                self.robots[index[0]].pos = key
        return None        

    # Helper function to decide and make the move
    def roboMove(self, OpenList):
        # moves robots want to take
        index = 0 # index of robots
        for r in self.robots:
            if index in OpenList:
                r.distance = r.calc_distance()
                r.desired_moves = r.desired_move()
            index += 1    
        # Decide the moves we are going to make
        updatedMoves = self.decideMoves(OpenList)
        # Robot makes those moves
        self.makeMoves(updatedMoves)    

        ReachedGoal = [] # Var to identify the robots that have reached their goal

        # Update the robot positions
        for robot in OpenList:
            if self.robots[robot].pos ==  self.robots[robot].goal:
                ReachedGoal.append(robot)
        # If robots reached their goal, we can remove them from the openList
        for robot in ReachedGoal:
            OpenList.remove(robot)

        return OpenList