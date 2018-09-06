from idmm import DMMClient
if __name__ == '__main__':
	c = DMMClient('10.113.181.91:9124')
	for line in open("b.txt"):
		v = line.strip().split()
		msgid,pubid,pubtopic,groupid = v[0],v[1],v[2],v[3]
		c.send_commit(pubtopic,pubid,msgid)

