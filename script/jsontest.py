import json

class ReadingInfo:
 def __init__(self):
   self.LeftFILE = '/home/haei/catkin_ws/src/MYROBOT_gazebo/json/LeftData.json'
   self.RightFILE = '/home/haei/catkin_ws/src/MYROBOT_gazebo/json/RightData.json'

  
  
 def readJson(self,filename):
   f = open(filename, 'r')
   js = json.loads(f.read())
   f.close()
   return js

 def LeftSideReading(self):
   LeftREAD = self.readJson(self.LeftFILE)
   LeftLists = LeftREAD.keys()
   DIC={}
   #read json then, push the value into type of Dictionary
   for strings in LeftLists :
     DIC.update({ strings :
                    [(LeftREAD[strings]['rdx'], LeftREAD[strings]['rdy']),
                     (LeftREAD[strings]['lux'],LeftREAD[strings]['luy'])]
                })
   return DIC
    

 def RightSideReading(self):
   RightREAD = self.readJson(self.RightFILE)
   RightLists = RightREAD.keys()
   #read json then, push the value into type of Dictionary
   DIC={}
   #read json then, push the value into type of Dictionary
   for strings in RightLists :
     DIC.update({ strings :
                    [(RightREAD[strings]['rdx'],RightREAD[strings]['rdy']),
                     (RightREAD[strings]['lux'],RightREAD[strings]['luy'])]
                })
   return DIC

if __name__ == "__main__":
        reads=ReadingInfo()
	print "LLLdic value :", reads.LeftSideReading()
	print "RRRdic value :", reads.RightSideReading()
