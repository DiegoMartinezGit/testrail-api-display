from testrail import *

client = APIClient('https://dmartinez.testrail.io//testrail/')
client.user = 'diego.martinezp@mail.udp.cl'
client.password = '3y5eVEvmTSFJk77NJ62X'
projects=client.send_get('get_projects')
print(projects)