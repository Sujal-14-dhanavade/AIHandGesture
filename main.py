import json
import cv2
from tkinter import *
from tkinter import filedialog
import os
import keyboard
import mouse
from cvzone.HandTrackingModule import HandDetector

HandGestureInfo = {}
# Dropdown menu options
options = [
    "w", "s", "d", "a", "Up", "Down", "Left", "Right", "space", "left-click", "right-click", "middle-click"
]


class GUI:
    def __init__(self, master, h, w, bgImg=None):
        self.master = master
        self.canvas = Canvas(master, height=h, width=w)
        self.canvas.pack()
        if bgImg:
            self.image = PhotoImage(file=bgImg)
            self.label = Label(self.canvas, image=self.image)
            self.label.place(x=0, y=0, relwidth=1, relheight=1)


filename = None


def selectfile():
    global filename, errorLabel, HandGestureInfo
    filename = filedialog.askopenfilename(initialdir='/', title='Select a file')
    extension = filename.split(".")[-1]
    if extension == "json":
        errorLabel = Label(errorFrame, bg='#ffffff', text=f'{filename.split("/")[-1]}', fg='#E8BCBC',
                           font=('Comic Sans MS', 15, 'bold'))
        errorLabel.place(relheight=1, relwidth=1)
        with open(filename) as f:
            HandGestureInfo = json.load(f)



    else:
        errorLabel = Label(errorFrame, bg='#ffffff', text=f'File is not json type', fg='#E8BCBC',
                           font=('Comic Sans MS', 15, 'bold'))
        errorLabel.place(relheight=1, relwidth=1)


def saveFile():
    with open("Gesture.json", "w+") as f:
        json.dump(HandGestureInfo, f)


def Set():
    global errorLabel, filename
    # hand gesture reading
    if filename:
        errorLabel = Label(errorFrame, bg='#ffffff', text='Gesture File already set', fg='#00000C',
                           font=('Comic Sans MS', 15, 'bold'))
        errorLabel.place(relheight=1, relwidth=1)
    else:
        vid = cv2.VideoCapture(0)
        vid.set(3, 600)
        vid.set(4, 400)
        detector = HandDetector(detectionCon=0.8, maxHands=1)

        while True:
            success, img = vid.read()
            img = cv2.flip(img, 1)
            hands, img = detector.findHands(img, flipType=False)
            cv2.imshow("image", img)
            k = cv2.waitKey(1)
            if k == 13:
                cv2.destroyAllWindows()
                break
        option = clicked.get()
        hands, img = detector.findHands(img, flipType=False)
        if hands:
            fingers = detector.fingersUp(hands[0])
            values = HandGestureInfo.values()
            for i in values:
                if i["type"] == hands[0]["type"] and i["fingers"] == fingers:
                    errorLabel = Label(errorFrame, bg='#ffffff', text='Gesture Already Set', fg='#00000C',
                                       font=('Comic Sans MS', 15, 'bold'))
                    errorLabel.place(relheight=1, relwidth=1)
                    return
            HandGestureInfo[option] = {"type": hands[0]["type"], "fingers": fingers}
            errorLabel = Label(errorFrame, bg='#ffffff', text='Set', fg='#00000C',
                               font=('Comic Sans MS', 15, 'bold'))
            errorLabel.place(relheight=1, relwidth=1)
        else:
            errorLabel = Label(errorFrame, bg='#ffffff', text='Show Hands for Controls Settings', fg='#00000C',
                               font=('Comic Sans MS', 15, 'bold'))
            errorLabel.place(relheight=1, relwidth=1)


def handGesture():
    root.destroy()
    # hand gesture reading
    vid = cv2.VideoCapture(0)
    vid.set(3, 600)
    vid.set(4, 400)
    detector = HandDetector(detectionCon=0.8, maxHands=2)
    values_left = list(filter(lambda x: HandGestureInfo[x]["type"] == "Left", HandGestureInfo))
    values_right = list(filter(lambda x: HandGestureInfo[x]["type"] == "Right", HandGestureInfo))
    while True:
        success, img = vid.read()
        img = cv2.flip(img, 1)

        # Find the hand and its landmarks
        hands, img = detector.findHands(img, flipType=False)  # with draw
        cv2.imshow("image", img)
        if hands:
            for hand in hands:
                handType = hand["type"]  # Hand type Left or Right
                fingers = detector.fingersUp(hand)
                if handType == "Left":
                    for i in values_left:
                        if HandGestureInfo[i]["fingers"] == fingers:
                            if i == "left-click":
                                mouse.click("left")
                            elif i == "right-click":
                                mouse.click("right")
                            elif i == "middle-click":
                                mouse.click("middle")
                            else:
                                keyboard.press(i)
                                keyboard.release(i)
                            break
                elif handType == "Right":
                    for i in values_right:
                        if HandGestureInfo[i]["fingers"] == fingers:
                            if i == "left-click":
                                mouse.click("left")
                            elif i == "right-click":
                                mouse.click("right")
                            elif i == "middle-click":
                                mouse.click("middle")
                            else:
                                keyboard.press(i)
                                keyboard.release(i)
                            break

        k = cv2.waitKey(1)
        if k == 13:
            cv2.destroyAllWindows()
            break


def control():
    Control = Toplevel()
    values = list(HandGestureInfo.values())
    keys = list(HandGestureInfo.keys())
    GUI(Control, 480, 640)
    frameKey = Frame(Control, bg='#F2D0D0', bd=5)
    frameKey.place(relx=0, rely=0, relheight=1, relwidth=1)
    list1 = Listbox(frameKey, bg='#FFE4C4', font=(
        'Comic Sans MS', 15, 'bold'))
    list1.place(relheight=1, relwidth=0.33)
    list1.insert(0, "")
    list1.insert(1, "-----------------------")
    list2 = Listbox(frameKey, bg='#FFE4C4', font=(
        'Comic Sans MS', 15, 'normal'))
    list2.place(relheight=1, relwidth=0.66, relx=0.33)
    list2.insert(0, "Data")
    list2.insert(1, "-----------------------")
    for i in range(len(keys)):
        list1.insert(i + 2, keys[i])

    for i in range(len(values)):
        list2.insert(i + 2, f"Hand Type: {values[i]['type']} <-> Fingers: {values[i]['fingers']}")

    Control.mainloop()


# tkinter window
root = Tk()
root.title("Ai Hand Gesture Setup")
a = GUI(root, 600, 1024, "bg.png")
frame = Frame(root, bg='#F2D0D0', bd=5)
frame.place(relx=0.3, rely=0.1, relheight=0.1, relwidth=0.4)
label1 = Label(frame, bg='#FC1616', text='AI HAND GESTURE', fg='#E8BCBC',
               font=('Comic Sans MS', 15, 'bold'))
label1.place(relheight=1, relwidth=1)

frameInfo = Frame(root, bg='#FC1616', bd=5)
frameInfo.place(relx=0.03, rely=0.1, relheight=0.6, relwidth=0.15)
labelInfo = Label(frameInfo, bg='#FFFFFF', text='Max Key\nBindings 12\nPress Enter for\nsetting Gesture', fg='#000',
                  font=('Comic Sans MS', 10, 'bold'))
labelInfo.place(relheight=1, relwidth=1)

# datatype of menu text
clicked = StringVar()

# initial menu text
clicked.set("w")
frameMenu = Frame(root, bg='#FC1616', bd=5)
frameMenu.place(relx=0.2, rely=0.3, relheight=0.1, relwidth=0.6)
drop = OptionMenu(frameMenu, clicked, *options)
drop.place(relheight=1, relwidth=0.6)
buttonMenu = Button(frameMenu, text="Set", command=Set)
buttonMenu.place(relx=0.6, relheight=1, relwidth=0.4)

errorFrame = Frame(root, bg='#F2D0D0', bd=5)
errorFrame.place(relx=0.2, rely=0.6, relheight=0.1, relwidth=0.6)
errorLabel = Label(errorFrame, bg='#ffffff', text='', fg='#E8BCBC',
                   font=('Comic Sans MS', 15, 'bold'))
errorLabel.place(relheight=1, relwidth=1)
frame1 = Frame(root, bg='DarkGoldenrod1', bd=3)
frame1.place(relx=0.35, rely=0.7, relheight=0.2, relwidth=0.3)
select = Button(frame1, text='S E L E C T  G A M E  G E S T U R E S', fg='sienna2', bg='Antiquewhite2',
                font=('Comic Sans MS', 7, 'bold'), command=selectfile)
select.place(relheight=0.5, relwidth=1)
save = Button(frame1, text='S A V E  G A M E  G E S T U R E S', fg='sienna2', bg='Antiquewhite2',
              font=('Comic Sans MS', 7, 'bold'), command=saveFile)
save.place(rely=0.5, relheight=0.5, relwidth=1)
frameSetting = Frame(root, bg='DarkGoldenrod1', bd=3)
frameSetting.place(relx=0.8, rely=0.45, relheight=0.08, relwidth=0.15)
Setting = Button(frameSetting, text='C O N T R O L S', fg='sienna2', bg='Antiquewhite2',
                 font=('Comic Sans MS', 10, 'bold'), command=control)
Setting.place(relheight=1, relwidth=1)
frameRun = Frame(root, bg='DarkGoldenrod1', bd=3)
frameRun.place(relx=0.9, rely=0.05, relheight=0.05, relwidth=0.08)
Run = Button(frameRun, text='R U N', fg='sienna2', bg='Antiquewhite2',
             font=('Comic Sans MS', 10, 'bold'), command=handGesture)
Run.place(relheight=1, relwidth=1)
root.mainloop()
