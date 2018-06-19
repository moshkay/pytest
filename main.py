from kivy.app import App
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.clock import Clock
from kivymd.theming import ThemeManager
from kivy.properties import StringProperty,ObjectProperty,ListProperty
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
from random import sample
from kivymd.list import ILeftBodyTouch
from kivymd.button import MDIconButton
from kivy.utils import get_color_from_hex as get_color



class ToolbarScreen(Screen):
    page_title=StringProperty("")
    left=ListProperty([])
    right=ListProperty([])
    next_page=StringProperty("")
    childer = ObjectProperty(None)
    def __init__(self,**opt):
        super(ToolbarScreen,self).__init__(**opt)

    def move(self,*args):
        #print(self.next_page)
        app.root.current=self.next_page

class Splash(Screen):
    def __init__(self,**opt):
        super(Splash,self).__init__(**opt)
        

class Home(ToolbarScreen):
    def __init__(self,**opt):
        super(Home,self).__init__(**opt)

class About(ToolbarScreen):
    def __init__(self,**opt):
        super(About,self).__init__(**opt)

class Question(ToolbarScreen):
    quest=ObjectProperty(None)
    optA=ObjectProperty(None)
    optB=ObjectProperty(None)
    optC=ObjectProperty(None)
    optD=ObjectProperty(None)
    exp = ObjectProperty(None)
    questNum = ObjectProperty(None)
    questStatus =ObjectProperty(None)
    
    
    def __init__(self,**opt):
        super(Question,self).__init__(**opt)
    def choice(self,widget):
        if widget.state == "down":
            #print(widget.value,"is picked")
            val_select = widget.value
            #storing the selected ans
            #print("previous",self.choosedAns)
            self.choosedAns[self.index-1] = val_select
            correct_ans = self.correctAns[self.index-1]
            #print("current",self.choosedAns)
            #print(val_select.lower())
            if correct_ans != val_select.lower():
                self.exp.text = "Explanation: \n"+self.store.get(self.all_questions[self.index-1])["explanation"]
                #print(type(self.ids["stateB"].icon
                #print(val_select)
                self.questStatus.text="Wrong"
                self.questStatus.secondary_text="The correct Answer is {}".format(correct_ans.upper())
                self.questStatus.children[0].children[0].icon = "close"
                self.questStatus.children[0].children[0].text_color=[1,0,0,1]
            else:
                self.exp.text = "Explanation: \n"+self.store.get(self.all_questions[self.index-1])["explanation"]
                self.questStatus.text="Correct"
                self.questStatus.secondary_text="..."
                self.questStatus.children[0].children[0].icon="check"
                self.questStatus.children[0].children[0].text_color=[0,1,0,1]
            
            
    def load_quest(self):
        self.store = JsonStore("question.json")
        ids = self.store.keys()
        
        self.all_questions = sample(ids,20)
        
        #refreshing the checkbuttons
        self.exp.text = ""
        self.questStatus.text=""
        self.questStatus.secondary_text=""
        self.questStatus.children[0].children[0].text_color = get_color("#fce4ec")
        self.clearOpts()
        self.index=1
        self.correctAns = [self.store.get(i)['answer'].replace("\r","") for i in self.all_questions]
        self.choosedAns = ["" for i in range(len(self.all_questions))]
        #self.quest1=self.store.get(self.all_questions[self.index-1])["quest"]
        self.questNum.text = str(self.index)+"/"+str(len(self.all_questions))
        self.quest.text=str(self.index)+". " +self.store.get(self.all_questions[self.index-1])["quest"]
        self.optA.text=self.store.get(self.all_questions[self.index-1])["a"]
        self.optB.text=self.store.get(self.all_questions[self.index-1])["b"]
        self.optC.text=self.store.get(self.all_questions[self.index-1])["c"]
        self.optD.text=self.store.get(self.all_questions[self.index-1])["d"]
       # print(self.store.get(self.all_questions[self.index-1]))
    def next_quest(self,*args):
        if self.index<len(self.all_questions):
            self.index+=1
            #self.quest1=self.all_questions[self.index-1]
            self.questNum.text = str(self.index)+"/"+str(len(self.all_questions))
            self.quest.text=str(self.index)+". " +self.store.get(self.all_questions[self.index-1])["quest"]
            self.optA.text = self.store.get(self.all_questions[self.index-1])["a"]
            self.optB.text = self.store.get(self.all_questions[self.index-1])["b"]
            self.optC.text = self.store.get(self.all_questions[self.index-1])["c"]
            self.optD.text = self.store.get(self.all_questions[self.index-1])["d"]
            self.clearOpts()
            #print(self.choosedAns)
            #print(self.correctAns)
            #refreshing the checkbuttons
            #refreshing the checkbuttons
            if self.choosedAns[self.index-1] !="":
                print("previously answered")
                choice = "check"+self.choosedAns[self.index-1]
                self.ids[choice].active = True
            else:    
                self.exp.text = ""
                self.questStatus.text=""
                self.questStatus.secondary_text=""
                self.questStatus.children[0].children[0].text_color = get_color("#fce4ec")

    def submit(self):
        score = 0
        counter = 0
        for i in self.choosedAns:
            if i.lower() == self.correctAns[counter].lower():
                score += 1
            counter+=1
        return (counter,score)
            
    def prev_quest(self,*args):
        
        if self.index>1:
        	self.clearOpts()
        	self.index-=1
        	self.questNum.text = str(self.index)+"/"+str(len(self.all_questions))
        	self.quest.text=str(self.index)+". " +self.store.get(self.all_questions[self.index-1])["quest"]
        	self.optA.text = self.store.get(self.all_questions[self.index-1])["a"]
        	self.optB.text = self.store.get(self.all_questions[self.index-1])["b"]
        	self.optC.text = self.store.get(self.all_questions[self.index-1])["c"]
        	self.optD.text = self.store.get(self.all_questions[self.index-1])["d"]
        	if self.choosedAns[self.index-1] !="":
        		#print("previously answered")
        		choice = "check"+self.choosedAns[self.index-1]
        		self.ids[choice].active = True
        #print(self.index)
    def clearOpts(self):
        
        checkButs = ["checkA","checkB","checkC","checkD"]
        for checkbut in checkButs:
            self.ids[checkbut].active =False
        

class Result(ToolbarScreen):
    result_out=""
    scoreLab= ObjectProperty(None)
    overallLab = ObjectProperty(None)
    def __init__(self,**opt):
        super(Result,self).__init__(**opt)
    def result(self,*args):
        quest = app.root.screens[1]
        noQuest_and_score = quest.submit()
        noQuest = noQuest_and_score[0]
        score = noQuest_and_score[1]
        self.scoreLab.text = str(score)
        self.overallLab.text = str(noQuest)
        #print("You scored %d out of %d questions"%(score,noQuest))

class Manager(ScreenManager):
    def __init__(self,**opt):
        super(Manager,self).__init__(**opt)
        Clock.schedule_once(self.move,10)
    def move(self,dt):
        #print(self.current)
        self.switch_to(Home(),direction="right")
class IconLeftWidget(ILeftBodyTouch, MDIconButton):
    pass
class QuizApp(App):
    title="Python Quiz Mobile"
    icon = "images/splash_icon.png"
    theme_cls = ThemeManager()
    
    def build(self):
        return Manager()
    def on_pause(self):
    	return True 

#Window.system_size=(360,470)
app=QuizApp()
app.run()
