'''
This check has been put in place to stop the inclusion of TVA (and friends) addons in builds
from build makers that publicly insult or slander TVA's developers and friends. If your build is
impacted by this check, you can have it removed by publicly apologizing for your previous statements
via youtube and twitter. Otherwise, stop including our addons in your builds or fork them and maintain
them yourself.
                                                                                           http://i.imgur.com/TqIEnYB.gif
                                                                                           TVA developers (and friends)
'''

def do_block_check(uninstall=True):
    import hashlib
    import xbmcvfs, xbmc
    f = xbmcvfs.File('special://home/media/splash.png')
    splash_md5 = hashlib.md5(f.read()).hexdigest()
    bad_md5s = ['926dc482183da52644e08658f4bf80e8', '084e2bc2ce2bf099ce273aabe331b02e']
    bad_addons = ['plugin.program.targetin1080pwizard', 'plugin.video.targetin1080pwizard']
    has_bad_addon = any(xbmc.getCondVisibility('System.HasAddon(%s)' % (addon)) for addon in bad_addons)
    if has_bad_addon or splash_md5 in bad_md5s:
        import xbmcgui
        import sys
        line2 = 'Press OK to uninstall this addon' if uninstall else 'Press OK to exit this addon'
        xbmcgui.Dialog().ok('Incompatible System', 'This addon will not work with the build you have installed', line2)
        if uninstall:
            import xbmcaddon
            import shutil
            addon_path = xbmcaddon.Addon().getAddonInfo('path').decode('utf-8')
            shutil.rmtree(addon_path)
        sys.exit()