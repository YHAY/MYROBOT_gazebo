#!/usr/bin/env python
import rospy
import math
import tf
import geometry_msgs.msg
from	geometry_msgs.msg	import	Twist
from	sensor_msgs.msg	import	LaserScan
from std_msgs.msg import Int32
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry

LeftDoor  = ['901', '902', '903', '904', '905', '906', '907']
RightDoor = ['920','919','918','917','916']
def callback(Odometry):
	global poi_x, poi_y, touch_x        
	angle = 0
	location = 'none'
	direction = ''
        poi_x = round(Odometry.pose.pose.position.x,1)
	poi_y = round(Odometry.pose.pose.position.y,1)
	z = round(Odometry.pose.pose.orientation.z,3)
	w = round(Odometry.pose.pose.orientation.w,3)
	x = round(Odometry.pose.pose.orientation.x,3)
	y = round(Odometry.pose.pose.orientation.y,3)
	(roll, pitch, yaw) = tf.transformations.euler_from_quaternion([x, y,z,w])
	yaw_degree = math.degrees(yaw)
	if yaw_degree < 0:
		yaw_degree += 360.0
	angle = round((yaw_degree + 25) % 360,1)
	#if z*w >=0:
	#	angle =  ( abs(z) * 180)
	#	direction = 'Left'
	#else:
	#	angle =  ( (2 - abs(z)) * 180)
	#	direction = 'Right'
	#angle = (angle+30)%360
	
	if angle <= 180:
		direction = 'Left'
		#touch_x = math.tan(angle) * (-1 - poi_y) + poi_x
		#print 'touch_x : ' , touch_x
	else:
		direction = 'Right'
	print 'direction : ' , direction , 'angle : ' , angle
	if direction == 'Left':
		touch_x = round(poi_x + (-1 - poi_y)/math.tan(math.radians(angle)),1)
		if (touch_x >= -2.0) & (touch_x <= 26.0):
			for i in range(len(LeftDoor)):
				if (touch_x >= -2.0+i*4.0) & (touch_x <-2.0 +  (i+1)*4.0):
					location =  LeftDoor[i]

	elif direction == 'Right':
                touch_x = round(poi_x + (1 - poi_y)/-math.tan(math.radians(angle)),1)
		if (touch_x >= -2.0) & (touch_x <= 38.5):
			for j in range(len(RightDoor)):
				if (touch_x >= -2.0 + j*8.1 ) & (touch_x < -2.0 + (j+1)*8.1 ):
					location = RightDoor[j]
					break  
	
	
	print 'location : ' , location			
	print 'touch x : ', touch_x
	print 'poi_x :', poi_x
	print 'poi_y :', poi_y
	print '##########################################'
	#print 'roll :', roll
	#print 'pitch :', pitch
	#print 'yaw :', yaw
	#print 'yaw_degree :', yaw_degree
odom_sub = rospy.Subscriber('/odom', Odometry, callback)
rospy.init_node('wander')
rate = rospy.Rate(5)
while not rospy.is_shutdown():
	rate.sleep()
