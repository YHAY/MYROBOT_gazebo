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
  #readJson
  readInfo = jsontest.ReadingInfo()

  # {u'902': [(u'1.45', u'0'), (u'5.00', u'0')], u'903': [(u'5.01', u'0'), (u'8.28', u'0')], ...}
  self.LeftDoor = readInfo.LeftSideReading()
  self.RightDoor = readInfo.RightSideReading()

  #example, LeftDoorlist =[u'901', u'902', ...]
  self.LeftDoorlist = readInfo.LeftDoorlist()

  #{u'902': 902, u'903': 903, ...} '902' match with int('902')
  self.Lefttemp = readInfo.LeftTemp()

  #[u'916', u'917', u'918', u'919', u'920']
  self.RightDoorlist = readInfo.RightDoorlist()

  #{u'920': 920, u'917': 917, ...}
  self.Righttemp = readInfo.RightTemp()

  # <type 'dict'> {u'902': 1.45, u'903': 5.01, u'901': 0.0,...}
  self.left_rdx_list={}
  self.left_lux_list={}
  self.left_rdx_list = readInfo.left_rdx_list()
  self.left_lux_list = readInfo.left_lux_list()

  # <type 'dict'> {u'920': 0.0, u'917': 20.18, u'916': 0.0, ...}  
  self.right_rdx_list={}
  self.right_lux_list={}
  self.right_rdx_list = readInfo.right_rdx_list()
  self.right_lux_list = readInfo.right_lux_list()
  print 'self.right_rdx_list>>>? ', type(self.right_rdx_list), self.right_rdx_list

  self.Leftstart = '901'
  self.Leftend = '907'
  self.Rightstart = '916'
  self.Rightend = '920'

  self.angle = 0 #xxx
  self.direction = ''
  self.touch_x = -3.0 #xxx
  self.poi_x = 0 #xxx
  self.poi_y = 0 #xxx

  
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

   if(state=='Left'):
     self.touch_x = round(self.poi_x + ((-1) - self.poi_y)/math.tan(math.radians(self.angle)),1)
   elif(state=='Right'):
     self.touch_x = round(self.poi_x + (1 - self.poi_y)/-math.tan(math.radians(self.angle)),1)



 def calculate_location(self, state):#state = Left/Right,
  self.location = 'none'

  if state =='Left':
   self.calculate_touch_x(state)#set the value of touch_x
   print 'touch_x is :', self.touch_x

   LeftStart = self.left_rdx_list[self.Leftstart]
   LeftEnd = self.left_lux_list[self.Leftend]
   print 'LeftStart, End : ', LeftStart, LeftEnd

   if (self.touch_x >= LeftStart) & (self.touch_x <= LeftEnd): # 901 -5 <  touch_x  <907 +5 -> this is rooms #specify the room number.
    for i in self.LeftDoorlist: # as room numbers as
        
        if(self.touch_x >= float(self.left_rdx_list[i])) & (self.touch_x <  + float(self.left_lux_list[i]) ): # error range is 1.
           print 'float(self.left_rdx_list[i]) is :', float(self.left_rdx_list[i]), float(self.left_lux_list[i])
           self.location = i #Lefttemp
           break
       
  elif state =='Right':
    self.calculate_touch_x(state)
    print 'touch_x is :', self.touch_x

    RightStart = float(self.right_rdx_list[self.Rightstart])
    RightEnd = float(self.right_lux_list[self.Rightend])
    print 'RightStart, End : ', RightStart, RightEnd

    if (self.touch_x >= -RightStart) & (self.touch_x <= RightEnd): # 920 <  touch_x < 918
      for i in self.RightDoorlist: # as room numbers as

        if(self.touch_x >= -2.0 + float(self.right_rdx_list[i])) & (self.touch_x < -2.0 + float(self.right_lux_list[i]) ): # error range is 1.
          print 'now float(self.right_rdx_list[i] is :', float(self.right_rdx_list[i]), float(self.right_lux_list[i])
          self.location =  i
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
rate = rospy.Rate(100000)
while not rospy.is_shutdown():
	rate.sleep()

