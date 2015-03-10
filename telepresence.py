#!/usr/bin/env python

'''
Copyright (c) 2015, Mark Silliman
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

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
		
		cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
		move_cmd = Twist()
		move_cmd.angular.z = 0 # turn at radians/s
		move_cmd.linear.x = 0 # forward at m/s
		
		if(data["action"] == "forward"):
			move_cmd.linear.x = 0.2
		if(data["action"] == "left"):
			move_cmd.angular.z = 0.6
		if(data["action"] == "right"):	
			move_cmd.angular.z = -0.6
		if(data["action"] == "reverse"):
			move_cmd.linear.x = -0.2
		
		cmd_vel.publish(move_cmd)
			
		#avoid overloading server by only requesting every 250 msec
		time.sleep(0.25) 
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