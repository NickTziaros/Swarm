#!/usr/bin/env python
import	rospy
import 	sys
import 	math
from 	geometry_msgs.msg import Twist,Point
from 	nav_msgs.msg import Odometry
import	smach
import  smach_ros
import	time
from 	robot_Class import robot


# while not rospy.is_shutdown():	
args=rospy.myargv(argv=sys.argv)
robotname= args[1]
	# speed=Twist()
	
	# def go():
	# 	speed.linear.x=0.1
	# def stop():
	# 	speed.linear.x=0

# States of state machine
#----------------------------------------------------------------------------------------------------------

	#Define Attraction State
class Attract(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['finished','failed'])
		self.subscriber = rospy.Subscriber("/{}/odom".format(robotname),Odometry,self.callback)
		global r
		r=robot(robotname)	

	def callback(self,msg):
                        
		self.robot_pose_x=msg.pose.pose.position.x
		self.robot_pose_y=msg.pose.pose.position.y
		# rospy.loginfo("Odom {} {}".format(self.robot_pose_x,self.robot_pose_y))

	def execute(self, userdata):
		# Publishes speed and waits 2 secs
		rospy.loginfo('Changing to..')
		r.go()
		# pub.publish(speed)
		time.sleep(2)
		return 'finished'

class Repulse(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['finished', 'failed'])

	def execute(self, userdata):
		# Publishes speed and waits 2 secs
		rospy.loginfo('Change to Attract')
		r.turn_left()
		# pub.publish(speed)
		time.sleep(2)
		return 'finished'


# Initializations of SM && publishers
# -------------------------------------------------------------------------------------------------------------




 
if __name__ == '__main__':		


# Initialize node
	rospy.init_node('State_machine_node')
	sm =smach.StateMachine(outcomes=['I_have_finished'])
	pub = rospy.Publisher("/{}/cmd_vel".format(robotname),Twist, queue_size=10)


	
# Create and start the introspection server for visualising state machine

	sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
	sis.start()




	# Adding states
	with sm:
		smach.StateMachine.add('Attract', Attract(),
                                transitions={'finished': 'Repulse', 'failed': 'Attract'})
		smach.StateMachine.add('Repulse', Repulse(),
                                transitions={'finished': 'Attract', 'failed': 'Repulse'})
		# smach.StateMachine.add('Attract',CBState(Attract_state_callback),{'finished':'Repulse', 'failed':'Attract'})
		# smach.StateMachine.add('Repulse',CBState(Repulse_state_callback),{'finished':'Attract', 'failed':'Repulse'})



	# Start State_Machine
	outcome =sm.execute()
	sis.stop()
	rospy.spin()









