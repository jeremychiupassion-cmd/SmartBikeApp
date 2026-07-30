import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Mesh, Point
from kivy.utils import platform
from plyer import gps
import cv2
import numpy as np
import threading
import time

# ==========================================
# Android 系統 JNI 介面綁定 (語音與蜂鳴器)
# ==========================================
if platform == 'android':
    from jnius import autoclass, PythonJavaClass, java_method, cast
    from android.permissions import request_permissions, Permission
    from android.runnable import run_on_ui_thread

    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    RecognizerIntent = autoclass('android.speech.RecognizerIntent')
    SpeechRecognizer = autoclass('android.speech.SpeechRecognizer')
    Context = autoclass('android.content.Context')
    ToneGenerator = autoclass('android.media.ToneGenerator')
    AudioManager = autoclass('android.media.AudioManager')
    
    class BackgroundSpeechListener(PythonJavaClass):
        __javainterfaces__ = ['android/speech/RecognitionListener']

        def __init__(self, callback, restart_callback):
            super(BackgroundSpeechListener, self).__init__()
            self.callback = callback
            self.restart_callback = restart_callback

        @java_method('(Landroid/os/Bundle;)V')
        def onReadyForSpeech(self, params): pass
        @java_method('()V')
        def onBeginningOfSpeech(self): pass
        @java_method('(F)V')
        def onRmsChanged(self, rmsdB): pass
        @java_method('([B)V')
        def onBufferReceived(self, buffer): pass
        @java_method('()V')
        def onEndOfSpeech(self): pass

        @java_method('(I)V')
        def onError(self, error):
            self.restart_callback()
        
        @java_method('(Landroid/os/Bundle;)V')
        def onResults(self, results):
            matches = results.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
            if matches and matches.size() > 0:
                self.callback(str(matches.get(0)))
            self.restart_callback()
            
        @java_method('(Landroid/os/Bundle;)V')
        def onPartialResults(self, partialResults):
            matches = partialResults.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
            if matches and matches.size() > 0:
                self.callback(str(matches.get(0)))

        @java_method('(ILandroid/os/Bundle;)V')
        def onEvent(self, eventType, params): pass
else:
    def run_on_ui_thread(func):
        return func

# ==========================================
# 前鏡頭後方來車判斷邏輯 (OpenCV)
# ==========================================
class VehicleDetector:
    def __init__(self, alert_callback):
        self.alert_callback = alert_callback
        self.running = False
        self.cap = None
        self.prev_area = 0
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40, detectShadows=False)

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._process_camera)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.running = False
        if self.cap:
            try:
                self.cap.release()
            except Exception:
                pass

    def _process_camera(self):
        # 容錯處理：安全開啟鏡頭
        try:
            camera_idx = 1 if platform == 'android' else 0
            self.cap = cv2.VideoCapture(camera_idx)
            if not self.cap.isOpened():
                self.cap = cv2.VideoCapture(0)
        except Exception:
            return

        while self.running:
            try:
                ret, frame = self.cap.read()
                if not ret or frame is None:
                    time.sleep(0.1)
                    continue

                # 壓縮圖像加速計算
                frame = cv2.resize(frame, (320, 240))
                fg_mask = self.bg_subtractor.apply(frame)

                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
                fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)

                contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                max_area = 0
                for cnt in contours:
                    area = cv2.contourArea(cnt)
                    if area > 1000: 
                        if area > max_area:
                            max_area = area

                # 判定車輛急速靠近
                if self.prev_area > 0 and max_area > self.prev_area * 1.5 and max_area > 3000:
                    # 安全修正：透過 Kivy Clock 安全投遞至主線程，避免跨線程繪圖閃退
                    Clock.schedule_once(lambda dt: self.alert_callback(), 0)

                self.prev_area = max_area
                time.sleep(0.1) 
            except Exception:
                time.sleep(0.2)

# ==========================================
# 中控台主程式
# ==========================================
class BikeDashboard(Widget):
    def __init__(self, **kwargs):
        super(BikeDashboard, self).__init__(**kwargs)
        self.mode = 'straight'
        self.anim_step = 0
        self.flash_state = False
        self.light_color = (1.0, 0.5, 0.0) 
        self.sound_alert_enabled = True 
        
        self.tone_gen = None
        if platform == 'android':
            try:
                self.tone_gen = ToneGenerator(AudioManager.STREAM_ALARM, 100)
            except Exception:
                pass
                
        self.speech_recognizer = None
        self.speech_intent = None
        self.speech_listener = None
        self.detector = None
        
        self.last_warning_time = 0
        self.backup_color = self.light_color
        
        self.left_points = []
        self.right_points = []
        self.dot_radius = 4

        self.bind(size=self.update_shapes, pos=self.update_shapes)
        Clock.schedule_interval(self.update_animation, 0.05) 
        Clock.schedule_once(self.init_android_system, 1.5)

    def init_android_system(self, dt):
        if platform == 'android':
            try:
                request_permissions([
                    Permission.RECORD_AUDIO, 
                    Permission.CAMERA,
                    Permission.ACCESS_FINE_LOCATION,
                    Permission.ACCESS_COARSE_LOCATION
                ], self.on_permissions_result)
            except Exception:
                pass
        else:
            self.start_camera_detection()

    def on_permissions_result(self, permissions, grant_results):
        if all(grant_results):
            Clock.schedule_once(lambda dt: self.start_background_listening(), 1.0)
            Clock.schedule_once(lambda dt: self.start_gps(), 1.0)
            Clock.schedule_once(lambda dt: self.start_camera_detection(), 2.0)

    def start_camera_detection(self):
        self.detector = VehicleDetector(self.trigger_approaching_warning)
        self.detector.start()

    def trigger_approaching_warning(self):
        # 冷卻機制：防範重複觸發
        current_time = time.time()
        if current_time - self.last_warning_time > 3.0:
            self.last_warning_time = current_time
            self._process_warning_ui()

    def _process_warning_ui(self):
        self.backup_color = self.light_color
        self.set_color((1.0, 0.0, 0.0))
        
        if self.sound_alert_enabled and self.tone_gen:
            try:
                self.tone_gen.startTone(ToneGenerator.TONE_CDMA_EMERGENCY_RINGBACK, 400)
            except Exception:
                pass
                
        # 0.5 秒後恢復先前色彩
        Clock.schedule_once(self._restore_color, 0.5)

    def _restore_color(self, dt):
        self.set_color(self.backup_color)

    def start_gps(self):
        if platform == 'android':
            try:
                gps.configure(on_location=self.on_location, on_status=self.on_gps_status)
                gps.start(minTime=1000, minDistance=1)
            except Exception: pass

    def on_location(self, **kwargs):
        speed_ms = kwargs.get('speed') or 0  
        Clock.schedule_once(lambda dt: self.update_speed_ui(speed_ms), 0)

    def update_speed_ui(self, speed_ms):
        app = App.get_running_app()
        if speed_ms > 0:
            app.speed_label.text = f"{int(speed_ms * 3.6)} km/h"
        else:
            app.speed_label.text = "0 km/h"

    def on_gps_status(self, stype, status): pass

    @run_on_ui_thread
    def start_background_listening(self):
        if platform == 'android':
            try:
                activity = PythonActivity.mActivity
                self.speech_recognizer = SpeechRecognizer.createSpeechRecognizer(activity)
                self.speech_listener = BackgroundSpeechListener(self.process_command_safe, self.restart_listening_safe)
                self.speech_recognizer.setRecognitionListener(self.speech_listener)
                self.speech_intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
                self.speech_intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                self.speech_intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, "zh-TW")
                self.speech_intent.putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, True)
                self.speech_recognizer.startListening(self.speech_intent)
            except Exception: pass

    def process_command_safe(self, text):
        Clock.schedule_once(lambda dt: self.process_command(text), 0)

    def restart_listening_safe(self):
        Clock.schedule_once(lambda dt: self.restart_listening(), 0.3)

    @run_on_ui_thread
    def restart_listening(self):
        if platform == 'android' and self.speech_recognizer and self.speech_intent:
            try:
                self.speech_recognizer.cancel()
                self.speech_recognizer.startListening(self.speech_intent)
            except Exception: pass

    def process_command(self, command):
        if "左" in command or "向左" in command: self.mode = 'left'
        elif "右" in command or "向右" in command: self.mode = 'right'
        elif "正常" in command or "直行" in command: self.mode = 'straight'
        elif "開燈" in command or "亮燈" in command: self.toggle_flash(True)
        elif "關燈" in command or "熄滅" in command: self.toggle_flash(False)
        elif "開啟警報" in command or "開警報" in command:
            self.sound_alert_enabled = True
            App.get_running_app().update_sound_btn_ui()
        elif "關閉警報" in command or "關警報" in command:
            self.sound_alert_enabled = False
            App.get_running_app().update_sound_btn_ui()
        elif "紅" in command: self.set_color((1.0, 0.1, 0.1))
        elif "綠" in command: self.set_color((0.2, 1.0, 0.2))
        elif "藍" in command: self.set_color((0.2, 0.5, 1.0))
        elif "黃" in command or "橘" in command: self.set_color((1.0, 0.5, 0.0))

    def set_color(self, color_tuple):
        self.light_color = color_tuple[:3]

    @run_on_ui_thread
    def toggle_flash(self, state):
        self.flash_state = state
        if platform == 'android':
            try:
                activity = PythonActivity.mActivity
                camera_manager = cast('android.hardware.camera2.CameraManager', activity.getSystemService(Context.CAMERA_SERVICE))
                for cam_id in camera_manager.getCameraIdList():
                    try:
                        camera_manager.setTorchMode(cam_id, state)
                        break
                    except Exception: continue
            except Exception: pass

    def update_shapes(self, *args):
        w, h = self.width, self.height
        if w < 100 or h < 100: return
        cx, cy = w / 2, h / 2
        total_len = w * 0.75
        head_len = total_len * 0.45
        tail_h = h * 0.35
        head_h = h * 0.75
        start_x = cx - total_len / 2
        end_x = cx + total_len / 2
        head_start_x = end_x - head_len
        spacing = max(10, int(h / 25))
        self.dot_radius = max(3, int(spacing * 0.4))
        self.right_points = []
        self.left_points = []
        for x in range(int(start_x), int(end_x), spacing):
            for y in range(int(cy - head_h/2), int(cy + head_h/2), spacing):
                inside = False
                if x <= head_start_x:
                    if abs(y - cy) <= tail_h / 2: inside = True
                else:
                    progress = (x - head_start_x) / head_len
                    current_half_h = (head_h / 2) * (1 - progress)
                    if abs(y - cy) <= current_half_h: inside = True
                if inside:
                    self.right_points.append((x, y))
                    self.left_points.append((2 * cx - x, y))
        self.draw_ui()

    def update_animation(self, dt):
        self.anim_step += 1
        self.draw_ui()

    def draw_polygon(self, points):
        vertices = []
        indices = list(range(len(points)))
        for pt in points: vertices.extend([pt[0], pt[1], 0, 0])
        return Mesh(vertices=vertices, indices=indices, mode='triangle_fan')

    def draw_ui(self, *args):
        self.canvas.clear()
        r, g, b = self.light_color
        with self.canvas:
            Color(0, 0, 0, 1) 
            Rectangle(pos=(0, 0), size=(self.width, self.height))
            if self.mode == 'straight':
                if (self.anim_step // 10) % 2 == 0:
                    Color(r, g, b, 1) 
                    tri_w = self.width / 5
                    tri_h = self.height * 0.6
                    base_y = (self.height - tri_h) / 2
                    for i in range(3):
                        center_x = self.width * (0.3 + i * 0.2)
                        pts = [(center_x, base_y + tri_h), (center_x - tri_w/2, base_y), (center_x + tri_w/2, base_y)]
                        self.draw_polygon(pts)
            elif self.mode in ('left', 'right'):
                total_steps = 15
                current_step = self.anim_step % total_steps
                progress = current_step / float(total_steps)
                w = self.width
                total_len = w * 0.75
                bright_flat = []
                dim_flat = []
                if self.mode == 'right':
                    start_x = (w / 2) - total_len / 2
                    cutoff_x = start_x + total_len * progress
                    for (x, y) in self.right_points:
                        if x <= cutoff_x: bright_flat.extend([x, y])
                        else: dim_flat.extend([x, y])
                elif self.mode == 'left':
                    end_x = (w / 2) + total_len / 2
                    cutoff_x = end_x - total_len * progress
                    for (x, y) in self.left_points:
                        if x >= cutoff_x: bright_flat.extend([x, y])
                        else: dim_flat.extend([x, y])

                Color(0.15, 0.05, 0, 1)
                if dim_flat: Point(points=dim_flat, pointsize=self.dot_radius)
                if bright_flat:
                    Color(r, g, b, 0.15) 
                    Point(points=bright_flat, pointsize=self.dot_radius * 4) 
                    Color(r, g, b, 1) 
                    Point(points=bright_flat, pointsize=self.dot_radius)

    @run_on_ui_thread
    def stop_services(self):
        if self.detector: self.detector.stop()
        if platform == 'android':
            try:
                gps.stop()
                if self.speech_recognizer:
                    self.speech_recognizer.cancel()
                    self.speech_recognizer.destroy()
                if self.tone_gen:
                    self.tone_gen.release()
            except Exception: pass

class SmartBikeApp(App):
    def build(self):
        root = FloatLayout()
        self.dashboard = BikeDashboard()
        root.add_widget(self.dashboard)
        
        self.speed_label = Label(
            text="0 km/h", font_size='36sp', bold=True, color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.3, 'top': 0.98}, size_hint=(None, None)
        )
        root.add_widget(self.speed_label)
        
        self.sound_btn = Button(
            text="SOUND: ON", font_size='14sp', bold=True,
            background_normal='', background_color=(0.2, 0.8, 0.2, 1),
            pos_hint={'right': 0.98, 'top': 0.95}, size_hint=(0.2, 0.1)
        )
        self.sound_btn.bind(on_press=self.toggle_sound_setting)
        root.add_widget(self.sound_btn)
        
        btn_layout = BoxLayout(
            orientation='horizontal', size_hint=(0.9, 0.12),  
            pos_hint={'center_x': 0.5, 'y': 0.03}, spacing=10              
        )
        btn_red = Button(text="RED", background_normal='', background_color=(1, 0.2, 0.2, 1))
        btn_red.bind(on_press=lambda x: self.dashboard.set_color((1.0, 0.1, 0.1)))
        
        btn_green = Button(text="GREEN", background_normal='', background_color=(0.2, 1.0, 0.2, 1))
        btn_green.bind(on_press=lambda x: self.dashboard.set_color((0.2, 1.0, 0.2)))
        
        btn_blue = Button(text="BLUE", background_normal='', background_color=(0.2, 0.5, 1.0, 1))
        btn_blue.bind(on_press=lambda x: self.dashboard.set_color((0.2, 0.5, 1.0)))
        
        btn_orange = Button(text="ORANGE", background_normal='', background_color=(1.0, 0.5, 0.0, 1))
        btn_orange.bind(on_press=lambda x: self.dashboard.set_color((1.0, 0.5, 0.0)))
        
        btn_layout.add_widget(btn_red)
        btn_layout.add_widget(btn_green)
        btn_layout.add_widget(btn_blue)
        btn_layout.add_widget(btn_orange)
        root.add_widget(btn_layout)
        return root

    def toggle_sound_setting(self, instance):
        self.dashboard.sound_alert_enabled = not self.dashboard.sound_alert_enabled
        self.update_sound_btn_ui()

    def update_sound_btn_ui(self):
        if self.dashboard.sound_alert_enabled:
            self.sound_btn.text = "SOUND: ON"
            self.sound_btn.background_color = (0.2, 0.8, 0.2, 1)
        else:
            self.sound_btn.text = "SOUND: OFF"
            self.sound_btn.background_color = (0.5, 0.5, 0.5, 1)

    def on_pause(self): return True
    def on_stop(self): self.dashboard.stop_services()

if __name__ == '__main__':
    SmartBikeApp().run()