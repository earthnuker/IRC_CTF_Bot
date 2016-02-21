import util
import base64
import hashlib
import os
class Level_1(object):
	hint="Come on, it's the first challenge and you already need a hint?"
	flag=util.rand_str(10)
	challenge=base64.b64encode(flag.encode("utf-8")).decode("utf-8")
	text="Decode me: {}".format(challenge)
	points=10
	def __init__(self):
		self.name=self.__class__.__name__
		print("{} flag is: {}".format(self.name,self.flag))
	def verify(self,answer):
		return answer==self.flag

class Level_2(object):
	hint="Similar to the first one, but not quite"
	flag=util.rand_str(10)
	_flag=flag.ljust(len(flag)+(3-len(flag)%3),"\0").encode("utf-16")[2:]
	challenge=base64.b64encode(_flag).decode("utf-8")
	text="Decode me: {}".format(challenge)
	points=10
	def __init__(self):
		self.name=self.__class__.__name__
		print("{} flag is: {}".format(self.name,self.flag))
	def verify(self,answer):
		return answer==self.flag


class Level_3(object):
	hint="Rhymes with Wash"
	flag=util.rand_str(5)
	challenge=hashlib.md5(flag.encode("utf-8")).hexdigest()
	text="Crack me: {}".format(challenge)
	points=30
	def __init__(self):
		self.name=self.__class__.__name__
		print("{} flag is: {}".format(self.name,self.flag))
	def verify(self,answer):
		return answer==self.flag