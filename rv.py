from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview import RecycleView
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.properties import DictProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import ScreenManager, Screen

import json
import os


data = []

if not os.path.exists('res.json'):
    with open('res.json','x') as f:
        json.dump(data,f)
else:
    with open('res.json','r') as f:
        data = json.load(f)     

oof = 'aaaa'
# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        Button:
            text: 'Create'
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current = 'create'
        Button:
            text: 'Update'
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.current = 'update'

<RV>:
    data: app.data
    viewclass: 'SelectableLabel'
    SelectableRecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: True
        touch_multiselect: True

<UpdateScreen>:
    BoxLayout:
        orientation: "vertical"
        RV:
        Button:
            text: 'Previous screen'
            size_hint: None, None
            size: 150, 50
            on_release: 
                root.manager.transition.direction = 'right'
                root.manager.current = 'menu'

<CreateScreen>:
    submit_button : button
    GridLayout:
        cols : 1
        
        GridLayout:
            cols:2
            padding:[20,20,20,20]
            spacing:[20,20]
            Label:
                text:'Name'
            TextInput:
                id : input_name
                write_tab:False
                hint_text:'Name'

            Label:
                text:'Number'
            TextInput:
                id : input_number
                write_tab:False
                hint_text:'Number'
            
            Label:
                text:'Notes'
            TextInput:
                id : input_notes
                write_tab:False
                hint_text:'Notes'
            
            Label:
                text:'Interval'
            TextInput:
                id : input_interval
                write_tab:False
                hint_text:'Interval'
        AnchorLayout:
            anchor_x:'center'
            anchor_y:'center'
            size_hint_y:None

            Button:
                background_normal:'button.png'
                id:button
                color:1,0,0,1
                text:'Create'
                size_hint_x:None
                size_hint_y:None
                width: 200
                height:100
                on_press: 
                    root.create(input_name.text, input_number.text, input_notes.text, input_interval.text)
                    
        AnchorLayout:
            anchor_x:'center'
            anchor_y:'center'
            size_hint_y:None

            Button:
                background_normal:'button.png'
                color:1,0,0,1
                text:'Cancel'
                size_hint_x:None
                size_hint_y:None
                width: 200
                height:100
                on_press: 
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'menu'

<EditScreen>:
    edit_button : button_edit
    GridLayout:
        cols : 1
        
        GridLayout:
            cols:2
            padding:[20,20,20,20]
            spacing:[20,20]
            Label:
                text:'Name'
            TextInput:
                id : edit_name
                write_tab:False
                hint_text:'Name'
                text : root.dic["name"]
            Label:
                text:'Number'
            TextInput:
                id : edit_number
                write_tab:False
                hint_text:'Number'
                text : root.dic["number"]
            
            Label:
                text:'Notes'
            TextInput:
                id : edit_notes
                write_tab:False
                hint_text:'Notes'
                text : root.dic["notes"]

            
            Label:
                text:'Interval'
            TextInput:
                id : edit_interval
                write_tab:False
                hint_text:'Interval'
                text : root.dic["interval"]

        AnchorLayout:
            anchor_x:'center'
            anchor_y:'center'
            size_hint_y:None

            Button:
                background_normal:'button.png'
                id:button_edit
                color:1,0,0,1
                text:'Update'
                size_hint_x:None
                size_hint_y:None
                width: 200
                height:100
                on_press: 
                    root.update(edit_name.text, edit_number.text, edit_notes.text, edit_interval.text)
                    
        AnchorLayout:
            anchor_x:'center'
            anchor_y:'center'
            size_hint_y:None

            Button:
                background_normal:'button.png'
                color:1,0,0,1
                text:'Cancel'
                size_hint_x:None
                size_hint_y:None
                width: 200
                height:100
                on_press: 
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'update'
""")

# Declare both screens
class MenuScreen(Screen):
    pass

class UpdateScreen(Screen):
    def __init__(self, **kwargs):
        super(UpdateScreen, self).__init__(**kwargs)
        self.update()
    def update(self):
        self.data = [{'text': str(x)} for x in range(100)]


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        #self.update()
    def update(self):
        self.data = [{'text': x["name"], 'lol':x} for x in data]

class CreateScreen(Screen):
    def create(self,name,number,notes,interval):
        if name != "":
            print('')
            TestApp.get_running_app().data.append({
                    "name":str(name),
                    "number":str(number),
                    "notes":str(notes),
                    "interval":str(interval)
                    })
            with open('res.json','w') as f:
                json.dump(TestApp.get_running_app().data,f,indent=4)
            print('written')
            self.manager.transition.direction = 'left'
            self.manager.current='menu'
        else:
            self.submit_button.text = "Name cannot be empty"

class EditScreen(Screen):
    dic = DictProperty({"name":"placeholder",
                        "notes":"placeholder",
                        "number":"placeholder",
                        "interval":"placeholder"})
    def update(self,name,number,notes,interval):
        new_dic = {"name":name,
                   "number":number,
                   "notes":notes,
                   "interval":interval}
        print(self.dic)
        TestApp.get_running_app().data.remove({"text":self.dic["name"], "lol":self.dic})
        TestApp.get_running_app().data.append(new_dic)
        with open('res.json','w') as f:
            json.dump(TestApp.get_running_app().data,f,indent=4)
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''

class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)
            

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        
        if is_selected:
            #print("selection changed to {0}".format(rv.data[index]))
            TestApp.get_running_app().switch_to_edit(rv.data[index]["lol"])
            
            #print(rv.data[index]["lol"])
        else:
            print("selection removed for {0}".format(rv.data[index]))



# Create the screen manager

class TestApp(App):
    data = ListProperty()
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(UpdateScreen(name='update'))
        sm.add_widget(CreateScreen(name='create'))
        #sm.add_widget(EditScreen(name='edit'))
        self.sm = sm
        self.edit_screen = EditScreen(name='edit')
        self.sm.add_widget(self.edit_screen)
        self.data = [{'text': x["name"], 'lol':x} for x in data]
        
        return sm
    
    def switch_to_edit(self, dic):

        self.edit_screen.dic = dic
        self.sm.current = 'edit'

    

if __name__ == '__main__':
    TestApp().run()