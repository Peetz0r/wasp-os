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
        self.meter = widgets.BatteryMeter()
        self._minute = None

    def handle_event(self, event_view):
        """Process events that the app is subscribed to."""
        if event_view[0] == manager.EVENT_TICK:
            self.update()
        else:
            # TODO: Raise an unexpected event exception
            pass

    def foreground(self, system, effect=None):
        """Activate the application."""
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
        watch.drawable.string('B%d' % (watch.backlight.get()), 100, 0, width=40)

    def wake(self):
        self.update()

    def draw(self, effect=None):
        """Redraw the display from scratch."""
        self._minute = None
        watch.drawable.fill()
        self.update()

    def update(self):
        """Update the display"""

        draw = watch.drawable
        now = watch.rtc.get_localtime()
        print(now)

        if self._minute is not now[4]:
            draw.rleblit(digits.clock_colon, pos=(2*30+10, 80), fg=0x8000)
            draw.rleblit(digits.clock_colon, pos=(5*30+10, 80), fg=0x8000)
            draw.rleblit(DIGITS[now[4]  % 10],  pos=(4*30, 80), fg=0xf800)
            draw.rleblit(DIGITS[now[4] // 10],  pos=(3*30, 80), fg=0xf800)
            draw.rleblit(DIGITS[now[3]  % 10],  pos=(1*30, 80), fg=0xf800)
            draw.rleblit(DIGITS[now[3] // 10],  pos=(0*30, 80), fg=0xf800)

            draw.string(WEEKDAYS[now[6]], 0, 180, width=240, spacing=8)
            draw.string('%04d - %02d - %02d' % (now[0], now[1], now[2]), 0, 210, width=240, spacing=2)

        if watch.battery.power() or self._minute is not now[4]:
            if watch.battery.charging():
                draw.set_color(0x07ff) # blue during charging
            elif watch.battery.power():
                draw.set_color(0x07e0) # green when full
            draw.string('%4.2fv' % (watch.battery.voltage_mv()/1000), 0, 0)
            draw.set_color(0xffff) #white for everything else
            draw.string('B%d' % (watch.backlight.get()), 100, 0, width=40)

            self.meter.draw()
            self.meter.update()

        draw.rleblit(DIGITS[now[5]  % 10], pos=(7*30, 80), fg=0xf800)
        draw.rleblit(DIGITS[now[5] // 10], pos=(6*30, 80), fg=0xf800)

        self._minute = now[4]
        return True
