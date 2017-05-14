#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
'''
When the program is starting, the location set on 0
'''
'''
class image_converter:
  def __init(self, roomnum):
    self.roomnum = roomnum
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("### -----topicname ----- ###", Image, self.callback) #input topic name

  def callback(self, data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)
    (rows, cols, channels) = cv_image.shape
    cv2.circle(cv_image, (rows/2, cols/2), 10, (0,50,100),-1)
    cv2.putText(cv_image, roomnum, (30, 30),  cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
    cv2.imshow("Image window", cv_image)
    cv2.waitKey(3)

    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    except CvBridgeError as e:
      print(e)
'''
def callback(Odometry):
  con = controller()
  con.find_location(Odometry)

def scan_callback(msg):
  global g_range_ahead
  g_range_ahead = min(msg.ranges)

class controller:

 def __init__(self):
  self.LeftDoor = ['901', '902', '903', '904', '905', '906', '907']
  self.RightDoor = ['920','919','918','917','916']
  self.angle = 0
  self.location = 'none'
  self.direction = ''
  self.touch_x = -3.0
  self.poi_x = 0
  self.poi_y = 0
  self.w = 0
  self.x = 0
  self.y = 0
  self.z =0
  
 def find_location(Odometry):
  self.poi_x = round(Odometry.pose.pose.position.x, 1)
  self.poi_y = round(Odometry.pose.pose.position.y, 1)
  self.w = round(Odometry.pose.pose.orientation.w,3)
  self.x = round(Odometry.pose.pose.orientation.x,3)
  self.y = round(Odometry.pose.pose.orientation.y,3)
  self.z = round(Odometry.pose.pose.orientation.z,3)
  (roll, pitch, yaw) = tf.transformations.euler_from_quaternion([x,y,z,w])
  yaw_degree = math.degrees(yaw)
  if yaw_degree < 0:
   yaw_degree += 360.0
   self.angle = round((yaw_degree + 25) % 360,1)
  if self.angle <= 180:
   self.direction = 'Left'
  else:
   self.direction = 'Right'
   print 'direction : ' , self.direction , 'angle : ' , self.angle#방향이랑 돈 각도
  if self.direction == 'Left':
    self.touch_x = round(self.poi_x + (-1 - self.poi_y)/math.tan(math.radians(self.angle)),1)
    if (self.touch_x >= -2.0) & (self.touch_x <= 26.0):
       for i in range(len(self.LeftDoor)):
         if (self.touch_x >= -2.0+i*4.0) & (self.touch_x <-2.0 +  (i+1)*4.0):
           self.location =  self.LeftDoor[i]
  elif self.direction == 'Right':
       self.touch_x = round(self.poi_x + (1 - self.poi_y)/-math.tan(math.radians(self.angle)),1)
       if (self.touch_x >= -2.0) & (self.touch_x <= 38.5):
         for j in range(len(self.RightDoor)):
           if (self.touch_x >= -2.0 + j*8.1 ) & (self.touch_x < -2.0 + (j+1)*8.1 ):
             self.location = self.RightDoor[j]
             break
  self.prints(locationm,touch_x,poi_x, poi_y)

 def prints(self, location, touch_x, poi_x, poi_y):
  print 'location : ' , location			
  print 'touch x : ', touch_x
  print 'poi_x :', poi_x
  print 'poi_y :', poi_y
  print '##########################################'

if __name__ == "__main__":
 test = controller()
 g_range_ahead = 1 #anythingtostart
 scan_sub = rospy.Subscriber('scan', LaserScan, scan_callback) # Subscribe  "LaserScan"
 cmd_vel_pub = rospy.Publisher('cmd_vel', Twist,queue_size=1) # Publish Change location.
 odom_sub = rospy.Subscriber('/odom', Odometry, callback) # 
 rospy.init_node('wander')
 state_change_time = rospy.Time.now()
 driving_forward	= True
 rate = rospy.Rate(5)

 while not rospy.is_shutdown():
  if driving_forward:
   if (g_range_ahead < 1.0):
      driving_forward =	False
      twist = Twist()
      twist.angular.z = -1.0
      state_change_time=rospy.Time.now() + rospy.Duration(10)
   elif (poi_x == 1.4):
      driving_forward = False
      twist = Twist()
      twist.angular.z = -1.0
      state_change_time = rospy.Time.now() + rospy.Duration(5)
      rate.sleep()
      twist = Twist()
      twist.angular.z = 1.0
      state_change_time = rospy.Time.now() + rospy.Duration(5)
			    
  else:#we're not driving_forward
   if rospy.Time.now() > state_change_time:
      driving_forward = True # we're done spinning, time to go forward!
      state_change_time	= rospy.Time.now() + rospy.Duration(20)				
      twist = Twist()
      if driving_forward:
        twist.linear.x = 0.2
      else:
        twist.angular.z	= -0.3
   cmd_vel_pub.publish(twist)
   rate.sleep()
