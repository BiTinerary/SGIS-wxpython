import httplib
import urllib2
import traceback
import os
import csv

def readFile(fp):
    '''
    read file from fp
    '''
    with open(fp, 'r')as f:
        lines = f.readlines()
    return lines


def returnResponseRequestPair(refNumber):
    '''
    return file paths for response and request pairs based on ref number
    '''
    responseRequestDir = 'C:\\Users\\User\\Downloads'
    pair = []
    for f in os.listdir(responseRequestDir):
        if refNumber in f:
            fp = os.path.join(responseRequestDir, f)
            pair.append(fp)
    return pair

def returnRefNumber():
    '''
    return last line of reference number file.
    '''
    fp = 'C:\\Users\\User\\Desktop\\Photos\\MEE_6668-687\\MEE_received\\MEE_spreadsheets\\reportHandlers\\VerificationRequestResults\\verifyRequestRefNumber.csv'
    with open(fp, 'r') as f:
        lines = f.readlines()
    return lines[-1].split(',')[-1].rstrip('\r\n')

def combinePair(pair_dict):
    '''
    given pair_dict combine pair
    '''
    request_lines = pair_dict['request_lines']
    response_lines = pair_dict['response_lines']
    request_reader = csv.reader(request_lines)
    response_reader = csv.reader(response_lines)

    request_list = []
    for line in request_reader:
        line[-1] = line[-1].rstrip('\r\n')
        request_list.append(line)

    # response list had an extra column after headers?? wth.
    # this checks the length of headers and if following rows are > subtract dif
    response_list = []
    count = 0
    for line in response_reader:
        if count == 0:
            start_len = len(line)
            print(start_len)
            count = None
        if start_len == len(line):
            response_list.append(line)
        elif start_len < len(line):
            dif = start_len - len(line)
            response_list.append(line[:dif])
    # not sure how to handle quote characters so this
    line_list = []
    for index in xrange(0,len(request_list)):
        line = []
        for x in response_list[index]:
            line.append(x)
        for x in request_list[index]:
            line.append(x)
        line_list.append(line)
    # tmp file
    with open('HALP.csv','wb') as f:
        writer = csv.writer(f)
        writer.writerows(line_list)

    return

def returnErrors():
    '''
    opens tmpfile 'HALP.csv'
    reads rows and checks headers
    returning a list of rows
    '''
    # open tempfile
    f = open('HALP.csv','rb')
    reader = csv.reader(f)
    header = reader.next()
    index_list = [ 'ErrorCode',
                   'CustomLabel',
                   '*CustomLabel',
                   'ErrorMessage',
                   'ItemID',
                   'Action',
                   'Status',
                   '*Category',
                   '*Title']

    header_dict_indexes = {}
    for index in index_list:
        header_dict_indexes.update({index:header.index(index)})

    # from paired line grab index_list and fill a line for item specifics archive
    failed_item_specifics = []
    successful_items = []
    unhandled_errors = []
    for line in reader:
        ErrorCode = line[header_dict_indexes['ErrorCode']]
        # ErrorCode: 21916519 ... item specifics missing
        if '21916519' in ErrorCode:
            cell_contents = []
            # create empty line
            for cell in line:
                cell_contents.append('')
            # fill empty line with index_list contents
            for header_key in header_dict_indexes:
                cell_contents[header_dict_indexes[header_key]] = line[header_dict_indexes[header_key]]
            jnumber = returnJnumberFromListing(fullSku)
            cell_contents[header_dict_indexes['CustomLabel']] = jnumber
            failed_item_specifics.append(cell_contents)
        elif len(ErrorCode) is 0:
            successful_items.append(line)
        else:
            unhandled_errors.append(line)

    f.close()
    # remove tmp file
    os.remove('HALP.csv')
    return header, failed_item_specifics, successful_items, unhandled_errors


def returnJnumberFromListing(fullSku):

    jnumber_url = 'http://192.168.0.170/'+fullSku+'/jnumber.txt'
    print(jnumber_url)
    httplib.HTTPConnection.debuglevel = 1
    try:
        try:
            request = urllib2.Request(jnumber_url)
        except HTTPError, e:
            print(e)
            print(traceback.format_exc())
            return None
        request.add_header('User-Agent','jmunsch_thnx_v2.0 +http://jamesmunsch.com/')
        opener = urllib2.build_opener()
        data = opener.open(request).read()
        print(repr(data))
        print(type(data))
        print "Fetched."
    except Exception, e:
        print(e)
        print(traceback.format_exc())
    return data
