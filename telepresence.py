# Create a Telepresence robot using TurtleBot2

import rospy
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
import json
import urllib2
import roslib
import time #for sleep()

class turtlebot_telep():
	server_public_dns = 'http://ec2-52-11-246-12.us-west-2.compute.amazonaws.com/'
	
	def __init__(self):
		#initialize ros node
		rospy.init_node('turtlebot_telep', anonymous=False)

		#what to do if shut down (e.g. ctrl + C or failure)
		rospy.on_shutdown(self.shutdown)
		
	def move(self):
		
		data = json.load(urllib2.urlopen(self.server_public_dns + "/telepresence-turtlebot/api.php?read"))
		rospy.loginfo(data["action"])
		time.sleep(0.5)
		return True
		
	def shutdown(self):
		rospy.loginfo("Stop")



if __name__ == '__main__':
   move_checks = 0
   try:
       telebot = turtlebot_telep()
       #keep checking for deliver_coffee until we shutdown the script with ctrl + c
       while(telebot.move() and not rospy.is_shutdown()):
        	move_checks = move_checks + 1

   except rospy.ROSInterruptException:
        rospy.loginfo("Exception thrown")