# exchange rate view

# exrateview.py
import httplib
import smtplib

smtpServer = 'smtp.gmail.com'
userId = 'jackyma1981@gmail.com'
password = 'thmb7890'
fromaddr = 'jackyma1981@gmail.com'
toaddrs = 'jacky_mb1103@yahoo.co.jp'

url = '/en/markets/csv/exchange_eng.csv'
conn = httplib.HTTPConnection('www.bankofcanada.ca')
conn.request('GET',url)
response = conn.getresponse()
data = response.read()
start = data.index('Japanese Yen')
end = data.index('\n',start)
line = data[start:end]

rate = line.split(',')[-1]
print start

print 'end', end

print line

print rate 
# sent the email

msg = 'Subject:Bank of canada exchange rate alert %s' %rate
server = smtplib.SMTP(smtpServer,587)
server.ehlo()
server.starttls()
server.ehlo()
server.login(userId,password)


server.sendmail(fromaddr,toaddrs,msg)
server.quit()
conn.close()

