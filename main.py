from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.core.window import Window
import itertools

# === Ряды сопротивлений ===
E12_BASE = [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82]
E24_BASE = [10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 
            33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91]

def generate_resistor_values(series='E24'):
    """Генерирует список номиналов выбранного ряда от 1 Ома до 10 МОм"""
    base = E12_BASE if series == 'E12' else E24_BASE
    all_resistors = []
    for multiplier_exp in range(-1, 7):
        multiplier = 10 ** multiplier_exp
        for b in base:
            all_resistors.append(round(b * multiplier, 5))
    return sorted(list(set(all_resistors)))

def format_resistor(val):
    """Форматирует номинал с 3 знаками после запятой"""
    if val >= 1_000_000:
        return f"{val/1_000_000:.3f}M"
    elif val >= 1_000:
        return f"{val/1_000:.3f}k"
    elif val >= 1:
        return f"{val:.3f}"
    else:
        return f"{val*1000:.3f}m"

def find_combinations(target_r, count, series='E24'):
    """Ищет лучшие комбинации резисторов"""
    resistors = generate_resistor_values(series)
    search_pool = [r for r in resistors if target_r <= r <= target_r * 20]
    results = []
    
    if count == 2:
        for r1, r2 in itertools.combinations(search_pool, 2):
            r_total = (r1 * r2) / (r1 + r2)
            error = (r_total - target_r) / target_r * 100  # со знаком
            results.append({'values': (r1, r2), 'total': r_total, 'error': error})
        for r1 in search_pool:
            r_total = r1 / 2
            error = (r_total - target_r) / target_r * 100
            results.append({'values': (r1, r1), 'total': r_total, 'error': error})
    elif count == 3:
        for r1, r2, r3 in itertools.combinations(search_pool, 3):
            r_total = 1 / (1/r1 + 1/r2 + 1/r3)
            error = (r_total - target_r) / target_r * 100
            results.append({'values': (r1, r2, r3), 'total': r_total, 'error': error})
    
    results.sort(key=lambda x: abs(x['error']))  # сортировка по модулю погрешности
    return results[:15]

# === UI ===
class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_mode = 2  # 2 или 3 резистора
        self.current_series = 'E24'  # ряд E12 или E24
        
        # Главный контейнер
        layout = MDBoxLayout(orientation='vertical', padding=dp(16), spacing=dp(12))
        
        # 📋 Заголовок
        title_label = MDLabel(
            text="Подбор резисторов",
            font_style="H5",
            size_hint=(1, None),
            height=dp(40),
            halign="center"
        )
        
        # 📝 Надпись над полем ввода
        input_label = MDLabel(
            text="Необходимое сопротивление:",
            font_style="Subtitle1",
            size_hint=(1, None),
            height=dp(30),
            padding=(0, dp(10), 0, 0)
        )
        
        # 📥 Поле ввода (без input_filter для поддержки kKmM)
        self.input_field = MDTextField(
            hint_text="Например: 1354 или 1.5k или 2.2M",
            mode="rectangle",
            size_hint=(1, None),
            height=dp(56),
            multiline=False
        )
        
        # 🔘 Кнопки выбора ряда (E12 / E24)
        series_label = MDLabel(
            text="Ряд сопротивлений:",
            font_style="Subtitle1",
            size_hint=(1, None),
            height=dp(30),
            padding=(0, dp(5), 0, 0)
        )
        
        series_box = MDBoxLayout(size_hint=(1, None), height=dp(40), spacing=dp(10))
        self.btn_e12 = MDFlatButton(text="Ряд E12", size_hint=(0.5, 1))
        self.btn_e24 = MDFlatButton(text="Ряд E24", size_hint=(0.5, 1))
        self.btn_e12.md_bg_color = (0.8, 0.8, 0.8, 1)
        self.btn_e12.text_color = (0, 0, 0, 1)
        self.btn_e24.md_bg_color = (0.25, 0.55, 1, 1)
        self.btn_e24.text_color = (1, 1, 1, 1)
        self.btn_e12.bind(on_press=lambda x: self.set_series('E12'))
        self.btn_e24.bind(on_press=lambda x: self.set_series('E24'))
        series_box.add_widget(self.btn_e12)
        series_box.add_widget(self.btn_e24)
        
        # 🔘 Кнопки переключения режима (2 / 3 резистора)
        mode_label = MDLabel(
            text="Количество резисторов:",
            font_style="Subtitle1",
            size_hint=(1, None),
            height=dp(30),
            padding=(0, dp(5), 0, 0)
        )
        
        btn_box = MDBoxLayout(size_hint=(1, None), height=dp(40), spacing=dp(10))
        self.btn_2 = MDFlatButton(text="2 резистора", size_hint=(0.5, 1))
        self.btn_3 = MDFlatButton(text="3 резистора", size_hint=(0.5, 1))
        self.btn_2.md_bg_color = (0.25, 0.55, 1, 1)
        self.btn_2.text_color = (1, 1, 1, 1)
        self.btn_3.md_bg_color = (0.8, 0.8, 0.8, 1)
        self.btn_3.text_color = (0, 0, 0, 1)
        self.btn_2.bind(on_press=lambda x: self.set_mode(2))
        self.btn_3.bind(on_press=lambda x: self.set_mode(3))
        btn_box.add_widget(self.btn_2)
        btn_box.add_widget(self.btn_3)
        
        # 🧮 Кнопка расчёта
        self.calc_button = MDRaisedButton(
            text="🔍 Рассчитать",
            size_hint=(1, None),
            height=dp(50),
            md_bg_color=(0.25, 0.55, 1, 1)
        )
        self.calc_button.bind(on_press=self.calculate)
        
        # 📋 Заголовок результатов
        self.result_label = MDLabel(
            text="Результаты:",
            font_style="Subtitle1",
            size_hint=(1, None),
            height=dp(30),
            padding=(0, dp(10), 0, 0)
        )
        
        # 📜 Список результатов
        self.scroll = MDScrollView(size_hint=(1, 1), bar_width=dp(4))
        self.result_list = MDBoxLayout(
            orientation='vertical',
            spacing=dp(6),
            padding=dp(8),
            size_hint_y=None,
            height=dp(100)
        )
        self.scroll.add_widget(self.result_list)
        
        # Сборка
        layout.add_widget(title_label)
        layout.add_widget(input_label)
        layout.add_widget(self.input_field)
        layout.add_widget(series_label)
        layout.add_widget(series_box)
        layout.add_widget(mode_label)
        layout.add_widget(btn_box)
        layout.add_widget(self.calc_button)
        layout.add_widget(self.result_label)
        layout.add_widget(self.scroll)
        self.add_widget(layout)
    
    def set_series(self, series):
        """Установка ряда сопротивлений"""
        self.current_series = series
        for btn, s in [(self.btn_e12, 'E12'), (self.btn_e24, 'E24')]:
            if s == series:
                btn.md_bg_color = (0.25, 0.55, 1, 1)
                btn.text_color = (1, 1, 1, 1)
            else:
                btn.md_bg_color = (0.8, 0.8, 0.8, 1)
                btn.text_color = (0, 0, 0, 1)
        if self.result_list.children:
            self.calculate(None)
    
    def set_mode(self, mode):
        """Установка количества резисторов"""
        self.current_mode = mode
        for btn, m in [(self.btn_2, 2), (self.btn_3, 3)]:
            if m == mode:
                btn.md_bg_color = (0.25, 0.55, 1, 1)
                btn.text_color = (1, 1, 1, 1)
            else:
                btn.md_bg_color = (0.8, 0.8, 0.8, 1)
                btn.text_color = (0, 0, 0, 1)
        if self.result_list.children:
            self.calculate(None)
    
    def calculate(self, instance):
        try:
            text = self.input_field.text.lower().replace(',', '.').strip()
            mult = 1
            
            # Обработка суффиксов k, K, m, M
            if text.endswith('k'):
                mult, text = 1000, text[:-1]
            elif text.endswith('m'):
                mult, text = 1000000, text[:-1]
            
            target = float(text) * mult
            
            self.result_list.clear_widgets()
            results = find_combinations(target, self.current_mode, self.current_series)
            
            for res in results:
                vals = " || ".join(format_resistor(v) for v in res['values'])
                error = res['error']
                # Форматирование погрешности со знаком +/-
                error_str = f"{error:+.3f}%"
                color = self._get_color(abs(error))
                
                item = TwoLineListItem(
                    text=vals,
                    secondary_text=f"= {format_resistor(res['total'])}  |  {error_str}",
                    secondary_text_color=color,
                    size_hint=(1, None),
                    height=dp(60)
                )
                self.result_list.add_widget(item)
            
            Clock.schedule_once(lambda dt: self._update_height(), 0.05)
                
        except ValueError:
            self.input_field.error = True
            self.input_field.hint_text = "❌ Введите число (например: 1354, 1.5k, 2.2M)"
    
    def _update_height(self):
        if hasattr(self, 'result_list'):
            self.result_list.height = max(dp(100), self.result_list.minimum_height)
    
    def _get_color(self, error):
        """Цвет погрешности: зелёный <0.5%, жёлтый <2%, красный >=2%"""
        if error < 0.5:
            return (0, 0.75, 0, 1)
        elif error < 2:
            return (1, 0.7, 0, 1)
        else:
            return (1, 0, 0, 1)

class ResistorApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        Window.size = (400, 700)  # Чуть больше для нового интерфейса
        return MainScreen()

if __name__ == '__main__':
    ResistorApp().run()
