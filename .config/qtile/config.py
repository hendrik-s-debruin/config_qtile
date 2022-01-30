#  ================================== Imports ============================== {{{
from typing import List , Optional, Tuple # noqa: F401
from enum import Enum

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, KeyChord
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.command import lazy
from libqtile.layout.tree import Section as TreeSection
from libqtile.command.client import InteractiveCommandClient
import subprocess
import os
from typing import NamedTuple, Any
from libqtile.core.manager import Qtile
from collections import deque
# }}}
# =============================== Qtile Settings =========================== {{{
auto_fullscreen            = True
focus_on_window_activation = "smart"
reconfigure_screens        = True
auto_minimize              = True
dgroups_key_binder         = None
dgroups_app_rules          = []
follow_mouse_focus         = True
bring_front_click          = False
cursor_warp                = False
wmname                     = "LG3D"
# }}}
# =================================== Globals ============================== {{{
mod                  = "mod4"
terminal             = guess_terminal()
border_width         = 2
margin               = 10
config_dir           = os.path.expanduser("~/.config/qtile")
# }}}
# ================================ Key Bindings ============================ {{{
@lazy.function
def active_group_to_next_screen(qtile):
    current_group = qtile.current_group
    qtile.cmd_next_screen()
    current_group.cmd_toscreen()

keys = [
    # ---------------------------- Window management ---------------------- {{{{
    # Focus
    Key([mod], "h", lazy.layout.left(),  desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(),  desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(),    desc="Move focus up"),

    # Move
    Key([mod, "shift"],   "h", lazy.layout.shuffle_left(),  lazy.layout.move_left(),  desc="Move window to the left"),
    Key([mod, "shift"],   "l", lazy.layout.shuffle_right(), lazy.layout.move_right(), desc="Move window to the right"),
    Key([mod, "shift"],   "j", lazy.layout.shuffle_down(),  lazy.layout.move_down(),  desc="Move window down"),
    Key([mod, "shift"],   "k", lazy.layout.shuffle_up(),    lazy.layout.move_up(),    desc="Move window up"),
    Key([mod, "control"], "k", lazy.layout.section_up(),                              desc="Move window up a section"),
    Key([mod, "control"], "j", lazy.layout.section_down(),                            desc="Move window down a section"),

    # Screen management
    Key([mod], "space",          lazy.next_screen(),           desc="Focus next screen"),
    Key([mod, "shift"], "space", active_group_to_next_screen,  desc="Move current group to the next screen"),

    Key([mod], "w", lazy.layout.toggle_split(), desc="Toggle layout split"),

    # Kill
    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),

    # Full screen and floating
    Key([mod],          "f", lazy.window.toggle_fullscreen(), desc="Toggle full screen"),
    Key([mod, "shift"], "f", lazy.window.toggle_floating(),   desc="Toggle full screen"),

    # Resize
    KeyChord([mod], "r", [
            Key([], "g", lazy.layout.increase_ratio(),  desc="Grow window"),
            Key([], "s", lazy.layout.decrease_ratio(), desc="Shrink window"),
            Key([], "n", lazy.layout.normalize(),      desc="Normalize window"),
            Key([], "m", lazy.layout.maximize(),       desc="Maximize window"),
            Key([], "h", lazy.layout.grow_left(),      desc="Grow window to the left"),
            Key([], "l", lazy.layout.grow_right(),     desc="Grow window to the right"),
            Key([], "j", lazy.layout.grow_down(),      desc="Grow window down"),
            Key([], "k", lazy.layout.grow_up(),        desc="Grow window up"),
        ],
        mode="Resize [G]row [S]hrink [N]ormalize [M]aximize [hljk]"
    ),
    # }}}}
    # -------------------------------- Shutdown --------------------------- {{{{
    KeyChord([mod, "shift"], "e", [
            Key([], "s", lazy.spawn("shutdown now"), desc="Shutdown"),
            Key([], "r", lazy.spawn("reboot"),       desc="Reboot"),
            Key([], "k", lazy.shutdown(),            desc="Shutdown Qtile"),
        ],
        mode="[S]utdown [R]eboot [K]ill Qtile"
    ),
    # }}}}
    # ------------------------------- Screenshots ------------------------- {{{{
    KeyChord([mod, "shift"], "p", [
            Key([], "a", lazy.spawn(config_dir + "/screenshot active"),  desc="Take a screenshot of the active window"),
            Key([], "s", lazy.spawn(config_dir + "/screenshot section"), desc="Take a screenshot of a section of the screen"),
            Key([], "f", lazy.spawn(config_dir + "/screenshot full"),    desc="Take a screenshot of the entire desktop"),
        ],
        mode="Screenshot [A]ctive [S]ection [F]ull"
    ),
    # }}}}
    # ----------------------------- Record Desktop ------------------------ {{{{
    KeyChord([mod, "shift"], "d", [
            # record
            Key([], "a", lazy.spawn("record_active_window"), desc="Record active window"),
            Key([], "f", lazy.spawn("record_full_desktop"),  desc="Record full desktop"),

            # pause/resume
            Key([], "p", lazy.spawn("killalll recordmydesktop --signal SIGUSR1"), desc="Pause recording"),
            Key([], "r", lazy.spawn("killalll recordmydesktop --signal SIGUSR1"), desc="Resume recording"),

            # stop/abort
            Key([], "c", lazy.spawn("killalll recordmydesktop --signal SIGABRT"), desc="Abort recording"),
            Key([], "s", lazy.spawn("killalll recordmydesktop --signal SIGTERM"), desc="Finish recording"),
        ],
        mode="Record Desktop [A]active [F]ull [P]ause [R]esume [C]ancel [S]top"
    ),
    # }}}}
    # ---------------------------- Volume Management ---------------------- {{{{
    KeyChord([mod, "shift"], "v", [
            Key([], "m",        lazy.spawn("amixer set Master mute"),   desc="Mute volume"),
            Key(["shift"], "m", lazy.spawn("amixer set Master unmute"), desc="Unmute volume"),
            Key([], "l",        lazy.spawn("amixer set Master 5%+"),    desc="Louder 5%"),
            Key(["shift"], "l", lazy.spawn("amixer set Master 1%+"),    desc="Louder 1%"),
            Key([], "s",        lazy.spawn("amixer set Master 5%-"),    desc="Softer 5%"),
            Key(["shift"], "s", lazy.spawn("amixer set Master 1%-"),    desc="Softer 1%"),
            Key([], "1",        lazy.spawn("amixer set Master 10%"),    desc="Volume 10%"),
            Key([], "2",        lazy.spawn("amixer set Master 20%"),    desc="Volume 20%"),
            Key([], "3",        lazy.spawn("amixer set Master 30%"),    desc="Volume 30%"),
            Key([], "4",        lazy.spawn("amixer set Master 40%"),    desc="Volume 40%"),
            Key([], "5",        lazy.spawn("amixer set Master 50%"),    desc="Volume 50%"),
            Key([], "6",        lazy.spawn("amixer set Master 60%"),    desc="Volume 60%"),
            Key([], "7",        lazy.spawn("amixer set Master 70%"),    desc="Volume 70%"),
            Key([], "8",        lazy.spawn("amixer set Master 80%"),    desc="Volume 80%"),
            Key([], "9",        lazy.spawn("amixer set Master 90%"),    desc="Volume 90%"),
            Key([], "0",        lazy.spawn("amixer set Master 100%"),   desc="Volume 100%"),
        ],
        mode="Volume [M]ute [L]ouder [S]ofter [1234567890]"
    ),

    Key([],        "XF86AudioRaiseVolume", lazy.spawn("amixer set Master 5%+"),    desc="Louder 5%"),
    Key([],        "XF86AudioLowerVolume", lazy.spawn("amixer set Master 5%-"),    desc="Softer 5%"),
    Key(["shift"], "XF86AudioRaiseVolume", lazy.spawn("amixer set Master 1%+"),    desc="Louder 1%"),
    Key(["shift"], "XF86AudioLowerVolume", lazy.spawn("amixer set Master 1%-"),    desc="Softer 1%"),
    Key([],        "XF86AudioMute",        lazy.spawn("amixer set Master toggle"), desc="Toggle mute"),
    # }}}}
    # ---------------------------- Launch Programmes ---------------------- {{{{
    Key([mod], "d",             lazy.spawn("rofi -combi-modi drun,run -show combi"), desc="Launch a programme"),
    Key([mod], "t",             lazy.spawn("rofi -show window"),                     desc="Jump to a window"),
    Key([mod,  "control"], "f", lazy.spawn("alacritty -e ranger"),                   desc="Open ranger"),
    Key([mod], "m",             lazy.spawn("unclutter -grab -idle 1 -root &"),       desc="Hide the mouse"),
    Key([mod, "shift"], "m",    lazy.spawn("killall unclutter"),                     desc="Show the mouse"),
    Key([mod], "Return",        lazy.spawn(terminal),                                desc="Launch a terminal"),
    Key([mod, "shift"], "x",    lazy.spawn(config_dir + "/lock_qtile"),              desc="Lock the screen"),
    # }}}}
    # ----------------------------- Keyboard Layout ----------------------- {{{{
    KeyChord([mod], "q", [
            Key([], "l", lazy.spawn("fcitx-remote -s fcitx-keyboard-us-intl"), desc="Switch to Latin keybord layout"),
            Key([], "c", lazy.spawn("fcitx-remote -s pinyin"),                 desc="Switch to Chinese keybord layout"),
            Key([], "r", lazy.spawn("fcitx-remote -s fcitx-keyboard-ru"),      desc="Switch to Russian keybord layout"),
            Key([], "u", lazy.spawn("fcitx-remote -s fcitx-keyboard-us"),      desc="Switch to English keybord layout"),
            Key([], "g", lazy.spawn("fcitx-remote -s fcitx-keyboard-gr"),      desc="Switch to Greek keybord layout"),
            Key([], "k", lazy.spawn("fcitx-remote -s hangul"),                 desc="Switch to Korean keybord layout"),
        ],
        mode="Keyboard Layout [U]s [L]atin [C]hinese [R]ussian [G]reek [K]orean"
    ),
    # }}}}
    # -------------------------------- Backlight -------------------------- {{{{
    KeyChord([mod, "shift"], "b", [
            Key([], "d", lazy.spawn("backlight dec 3"),   desc="Dim backlight"),
            Key([], "l", lazy.spawn("backlight inc 3"),   desc="Increase backlight"),
            Key([], "1", lazy.spawn("backlight set 1"),   desc="Backlight 1%"),
            Key([], "2", lazy.spawn("backlight set 20"),  desc="Backlight 10%"),
            Key([], "3", lazy.spawn("backlight set 30"),  desc="Backlight 20%"),
            Key([], "4", lazy.spawn("backlight set 40"),  desc="Backlight 30%"),
            Key([], "5", lazy.spawn("backlight set 50"),  desc="Backlight 40%"),
            Key([], "6", lazy.spawn("backlight set 60"),  desc="Backlight 60%"),
            Key([], "7", lazy.spawn("backlight set 70"),  desc="Backlight 70%"),
            Key([], "8", lazy.spawn("backlight set 80"),  desc="Backlight 80%"),
            Key([], "9", lazy.spawn("backlight set 90"),  desc="Backlight 90%"),
            Key([], "0", lazy.spawn("backlight set 100"), desc="Backlight 100%"),

	        Key([], "XF86AudioRaiseVolume", lazy.spawn("backlight inc 10"), desc="Backlight increase 10%"),
	        Key([], "XF86AudioLowerVolume", lazy.spawn("backlight dec 10"), desc="Backlight dim 10%"),
        ],
        mode="Backlight [D]arker [L]ighter [1234567890]"
    ),
    # }}}}
    # -------------------------- Multi Monitor Layout --------------------- {{{{
    KeyChord([mod, "shift"], "s", [
            Key([], "m", lazy.spawn("mirrorscreen"),     desc="Mirror monitors"),
            Key([], "l", lazy.spawn("dualscreen_left"),  desc="External monitor on left"),
            Key([], "r", lazy.spawn("dualscreen_right"), desc="External monitor on right"),
            Key([], "s", lazy.spawn("singlescreen"),     desc="Only built-in monitor"),
            Key([], "o", lazy.spawn("otherscreen"),      desc="Only external monitor"),
        ],
        mode="Multi Monitor [M]irror [L]eft [R]ight [S]ingle [O]ther"
    ),
    # }}}}
    # --------------------------------- Layout ---------------------------- {{{{
    Key([mod], "Tab",   lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "s",     lazy.layout.next(), lazy.layout.shuffle_right(), desc="Move window focus to other window"),
    # }}}}
    # ----------------------------- Qtile Commands ------------------------ {{{{
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    # }}}}
]
# }}}
# =========================== Auto Start Applications ====================== {{{
@hook.subscribe.startup_once
def autostart():
    autostart_script = os.path.expanduser(config_dir + "/autostart.sh")
    subprocess.run([autostart_script])

@hook.subscribe.startup
def autostart_always():
    autostart_script = os.path.expanduser(config_dir + "/autostart_always.sh")
    subprocess.run([autostart_script])
# }}}
# ==================================== Theme =============================== {{{
# ----------------------------------- Colors ------------------------------ {{{{
bg_color             = "#32302f"
bg_color_transparent = "#ef2f343f"
inactive_bg_color    = "#32302f"
text_color           = "#ebdbb2"
inactive_text_color  = "#929378"
urgent_bg_color      = "#cc241d"

black                = "#282828"
red                  = "#cc241d"
green                = "#98971a"
yellow               = "#d79921"
blue                 = "#458588"
magenta              = "#b16286"
cyan                 = "#689d6a"
white                = "#a89984"
# }}}}

theme = {
    # Columns
    "border_focus":        green,
    "border_focus_stack":  blue,
    "border_normal":       bg_color,
    "border_normal_stack": bg_color,
    "margin":              margin,
    "border_width":        border_width,
    "grow_amount":         3*border_width,
    "margin_on_single":    0,

    # TreeTab
    "active_bg":        green,
    "active_fg":        text_color,
    "bg_color":         bg_color,
    "inactive_bg":      bg_color,
    "urgent_fg":        red,
    "urgent_bg":        bg_color,
    "panel_width":      150,
    "level_shift":      20,
    "font":             "Source Code Pro Bold",
    "section_fg":       text_color,
    "section_fontsize": 14,
    "section_fg":       white,
    "fontsize":         11,

}
# }}}
# =================================== Layouts ============================== {{{
# Default layouts
layouts = [
    layout.Columns(**theme),
    layout.Max(),
]

web_tree_layout = layout.TreeTab(sections=["General", "Code"], **theme)
chats_layout    = layout.Tile(**theme)
# }}}
# ================================= Workspaces ============================= {{{
# ---------------------------------- Defaults ----------------------------- {{{{
chat_matches = [
    Match(wm_class=["TelegramDesktop"]),
    Match(wm_class=["Signal"]),
    Match(wm_class=["Slack"]),
]

media_matches = [
    Match(title=["Spotify"]) # TODO this should probably be done through a hook
]
# }}}}
web_group = Group("", layouts=[web_tree_layout])
groups = [
    Group(""),
    Group(""),
    web_group,
    Group("", layouts=[chats_layout, layout.Max()], matches=chat_matches),
    Group(""),
    Group("", matches=media_matches),
]

for i in range(len(groups)):
    key = str(i + 1)
    keys.extend([
        Key([mod],            key, lazy.group[groups[i].name].toscreen(),                  desc="Switch to group {}".format(groups[i].name)),
        Key([mod, "shift"],   key, lazy.window.togroup(groups[i].name),                    desc="Switch to & move focused window to group {}".format(groups[i].name)),
        Key([mod, "control"], key, lazy.window.togroup(groups[i].name, switch_group=True), desc="Switch to & move focused window to group {}".format(groups[i].name)),
    ])
# }}}
# =================================== Widgets ============================== {{{
widget_defaults = dict(
    font='Source Code Pro bold',
    fontsize=12,
    padding=5,
    foreground=text_color
)
extension_defaults = widget_defaults.copy()

groupbox_settings = {
    "active": text_color,
    "rounded": False,
    "inactive": inactive_text_color,
    "disable_drag": True,
    "hide_unused": False,
    "border_width": 0,
    # "block_highlight_text_color": green,
    "urgent_alert_method": 'block',
    "urgent_text": green,
    "urgent_border": red,
    # "background": yellow,
    "highlight_color": green,
    "highlight_method": "line",
    "margin_x": 0,
    "padding_x": 10,

    # inactive monitor active workspace shown on active monitor
    "other_screen_border": green,

    # active monitor active workspace shown on active monitor
    "this_current_screen_border": green,

    # active monitor active workspace shown on inactive monitor
    "other_current_screen_border": bg_color,

    # Inactive monitor active workspace shown on inactive monitor
    "this_screen_border": green,
}

spacer       = widget.Spacer()
chord        = widget.Chord(background=red)
updates      = widget.CheckUpdates(custom_command="/sbin/checkupdates",     update_interval=60 * 30, foreground=yellow, colour_have_updates=text_color, display_format="Updates: {updates}")
updates_aur  = widget.CheckUpdates(custom_command="/sbin/checkupdates-aur", update_interval=60 * 30, foreground=yellow, colour_have_updates=yellow,     display_format="AUR: {updates}")
memory_graph = widget.MemoryGraph( border_color=bg_color, graph_color=yellow, fill_color=yellow)
cpu_graph    = widget.CPUGraph(border_color=bg_color, graph_color=blue,   fill_color=blue)
net_graph    = widget.NetGraph(border_color=bg_color, graph_color=green,   fill_color=green)
clock        = widget.Clock(format='%Y-%m-%d %a %I:%M %p')
battery      = widget.Battery(format="{percent:2.0%} {char}", charge_char="", discharge_char="", low_foreground=red, foreground=green)
prompt       = widget.Prompt(cursor=False, background=yellow, foreground=bg_color, prompt='{prompt} ')
text_boxes   = [widget.TextBox() for i in range(2)]

bar1 = bar.Bar([ widget.GroupBox(**groupbox_settings), widget.CurrentLayout(), prompt, spacer, chord, text_boxes[0], updates, updates_aur, memory_graph, cpu_graph, net_graph, clock, battery, ], 24, background=bg_color)
bar2 = bar.Bar([ widget.GroupBox(**groupbox_settings), widget.CurrentLayout(), prompt, spacer, chord, text_boxes[1], updates, updates_aur, memory_graph, cpu_graph, net_graph, clock, battery, ], 24, background=bg_color)

screens = [ Screen(bottom=bar1), Screen(bottom=bar2), ]
# }}}
# ================================ Notifications =========================== {{{
class Urgency(Enum):
    INFO  = 0
    ERROR = 1

class Notification:
    def __init__(self, msg: str, urgency: Urgency, timeout: int):
        self.msg     = msg
        self.timeout = timeout
        self.urgency = urgency

notifications = deque()
notifications_running = False

def update_notifications():
    global notifications_running
    if len(notifications) != 0:
        notification = notifications.popleft()
        for text_box in text_boxes:
            text_box.cmd_update(notification.msg)

            # TODO the background colours don't display on all bars
            if notification.urgency == Urgency.INFO:
                text_box.background = yellow
                text_box.foreground = bg_color
            elif notification.urgency == Urgency.ERROR:
                text_box.background = red
                text_box.foreground = text_color

            text_box.timeout_add(notification.timeout, update_notifications)
    else:
        for text_box in text_boxes:
            text_box.cmd_update("")
        notifications_running = False

def notify(msg: str, urgency: Urgency=Urgency.INFO, timeout = 2):
    global notifications_running
    notification = Notification(msg, urgency, timeout)
    notifications.append(notification)
    if not notifications_running:
        notifications_running = True
        update_notifications()

# }}}
# =============================== Custom Commands ========================== {{{
class Callback(NamedTuple):
    callback: Any
    doc: str

def find_web_layout():
    global QTILE_INSTANCE
    for group in QTILE_INSTANCE.groups:
        if group.name == web_group.name:
            return group.layout

def add_web_section(args: list[str]):
    layout = find_web_layout()
    for arg in args:
        layout.cmd_add_section(arg)

def remove_web_section(args: list[str]):
    layout = find_web_layout()
    for arg in args:
        layout.cmd_del_section(arg)


command_map = {
    "add": Callback(add_web_section, "add sections to web layout"),
    "del": Callback(remove_web_section,"remove sections from web layout"),
}

def print_doc_string(args: list[str]):
    if len(args) == 0:
        notify("Expected command name", Urgency.ERROR)
    for arg in args:
        command = command_map.get(arg)
        if command is not None:
            notify(command.doc, Urgency.INFO)
        else:
            notify("Unknown command '" + arg + "'", Urgency.ERROR)

command_map["help"] = Callback(print_doc_string, "prints documentation of a command")

def run_command(cmd_line: str):
    cmd_split = cmd_line.split()
    cmd = cmd_split[0]
    args = cmd_split[1:]

    callback = command_map.get(cmd)
    if callback is not None:
        callback.callback(args)
    else:
        notify("Unknown command '" + cmd + "'", Urgency.ERROR)

class CustomCommandCompleter:
    def __init__(self, qtile):
        self.thisfinal: Optional[str] = None
        self.lookup: Optional[List[Tuple[str, str]]] = None
        self.offset = -1

    def actual(self) -> Optional[str]:
        return self.thisfinal

    def reset(self) -> None:
        self.lookup = None
        self.offset = -1

    def complete(self, txt: str) -> str:
        txt = txt.lower()
        if not self.lookup:
            self.lookup = []
            for cmd in command_map.keys():
                if cmd.lower().startswith(txt):
                    self.lookup.append((cmd, cmd))

            self.lookup.sort()
            self.offset = -1
            self.lookup.append((txt, txt))

        self.offset += 1
        if self.offset >= len(self.lookup):
            self.offset = 0
        ret = self.lookup[self.offset]
        self.thisfinal = ret[1]
        return ret[0]

prompt.completers["custom_command_completer"] = CustomCommandCompleter

@lazy.function
def run_custom_command(qtile: Qtile):
    global QTILE_INSTANCE
    QTILE_INSTANCE = qtile
    prompt.start_input(">", run_command, "custom_command_completer")

keys.extend([
    Key([mod, "shift"], "i", run_custom_command, desc="Runs custom commands with prompted input")
])
# }}}
# ============================== Floating Windows ========================== {{{
mouse = [
    Drag([mod],  "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod],  "Button3", lazy.window.set_size_floating(),     start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

floating_layout = layout.Floating(float_rules=[
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'), # gitk
    Match(wm_class='makebranch'),   # gitk
    Match(wm_class='maketag'),      # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),    # gitk
    Match(title='pinentry'),        # GPG key password entry
])
# }}}
