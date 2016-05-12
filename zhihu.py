from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
from email.MIMEBase import MIMEBase
from email import Encoders
import smtplib
from email import Encoders,Utils
from email.Header import Header
import urllib2,urllib,time,datetime,codecs,sys,re,sys,os
reload(sys)
sys.setdefaultencoding('utf-8')

def save2file(filename,content):
	#保存为电子书文件
	filename=filename+".txt"
	f=open(filename,'a')
	f.write(content)
	f.close()


def getAnswer(answerID):
	host="http://www.zhihu.com"
	url=host+answerID
	print url
	user_agent="Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
	#构造header 伪装一下
	header={"User-Agent":user_agent}
	req=urllib2.Request(url,headers=header)
	resp=urllib2.urlopen(req)
	
	#这里已经获取了 网页的代码，接下来就是提取你想要的内容。 使用beautifulSoup 来处理，很方便
	
	bs=BeautifulSoup(resp,"html.parser")
	title=bs.title
	#获取的标题

	filename_old=title.string.strip()
	print filename_old
	filename = re.sub('[\/:*?"<>|]','-',filename_old)
	#用来保存内容的文件名，因为文件名不能有一些特殊符号，所以使用正则表达式过滤掉
	
	save2file(filename,title.string)
	title_content=title.string
	
	answer=[]
	
	detail=bs.find("div",class_="zm-editable-content")
	user_ids=bs.find_all("a",class_="author-link")

	
	save2file(filename,"\n\n\n\n--------------------Detail----------------------\n\n")
	#获取问题的补充内容
	
	for i in detail.strings:

		save2file(filename,unicode(i))
	
	answer=bs.find_all("div",class_="zm-editable-content clearfix")
	k=0
	index=0
	for each_answer in answer:
	
		save2file(filename,"\n\n-------------------------answer %s via  -------------------------\n\n" %k)
		
		for a in each_answer.strings:
			#循环获取每一个答案的内容，然后保存到文件中
			save2file(filename,unicode(a))
		k+=1
		index=index+1
	
	smtp_server='smtp.126.com'
	from_mail='your@126.com'
	password='yourpassword'
	to_mail='yourname@kindle.cn'
	send_kindle=MailAtt(smtp_server,from_mail,password,to_mail)
	send_kindle.send_txt(filename)
	#调用发送邮件函数，把电子书发送到你的kindle用户的邮箱账号，这样你的kindle就可以收到电子书啦
	print filename

class MailAtt():
	def __init__(self,smtp_server,from_mail,password,to_mail):
		self.server=smtp_server
		self.username=from_mail.split("@")[0]
		self.from_mail=from_mail
		self.password=password
		self.to_mail=to_mail
		#初始化邮箱设置
		
	def send_txt(self,filename):
		#这里发送附件尤其要注意字符编码，当时调试了挺久的，因为收到的文件总是乱码
		self.smtp=smtplib.SMTP()
		self.smtp.connect(self.server)
		self.smtp.login(self.username,self.password)
		self.msg=MIMEMultipart()
		self.msg['to']=self.to_mail
		self.msg['from'] =self.from_mail
		self.msg['Subject']="Convert"
		self.filename=filename+ ".txt"
		self.msg['Date']=Utils.formatdate(localtime = 1)
		content=open(self.filename.decode('utf-8'),'rb').read()
		#print content
		self.att=MIMEText(content,'base64','utf-8')
		self.att['Content-Type']='application/octet-stream'
		#self.att["Content-Disposition"] = "attachment;filename=\"%s\"" %(self.filename.encode('gb2312'))
		self.att["Content-Disposition"] = "attachment;filename=\"%s\"" % Header(self.filename,'gb2312')
		#print self.att["Content-Disposition"]
		self.msg.attach(self.att)
		
		self.smtp.sendmail(self.msg['from'],self.msg['to'],self.msg.as_string())
		self.smtp.quit()
		
if __name__=="__main__":

	sub_folder=os.path.join(os.getcwd(),"content")
	#专门用于存放下载的电子书的目录
	
	if not os.path.exists(sub_folder):
		os.mkdir(sub_folder)
	
	os.chdir(sub_folder)
	
	id=sys.argv[1]
	#给出的第一个参数 就是你要下载的问题的id
	#比如 想要下载的问题链接是 https://www.zhihu.com/question/29372574
	#那么 就输入 python zhihu.py 29372574
	
	id_link="/question/"+id
	getAnswer(id_link)
	#调用获取函数
	
	print "Done"
	
	
