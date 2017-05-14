#!/usr/bin/env python

import rospy
import json
from std_msgs.msg import Int32
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped


FILE = "/home/haei/catkin_ws/src/MYROBOT_gazebo/json/data.json"
READ={}
DIC={}

def readJson(filename): #read json
	f = open(filename, 'r')
	js = json.loads(f.read())
	f.close()
	return js

def callback(PoseWithCovarianceStamped):
 if(PoseWithCovarianceStamped.pose.pose.position.x > DIC['901'][0][0] & PoseWithCovarianceStamped.pose.pose.position.x < DIC['901'][1][0]):
  print '901!!!!!!!'
 if(PoseWithCovarianceStamped.pose.pose.position.x > DIC['902'][0][0] & PoseWithCovarianceStamped.pose.pose.position.x < DIC['902'][1][0]):
  print '902!!!!!!!' 
 if(PoseWithCovarianceStamped.pose.pose.position.x > DIC['903'][0][0] & PoseWithCovarianceStamped.pose.pose.position.x < DIC['903'][1][0]):
  print '903!!!!!!!'
 if(PoseWithCovarianceStamped.pose.pose.position.x > DIC['904'][0][0] & PoseWithCovarianceStamped.pose.pose.position.x < DIC['904'][1][0]):
  print '904!!!!!!!'
 if(PoseWithCovarianceStamped.pose.pose.position.x > DIC['905'][0][0] & PoseWithCovarianceStamped.pose.pose.position.x < DIC['905'][1][0]):
  print '905!!!!!!!'
 if(PoseWithCovarianceStamped.pose.pose.position.x > DIC['906'][0][0] & PoseWithCovarianceStamped.pose.pose.position.x < DIC['906'][1][0]):
  print '906!!!!!!!'
 if(PoseWithCovarianceStamped.pose.pose.position.x > DIC['907'][0][0] & PoseWithCovarianceStamped.pose.pose.position.x < DIC['907'][1][0]):
  print '907!!!!!!!'
 if(PoseWithCovarianceStamped.pose.pose.position.x > DIC['917'][0][0] & PoseWithCovarianceStamped.pose.pose.position.x < DIC['917'][1][0]):
  print '917!!!!!!!'
 if(PoseWithCovarianceStamped.pose.pose.position.x > DIC['918'][0][0] & PoseWithCovarianceStamped.pose.pose.position.x < DIC['918'][1][0]):
  print '918!!!!!!!'
 if(PoseWithCovarianceStamped.pose.pose.position.x > DIC['919'][0][0] & PoseWithCovarianceStamped.pose.pose.position.x < DIC['919'][1][0]):
  print '919!!!!!!!'
 if(PoseWithCovarianceStamped.pose.pose.position.x > DIC['920'][0][0] & PoseWithCovarianceStamped.pose.pose.position.x < DIC['920'][1][0]):
  print '920!!!!!!!'

 print 'now x : ', PoseWithCovarianceStamped.pose.pose.position.x
 print 'now y : ', PoseWithCovarianceStamped.pose.pose.position.y

def saveDic():
 global FILE
 global READ
 READ = readJson(FILE)
	
 #read json then, push the value into type of Dictionary
 DIC = {
  '901':[ 
   (READ['901']['rdx'],READ['901']['rdy']),
   (READ['901']['lux'],READ['901']['luy'])
  ],
  '902':[
   (READ['902']['rdx'],READ['902']['rdy']),
   (READ['902']['lux'],READ['902']['luy'])
  ],
  '903':[
   (READ['903']['rdx'],READ['903']['rdy']),
   (READ['903']['lux'],READ['903']['luy'])
  ],
  '904':[
   (READ['904']['rdx'],READ['904']['rdy']),
   (READ['904']['lux'],READ['904']['luy'])
  ],
  '905':[
   (READ['905']['rdx'],READ['905']['rdy']),
   (READ['905']['lux'],READ['905']['luy'])
  ],
  '906':[
   (READ['906']['rdx'],READ['906']['rdy']),
   (READ['906']['lux'],READ['906']['luy'])
  ],
  '907':[
   (READ['907']['rdx'],READ['907']['rdy']),
   (READ['907']['lux'],READ['907']['luy'])
  ],
  '917':[
   (READ['917']['rdx'],READ['917']['rdy']),
   (READ['917']['lux'],READ['917']['luy'])
  ],
  '918':[
   (READ['918']['rdx'],READ['918']['rdy']),
   (READ['918']['lux'],READ['918']['luy'])
  ],
  '919':[
   (READ['919']['rdx'],READ['919']['rdy']),
   (READ['919']['lux'],READ['919']['luy'])
  ],
  '920':[
   (READ['920']['rdx'],READ['920']['rdy']),
   (READ['920']['lux'],READ['920']['luy'])
  ]
}
 #x1_901 = READ['901']['rdx']
#	y1_901 = READ['901']['rdy']
#	x2_901 = READ['901']['lux']
#	y2_901 = READ['901']['luy']

#	print "x value :" ,x1_901,y1_901
#	print "y value :" ,x2_901,y2_901
#	print "dic value :", DIC['901'][0][0], DIC['901'][0][1]

rospy.init_node('topic_subscriber')
sub = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, callback)
readJson(FILE)
saveDic()
rospy.spin()
