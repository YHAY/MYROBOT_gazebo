#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry


def callback(Odometry):
 print Odometry.pose

rospy.init_node('odom_subscriber')
sub = rospy.Subscriber('/odom', Odometry , callback)

rospy.spin()
