from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.properties import NumericProperty
from datetime import datetime, timedelta, date, time
from kivy.app import App


class PlannerScreen(Screen):
    hour_px = NumericProperty(50)
    header_h = NumericProperty(40)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        today = datetime.today()
        self.current_monday = today - timedelta(days=today.weekday())
        self.day_cols = []

    @staticmethod
    def parse_date(value):
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value).date()
            except ValueError:
                return None
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        return None

    @staticmethod
    def parse_time(value):
        if isinstance(value, str):
            for fmt in ("%H:%M:%S", "%H:%M"):
                try:
                    return datetime.strptime(value, fmt).time()
                except ValueError:
                    pass
            return None
        if isinstance(value, time):
            return value
        return None

    def _time_to_y(self, t: time) -> float:
        return self.hour_px * (t.hour + t.minute / 60.0) + 30

    def _bg_rect(self, widget, rgba, radius=8):
        with widget.canvas.before:
            Color(*rgba)
            rect = RoundedRectangle(pos=widget.pos, size=widget.size, radius=[radius,])
        widget.bind(
            pos=lambda inst, val: setattr(rect, "pos", val),
            size=lambda inst, val: setattr(rect, "size", val),
        )
        return rect

    def on_enter(self):
        self.update_week_view()

    def update_week_view(self):
        grid = self.ids.planner_grid
        grid.clear_widgets()
        grid.canvas.before.clear()
        grid.canvas.after.clear()
        self.day_cols = []

        monday = self.current_monday
        sunday = monday + timedelta(days=6)

        self.ids.month_label.text = monday.strftime("%B %Y")

        # headers row
        headers = ["Time"] + [(monday + timedelta(days=i)).strftime("%a\n%d") for i in range(7)]
        for text in headers:
            lbl = Label(
                text=text,
                bold=True,
                size_hint=(None, None),
                size=(grid.col_default_width, self.header_h),
                halign="center",
                valign="middle",
            )
            grid.add_widget(lbl)

        # time column
        total_height = self.hour_px * 24
        time_col = FloatLayout(size_hint=(None, None), size=(grid.col_default_width, total_height))
        self._draw_time_ticks(time_col)
        grid.add_widget(time_col)

        # days columns, which will contain by default the lines representing the "grid" of the planner
        for i in range(7):
            col = FloatLayout(size_hint=(None, None), size=(grid.col_default_width, total_height))
            with col.canvas.after:
                Color(1, 1, 1, 0.15)
                for h in range(0, 23, 2):
                    y = self._time_to_y(time(hour=h, minute=0))
                    Line(points=[col.x, col.y + y, col.x + col.width, col.y + y], width=1)
            col.bind(
                pos=lambda c, *_: self._redraw_day_grid(c),
                size=lambda c, *_: self._redraw_day_grid(c),
            )
            grid.add_widget(col)
            self.day_cols.append(col)

        # finally tasks are drawn on the planner
        self.draw_tasks(monday, sunday)

    def _redraw_day_grid(self, col):
        col.canvas.after.clear()
        with col.canvas.after:
            Color(1, 1, 1, 0.12)
            for h in range(0, 23, 2):
                y = self._time_to_y(time(hour=h, minute=0))
                y_coord = col.height - y
                Line(points=[col.x, y_coord, col.x + col.width, y_coord], width=1)

    # method to fill the time column
    def _draw_time_ticks(self, time_col: FloatLayout):
        time_col.clear_widgets()
        total_height = self.hour_px * 24

        for h in range(0, 24, 2):
            y = self._time_to_y(time(hour=h, minute=0))
            y_coord = total_height - y

            lbl = Label(
                text=f"{h:02d}:00",
                size_hint=(1, None),
                height=20,
                halign="center",
                valign="middle",
                color=(1, 1, 1, 0.9),
            )
            lbl.center_y = y_coord
            time_col.add_widget(lbl)

    # method to draw the tasks on the planner
    def draw_tasks(self, monday, sunday):
        grid = self.ids.planner_grid
        # to avoid an overlapping of drawn tasks, we clear them all at the beginning of the function
        for col in self.day_cols:
            col.clear_widgets()

        app = App.get_running_app()
        tasks = app.task_controller.get_all_tasks()

        for task in tasks:
            try:
                if not task.scheduled_date or not task.start_time or not task.end_time:
                    continue

                day_date = self.parse_date(task.scheduled_date)
                if not day_date or not (monday.date() <= day_date <= sunday.date()):
                    continue

                start = self.parse_time(task.start_time)
                end = self.parse_time(task.end_time)
                if not start or not end:
                    continue

                day_index = (day_date - monday.date()).days
                if day_index < 0 or day_index > 6:
                    continue

                col = self.day_cols[day_index]

                # positioning the rectangle representing the task
                total_height = self.hour_px * 24
                y1 = self._time_to_y(end)
                y2 = self._time_to_y(start)
                task_height = abs(y2 - y1)

                task_box = FloatLayout(
                    size_hint=(1, None),
                    height=task_height
                )
                task_box.pos = (day_index*grid.col_default_width, total_height - y1)

                # the color of the rectangle changes based on its priority
                task_color = (0.85,0,0,0.9) if task.priority == 3 else (1,0.65,0,0.9) if task.priority == 2 else (0,0.6,0,0.9)
                self._bg_rect(task_box, task_color, radius=8)

                # creating a label inside the rectangle with the description of the task
                txt = task.description if getattr(task, "description", "") else "Task"
                lbl = Label(
                    text=txt,
                    size_hint=(1, 1),
                    halign="center",
                    valign="middle",
                    color=(1, 1, 1, 1),
                )
                task_box.add_widget(lbl)
                lbl.pos = (day_index*grid.col_default_width, total_height - y1)

                col.add_widget(task_box)

            except Exception as e:
                print("Task planner error:", e)

    # Week navigation
    def next_week(self):
        self.current_monday += timedelta(days=7)
        self.update_week_view()

    def previous_week(self):
        self.current_monday -= timedelta(days=7)
        self.update_week_view()
