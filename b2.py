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
  print 'LeftDoor :' , self.LeftDoor
  self.RightDoor = readInfo.RightSideReading()
  print 'RightDoor :' , self.RightDoor
#  print 'RightDoor :' , self.RightDoor['902']

  #example, Left =['901','902','903'...]
  self.LeftDoorlist = sorted(self.LeftDoor.keys())
  self.Lefttemp = {k:int(k) for (k,v) in self.LeftDoor.items()}
  print 'Ltemp', self.Lefttemp
  self.RightDoorlist = sorted(self.RightDoor.keys())
  self.Righttemp = {k:int(k) for (k,v) in self.RightDoor.items()}
  print 'Rtemp', self.Righttemp
  print 'RightDoorlist :' , self.RightDoorlist

  self.left_rdx_list={}
  self.left_lux_list={}
  for i in self.LeftDoorlist:
   self.left_rdx_list[i]  = float(self.LeftDoor[i][0][0])
   self.left_lux_list[i]  = float(self.LeftDoor[i][1][0])
   print 'left_all_x : ', type(i), type(self.left_rdx_list[i]), self.left_lux_list[i]
  self.start = '901'
  self.end = '906'
  self.right_rdx_list={}
  self.right_lux_list={}
  for i in self.RightDoorlist:
   self.right_rdx_list[i]  = float(self.RightDoor[i][0][0])
   self.right_lux_list[i]  = float(self.RightDoor[i][1][0])
   print 'right_all_x : ', type(i), type(self.right_rdx_list[i]), self.right_lux_list[i]

  
  self.angle = 0 #xxx
  self.location = 'none'
  self.direction = ''
  self.touch_x = -3.0 #xxx
  self.poi_x = 0 #xxx
  self.poi_y = 0 #xxx

#  self.rangeOfstart_x = 1.44#901
#  self.rangeOfend_x = 22.59#
#  self.rangeOfy = 0
  
 def callback(self,Odometry):
  self.poi_x = round(Odometry.pose.pose.position.x, 1)
  self.poi_y = round(Odometry.pose.pose.position.y, 1)
  self.touch_x
  w = round(Odometry.pose.pose.orientation.w,3)
  x = round(Odometry.pose.pose.orientation.x,3)
  y = round(Odometry.pose.pose.orientation.y,3)
  z = round(Odometry.pose.pose.orientation.z,3)

  (roll, pitch, yaw) = tf.transformations.euler_from_quaternion([x, y, z, w])
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

 def calculate_touch_x(self, state):
   print 'calculate...***************************************8'
   print 'state is :', state
   if(state=='Left'):
     num = -1
     self.touch_x = round(self.poi_x + (num - self.poi_y)/math.tan(math.radians(self.angle)),1)
   elif(state=='Right'):
     num = 1
     self.touch_x = round(self.poi_x + (num - self.poi_y)/-math.tan(math.radians(self.angle)),1)
#   self.touch_x = round(self.poi_x + (num - self.poi_y)/((num)*math.tan(math.radians(self.angle))),1)##### -1

 def calculate_location(self, state):#state = Left/Right, 

  if state =='Left':
   self.calculate_touch_x(state)#set the value of touch_x

   LeftStart = float(self.left_rdx_list[self.start])
   LeftEnd = float(self.left_rdx_list[self.end])
   


   if (self.touch_x >= LeftStart) & (self.touch_x <= LeftEnd): # 901 -5 <  touch_x  <907 +5 -> this is rooms
      #specify the room number.
    for i in self.LeftDoorlist: # as room numbers as
        if(self.touch_x >= float(self.left_rdx_list[i])) & (self.touch_x < float(self.left_lux_list[i]) ): # error range is 1.
          self.location =  self.Lefttemp[i]
        else:
          print 'empty..'


  elif state =='Right':
    self.calculate_touch_x(state)
    RightStart = float(self.left_rdx_list[self.start])
    RightEnd = float(self.left_rdx_list[self.end])
    if (self.touch_x >= -RightStart) & (self.touch_x <= RightEnd): # 920 <  touch_x < 918
      for i in self.RightDoorlist: # as room numbers as
        if(self.touch_x >= float(self.right_rdx_list[i])) & (self.touch_x < float(self.right_lux_list[i]) ): # error range is 1.
          self.location =  self.Righttemp[i]
          break


  
 def prints(self, location, touch_x, poi_x, poi_y):
  print 'location : ' , location
  print 'touch x : ', touch_x
  print 'poi_x :', poi_x
  print 'poi_y :', poi_y
  print '##########################################'



con = Controller()
odom_sub = rospy.Subscriber('/odom', Odometry, con.callback)
rospy.init_node('wander')
rate = rospy.Rate(1000)
while not rospy.is_shutdown():
	rate.sleep()
