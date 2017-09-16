# python-scripts-conf-desktop-icon-files
A place for all my scripts, programs, customizations, inflicted on my gentoo/funtoo hybrid

# urxtheme and icons on display
urxvt is utilizing TheHulk for primary theme and rjorgenson for commandline theme.
You can also see many of the icons on display, from within pcmanfm, dockbarx (top), 
xfce-panel (bot & right), as well as the menu.

![Desktop](custom_iconset/images/desk_music.jpg?raw=true)
![rxvt](custom_iconset/images/urxvt806.jpg?raw=true)
![pcman](custom_iconset/images/pcmanfm908.jpg?raw=true)


# Urxvt theme is using Galaxy for backdrop and sexy for commandline  
![Butterflies](custom_iconset/images/beauty&butterflies.jpg?raw=true)

# Urxvt theme is stinkypinky and fukmeright for commandline
![Budo](custom_iconset/images/bushiboje.jpg?raw=true)


# python_* files | sqlite | seam_carve | base64decode
These three dirs, contain python scripts that automate some tedious or slow building processes.

# bash_ * | conf | forensics
This dir, contains my build environment conf files, as well as my make.conf file. In addition,
it also has my plugins converted to regular scripts, so you can do with them as you chose. 
Labeled either with alias* or sourced*, they mean just that. Either ran under an alias, or when
sourced executes, or creates a callable function. These can easily be incorperated into any plugin (shell)
system you have currently, or just tagged onto the end of your bashrc file (I caution against creating a huge
bashrc or bash_profile, it can noticibly bog a system down, hence why I opted for a plugin system).

Underneath the profile, you will find my env setup, which allows me to specify per package, how
to best utilize either clang/llvm-5.0 or gcc-7.0. compiler optimizations, I use both graphite 
and lto (ld.gold), and this has a tendency to break some packages. 
So, my solution is here, in this area. Be careful if you do decide to use 
any settings, I have a hybrid gentoo/funtoo build, and although techincally complete,
there are a few missing ingredients if you have either a gentoo or funtoo build, and they would likely
render your portage unoperable, or your compilers unable to generate code. Any other distrabution,
I would strongly caution against using any of my settings, as your global environments are vastly
different, namely because they are binary distrabutions. Feel free to message me, and
I can help optimzing your environment and setting up an env per package compiler system like mine.

