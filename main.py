#!/usr/bin/python
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy_communication import *
from kivy.uix.screenmanager import ScreenManager, Screen
from text_handling import *
try:
    from jnius import autoclass
    from android.runnable import run_on_ui_thread

    android_api_version = autoclass('android.os.Build$VERSION')
    AndroidView = autoclass('android.view.View')
    # AndroidPythonActivity = autoclass('org.renpy.android.PythonActivity')
    AndroidPythonActivity = autoclass('org.kivy.android.PythonActivity')

    Logger.debug(
        'Application runs on Android, API level {0}'.format(
            android_api_version.SDK_INT
        )
    )
except ImportError:
    def run_on_ui_thread(func):
        def wrapper(*args):
            Logger.debug('{0} called on non android platform'.format(
                func.__name__
            ))
        return wrapper

class SetupScreenRoom(Screen):
    ip = ''

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
        elif self.current_question < 6:
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
        KL.log.insert(action=LogAction.press, obj=answer, comment='user_answer')
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

        TTS.start()
        self.sm = ScreenManager()
        self.sm.add_widget(SetupScreenRoom(name='setup_screen_room'))
        self.sm.current = 'setup_screen_room'

        return self.sm

    def on_start(self):
        self.android_set_hide_menu()

    def init_communication(self, ip_addr):
        self.local_ip = ip_addr
        KC.start(the_ip=self.local_ip, the_parents=[self])  # 127.0.0.1

        if ip_addr == "":
            self.on_connection()

    def on_connection(self):
        self.zero_screen = ZeroScreen(name='zero_screen')
        self.sm.add_widget(self.zero_screen)
        self.questions = []
        for i in xrange(1,33):
            name = 'question_screen_'+str(i).zfill(2)
            self.questions.append(QuestionScreen(name=name))
            self.questions[-1].current_question = i
            self.sm.add_widget(self.questions[-1])

        self.end_screen = EndScreen(name='end_screen')
        self.sm.add_widget(self.end_screen)

        self.android_set_hide_menu()
        self.sm.current = 'zero_screen'

    def press_connect_button(self, ip_addr):
        # To-Do: save previous ip input
        print ip_addr
        self.init_communication(ip_addr)

    def start_assessment(self, pre_post_flag, subject_id, subject_initial):
        self.subject_id = subject_id
        self.subject_initial = subject_initial

        session = "pre" if pre_post_flag == 1 else "post"

        if self.subject_id == "" or self.subject_initial == "":
            return

        KL.start(mode=[DataMode.file, DataMode.communication, DataMode.ros], pathname=self.user_data_dir,
                 file_prefix=session + "_" + self.subject_id + "_" + self.subject_initial + "_", the_ip=self.local_ip)

        KL.log.insert(action=LogAction.data, obj='SpatialCMTTAssessmentApp', comment='start')

        self.sm.current = 'question_screen_' + str(pre_post_flag).zfill(2)
        self.android_set_hide_menu()

    def end_game(self):
        self.stop()

    @run_on_ui_thread
    def android_set_hide_menu(self):
        if android_api_version.SDK_INT >= 19:
            Logger.debug('API >= 19. Set hide menu')
            view = AndroidPythonActivity.mActivity.getWindow().getDecorView()
            view.setSystemUiVisibility(
                AndroidView.SYSTEM_UI_FLAG_LAYOUT_STABLE |
                AndroidView.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION |
                AndroidView.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN |
                AndroidView.SYSTEM_UI_FLAG_HIDE_NAVIGATION |
                AndroidView.SYSTEM_UI_FLAG_FULLSCREEN |
                AndroidView.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
            )

if __name__ == '__main__':
    SpatialSkillAssessmentApp().run()
