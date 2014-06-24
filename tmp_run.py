from display_image.sky_manifest import ManifestReader
fn = "C:/Users/User/SGIS_CLONE/grrrrr/spreadsheets/MEE2_ebay_pallets.csv"
input_fn = 'tmp_input.txt'
class MainFrame(object):
    def __init__(self):
        pass
reader = ManifestReader(fn,MainFrame())
reader.MainFrame.threading = True

#--------------------------------------
# Read through and grab a list of lines from a csv
#-------------------------------

with open(input_fn) as f:
    sku_list = f.readlines()
# import pdb;pdb.set_trace()

key = 'msrp'
tmp_list = []
for f_sku in sku_list:
    try:
        sku = f_sku.split('-')[0]
        result = reader.returnRowBySku(sku)
        index = result[0].index(key)
        tmp_list.append(result[1][index])
        # print(result)
        #result[1] = [x.rstrip('/r/n') for x in result[1]]
        # result[1] = result[1]+[f_sku]+['/n']
    except Exception, e:
        print(e)
        pass

with open('tmp_output.csv','w+') as f:        
    f.write('\n'.join(tmp_list))
 
 