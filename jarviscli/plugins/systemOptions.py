import os
from platform import architecture, release, mac_ver
from platform import system as sys
import distro
from colorama import Fore, Style
from plugin import LINUX, UNIX, MACOS, WINDOWS, plugin, require


@require(platform=MACOS, native="pmset")
@plugin('screen off')
def screen_off__MAC(jarvis, s):
    """Turn of screen instantly"""
    os.system('pmset displaysleepnow')


@require(platform=LINUX, native="xset")
@plugin('screen off')
def screen_off__LINUX(jarvis, s):
    """Turn of screen instantly"""
    os.system('xset dpms force off')


@require(platform=MACOS)
@plugin('os')
def Os__MAC(jarvis, s):
    """Displays information about your operating system"""
    jarvis.say(
        Style.BRIGHT
        + '[!] Operating System Information'
        + Style.RESET_ALL,
        Fore.BLUE)
    jarvis.say('[*] Kernel: ' + sys(), Fore.GREEN)
    jarvis.say('[*] Kernel Release Version: ' + release(), Fore.GREEN)
    jarvis.say('[*] macOS System version: ' + mac_ver()[0], Fore.GREEN)
    for _ in architecture():
        if _ != '':
            jarvis.say('[*] ' + _, Fore.GREEN)


@require(platform=[LINUX, WINDOWS])
@plugin('os')
def Os__LINUX(jarvis, s):
    """Displays information about your operating system"""
    jarvis.say('[!] Operating System Information', Fore.BLUE)
    jarvis.say('[*] ' + sys(), Fore.GREEN)
    jarvis.say('[*] ' + release(), Fore.GREEN)
    jarvis.say('[*] ' + distro.name(), Fore.GREEN)
    for _ in architecture():
        jarvis.say('[*] ' + _, Fore.GREEN)


@require(platform=LINUX)
@plugin('systeminfo')
def systeminfo__LINUX(jarvis, s):
    """Display system information with distribution logo"""
    from archey import archey
    archey.main()


@require(platform=MACOS, native="screenfetch")
@plugin('systeminfo')
def systeminfo__MAC(jarvis, s):
    """Display system information with distribution logo"""
    os.system("screenfetch")


@require(platform=WINDOWS)
@plugin('systeminfo')
def systeminfo_win(jarvis, s):
    """Display system infomation"""
    os.system("systeminfo")


@require(native="free", platform=UNIX)
@plugin("check ram")
def check_ram__UNIX(jarvis, s):
    """
    checks your system's RAM stats.
    -- Examples:
        check ram
    """
    os.system("free -lm")


@require(platform=WINDOWS)
@plugin("check ram")
def check_ram__WINDOWS(jarvis, s):
    """
    checks your system's RAM stats.
    -- Examples:
        check ram
    """
    import psutil
    mem = psutil.virtual_memory()

    def format(size):
        mb, _ = divmod(size, 1024 * 1024)
        gb, mb = divmod(mb, 1024)
        return "%s GB %s MB" % (gb, mb)
    jarvis.say("Total RAM: %s" % (format(mem.total)), Fore.BLUE)
    if mem.percent > 80:
        color = Fore.RED
    elif mem.percent > 60:
        color = Fore.YELLOW
    else:
        color = Fore.GREEN
    jarvis.say("Available RAM: %s" % (format(mem.available)), color)
    jarvis.say("RAM used: %s%%" % (mem.percent), color)
