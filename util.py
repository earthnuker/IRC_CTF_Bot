import base64
import struct
import hashlib
import random
import string
class _CS(object):
	l=string.ascii_lowercase
	u=string.ascii_uppercase
	d=string.digits
	x=string.hexdigits
	def __getattr__(self,attr):
		cs=""
		cs_chars=[n for n in dir(self) if not n.startswith("_")]
		for n in set(attr):
			try:
				cs+=self.__getattribute__(n)
			except AttributeError:
				raise RuntimeError("Invalid mask char: '{}'".format(n))
		return cs
CS=_CS()
def rand_str(l,cs=CS.dl):
	return "".join(random.choice(cs) for _ in range(l))