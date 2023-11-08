
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import hook
import subprocess
import os

colors = {
    "dark": "#1a1a1a",
    "light": "#c6c6c6",
    "accent": "#a4a4a4",
    "accent2": "#46433a",
    "beige": "#f5f5dc",
    "orange": "#e06c4d"
}

@hook.subscribe.startup_once
def autostart():
    xrandr_start()
    picom_start()
    subprocess.Popen(['xsetroot', '-cursor_name', 'theme-name'])


    
def picom_start():
    home = os.path.expanduser('~')  # Expands the '~' to the full home directory path
    # Picom command
    picom_command = ['picom', '--config', f'{home}/.config/picom/picom.conf']
    subprocess.Popen(picom_command)  # This will start Picom in the background
    
def xrandr_start():
    xrandr_path = '/usr/bin/xrandr'
    cmd = [
        xrandr_path,
        '--output', 'DisplayPort-1', '--primary', '--mode', '1920x1080', '--pos', '0x0', '--rotate', 'normal',
        '--output', 'HDMI-A-1', '--mode', '1920x1080', '--pos', '1920x-600', '--rotate', 'left'
    ]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f'Failed to run command: {e.cmd}')

    
mod = "mod4"

# terminal = guess_terminal()
terminal = "kitty"
keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html


    # Snipping tool functionality
    Key([mod, "shift"], "s", lazy.spawn("sh -c 'maim -s | xclip -selection clipboard -t image/png'")),
    
    # Volume control with pactl (PulseAudio)
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),

    # Switch between windowsd
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    # Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),



    Key([mod], "space", lazy.spawn("rofi -show drun"), desc="Rofi drun show"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="RToggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

]
# Kanji characters for display
kanji_display = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]

# Group definitions with Kanji display names
groups = [Group(i[1], label=i[1]) for i in zip("1234567890", kanji_display)]
for i, group in enumerate(groups):
    actual_key = str(i + 1) if i < 9 else "0"
    keys.extend([
        # Switch to group
        Key([mod], actual_key, lazy.group[group.name].toscreen(),
            desc="Switch to group {}".format(group.name)),
        # Move window to group and switch to it
        Key([mod, "shift"], actual_key, lazy.window.togroup(group.name),
            desc="Move focused window to group {}".format(group.name)),
    ])




borders = dict(
    border_focus=colors["accent2"],  # Active window border color
    border_normal=colors["accent"],     # Inactive window border color
    border_width=3,
)
layouts = [
    layout.Columns(**borders),
    layout.Max(**borders),
    layout.Floating(**borders),

    # Try more layouts by unleashing below layouts.
    layout.Stack(**borders, num_stacks=2),
    layout.Bsp(**borders),
    layout.Matrix(**borders),
    layout.MonadTall(**borders),
    layout.MonadWide(**borders),
    layout.RatioTile(**borders),
    layout.Tile(**borders),
    layout.TreeTab(**borders),
    layout.VerticalTile(**borders),
    layout.Zoomy(**borders),
]

widget_defaults = dict(
    font = "FOT-Rodin Pro DB",
    #font = "UbuntuMonoNerdFontMono",
    fontsize=12,
    padding=8,
)
extension_defaults = widget_defaults.copy()


screens = [
    Screen(
        top=bar.Bar(
            [
                # widget.CurrentLayout(foreground=colors["dark"]),
                widget.GroupBox(active=colors["orange"],
                                borderwidth = 3,
                                highlight_color = colors["beige"],
                                highlight_method="line",
                                other_screen_border=colors["accent2"],
                                other_current_screen_border=colors["accent2"],
                                this_screen_border=colors["orange"],
                                this_current_screen_border=colors["orange"],

                                ),
                                
                widget.Spacer(),
                widget.Systray(),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p', foreground=colors["dark"]),
            ],
            24,  # This is the height of the top bar. Adjust as needed.
            background=colors["beige"],  # Beige background color
            opacity=0.9
        ),
        wallpaper='/home/bocchi/.config/qtile/pictures/2BL.png',
        wallpaper_mode='fill'
    ),
    Screen(
        top=bar.Bar(
            [
                # widget.CurrentLayout(foreground=colors["dark"]),
                widget.GroupBox(active=colors["orange"],
                                borderwidth = 3,
                                highlight_color = colors["beige"],
                                highlight_method="line",
                                other_screen_border=colors["accent2"],
                                other_current_screen_border=colors["accent2"],
                                this_screen_border=colors["orange"],
                                this_current_screen_border=colors["orange"],

                                ),
                                
                widget.Spacer(),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p', foreground=colors["dark"]),
            ],
            24,  # This is the width of the vertical bar. Adjust as needed.
            background=colors["beige"],  # Beige background color
            opacity=0.9,
            vertical=True
        ),
        wallpaper='/home/bocchi/.config/qtile/pictures/2BP.png',
        wallpaper_mode='fill'
    )
]


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None


wmname = "NAVI"


