# coding=utf-8
import subprocess
import os
import sys
import codecs
import time
import re
import datetime
from optparse import OptionParser
cur_time = time.strftime("%Y-%m-%d %X")

def get_cli_options():
    parser = OptionParser(usage="usage: python %prog [options]",
                          description="""This script prints some info of ogg.""")

    parser.add_option("-d", "--from_date",
                      dest="from_date",
                      help="Simple:yyyy-mm-dd hh:mi:ss or yyyy-mm-dd(default 00:00:00)")
    (options, args) = parser.parse_args()
    return options

def get_oggproc_name(gg_home):
        list = []
	collist = []
	ggsci_order = gg_home+"ggsci"
	proc = subprocess.Popen(ggsci_order, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
								stderr=subprocess.STDOUT)
	for line in proc.communicate("info all"):
			list.append(line)
	linecount = len(list[0].split("\n"))-3-13
	linelen = 0
	for col in range(13,len(list[0].split("\n"))-3):
			linelen = len(list[0].split("\n")[col].split(" "))
			for linecol in range(linelen):
					if list[0].split("\n")[col].split(" ")[linecol] != '':
							collist.append(list[0].split("\n")[col].split(" ")[linecol])
					else:
							continue
	proclist = []
	start_n = 2
	for proccol in range(len(collist)):
			if start_n < len(collist):
					proclist.append(collist[start_n])
			else:
					break
			start_n +=5
	return collist,proclist

def str2date(str_date):
   return datetime.datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')

def get_matched(tmp_list,simple_date,gg_home):
	dis_list = []
	match_count = 0
	result_list = []
	count_list = []
	simple_btime = simple_date
	if simple_btime is None:
		cur_dawn = cur_time.split(" ")[0] + " 00:00:00"
		d_dawn = str2date(cur_dawn)
	else:
		if len(simple_btime)>10:
			d_dawn = str2date(simple_btime)
		else:	
			d_dawn = str2date(simple_btime+" 00:00:00")
	print	
	print "=================Simple_time:"+str(d_dawn)+"~"+cur_time+"================="
	print
	for col in range(len(tmp_list)):
		file = codecs.open(gg_home+"dirrpt/"+tmp_list[col], 'rb', 'utf-8')
		String = file.read()
		file.close()
		SkipHeadLine = 0
		NumList = []
		newList = []
		match_count = 0
		StringList = String.split('Current time: ')
		LineNum = 0
		for Line in StringList:
			LineNum = LineNum + 1
			if (LineNum > SkipHeadLine):
				if len(Line) > 0:
					NumList.append(Line)
		pattern = re.compile(r'Discarding record on action DISCARD on error')
		for col in range(len(NumList)):
			match = pattern.search(NumList[col])
			if match:
				newList.append(NumList[col])
		for count_col in range(len(newList)):
			if str2date(newList[count_col].split("\n")[0]) > d_dawn:
				match_count += 1
		count_list.append(match_count)
	return count_list
	
def get_dscfile(dsc_list,gg_home):
	SkipHeadLine = 0
	n_new_list = []
	newList = []
	for dsc_col in range(len(dsc_list)):
		file = codecs.open(gg_home+"dirprm/"+dsc_list[dsc_col], 'rb', 'utf-8')
		String = file.read()
		file.close()
		NumList = []
		StringList = String.split('\n')
		LineNum = 0
		for Line in StringList:
			LineNum = LineNum + 1
			if (LineNum > SkipHeadLine):
				if len(Line) > 0:
					NumList.append(Line)
		pattern = re.compile(r'DISCARDFILE',re.IGNORECASE)
		for col in range(len(NumList)):
			match = pattern.search(NumList[col])
			if match:
				newList.append(NumList[col])
	for col in range(len(newList)):
			n_new_list.append(newList[col].split(",")[0].split("/")[2])
	return n_new_list


def dsc_list(proclist,simpledate,gg_home):
	dsc_list = []
	for col in range(len(proclist)):
		#print proclist[col].lower()+".prm"
		dsc_list.append(proclist[col].lower()+".prm")
	tmp_list = []
	tmp_list = get_dscfile(dsc_list,gg_home)
	return get_matched(tmp_list,simpledate,gg_home)

def format_col(collist,dsclist):
	col1_list = []
	col2_list = []
	col3_list = []
	col4_list = []
	col5_list = []
	for col in range(len(collist)):
		if col %5 == 0:
			col1_list.append(collist[col])
			col2_list.append(collist[col+1])
			col3_list.append(collist[col+2])
			col4_list.append(collist[col+3])
			col5_list.append(collist[col+4])
	print '{0:<10}{1:<10}{2:<10}{3:<15}{4:<20}{5:<20}'.format("Program", "Status", "Group", "Lag at Chkpt","Time Since Chkpt","Discard count")
	for for_col in range(len(col1_list)):
		print '{0:<10}{1:<10}{2:<10}{3:<15}{4:<20}{5:<20}'.format(col1_list[for_col],col2_list[for_col],col3_list[for_col],col4_list[for_col],col5_list[for_col],dsclist[for_col])
def get_gg_home():
	proc_mgr = os.popen('ps -ef|grep mgr|grep oracle|grep -v grep').readlines()
	return proc_mgr[0].split("PARAMFILE")[1].split("dirprm")[0]

def main():
	options = get_cli_options()
    	collist,proclist = get_oggproc_name(get_gg_home())
	format_col(collist,dsc_list(proclist,options.from_date,get_gg_home().strip()))

if __name__ == '__main__':
   main()

