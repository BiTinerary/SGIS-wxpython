import imaplib
import email
import datetime
import sys


def returnUsernamePassword():
    with open('../../really_secret_gmail.txt', 'r') as f:
        lines = f.readlines()[0]
    return lines.split(',')

def process_mailbox(mail):
    # import pdb;pdb.set_trace()
    tmp_list = []
    rv, data = mail.search(None, "ALL")
    if rv != 'OK':
        print "No messages found!"
        #return

    for num in data[0].split():
        rv, data = mail.fetch(num, '(RFC822)')
        if rv != 'OK':
            print "ERROR getting message", num
            #return

        msg = email.message_from_string(data[0][1])
        # print(msg)
        print 'Message %s: %s\n%s' % (num, msg['Subject'], msg['Body'])
        print 'Raw Date:', msg['Date']
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(
                email.utils.mktime_tz(date_tuple))
            print("Local Date:", 
                    local_date.strftime("%a, %d %b %Y %H:%M:%S"))
        tmp_list.append(str(msg))
    ref_list = []
    for ref_number in tmp_list:
        ref_number = ref_number.split('http://bulksell.ebay.com/ws/eBayISAPI.dll?FileExchangeDownload&amp;RefId=')[-1].split('&amp;uname=pointonepremiums')[0]
        ref_list.append(ref_number)
    return ref_list

def returnDownloadLinks():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    try:
        mail.login(username, password)
    except imaplib.IMAP4.error:
        print "LOGIN FAILED!!! "
    rv, mailboxes = mail.list()
    if rv == 'OK':
        print "Mailboxes:"
        print mailboxes
    rv, data = mail.select("downloadcenter")
    if rv == 'OK':
        print "Processing mailbox...\n"
        results = process_mailbox(mail)
    mail.logout()
    return results

values = returnUsernamePassword()
username = values[0]
password = values[1].rstrip('\r\n')

print(returnDownloadLinks())


# Example output/results
# Message 61: Items Paid and Shipped Download Request Completed
# None
# Raw Date: Fri, 27 Jun 2014 01:32:03 -0700
# ('Local Date:', 'Fri, 27 Jun 2014 03:32:03')
# ['22882429', '22895772', '22909055', '22926443', '22939692', '22952425', '22964206', '22977346', '22991094', '23004692', '23018784', '23032648',
# '23045577', '23057130', '23070445', '23084800', '23098715', '23112425', '23127368', '23140663', '23152151', '23165699', '23179850', '23193729', '
# 23207423', '23221382', '23234192', '23245058', '23256400', '23267933', '23281165', '23294892', '23308758', '23321936', '23338244', '23351598', '2
# 3366319', '23380418', '23394565', '23408585', '23421961', '23433442', '23446592', '23460709', '23474734', '23488636', '23502658', '23515921', '23
# 527394', '23540569', '23554246', '23567867', '23581424', '23595175', '23608434', '23619925', '23633111', '23647271', '23661190', '23674576', '236
# 87438']
# ------------------
# Next
# Concatenate url
# Download url
# compile
