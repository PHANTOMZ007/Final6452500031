#!/usr/bin/env python3
from tkinter import *
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from turtlesim.srv import SetPen

frame = Tk()
frame.title("REMOTE")
frame.geometry("200x400")

rospy.init_node("Turtle_Control")
pub = rospy.Publisher("turtle1/cmd_vel", Twist, queue_size=10)
pub_motion = rospy.Publisher("Motion", String, queue_size=10)
pub_led = rospy.Publisher("Topic_LED",Int16,queue_size=10)

def status(val):
    status_text.config(text="Status: " + str(val.data))
    sub = rospy.Subscriber("status",String,callback=status)
    

def fw():
    cmd = Twist()
    cmd.linear.x = LinearVel.get()
    cmd.angular.z = 0.0
    pub.publish(cmd)
    pub_motion.publish("Fw")

def bw():
    cmd = Twist()
    cmd.linear.x = -LinearVel.get()
    cmd.angular.z = 0.0
    pub.publish(cmd)
    pub_motion.publish("BW")

def lt():
    cmd = Twist()
    cmd.linear.x = LinearVel.get()
    cmd.angular.z = AngularVel.get()
    pub.publish(cmd)
    pub_motion.publish("LT")

def rt():
    cmd = Twist()
    cmd.linear.x = LinearVel.get()
    cmd.angular.z = -AngularVel.get()
    pub.publish(cmd)
    pub_motion.publish("RT")
    
def set_pen_on():
    success = set_pen_status(True)
    if success:
        pub_motion.publish("PEN ON")
    else:
        pub_motion.publish("Failed to set pen ON")

def set_pen_off():
    success = set_pen_status(False)
    if success:
        pub_motion.publish("PEN OFF")
    else:
        pub_motion.publish("Failed to set pen OFF")
        
def set_pen_status(on):

    success = False
    rospy.wait_for_service('/turtle1/set_pen')
    try:
        set_pen = rospy.ServiceProxy('/turtle1/set_pen', SetPen)
        pen_args = SetPen()
        pen_args.r = 255  # Adjust color values as needed
        pen_args.g = 0
        pen_args.b = 0
        pen_args.width = 2
        pen_args.off = not on  # Invert on value for consistency
        response = set_pen(pen_args)
        success = response.success
    except rospy.ServiceException as e:
        print("Service call failed:", e)
        
        
LinearVel = Scale(frame, from_=0, to=2, orient=HORIZONTAL)
LinearVel.set(1)  # 1 is default value for scale
LinearVel.pack()

AngularVel = Scale(frame, from_=0, to=2, orient=HORIZONTAL)
AngularVel.set(1)  # 1 is default value for scale
AngularVel.pack()

B1 = Button(text="FW", command=fw)
B1.place(x=73, y=120)

B2 = Button(text="BW", command=bw)
B2.place(x=73, y=230)

B3 = Button(text="LT", command=lt)
B3.place(x=20, y=180)

B4 = Button(text="RT", command=rt)
B4.place(x=128, y=180)

B5 = Button(text="ON", command=set_pen_on)
B5.place(x=45, y=300)

B6 = Button(text="OFF", command=set_pen_off)
B6.place(x=100, y=300)

frame.mainloop()

