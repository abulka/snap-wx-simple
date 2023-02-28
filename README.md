# snap-wx-simple

Building a wxpython app using snapcraft, ensuring that `setup.py` is configured - which the snapcraft Python plugin requires.

Also allows you to use a github actions workflow to build the snap.  Uses the official github actions snapcraft action.

# Notes

## Rectangle text chars at runtime

Turns out the solution is to add the 'desktop' interface to the snapcraft.yaml file.

```yaml
apps:
  snap-wx-simple:
    command: bin/rubber
    plugs: [home, network, network-bind, removable-media, pulseaudio, desktop]
```

| Interface | First line | Second line | Description |
| --- | --- | --- | --- |
| home | Yes | Yes | Allows access to non-hidden files in user's home directory |
| network | Yes | Yes | Allows access to network resources |
| network-bind | Yes | No  | Allows binding to network ports |
| removable-media | Yes  | No  | Allows access to mounted removable storage devices |
| pulseaudio  | Yes  | No  | Allows access to sound server for playback and recording |
| desktop  | No  | Yes  | Allows access to basic graphical desktop resources such as **fonts** and themes <br> 😏<span style="color: green;">the lack of this 'desktop' entry caused rectangle chars at runtime</span> |
| x11  	| No 	| Yes	| Allows communication with X server for graphical display |
| audio-playback	| No	| Yes	| Allows playing audio on pulseaudio or ALSA sound servers |
| desktop-legacy		| No	| Yes	| Allows legacy methods of accessing graphical desktop resources such as GTK2 or Qt4 libraries |
| unity7			| No	| Yes	| Allows integration with Unity7 desktop environment such as indicators, notifications, etc.|
| gsettings			| No   	| Yes   | Allows reading and writing settings from GSettings configuration system|
| opengl			| No   	| Yes   | Allows access to OpenGL hardware acceleration|


## Missing linux libraries

Whilst snapcraft is building the snap, it will report missing libraries.  These can be added to the snapcraft.yaml file.  

All these missing packages are due to the needs of `wxpython`, not Python itself.

Example of original error message from snapcraft:
```yaml
+ snapcraftctl prime
The 'build-the-python-stuff-please' part is missing libraries that are not included in the snap or base. They can be satisfied by adding the following entry for this part
stage-packages:
- libpng16-16
This part is missing libraries that cannot be satisfied with any available stage-packages known to snapcraft:
- libEGL.so.1
- libGL.so.1
- libSDL2-2.0.so.0
- libSM.so.6
- libX11.so.6
- libXtst.so.6
- libXxf86vm.so.1
- libcairo.so.2
- libfontconfig.so.1
- libgdk-3.so.0
- libgdk_pixbuf-2.0.so.0
- libgstreamer-1.0.so.0
- libgstvideo-1.0.so.0
- libgtk-3.so.0
- libjavascriptcoregtk-4.0.so.18
- libjpeg.so.8
- libnotify.so.4
- libpango-1.0.so.0
- libpangocairo-1.0.so.0
- libpangoft2-1.0.so.0
- libpcre2-32.so.0
- libtiff.so.5
- libwayland-client.so.0
- libwayland-egl.so.1
- libwebkit2gtk-4.0.so.37
These dependencies can be satisfied via additional parts or content sharing. Consider validating configured filesets if this dependency was built.
```

### The need to modify the library names

However you will need to transform from the `.so` file name of a file shipped inside a deb to the proper package name. This can be done with the `apt-file` command.

If the name is rejected by snapcraft 
https://forum.snapcraft.io/t/package-not-found/26634 
this is not a package name but a file name of a file shipped inside a deb …
you can use apt-file to search for deb package names the file belongs to:
```
$ sudo apt install apt-file
$ sudo apt-file update
$ apt-file search libX11.so.6
libx11-6: /usr/lib/x86_64-linux-gnu/libX11.so.6
libx11-6: /usr/lib/x86_64-linux-gnu/libX11.so.6.3.0
```
before the colon you find the package name to use with your stage-packages, in the above example `libx11-6`.

You must do this for each file listed in the error message.

There may be additional packages that need to be added to the snapcraft.yaml file. Good luck guessing which ones - they may be reported on the terminal when you run the snap from the command line.



## Pulseaudio

I had lots of problems with the path to pulseaudio.  I had to add the `pulseaudio` or `audio-playback` interface to the snapcraft.yaml file.  I also had to add the following to the snapcraft.yaml file:

```yaml
environment:
  LD_LIBRARY_PATH: $LD_LIBRARY_PATH:/snap/snap-wx-simple/current/usr/lib/x86_64-linux-gnu/pulseaudio
```

I also added `libpulse0` to the stage-packages section of the snapcraft.yaml file. 
```
      - libpulse0
      # - libpulse-dev # don't need this
      # - pulseaudio # don't need this
```

### Debugging the pulse audio path

In debugging, inside the lxd container used by snapcraft (which I entered using `lxc start snapcraft-snap-wx-simple` then `lxc exec snapcraft-snap-wx-simple -- /bin/bash`) I found the pulse library
```
sudo find / -name libpulsecommon-13.99.so
/root/prime/usr/lib/x86_64-linux-gnu/pulseaudio/libpulsecommon-13.99.so
/root/stage/usr/lib/x86_64-linux-gnu/pulseaudio/libpulsecommon-13.99.so
/root/parts/build-the-python-stuff-please/install/usr/lib/x86_64-linux-gnu/pulseaudio/libpulsecommon-13.99.so
```
which helped me to find the correct path to add to the LD_LIBRARY_PATH environment variable.

It's not clear to me why the `pulseaudio` interface is not enough to make the pulseaudio library available to the snap.  Inside the snap I see
```
...
squashfs-root/usr/lib/x86_64-linux-gnu/pkgconfig/libsepol.pc
squashfs-root/usr/lib/x86_64-linux-gnu/pkgconfig/libxcrypt.pc
squashfs-root/usr/lib/x86_64-linux-gnu/pkgconfig/mount.pc
squashfs-root/usr/lib/x86_64-linux-gnu/pkgconfig/uuid.pc
squashfs-root/usr/lib/x86_64-linux-gnu/pkgconfig/zlib.pc
squashfs-root/usr/lib/x86_64-linux-gnu/primus
squashfs-root/usr/lib/x86_64-linux-gnu/primus/libGL.so.1
squashfs-root/usr/lib/x86_64-linux-gnu/pulseaudio
squashfs-root/usr/lib/x86_64-linux-gnu/pulseaudio/libpulsecommon-13.99.so
squashfs-root/usr/lib/x86_64-linux-gnu/pulseaudio/libpulsecore-13.99.so
squashfs-root/usr/lib/x86_64-linux-gnu/pulseaudio/libpulsedsp.so
....
```
which shows that lots of other packages have subdirectories in the `usr/lib/x86_64-linux-gnu` directory, as well as pulseaudio. 
Do subdirectories of `usr/lib/x86_64-linux-gnu` get searched as well?

### More musings on pulseaudio

A gptchat session

I just read that `$SNAP/lib:$SNAP/usr/lib:$SNAP/usr/lib/x86_64-linux-gnu` (on amd64 architecture) are default part of the `LD_LIBRARY_PATH`

> Yes, that is correct. When a snap is run on an amd64 architecture, the directories $SNAP/lib, $SNAP/usr/lib, and $SNAP/usr/lib/x86_64-linux-gnu are automatically added to the LD_LIBRARY_PATH environment variable by default. This means that any shared libraries located in those directories should be found by the system at runtime without the need to manually set the LD_LIBRARY_PATH environment variable in your snapcraft.yaml file.

> However, it's worth noting that this may not always be the case depending on the specific libraries and dependencies your snap requires. If you encounter any issues related to shared library loading at runtime, you may need to investigate further and adjust the LD_LIBRARY_PATH environment variable as necessary.


abulka@gmail.com
thus I shouldn't need `LD_LIBRARY_PATH: $LD_LIBRARY_PATH:$SNAP/usr/lib/x86_64-linux-gnu`

> That's correct. If the shared libraries you need to use in your snap are located in the $SNAP/usr/lib/x86_64-linux-gnu directory, and you are running the snap on an amd64 architecture, then you shouldn't need to explicitly set the LD_LIBRARY_PATH environment variable to include that directory.

> By default, $SNAP/usr/lib/x86_64-linux-gnu should already be included in the LD_LIBRARY_PATH environment variable for your snap, as mentioned in my previous answer.

abulka@gmail.com
thus I shouldnt need `LD_LIBRARY_PATH: $LD_LIBRARY_PATH:/snap/snap-wx-simple/current/usr/lib/x86_64-linux-gnu/pulseaudio` since subdirectories of x86_64-linux-gnu are also searched

> That's correct. If the shared library you need to use is located in a subdirectory of $SNAP/usr/lib/x86_64-linux-gnu, then it should already be searched by default and you shouldn't need to explicitly add it to the LD_LIBRARY_PATH environment variable in your snapcraft.yaml file.

> Therefore, if the shared library you need is located at /snap/snap-wx-simple/current/usr/lib/x86_64-linux-gnu/pulseaudio/libpulsecommon-13.99.so, you should not need to include LD_LIBRARY_PATH: $LD_LIBRARY_PATH:/snap/snap-wx-simple/current/usr/lib/x86_64-linux-gnu/pulseaudio in your snapcraft.yaml file.

yet I seem to need that path to avoid the pulseaudio library not found error.

```
Traceback (most recent call last):
  File "/snap/snap-wx-simple/x10/bin/rubber", line 11, in <module>
    load_entry_point('snap-wx-simple==1.0.0', 'console_scripts', 'rubber')()
  File "/snap/snap-wx-simple/x10/lib/python3.8/site-packages/pkg_resources/__init__.py", line 489, in load_entry_point
    return get_distribution(dist).load_entry_point(group, name)
  File "/snap/snap-wx-simple/x10/lib/python3.8/site-packages/pkg_resources/__init__.py", line 2852, in load_entry_point
    return ep.load()
  File "/snap/snap-wx-simple/x10/lib/python3.8/site-packages/pkg_resources/__init__.py", line 2443, in load
    return self.resolve()
  File "/snap/snap-wx-simple/x10/lib/python3.8/site-packages/pkg_resources/__init__.py", line 2449, in resolve
    module = __import__(self.module_name, fromlist=['__name__'], level=0)
  File "/snap/snap-wx-simple/x10/lib/python3.8/site-packages/rubber_band_async.py", line 3, in <module>
    import wx
  File "/snap/snap-wx-simple/x10/lib/python3.8/site-packages/wx/__init__.py", line 17, in <module>
    from wx.core import *
  File "/snap/snap-wx-simple/x10/lib/python3.8/site-packages/wx/core.py", line 12, in <module>
    from ._core import *
ImportError: libpulsecommon-13.99.so: cannot open shared object file: No such file or directory
```

I checked the path inside the snap

```
$ snap run --shell snap-wx-simple
bash: warning: setlocale: LC_ALL: cannot change locale (en_US.UTF-8)
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

andy@ubuntu-2204:/home/andy/Devel/snap-wx-simple$ echo $LD_LIBRARY_PATH
/var/lib/snapd/lib/gl:/var/lib/snapd/lib/gl32:/var/lib/snapd/void::/snap/snap-wx-simple/current/usr/lib/x86_64-linux-gnu:/snap/snap-wx-simple/x10/lib:/snap/snap-wx-simple/x10/usr/lib:/snap/snap-wx-simple/x10/lib/x86_64-linux-gnu:/snap/snap-wx-simple/x10/usr/lib/x86_64-linux-gnu
```

interestingly `ls /snap/snap-wx-simple/current/usr/lib/x86_64-linux-gnu/pulseaudio/libpulsecommon-13.99.so` confirms the file is there OK.

then I found a Bing summary 🎉

> However, you should be aware that the pulseaudio interface is deprecated as of snapd 2.41 and the audio-playback and audio-record interfaces should be used instead. If you want to connect your snap to PulseAudio, you need to add $ `{SNAP}/usr/lib/$SNAPCRAFT_ARCH_TRIPLET/pulseaudio` to `LD_LIBRARY_PATH`.
