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

 def magic(self, numList):
    s = ''.join(map(str, numList))
    return int(s)

 def LeftSideReading(self):
   LeftREAD = self.readJson(self.LeftFILE)
#   LeftLists = {int(k) for(k,v) in LeftREAD.items()}
   LeftLists = LeftREAD.keys()
   print 'LeftLists ', LeftLists 
   print 'LeftLists ', LeftLists 
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
