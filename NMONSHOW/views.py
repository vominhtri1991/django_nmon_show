from django.shortcuts import render
from django.conf import settings
import os

nmon_file_path=settings.NMON_FILE_PATH 
nmon_files=[]

class Server:
	def __init__(self,hostname,model,ip,avg_cpu,avg_memory):
		self.hostname=hostname.replace(' ','')
		self.model=model.replace('\"','')
		self.ip=ip.replace('\"','')
		self.avg_cpu=round(avg_cpu,2)
		self.avg_memory=round(avg_memory,2)

def parse_all(nmon_file):
	print("Processing file: "+nmon_file)
	f=open(nmon_file,"r")
	lines=f.readlines()
	hostname=""
	ip=""
	model=""
	list_cpu_usage=[]
	list_mem_usage=[]
	for line in lines:
		if("Host Name:" in line):
			hostname=line.split(":")[1]
		if("IP Address:" in line):
			ip=line.split(":")[1].replace(" ","")
		if("System Model:" in line):
			model=line.split(":")[1].replace(" ","")
		if("CPU_ALL,T" in line):
			cpu_use=float(line.split(",")[6])
			list_cpu_usage.append(cpu_use)
		if("MEM,T" in line):
			mem_free=float(line.split(",")[2])
			mem_use=100-mem_free
			list_mem_usage.append(mem_use)
	
	f.close()
	avg_cpu=(sum(list_cpu_usage)/len(list_cpu_usage))
	avg_memory=(sum(list_mem_usage)/len(list_mem_usage))
	server=Server(hostname,model,ip,avg_cpu,avg_memory)
	return server

def listnmonfiles(datechk):
	nmon_files=[]
	for file in os.listdir(nmon_file_path+"//"+datechk):
		if(file.endswith(".nmon")):
			#print(file)
			nmon_files.append(nmon_file_path+"//"+datechk+"//"+file)
	return nmon_files


def home(request):
	return render(request,'NMONSHOW/home.html',{"config":nmon_file_path})

def processnmon(request):
	list_servers=[]
	date=request.POST.get('date')
	date_str=date.split("-")[2]+"/"+date.split("-")[1]+"/"+date.split("-")[0]
	date_chk=date.split("-")[2]+date.split("-")[1]+date.split("-")[0]
	nmon_files=listnmonfiles(date_chk)
	for i in nmon_files:
		server=parse_all(i)
		list_servers.append(server)
	return render(request,'NMONSHOW/shownmon.html',{"date":date_str,"servers":list_servers})

# Create your views here.
