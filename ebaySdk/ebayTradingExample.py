
def run():
	try:
		import pdb;pdb.set_trace()
	except Exception, e:
		print(e)
	return
	
from ebaysdk.trading import Connection as Trading
api = Trading(domain='api.sandbox.ebay.com',config_file='../../superSecret.yml',debug='True')
while True:
	run()