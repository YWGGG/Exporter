import os
import shutil
import argparse
import urllib.request
import subprocess

stuDict = {}

class StuInfo():
	def __init__(self, stuID, stuUsername):
		self.id   = stuID
		self.uname  = stuUsername
		self.url = "https://github.com/"+self.uname+"/"

	def __str__(self):
		return self.id + " " + self.url


def initHWList(filename):
	if os.access(filename, os.R_OK):
		with open(filename) as f:
			for line in f:
				tokens = line.split()

				if(len(tokens) != 2):
					print("Error in initHWList : " + line)
					continue
				stuDict[tokens[0]] = StuInfo(tokens[0], tokens[1])


# wait to finsh
def cloneHW(stu, hwkid,dirname, filename):
	'Download the homework file to stuID-hwkid-filename'
	hwurl = stu.url + "/idshwk" + hwkid
	localfilename = dirname + "/" + stu.id + "-"+ filename
	if stu.uname == "ErrorError":
		shutil.copy("error_noaccount.txt",localfilename)
		print(" Error : bad username " + stu.id)
	else:
		try:
			subprocess.call(["git","clone", hwurl])
			subprocess.call(["mv","idshwk7", stu.id])

			#sometime github will not return 404 on missing file url, the following code treat this problem
			#sometime the rules file is too small be to a valid rule
			
		except IOError as e:
			print("Error : URL 404" + stu.id + " " + hwurl + " " + str(e))

def downloadHW(stu, hwkid, dirname, filename):
	'Download the homework file to stuID-hwkid-filename'


	hwurl = stu.url + "idshwk" + hwkid + "/raw/master/"+filename
	localfilename = dirname + "/" + stu.id + "-"+ filename


	if stu.uname == "ErrorError":
		shutil.copy("error_noaccount.txt",localfilename)
		print(" Error : bad username " + stu.id)
	else:
		try:
			print(hwurl)
			print(localfilename)
			urllib.request.urlretrieve(hwurl, localfilename)
			#sometime github will not return 404 on missing file url, the following code treat this problem
			#sometime the rules file is too small be to a valid rule
			filesize = os.path.getsize(localfilename)
			if filesize > 10000000 or filesize < 10:
				print("Error : File size error " + stu.id + " " + str(filesize) + " " + hwurl)
				shutil.copy("error_nohwk.txt",localfilename)
		except IOError as e:
			shutil.copy("error_nohwk.txt",localfilename)
			print("Error : URL 404" + stu.id + " " + hwurl + " " + str(e))

def main():
	parser = argparse.ArgumentParser(description="read all student's homework from github")
	parser.add_argument('-c', "--cloneflag", type=bool, default=False, help='cloneflag')
	parser.add_argument('-i', "--id", type=int, default=1, help='homeworkid')
	parser.add_argument('-f', "--filename", type=str, default="test.rules", help='filename of homework in github')

	args = parser.parse_args()
	cloneflag = args.cloneflag
	hwkid = args.id
	filename = args.filename
	dirname = "idshwk"+str(hwkid)

	print("Param: hwkid %s filename %s" %(hwkid, filename))
	initHWList("namesort.txt")

	if not os.access(dirname, os.R_OK):
		os.mkdir(dirname)
	idx = 0
	for stu in stuDict.values():
		print(stu)
		# if cloneflag:
		# 	cloneHW(stu, str(hwkid))
		# else:
		downloadHW(stu, str(hwkid), dirname, filename)
		idx += 1


		#if idx>2:
		#	break

if __name__ == '__main__':
	main()
