from kivymd.app import MDApp
from kivy.uix.screenmanager import (ScreenManager,Screen, FadeTransition)
from kivy.core.window import Window
from database.db_manager import DBStore
from kivy.animation import Animation
from notes_generator import Note
from kivy.lang import Builder
from kivymd.toast import toast
from datetime import datetime
from kivy.clock import Clock
from random import randint
from kivy import utils
import json
import re


class Loading(Screen):
    pass

class Starting(Screen):
    pass

class SignIn(Screen):
    pass

class SignUp(Screen):
    pass

class Home(Screen):
    pass

class NoteAdder(Screen):
    pass

class Gallery(Screen):
    pass

class MotivQuote(Screen):
    pass

class About(Screen):
    pass


class MainApp(MDApp):
    picked_clr = ""
    editON= False

    def build(self):
        Window.size = (360, 640)
        Window.minimum_width, Window.minimum_height = (360, 640)
        Window.clearcolor = utils.get_color_from_hex('#CEBB4E')
        self.theme_cls.primary_palette = 'DeepOrange'
        return Builder.load_file('main.kv')

    def user_id(self, rw):
        if rw == "r":
            with open('database/id_count.txt', 'r') as my_id:
                c = [line.strip() for line in my_id.readlines()]
                return c
        else:
            pass

    def on_start(self):
        self.screen_mg = self.root.ids.screen_manager
        self.screen_changer('to-loading')  # must be reset to "to-loading"
        Clock.schedule_once(lambda x: self.screen_changer('to-starting'), 6)
        idd = self.user_id('r')
        if len(idd) > 1:
            data = self.get_data()
            if data is not None:
                for li in data:
                    self.notes_adder(
                        title_txt=li[0], note_txt=li[1], color=li[2],
                        date=li[3], who="db")
            else: pass
        else: pass

    def get_data(self):
        idd = self.user_id('r')[-1]
        returned_list = []
        user_data = json.loads(open("database/users_data.json", "r").read())
        adder = user_data[idd]["notes_info"]
        if len(adder) == 0:
            pass
        else:
            for key in adder.keys():
                returned_list.append(list(adder[key].values()))
            return returned_list

    def screen_changer(self, the_screen):
        self.screen_mg.transition.direction = 'up'
        self.screen_mg.transition = FadeTransition()
        if the_screen == 'to-loading':
            self.screen_mg.current = 'loading_sc'
        elif the_screen == 'to-starting':
            self.screen_mg.current = 'starting_sc'
        elif the_screen == 'to-signin':
            self.screen_mg.current = 'signin_sc'
        elif the_screen == 'to-signup':
            self.screen_mg.current = 'signup_sc'
        elif the_screen == 'to-home':
            self.screen_mg.current = 'home_sc'
        elif the_screen == 'to-noteadder':
            self.screen_mg.current = 'noteadder_sc'
        elif the_screen == 'to-gallery':
            self.screen_mg.current = 'gallery_sc'
        elif the_screen == 'to-motive':
            self.screen_mg.current = 'motive_sc'
            self.quote_picker()
        elif the_screen == 'to-about':
            self.screen_mg.current = 'about_sc'
            self.txt_puter()

    def check_info_up(self, un, em, pw):
        txt = self.root.ids.signup_sc.ids.warning
        self.username = un.strip()
        self.email = em.strip()
        self.password = pw.strip()
        email_pattern = r'[A-Z]?\w+@[a-z]{,6}\.\w+'
        password_pattern = r'\w+\d+'
        if re.match('\w+', self.username) and re.match(email_pattern, self.email) and self.email.count('@') == 1 and re.match(password_pattern, self.password):
            DBStore(self.username, self.email, self.password)
            self.screen_changer('to-signin')
            self.root.ids.signin_sc.ids.warning2.text = "Account Created!! login to enter..."
            self.root.ids.signin_sc.ids.warning2.color = [0, 0, 1, 1]
            self.root.ids.signup_sc.ids.username.text = ""
            self.root.ids.signup_sc.ids.email.text = ""
            self.root.ids.signup_sc.ids.password.text = ""
        else:
            txt.color = [1, 0, 0, 1]
            txt.text = 'invalid email or password!'.title()

    def check_info_in(self, em, pw):
        txt = self.root.ids.signin_sc.ids.warning2
        self.email = em.strip()
        self.password = pw.strip()
        email_pattern = r'[A-Z]?\w+@[a-z]{,6}\.\w+'
        password_pattern = r'\w+\d+'
        if re.match(email_pattern, self.email) and self.email.count('@') == 1 and re.match(password_pattern, self.password):
            self.user_in = DBStore(None, self.email, self.password)
            access = self.user_in.exists
            if access:
                toast('login successfully!', 1)
                self.screen_changer("to-loading")
                self.root.ids.signin_sc.ids.email_txt.text = ""
                self.root.ids.signin_sc.ids.password_txt.text = ""
                Clock.schedule_once(
                    lambda x: self.screen_changer('to-home'), 3)
            else:
                txt.color = [1, 0, 0, 1]
                txt.text = 'this account does not exist!'.title()
        else:
            txt.color = [1, 0, 0, 1]
            txt.text = 'invalid email or password!'.title()

    def warn_em(self, warn):
        warn.color = [1, 0, 0, 1]
        warn.text = 'all text fields should be filled!'.title()

    def warn_em2(self):
        self.root.ids.noteadder_sc.ids.warning3.text = "make sure that everything is entered!".title()

    def notes_adder(self, title_txt, note_txt, color, date, who):
        self.title_txt = title_txt
        self.note_txt = note_txt
        self.color = color
        self.date = date
        if self.editON == False:
            box = self.root.ids.gallery_sc.ids.box1
            if who == "ur":
                box.add_widget(Note(self.title_txt, self.note_txt, color, app))
                self.user_in.notes_info_storer(
                    self.title_txt, self.note_txt, self.color, str(datetime.now().date()))
                self.screen_changer('to-gallery')
                self.noteadder_reseter()
            if who == 'db':
                box.add_widget(Note(self.title_txt, self.note_txt, color, app))
        else:
            self.user_in.edit_data(self.title_txt, self.note_txt, self.color, str(datetime.now().date()))
            toast('Note Edited!')
            self.noteadder_reseter()
            self.root.ids.noteadder_sc.ids.add_btn.text= "add note".upper()
            self.screen_changer('to-gallery')
            self.editON= False

    def noteadder_reseter(self):
        self.root.ids.noteadder_sc.ids.title.text = ''
        self.root.ids.noteadder_sc.ids.note_adder.text = ''
        self.picked_clr = ''
        self.root.ids.noteadder_sc.ids.a.background_color = utils.get_color_from_hex(
            '#00FFFF')
        self.root.ids.noteadder_sc.ids.b.background_color = utils.get_color_from_hex(
            '#FFFF00')
        self.root.ids.noteadder_sc.ids.c.background_color = utils.get_color_from_hex(
            '#00FF00')
        self.root.ids.noteadder_sc.ids.warning3.text = ""

    def note_clicked(self, title_txt, note_txt):
        self.screen_changer('to-noteadder')
        self.root.ids.noteadder_sc.ids.title.text = title_txt
        self.root.ids.noteadder_sc.ids.note_adder.text = note_txt
        self.root.ids.noteadder_sc.ids.add_btn.disabled = True
        self.root.ids.noteadder_sc.ids.a.disabled = True
        self.root.ids.noteadder_sc.ids.b.disabled = True
        self.root.ids.noteadder_sc.ids.c.disabled = True
        self.root.ids.noteadder_sc.ids.title.readonly=True
        self.root.ids.noteadder_sc.ids.note_adder.readonly=True

    def enable_btn(self):
        self.root.ids.noteadder_sc.ids.add_btn.disabled = False
        self.root.ids.noteadder_sc.ids.a.disabled = False
        self.root.ids.noteadder_sc.ids.b.disabled = False
        self.root.ids.noteadder_sc.ids.c.disabled = False
        self.root.ids.noteadder_sc.ids.title.readonly=False
        self.root.ids.noteadder_sc.ids.note_adder.readonly=False
        self.picked_clr = ""
        self.root.ids.noteadder_sc.ids.warning3.text = ""

    def note_del(self, target, t, n, c):
        self.target= target
        box = self.root.ids.gallery_sc.ids['box1']
        box.remove_widget(self. target)
        self.user_in.del_data(t, n, c)

    def note_edit(self, t, n ,c, d):
        if self.editON == True:
            self.info_saver(t, n, c)
            self.enable_btn()
            self.root.ids.noteadder_sc.ids.add_btn.text= "save note".upper()
            self.screen_changer('to-noteadder')
            self.root.ids.noteadder_sc.ids.title.text =t
            self.root.ids.noteadder_sc.ids.note_adder.text =n
        else:pass

    def info_saver(self, t, n ,c):
        self.user_in.c_t=t
        self.user_in.c_n=n
        self.user_in.c_c=c

    def txt_puter(self):
        with open('database/about_text.txt', 'r') as file:
            content= file.read()
        place= self.root.ids.about_sc.ids.txt00
        place.text= content

    def quote_picker(self):
        with open('database/quotes.txt', "r") as file:
            content= file.readlines()
            quotes= [line.strip() for line in content]
            quote= quotes[randint(0, len(quotes)-1)]
            text= quote[:quote.find(';')]
            author= quote[quote.find(';')+1:]
            self.root.ids.motive_sc.ids.quote.text='[b][color=#92D575]"[/color][/b]'+text+'[b][color=#92D575]"[/color][/b]'
            self.root.ids.motive_sc.ids.owner.text="[color=#FF0000]By: [/color]"+author

    def kill_app(self):
        self.stop()


if __name__ == '__main__':
    app = MainApp()
    app.run()
