import json


class DBStore:
    user_id= ""
    exists= None
    c_t=""
    c_n=''
    c_c=''
    
    def __init__(self, username, email, password):
        self.username= username
        self.email= email
        self.password= password
        if self.username is None:
            self.existing_user()
        else:
            self.new_user()

    @staticmethod
    def get_id():
        with open('database/id_count.txt', 'r') as my_id:
            d=[one.strip() for one in my_id.readlines()]
        with open('database/id_count.txt', 'w') as my_id2:
            my_id2.write(str(int(d[0])+1).zfill(8))
        return str(int(d[0])+1).zfill(8)
    
    def store_user_id(self, rw):
        if rw == "r":
            with open('database/id_count.txt', 'r') as my_id:
                c = [line.strip() for line in my_id.readlines()]
                return c[-1]
        elif rw == 'w':
            with open('database/id_count.txt', 'a+') as my_id2:
                if len(my_id2.readlines()) == 2:
                    pass
                else:
                    my_id2.write('\n'+str(self.user_id))
                
    def new_user(self):
        user_id= self.get_id()
        with open('database/users_data.json', 'r') as a:
            data= a.read()
        user_data= json.loads(data)
        user_data[user_id]={"personal_info":[self.username, self.email, self.password],
                              "notes_info":{}}
        json.dump(user_data, open('database/users_data.json', 'w'), indent=4)

    def existing_user(self):
        with open('database/users_data.json', 'r') as a:
            data2= a.read()
        user_data2= json.loads(data2)
        if len(user_data2) != 0:
            for one in range(len(user_data2.keys())):
                id_index= list(user_data2.keys())
                the_email= user_data2[id_index[one]]["personal_info"][1]
                the_password= user_data2[id_index[one]]["personal_info"][2]
                if the_email == self.email and the_password == self.password:
                    self.exists= True
                    self.user_id= id_index[one]
                    self.store_user_id('w')
                else: pass

    def notes_info_storer(self, *args):
        user_id=self.store_user_id('r')
        user_data= json.loads(open("database/users_data.json", "r").read())
        adder= user_data[user_id]["notes_info"]
        if len(adder) == 0:
            adder[0]=dict(title=args[0], text=args[1], color=args[2], date=args[3])
        else:
            i= int(list(adder.keys())[-1])+1
            adder[i]=dict(title=args[0], text=args[1], color=args[2], date=args[3])
        json.dump(user_data, open('database/users_data.json', 'w'), indent= 4)

    def del_data(self, title, text, color):
        data= json.loads(open('database/users_data.json',"r").read())
        idd= self.store_user_id('r')
        d= data[idd]['notes_info'].items()
        for one in d:
            title_db= one[1]['title']
            text_db= one[1]['text']
            clr_db= one[1]['color']
            if title == title_db and text == text_db and color == clr_db:
                del data[idd]['notes_info'][str(one[0])]
                break
            else: pass
        json.dump(data, open('database/users_data.json', "w"), indent=4)

    def edit_data(self, title, text, color, date):
        data= json.loads(open('database/users_data.json',"r").read())
        idd= self.store_user_id('r')
        d= data[idd]['notes_info'].items()
        for one in d:
            title_db= one[1]['title']
            text_db= one[1]['text']
            clr_db= one[1]['color']
            if self.c_t == title_db and self.c_n == text_db and self.c_c == clr_db:
                data[idd]['notes_info'][str(one[0])]['title']= title
                data[idd]['notes_info'][str(one[0])]['text']= text
                data[idd]['notes_info'][str(one[0])]['color']= color
                data[idd]['notes_info'][str(one[0])]['date']= date
                break
            else: pass
        json.dump(data, open('database/users_data.json', "w"), indent=4)