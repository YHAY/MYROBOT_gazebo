#!/usr/bin/env python
import rospy
import math
import tf
import cv2 ###
import roslib ###
import geometry_msgs.msg
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int32
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
from cv_bridge import CvBridge, CvBridgeError ###
from sensor_msgs.msg import Image ###
import json
import jsontest

class Controller:
 def __init__(self):
  #{'902':[Right(x,y),Left(x,y)],'903':[Right(x,y),Left(x,y)],...}
  readInfo = jsontest.ReadingInfo()
  
  self.LeftDoor = readInfo.LeftSideReading()
  self.RightDoor = readInfo.RightSideReading()
  #example, Left =['901','902','903'...]
  self.LeftDoorlist = self.LeftDoor.keys()
  self.RightDoorlist = self.RightDoor.keys()

  self.angle = 0
  self.location = 'none'
  self.direction = ''
  self.touch_x = -3.0
  self.poi_x = 0
  self.poi_y = 0
  self.w = 0
  self.x = 0
  self.y = 0
  self.z = 0
  
 def callback(self,Odometry):
  self.poi_x = round(Odometry.pose.pose.position.x, 1)
  self.poi_y = round(Odometry.pose.pose.position.y, 1)
  self.touch_x
  self.w = round(Odometry.pose.pose.orientation.w,3)
  self.x = round(Odometry.pose.pose.orientation.x,3)
  self.y = round(Odometry.pose.pose.orientation.y,3)
  self.z = round(Odometry.pose.pose.orientation.z,3)

  (roll, pitch, yaw) = tf.transformations.euler_from_quaternion([self.x, self.y,self.z,self.w])
  yaw_degree = math.degrees(yaw)
  if yaw_degree < 0:
    yaw_degree += 360.0
  self.angle = round((yaw_degree + 25) % 360,1)
  if self.angle <= 180:
    self.direction = 'Left'
  else:
    self.direction = 'Right'
  print 'direction : ' , self.direction , 'angle : ' , self.angle

  self.calculate_location(self.direction)
  self.prints(self.location,self.touch_x,self.poi_x, self.poi_y)

 def calculate_location(self, state):#state = Left/Right, 
  if state =='Left':
    self.calculate_touch_x(state)
    if (self.touch_x >= -2.0) & (self.touch_x <= 26.0):
      for i in range(len(self.LeftDoor)):
        if (self.touch_x >= -2.0+i*4.0) & (self.touch_x <-2.0 + (i+1)*4.0):
          self.location =  self.LeftDoorlist[i]

  elif state =='Right':
    self.calculate_touch_x(state)
    if (self.touch_x >= -2.0) & (self.touch_x <= 38.5):
      for j in range(len(self.RightDoor)):
        if (self.touch_x >= -2.0 + j*8.1 ) & (self.touch_x < -2.0 + (j+1)*8.1 ):
          self.location = self.RightDoorlist[j]
          break

 def calculate_touch_x(self, state):
    if(state=='Left'):
     num = -1
    elif(state=='Right'):
     num = 1
    self.touch_x = round(self.poi_x + (num - self.poi_y)/math.tan(math.radians(self.angle)),1)##### -1

  
 def prints(self, location, touch_x, poi_x, poi_y):
  print 'location : ' , location
  print 'touch x : ', touch_x
  print 'poi_x :', poi_x
  print 'poi_y :', poi_y
  print '##########################################'


con = Controller()
odom_sub = rospy.Subscriber('/odom', Odometry, con.callback)
rospy.init_node('wander')
rate = rospy.Rate(5)
while not rospy.is_shutdown():
	rate.sleep()
