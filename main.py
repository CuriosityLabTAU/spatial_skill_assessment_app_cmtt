#!/usr/bin/python
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy_communication import *
from kivy.uix.screenmanager import ScreenManager, Screen
from text_handling import *


class ZeroScreen(Screen):
    pass

class EndScreen(Screen):
    pass

class QuestionScreen(Screen):
    current_question = 0

    def on_pre_enter(self, *args):
        self.next_question()

    def on_enter(self, *args):
        if self.current_question < 3:
            TTS.speak(['Look at these pieces in the red card. Look at these pictures in the blue cards. If you put the pieces in the red card together, they will make one of the pictures in the blue cards. Press the picture the pieces make.'])
        else:
            TTS.speak(['Press the picture the pieces make.'])

    def next_question(self, current_question=None):
        self.ids['A_button'].background_normal = 'images/CMTT_A_Order1_Page_' + \
                                                                 str(self.current_question * 2).zfill(2) + '_A.jpg'
        self.ids['B_button'].background_normal = 'images/CMTT_A_Order1_Page_' + \
                                                                 str(self.current_question * 2).zfill(2) + '_B.jpg'
        self.ids['C_button'].background_normal = 'images/CMTT_A_Order1_Page_' + \
                                                                 str(self.current_question * 2).zfill(2) + '_C.jpg'
        self.ids['D_button'].background_normal = 'images/CMTT_A_Order1_Page_' + \
                                                                 str(self.current_question * 2).zfill(2) + '_D.jpg'
        self.ids['pieces'].source = 'images/CMTT_A_Order1_Page_' + \
                                                    str(self.current_question * 2 + 1).zfill(2) + '.jpg'

        # because log goes after this, the name is changed to (real number - 1)
        self.ids['A_button'].name = str(self.current_question) + '_A'
        self.ids['B_button'].name = str(self.current_question) + '_B'
        self.ids['C_button'].name = str(self.current_question) + '_C'
        self.ids['D_button'].name = str(self.current_question) + '_D'


    def pressed(self, answer):
        print(answer)
        if self.current_question < 31:
            next_question = self.current_question + 2
            next_screen = 'question_screen_' + str(next_question).zfill(2)
            self.manager.current = next_screen
        else:
            # self.ids['pieces'].source = ''
            # self.ids['A_button'].background_disabled_normal = ''
            # self.ids['B_button'].background_disabled_normal = ''
            # self.ids['C_button'].background_disabled_normal = ''
            # self.ids['D_button'].background_disabled_normal = ''
            # self.ids['C_button'].text = 'The End'
            # self.ids['C_button'].font_size =36
            # self.ids['C_button'].color = (0,1,0,1)
            # self.ids['C_button'].background_color = (1,0,1,1)
            # for i in self.ids:
            #     self.ids[i].disabled = True
            self.manager.current = 'end_screen'


class SpatialSkillAssessmentApp(App):

    def build(self):

        self.init_communication()

        TTS.start()
        self.sm = ScreenManager()

        self.zero_screen = ZeroScreen(name='zero_screen')
        self.zero_screen.ids['subject_id'].bind(text=self.zero_screen.ids['subject_id'].on_text_change)
        self.sm.add_widget(self.zero_screen)

        self.questions = []
        for i in range(1,33):
            self.questions.append(QuestionScreen(name='question_screen_' + str(i).zfill(2)))
            self.questions[-1].current_question = i
            self.sm.add_widget(self.questions[-1])


        self.end_screen = EndScreen(name='end_screen')
        self.sm.add_widget(self.end_screen)

        self.sm.current = 'zero_screen'
        return self.sm


    def init_communication(self):
        KC.start(the_ip='192.168.1.254', the_parents=[self])  # 127.0.0.1
        KL.start(mode=[DataMode.file, DataMode.communication, DataMode.ros], pathname=self.user_data_dir,
                 the_ip='192.168.1.254')

    def on_connection(self):
        KL.log.insert(action=LogAction.data, obj='SpatialSkillAssessmentApp', comment='start')

    def press_start(self, current_question):
        self.sm.current = 'question_screen_' + str(current_question).zfill(2)

    def end_game(self):
        self.stop()

if __name__ == '__main__':
    SpatialSkillAssessmentApp().run()
