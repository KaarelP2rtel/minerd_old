import unittest

def uptime(minutes):
	r=""
	dys=int(minutes/1440)
	hrs=int((minutes-dys*1440)/60)
	mns=minutes-dys*1440-hrs*60
	if dys==1:
		days=" day "
	else:
		days=" days "
	if hrs==1:
		hours=" hour "
	else:
		hours=" hours "
	if mns==1:
		mins=" minute"
	else:
		mins=" minutes"
	if dys:
		r+=str(dys)+days
	if hrs:
		r+=str(hrs)+hours
	if mns:
		r+=str(mns)+mins
	return r

class Test(unittest.TestCase):
	def test_returned_string(self):
		self.assertEqual(uptime(0),"")
		self.assertEqual(uptime(1),"1 minute")
		self.assertEqual(uptime(2),"2 minutes")
		self.assertEqual(uptime(59),"59 minutes")
		self.assertEqual(uptime(60),"1 hour ")
		self.assertEqual(uptime(120),"2 hours ")
		self.assertEqual(uptime(121),"2 hours 1 minute")
		self.assertEqual(uptime(150),"2 hours 30 minutes")
		self.assertEqual(uptime(1440),"1 day ")
		self.assertEqual(uptime(1500),"1 day 1 hour ")
		self.assertEqual(uptime(1550),"1 day 1 hour 50 minutes")
if __name__ == '__main__':
    unittest.main()