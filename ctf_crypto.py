import util
import base64
import hashlib
import os
class Level_1(object):
	hint="Come on, it's the first challenge and you already need a hint?"
	flag=util.rand_str(10)
	challenge=base64.b64encode(flag.encode("utf-8")).decode("utf-8")
	text="Decode me: {}".format(challenge)
	def __init__(self):
		self.name=self.__class__.__name__
		print("{} flag is: {}".format(self.name,self.flag))
	def verify(self,answer):
		return answer==self.flag
