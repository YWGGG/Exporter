# coding=utf-8 

import os
import shutil
import argparse
import urllib.request
import subprocess
import xlwt

stuDict = {}
testflag = False

# correctDict_1 = {"2.2.2.2:1080":0,"2.2.2.3:1080":0}
# wrongDict_1 = {"2.2.2.4":0, "2.2.2.5":0, "2.2.2.6":0, "2.2.2.7":0}

correctDict_1 = {"112.80.248.76:1080":0,"112.80.248.77:1080":0,"112.80.248.78:1080":0,"112.80.248.79:1080":0}
wrongDict_1 =  {"112.80.248.76:80":0,"112.80.248.77:80":0,"112.80.248.78:80":0,"112.80.248.79:80":0,"112.80.248.76:180":0,"112.80.248.77:180":0,"112.80.248.78:180":0,"112.80.248.79:180":0}

#hwk2
#1. Correct 192.168.1.5:65404 login 1.2.3.4:1
#2. Correct 192.168.1.5:65516 Initial 255.255.255.255:65535

#3. Wrong 192.168.1.5:49276 1.2.3.4:10
#4. Wrong 192.168.1.5:49353 login
#5. Wrong 192.168.1.5:49395 Initial
#6. Wrong 192.168.1.5:49450 login 123.4567.7.4:666
#7. Wrong 192.168.1.5:49496 login 999.999.999.999:999

# correctDict_2 = {"192.168.1.5:65404":0,"192.168.1.5:65516":0}
# wrongDict_2 = {"192.168.1.5:49276":0, "192.168.1.5:49353":0, "192.168.1.5:49395":0, "192.168.1.5:49450":0, "192.168.1.5:49496":0}
correctDict_2 = {"1.1.1.1:3399":0,"2.2.2.2:3399":0,"3.3.3.3:3399":0,"4.4.4.4:3399":0,"5.5.5.5:3399":0,"6.6.6.6:3399":0}
wrongDict_2 = {}


correctDict_3 = {"180.102.61.144":0}
wrongDict_3 = {"132.232.111.21":0,"192.81.128.138":0}

correctDict_4 = {"114.222.109.234":0}
wrongDict_4 = {"132.232.111.21":0,"192.81.128.138":0,"129.211.172.252":0,"10.206.0.2":0}

correctDict_5 = {}
wrongDict_5 = {}

ccDict = {1:correctDict_1, 2:correctDict_2, 3:correctDict_3, 4:correctDict_4, 5:correctDict_5}
wrDict = {1:wrongDict_1, 2:wrongDict_2, 3:wrongDict_3, 4:wrongDict_4, 5:wrongDict_5}

def initAnswer5():
	with open("testdga.txt") as f:
		for line in f:
			line = line.strip()
			if line.startswith("#") or line == "":
				continue
			correctDict_5[line] = 0
	with open("testnotdga.txt") as f:
		for line in f:
			line = line.strip()
			if line.startswith("#") or line == "":
				continue
			wrongDict_5[line] = 0

class StuInfo():
	def __init__(self, stuID, stuUsername):
		self.id   = stuID
		self.uname  = stuUsername
		self.url = "https://github.com/"+self.uname+"/"
		self.result = 0
		self.resultStr = "NO_ERROR"
		self.score = ""

	def checkFileValid(self, fname):
		self.fname = fname
		if not os.access(fname, os.R_OK):
			return -2
		with open(fname) as f:
			try :
				line = f.readline().strip()
				if line == "ERROR_NO_VALID_ACCOUT":
					self.result = -1
					self.resultStr = "ERROR_NO_VALID_ACCOUT"
				elif line == "ERROR_NO_HWK":
					self.result = -2
					self.resultStr = "ERROR_NO_HWK"
				else:
					self.result = 0
			except UnicodeDecodeError as e:
				self.result = 0

	def evelSnortAlert(self,hwkid):
		logfile = "/var/log/snort/alert"
		if hwkid == 1:
			correctDict = correctDict_1
			wrongDict = wrongDict_1
		elif hwkid == 2:
			correctDict = correctDict_2
			wrongDict = wrongDict_2
		else:
			print("Error : Wrong hwkid " + hwkid)
			return
		falsePosCnt = 0
		self.result = 0
		with open(logfile) as f:
			for line in f:
				for k in correctDict.keys():
					if line.find(k) != -1:
						correctDict[k] += 1
						break
				for k in wrongDict.keys():
					if line.find(k) != -1:
						wrongDict[k] = 1
						self.result = -4
						self.resultStr = "ERROR_WRONG_ALERT"
						print("Error " + k)
						break
		if self.result == 0:
			for k in correctDict.keys():
				if correctDict[k] == 0:
					self.result = -5
					self.resultStr = "ERROR_MISS_ALERT"
					print("Error " + k)


			# should be only 4
			if self.result == 0:
				for k in correctDict.keys():
					if correctDict[k] > 1:
						self.result = -6
						self.resultStr = "ERROR_SURPLUST_ALERT"
						print("Error " + k)

	def evelZeekAlert(self, hwkid, outstr):
		logfile = "/var/log/snort/alert"
		correctDict = ccDict[hwkid]
		wrongDict = wrDict[hwkid]
		
		falsePosCnt = 0
		self.result = 0
		for line in outstr.split("\r\n"):
			for k in correctDict.keys():
				if line.find(k) != -1:
					correctDict[k] = 1
					break
			for k in wrongDict.keys():
				if line.find(k) != -1:
					wrongDict[k] = 1
					self.result = -4
					self.resultStr = "ERROR_WRONG_ALERT"
					print("Error " + k)
					break
		if self.result == 0:
			for k in correctDict.keys():
				if correctDict[k] == 0:
					self.result = -5
					self.resultStr = "ERROR_MISS_ALERT"
					print("Error " + k)	

	def evalSKLearnAlert(self, hwkid, outstr):
		logfile = "result.txt"
		correctDict = ccDict[hwkid]
		wrongDict = wrDict[hwkid]
		
		falsePosCnt = 0
		self.result = 0

		with open("result.txt") as f:
			for line in f:
				line = line.strip()
				if line == "":
					continue
				toks = line.split(",")
				if len(toks) != 2:
					continue

				if toks[1] == "notdga":
					if toks[0] in correctDict:
						self.result = -4
						self.resultStr = "ERROR_WRONG_ALERT"
						print("Error " + k)
						break
				elif toks[1] == "dga":
					if toks[0] in correctDict:
						correctDict[toks[0]] = 1
				else:
					pass

		if self.result == 0:
			for k in correctDict.keys():
				if correctDict[k] == 0:
					self.result = -5
					self.resultStr = "ERROR_MISS_ALERT"
					print("Error " + k)	

	def calcScore(self):
		if self.result == 0:
			self.score = 100
		elif self.result == -6:
			self.score = 80
		elif self.result == -5:
			self.score = 80
		elif self.result == -4:
			self.score = 80
		elif self.result == -3:
			self.score = 60
		elif self.result == -2:
			self.score = 0
		elif self.result == -1:
			self.score = 0


	def __str__(self):
		return self.id + " " + self.url

def initHWList(filename):
	if os.access(filename, os.R_OK):
		with open(filename) as f:
			for line in f:
				tokens = line.split()
				if(len(tokens) != 2):
					printf("Error in initHWList : " + line)
					continue
				stuDict[tokens[0]] = StuInfo(tokens[0], tokens[1])


def evalSnort(stu, fname, pcapname, hwkid):
	#prepare work: clear alert, move test.rules to snort/local.rules
	subprocess.run(["rm","-r", "/var/log/snort/alert"])
	
	# shutil.copy(fname, "snort/local.rules")
	# snortconf = "/etc/snort/snort.conf.idshwk"   
	local_rules =  fname
	
	
	# ret = subprocess.run(["snort", "-A", "fast", "-c" ,local_rules, "-r", pcapname],capture_output=True)
	ret = subprocess.run(["snort", "-A", "fast", "-c" ,local_rules, "-r", pcapname],stderr=subprocess.PIPE)
	if ret.returncode != 0:
		stu.result = -3
		stu.resultStr = "ERROR_IDS_WRONG"
		errstr = str(ret.stderr)
		toks = errstr.split("ERROR")
		if len(toks) == 2:
			# local.rules -> test.rules
			if toks[1].find("test.rules") != -1:
				subtoks = toks[1].split("test.rules")
				stu.resultStr +=  " : " + subtoks[1]
			else:
				stu.resultStr += " : " + toks[1]
	else:
		print("begin test>>>>>>>>")
		stu.evelSnortAlert(hwkid)

def evalZeek(stu, fname, pcapname, hwkid):
	#prepare work: clear alert, move test.rules to snort/local.rules
	ret = subprocess.run(["dos2unix", fname])
	ret = subprocess.run(["zeek", "-r", pcapname, "hwk_init.zeek", fname],capture_output=True)
	if ret.returncode != 0:
		stu.result = -3
		stu.resultStr = "ERROR_IDS_WRONG"
		
		errstr = str(ret.stderr)
		print ("Error ",errstr);
		stu.resultStr +=errstr;
	else:
		outstr = str(ret.stdout)
		stu.evelZeekAlert(hwkid,outstr)

def evalSKLearn(stu, fname, pcapname, hwkid):
	#prepare work: clear alert, move test.rules to snort/local.rules
	#ret = subprocess.run(["dos2unix", fname])
	subprocess.run(["rm","-f", "resul.txt"])
	ret = subprocess.run(["python3", fname],capture_output=True)
	if ret.returncode != 0:
		stu.result = -3
		stu.resultStr = "ERROR_IDS_WRONG"
		
		errstr = str(ret.stderr)
		print ("Error ",errstr);
		stu.resultStr +=errstr;
	else:
		outstr = str(ret.stdout)
		stu.evalSKLearnAlert(hwkid,outstr)

def evalHwk6(stu, fname, pcapname, hwkid):
	fsize = os.stat(fname).st_size
	if fsize < 100:
		stu.result = -2
	else:
		stu.result = 0


def outputResult(hwkid):
	stuList = [(stu.id, stu) for stu in stuDict.values()]
	stuList.sort()

	workbook = xlwt.Workbook(encoding = 'utf-8')
	worksheet = workbook.add_sheet('IDS Course Score hwk'+str(hwkid))

	lineidx = 0
	for stuid, stu in stuList:
		worksheet.write(lineidx, 0, stu.id)
		worksheet.write(lineidx, 1, stu.score)
		worksheet.write(lineidx, 2, stu.resultStr)
		lineidx += 1

	workbook.save('score.xls')
	
			


def main():
	parser = argparse.ArgumentParser(description="read all student's homework from github")
	parser.add_argument('-t', "--test", type=bool, default=False, help='set testflag')
	parser.add_argument('-i', "--id", type=int, default=1, help='homeworkid')
	parser.add_argument('-f', "--filename", type=str, default="test.rules", help='filename of homework in github')

	args = parser.parse_args()
	testflag = args.test
	hwkid = args.id
	filename = args.filename


	dirname = "idshwk"+str(hwkid)
	pcapname = "idshwk"+str(hwkid)+".pcap"

	print("Param: hwkid %s filename %s" %(hwkid, filename))

	if not os.access(dirname, os.R_OK):
		print("Error : " + dirname + " not existed!")
		return

	initHWList("namesort.txt")

	idx = 0
	for stu in stuDict.values():
		fname = dirname + "/" + stu.id + "-"+ filename
		print(stu.id)
		stu.checkFileValid(fname)
		if stu.result == 0: 
			if hwkid == 1 or hwkid == 2:
				evalSnort(stu, fname, pcapname, hwkid)
			elif hwkid == 3 or hwkid == 4:
				evalZeek(stu, fname, pcapname, hwkid)
			elif hwkid == 5:
				evalSKLearn(stu, fname, pcapname, hwkid)
			elif hwkid == 6:
				evalHwk6(stu, fname, pcapname, hwkid)
			else:
				pass
		stu.calcScore()
		print(stu.resultStr)
		idx += 1
		if testflag:
			if idx>2:
				break
	outputResult(hwkid)


if __name__ == '__main__':
	main()