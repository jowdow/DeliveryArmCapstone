import time
import urx
import enum
from simple_facerec import SimpleFacerec
import cv2


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


# ROBOT SENDS ERROR WHEN SENDING COMMAND TO ENTER FREE DRIVE MODE. THIS FUNCTION DOES NOT WORK
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
            joints.append(float(round(x, 2)))
        return Point(joints, name)


# Purpose: Identifying faces and comparing to current data set and if so, if they have an order
# Input(Type = SimpleFacerec,Type = Dictionary): sfr , orders
# Output(Type = String): face_name
def faceChecking(sfr, orders):
    # Load Camera
    cap = cv2.VideoCapture(0)
    prevFace = "Unknown"  # This is used to compare the current face name
    faceCount = 0  # Used to count if the same face has been detected multiple times
    while True:
        ret, frame = cap.read()  # Reading a frame from video

        # Detect Faces
        face_locations, face_names = sfr.detect_known_faces(frame)
        # Since a list is returned above this is used to prevent out of range issues
        if not face_names:  # If not faces were found
            face_name = ""
        else:
            face_name = face_names[0]  # saving first face found
        if face_name == prevFace and face_name != "":
            if faceCount <= 5:
                print(str(faceCount) + str(face_name))  # HERE STRICTLY FOR TESTING
                faceCount += 1
            else:
                if face_name != "Unknown" and face_name in orders:
                    break
        else:
            prevFace = face_name
            faceCount = 0
        # All below is for printing video out and exiting looking
        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

            cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == 27:  # Escape Key
            break
    cap.release()
    cv2.destroyAllWindows()
    return face_name


def main():
    # Encode faces from a folder
    print("Starting to encode faces")
    sfr = SimpleFacerec()
    sfr.load_encoding_images("faces/")

    programState = Modes.stop

    ACC = 0.3
    VEL = 0.3

    userOrderDict = {"joe": "A1"}  # stores the user's name and where there order is

    # This list stores all the places for misc zones
    miscPointList = [Point([0.04, -1.79, -2.26, 0.98, 1.61, 0.10], "frontPick")]
    # This list stores all the places for delivery zones
    deliveryPointList = []
    # This list stores all the places for pickup zones
    pickupPointList = [Point([0.0602, -2.523, -0.314, 4.724, 1.531, -0.250], "A1"),
                       Point([-0.2, -2.523, -0.314, 4.723, 1.531, -0.250], "A2")]

    # This is the current static IP address for the arm: 192.168.50.2
    # When doing simulation on a local machine use the IP address "LocalHost"
    robotArm = urx.Robot("LocalHost")

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

            foundUser = faceChecking(sfr, userOrderDict)
            areaName = userOrderDict[foundUser]

            robotArm.movej(miscPointList[0].jointsDegree, ACC, VEL)  # Going to Standby
            #  For safety and best practice open the gripper here
            for point in pickupPointList:
                if point.name == areaName:
                    robotArm.movej(point.jointsDegree, ACC, VEL)  # Going to Item area
                    break
            #  This is where you close the gripper
            time.sleep(1)  # Give time for the gripper to close
            robotArm.movej(miscPointList[0].jointsDegree, ACC, VEL)  # Pulling out
            robotArm.movej(deliveryPointList[0].jointsDegree, ACC, VEL)  # Going to delivery point
            #  This is where you open the gripper
            time.sleep(1)  # Give time for the gripper to close
            robotArm.movej(miscPointList[0].jointsDegree, ACC, VEL)  # Going to Standby

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
        else:
            print("That is an invalid input, please enter a number 0-5")

    # Closing connection with arm
    robotArm.close()


if __name__ == '__main__':
    main()
