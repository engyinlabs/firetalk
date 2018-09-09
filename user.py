

class User:

    dic={
		'id': 'NULL',
		'email': 'NULL',
		'family_name' : 'NULL',
		'given_name' : 'NULL',
		'key': 'NULL'
	}


    def __init__(self,obj,key):
        # for i,o in obj.items():
        #     dic[i]=o;
        dic['key']=key;


        #
        # self.first=first;
        # self.last=last;
        # self.pay=pay;

     # @property
     # def email(self):
     #     return obj['email']
     # @property
     # def id(self):
     #     return obj['email']
    #
    #
    # @property
    # def fullname(self):
    #     return '{} {}'.format(self.first,self.last)
    #
    # def __repr__(self):
    #     return "Employee('{}','{}',{})".format(self.first,self.last,self.pay);
