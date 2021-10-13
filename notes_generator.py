from kivymd.uix.card import MDCard
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivymd.uix.label import MDLabel
from kivy.uix.button import ButtonBehavior
from kivymd.uix.button import MDIconButton
import datetime
import random
from kivy import utils


class LabelBtn(ButtonBehavior, MDLabel):
    def __init__(self, **kwargs):
        super(LabelBtn, self).__init__(**kwargs)
        self.theme_text_color= 'Custom'

class Note(MDCard):
    main_app=None

    def __init__(self, title, note, clr, app, **kwargs):
        super(Note, self).__init__(**kwargs)
        self.main_app= app
        self.size_hint_y= None
        self.height= random.randint(180, 200)
        self.size_hint_x= 0.5
        self.elevation= 8
        self.md_bg_color= clr
        self.container= FloatLayout()
        self.title_txt= LabelBtn(text=title.upper(), size_hint=[1, .1],
                        pos_hint={'center_x':.5, 'center_y':.55},
                        bold=True,
                        font_size="20sp",
                        underline=True,
                        halign="center")
        self.title_txt.bind(on_press= lambda x:self.color1(1))
        self.title_txt.bind(on_release= lambda x:self.color1(2))
        self.title_txt.bind(on_release= lambda x: app.note_clicked(title, note))
        self.time= Label(text=self.get_time(),
                        size_hint=[.4, .06],
                        pos_hint={'x':.02, 'top':.99},
                        font_size='14sp',
                        color=[0,0,0,1])
        self.btns_container= BoxLayout(orientation="horizontal",
                        size_hint=[0.2, 0.1],
                        pos_hint={'x':0.48, "top":0.1},
                        spacing=2)
        self.trash= MDIconButton(icon='trash-can', size_hint_x=.5)
        self.edit= MDIconButton(icon='pencil', size_hint_x=.5)
        self.trash.bind(on_release= lambda x : app.note_del(self, title, note, clr))
        self.edit.bind(on_press= lambda x : self.edittrue())
        self.edit.bind(on_release= lambda x : app.note_edit(title, note, clr, self.get_time()))

        self.btns_container.add_widget(self.edit)
        self.btns_container.add_widget(self.trash)
        self.container.add_widget(self.title_txt)
        self.container.add_widget(self.time)
        self.container.add_widget(self.btns_container)
        self.add_widget(self.container)

    def get_time(self):
        self.time_now= datetime.datetime.now().date()
        return str(self.time_now)

    def color1(self, w):
        if w == 1:
            self.title_txt.text_color= utils.get_color_from_hex('#FF9900')
        elif w == 2:
            self.title_txt.text_color= utils.get_color_from_hex('#000000')

    def edittrue(self):
        self.main_app.editON = True

    def change_note(self):
        self.title_txt.text=""
        self.md_bg_color=''
        self.time.text=''