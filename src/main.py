import time
import urx
import enum


# This is an enumeration that is planned to be used to tell if the arm is in running mode
# This may be thrown away with time as it might not be necessary.
class Modes(enum.Enum):
    stop = 1
    run = 2


# Custom class to allow for custom points
class Point:
    def __init__(self, joints, name):
        self.jointsDegree = joints
        self.name = name


# Purpose: Converting from degrees to radians
# Input(Type = float / list[float]): angle (In degrees)
# Output(Type = float / list[float]): angle (In radians)
def degreeToRads(angle):
    # FORMULA USED TO CONVERT FROM DEGREE TO RADS
    #  Angle in radians = Angle in degrees * (π/180)
    #  0.01745 comes from this quotient (π/180)
    if isinstance(angle, list):
        jointsAngleRads = []
        for joint in angle:
            jointsAngleRads.append(round(float(joint) * 0.01745, 2))
        return jointsAngleRads
    else:
        return round(angle * 0.01745, 2)


# Purpose: Converting from radians to degrees
# Input(Type = float / list[float]): angle (In radians)
# Output(Type = float / list[float]): angle (In degrees)
def radsToDegree(angle):
    # FORMULA USED TO CONVERT FROM RADS TO DEGREE
    #  Angle in degrees = Angle in radians * (180/π)
    #  57.29578 comes from this quotient (180/π)
    if isinstance(angle, list):
        jointsAngleDegree = []
        for joint in angle:
            jointsAngleDegree.append(round(float(joint) * 57.29578, 2))
        return jointsAngleDegree
    else:
        return round(angle * 57.29578, 2)


# Purpose: Converting from degrees to radians through print statements
# Input(): N/A
# Output(): Print statements
def printDegreeToRads():
    jointNames = ["Base", "Shoulder", "Elbow", "Wrist 1", "Wrist 2", "Wrist 3"]
    jointsAngleRads = []
    for joints in jointNames:
        print("Give %s Angle in Degrees:" % joints)
        jointsAngleRads.append(float(input()) * 0.017453)
    print("This is the angles in rads")
    count = 0
    arrayLength = len(jointsAngleRads)
    for x in jointsAngleRads:
        if count == 0:
            print("[", end='')
        if count == arrayLength - 1:
            print("{:.2f}".format(x), end='')
        else:
            print("{:.2f}".format(x), end=',')
        count += 1
    print("]")


# Purpose: Converting from degrees to radians through print statements
# Input(): N/A
# Output(Type = float / list[float]): angle (In radians)
def arrDegreeToRads():
    jointNames = ["Base", "Shoulder", "Elbow", "Wrist 1", "Wrist 2", "Wrist 3"]
    jointsAngleRads = []
    for joints in jointNames:
        while True:
            print("Give %s Angle in Degrees:" % joints, end='')
            angleRad = round(float(input()) * 0.017453, 2)
            if 6.28 > angleRad > -6.28:
                jointsAngleRads.append(angleRad)
                break
            else:
                print("%s is invalid rad")
    return jointsAngleRads


# Purpose: Validating degree angles
# Input(Type = float / list[float]): angle (In Degrees)
# Output(Type = Boolean): True / False
def validAngles(angles):
    jointNames = ["Base", "Shoulder", "Elbow", "Wrist 1", "Wrist 2", "Wrist 3"]
    for joint in angles:
        if joint > 360 or joint < -360:
            print("Angle %s is invalid, value: %s", jointNames[jointNames.index(joint)], joint)
            return False
    return True


# Purpose: Printing menu for selection
# Input(): N/A
# Output(): Print Statements
def printMenu():
    print("1) Start Program")
    print("2) something ")
    print("3) Test")
    print("4) Add Faces/Orders")
    print("5) Add Pick/Delivery Zones")
    print("0) Exit", end='')


# Purpose: Getting joints of arm through free drive mode
# Input(Type = URRobot): arm
# Output(Type = list[float]): arm.getj() (In Radians)
def setNewAreaFree(arm):
    print("You are about to enter free drive mode.")
    print("In this mode the arm will unlock and allow you to")
    print("psychically move the arm to the desired position.")
    print("After entering 'go' the arm will unlock and at that")
    print("time move the arm to the desired position. When done moving")
    print("press the enter key to lock the arm and save the position.")
    print("The free drive mode will timeout at 60 seconds if not ended.")
    print("")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("THE ARM MAY NOT BE ABLE TO SUPPORT ITS OWN WEIGHT HAVE")
    print("ONE HAND ON THE ARM WHEN YOU START FREE DRIVE MODE")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("")
    while True:
        print("Enter 'go' to start free drive mode.", end=':')
        userChoice = input().lower()
        if userChoice == "go":
            break
        else:
            print("%s is not a valid option", userChoice)
            print("")

    arm.set_freedrive(True)
    # This should start some timer that will end if the user presses "enter" however if they don't it will end the loop
    print("The arm is in free drive mode, you can move it now.")
    print("")
    print("Press the enter key to lock the arm and save the position", end=':')

    if input() == "":
        arm.set_freedrive(False)

    return arm.getj()


# Purpose: Getting joints of arm through manual manipulation
# Input(Type = URRobot): arm
# Output(Type = list[float]): arm.getj() (In Radians, rounded to the 2nd decimal place)
def setNewAreaMan(arm):
    name = input("What is the name of the position you are saving:")
    joints = []
    print("Move the arm to the desire position and then press enter to save the position")
    if input() == "":
        temp = arm.getj()
        for x in temp:
            joints.append(round(x, 2))
        return Point(joints, name)


def main():
    programState = Modes.stop

    # This list stores all of the places for delivery zones
    deliveryPointList = []
    # This list stores all of the places for pickup zones
    pickupPointList = [Point([0.0602, -2.523, -0.314, 4.724, 1.531, -0.250], "first"),
                       Point([-0.2, -2.523, -0.314, 4.723, 1.531, -0.250], "second")]

    # This is the current static IP address for the arm: 192.168.50.2
    # When doing simulation on a local machine use the IP address "LocalHost"
    robotArm = urx.Robot("192.168.50.2")

    # The below set up is a random/default for the TCP and payload.Details on the numbers to put in is in the link below
    # https://academy.universal-robots.com/modules/e-Series%20core%20track/English/module3/story_html5.html?courseId=2166&language=English
    robotArm.set_tcp((0, 0, 0.1, 0, 0, 0))
    robotArm.set_payload(2, (0, 0, 0.1))
    time.sleep(0.2)  # leave some time to robot to process the setup commands

    print("Starting Main Loop")
    while True:
        printMenu()
        print(":")
        userChoice = int(input())
        if userChoice == 1:  # Start Program:
            programState = Modes.run
        elif userChoice == 2:  # something:
            programState = Modes.stop
        elif userChoice == 3:  # Test: This is only meant to test if the pickup/delivery zone lists are working.
            for x in pickupPointList:
                print("Going to " + str(x.jointsDegree) + "      The name is " + x.name)
                robotArm.movej(x.jointsDegree, 0.1, 0.05)
        elif userChoice == 4:  # Add Faces/Orders:
            programState = Modes.stop
        elif userChoice == 5:  # Add Pick/Delivery Zones:
            # THIS ALL NEEDS TO BE VALIDATED
            areaSelection = input("Enter 0 for Pickup, 1 for delivery:")
            enteringSelection = input("Enter 0 for free drive mode, 1 for manual entering:")
            if areaSelection == "0":
                if enteringSelection == "0":
                    pickupPointList.append(setNewAreaFree(robotArm))
                elif enteringSelection == "1":
                    pickupPointList.append(setNewAreaMan(robotArm))
            elif areaSelection == "1":
                if enteringSelection == "0":
                    deliveryPointList.append(setNewAreaFree(robotArm))
                elif enteringSelection == "1":
                    deliveryPointList.append(setNewAreaMan(robotArm))
            # The data also need to be validated and I should make it so that people can enter their own joint values
            # I already made the function for this  ^
            programState = Modes.stop
        elif userChoice == 0:  # Exit: This is meant to close the program
            programState = Modes.stop
            break

        # This is a just a simple loop to test if the selection is working correctly
        while programState == Modes.run:
            print(robotArm.get_pos())
            print(robotArm.getj())
            print("")
            # start run function
            time.sleep(1)
        robotArm.close()


if __name__ == '__main__':
    main()
