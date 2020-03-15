import fonts.eightsegment as digits
import watch
import widgets
import manager

DIGITS = (
        digits.clock_0,
        digits.clock_1,
        digits.clock_2,
        digits.clock_3,
        digits.clock_4,
        digits.clock_5,
        digits.clock_6,
        digits.clock_7,
        digits.clock_8,
        digits.clock_9
)

WEEKDAYS = [
    'Maandag',
    'Dinsdag',
    'Woensdag',
    'Donderdag',
    'Vrijdag',
    'Zaterdag',
    'Zondag',
]

class EightSegmentClockApp(object):
    """Simple digital clock application.

    Shows a time (as HH:MM:SS) together with a battery meter and the date.
    """

    def __init__(self):
        self.on_screen = None

    def handle_event(self, event_view):
        """Process events that the app is subscribed to."""
        if event_view[0] == manager.EVENT_TICK:
            self.update()
        else:
            # TODO: Raise an unexpected event exception
            pass

    def foreground(self, system, effect=None):
        """Activate the application."""
        print('fg')
        self.draw()

        system.request_tick(1000)
        system.request_event(manager.EVENT_SWIPE_LEFTRIGHT)

    def tick(self, ticks):
        self.update()

    def background(self):
        """De-activate the application (without losing state)."""
        pass

    def sleep(self):
        return True

    def swipe(self, event):
        watch.backlight.set(watch.backlight.get()+event[0]*-2+7)

    def wake(self):
        print('wake')
        self.update()

    def draw(self, effect=None):
        """Redraw the display from scratch."""
        print('draw')
        self.on_screen = None
        watch.drawable.fill()
        self.update()

    def update(self):
        """Update the display"""

        draw = watch.drawable
        time = watch.rtc.get_localtime()
        bat = (
            watch.battery.voltage_mv(),
            watch.battery.charging(),
            watch.battery.power(),
        )
        now = (time[:5], bat)
        print(time, bat)

        if not self.on_screen or (now != self.on_screen):
            print("redraw")
            draw.rleblit(digits.clock_colon, pos=(2*30+10, 32), fg=0x8000)
            draw.rleblit(digits.clock_colon, pos=(5*30+10, 32), fg=0x8000)
            draw.rleblit(DIGITS[time[4]  % 10],  pos=(4*30, 32), fg=0xf800)
            draw.rleblit(DIGITS[time[4] // 10],  pos=(3*30, 32), fg=0xf800)
            draw.rleblit(DIGITS[time[3]  % 10],  pos=(1*30, 32), fg=0xf800)
            draw.rleblit(DIGITS[time[3] // 10],  pos=(0*30, 32), fg=0xf800)

            draw.set_color(0xffff) # white
            draw.string(WEEKDAYS[time[6]], 0, 110, width=240, spacing=8)
            draw.string('%04d - %02d - %02d' % (time[0], time[1], time[2]), 0, 140, width=240, spacing=3)

            if watch.battery.charging():
                draw.set_color(0x07ff) # blue during charging
            elif watch.battery.power():
                draw.set_color(0x07e0) # green when full
            draw.string('%4.2fv' % (watch.battery.voltage_mv()/1000), 0, 0, width=80)

        draw.rleblit(DIGITS[time[5]  % 10], pos=(7*30, 32), fg=0xf800)
        draw.rleblit(DIGITS[time[5] // 10], pos=(6*30, 32), fg=0xf800)

        self.on_screen = now
        return True
