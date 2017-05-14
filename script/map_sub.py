#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32
from geometry_msgs.msg import PoseStamped


def callback(PoseStamped):
 print PoseStamped.pose

rospy.init_node('topic_subscriber')
sub = rospy.Subscriber('move_base_simple/goal', PoseStamped, callback)

rospy.spin()
