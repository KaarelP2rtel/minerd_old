import unittest
import minerd

class Test(unittest.TestCase):
	def test_returned_string(self):
		self.assertEqual(minerd.upString(0),"")
		self.assertEqual(minerd.upString(1),"1 minute")
		self.assertEqual(minerd.upString(2),"2 minutes")
		self.assertEqual(minerd.upString(59),"59 minutes")
		self.assertEqual(minerd.upString(60),"1 hour ")
		self.assertEqual(minerd.upString(120),"2 hours ")
		self.assertEqual(minerd.upString(121),"2 hours 1 minute")
		self.assertEqual(minerd.upString(150),"2 hours 30 minutes")
		self.assertEqual(minerd.upString(1440),"1 day ")
		self.assertEqual(minerd.upString(1500),"1 day 1 hour ")
		self.assertEqual(minerd.upString(1550),"1 day 1 hour 50 minutes")
if __name__ == '__main__':
    unittest.main()