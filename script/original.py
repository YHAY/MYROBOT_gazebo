#!/usr/bin/env	python
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
def	scan_callback(msg):
	global	g_range_ahead
	g_range_ahead	=	min(msg.ranges)
def callback(Odometry):
	global poi_x, poi_y        
	angle = 0
	location = 'none'
	direction = ''
	touch_x = -3.0
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
                                        print 'now i is : ' , i, LeftDoor[i]

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
g_range_ahead	=	1	#	anything	to	start
scan_sub	=	rospy.Subscriber('scan',	LaserScan,	scan_callback)
cmd_vel_pub	=	rospy.Publisher('cmd_vel',	Twist,	queue_size=1)
odom_sub = rospy.Subscriber('/odom', Odometry , callback)
rospy.init_node('wander')
state_change_time	=	rospy.Time.now()
driving_forward	=	True
rate	=	rospy.Rate(5)
while   not rospy.is_shutdown():
		if  driving_forward:
				if  (g_range_ahead	<   1.0):
						driving_forward	=	False
						twist = Twist()
						twist.angular.z = -1.0
						state_change_time	=	rospy.Time.now()	+	rospy.Duration(10)
				elif    (poi_x == 1.4):
						driving_forward = False
						twist = Twist()
						twist.angular.z = -1.0
						state_change_time = rospy.Time.now() + rospy.Duration(5)
						rate.sleep()
						twist = Twist()
						twist.angular.z = 1.0
						state_change_time = rospy.Time.now() + rospy.Duration(5)
			            
			    
		else:	#	we're	not	driving_forward
				if	rospy.Time.now()	>	state_change_time:
						driving_forward	=	True	#	we're	done	spinning,	time	to	go	forward!
						state_change_time	=	rospy.Time.now()	+	rospy.Duration(20)				
		twist	=	Twist()
		if	driving_forward:
				twist.linear.x	=	0.2
		else:
				twist.angular.z	=	-0.3
		cmd_vel_pub.publish(twist)
		rate.sleep()
