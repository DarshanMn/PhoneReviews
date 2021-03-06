import sys
import MySQLdb
import re
import webbrowser
from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts

class insertReview:
	
	review = ""
	set = 0
	count = 0
	good=0
	bad=0
	actual_review=""
	word_dict={}

	def __init__(self):
		self.mydb = MySQLdb.connect(host='localhost',
		 	user='root',
		 	passwd='neo&trinity',
		 	db='training_data')
		self.mydb1 = MySQLdb.connect(host='localhost',
		 	user='root',
		 	passwd='neo&trinity',
		 	db='phone_reviews')
		self.cursor = self.mydb.cursor()
		self.cursor1 = self.mydb1.cursor()
		self.frequency=0
		self.calAccuracy()
	
	def getReview(self, x):

		self.cursor1.execute("select review from reviews where phone_id="+self.phone_id+" and types="+str(x)+";")
		result = self.cursor1.fetchall()
		i=0
		for data in result:
			self.review = data[0]
			self.review = re.sub('[.,;/<>+:_=!\\\'\"?~$^*|`]', "", self.review)
		 	self.review = self.review.replace(")","")
			self.review = self.review.replace("(","")
		 	self.review = self.review.replace("]","")
		 	self.review = self.review.replace("[","")
		 	self.review = self.review.replace("-","")
			self.review = self.review.lower()
			self.actual_review = self.actual_review + self.review
			i+=1
			
	def calAccuracy(self):	
		self.cursor1.execute("select id, name from phone_id;")
		result = self.cursor1.fetchall()
		for data in result:
			print data[0],data[1]
		self.phone_id=raw_input("Enter phone id\n");
		self.name = raw_input("Enter name:")
		import os
		os.mkdir('/home/darshan-ubuntu/Project/Products/Features/'+self.name)

		self.getReview(1)
		tags = make_tags(get_tag_counts(self.actual_review), maxsize=120)
		create_tag_image(tags, self.name+'/positive.png', size=(900, 600))
		self.actual_review=""
		
		self.getReview(0)
		tags = make_tags(get_tag_counts(self.actual_review), maxsize=60)
		create_tag_image(tags, self.name+'/negative.png', size=(900, 600))

def main():
	obj = insertReview()
		
if __name__ == "__main__":
    main()
