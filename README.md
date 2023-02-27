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
    # plugs: [home, network, network-bind, removable-media, pulseaudio]
    # plugs: [desktop, x11, audio-playback, desktop-legacy, unity7, network, home, gsettings, opengl]
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


## Missing packages

Whilst snapcraft is building the snap, it will report missing packages.  These can be added to the snapcraft.yaml file.  However you will need to transform from the `.so` file name of a file shipped inside a deb to the proper package name. This can be done with the `apt-file` command.

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

## Pulseaudio

I had lots of problems with pulseaudio.  I had to add the `pulseaudio` interface to the snapcraft.yaml file.  I also had to add the following to the snapcraft.yaml file:

```yaml
environment:
  LD_LIBRARY_PATH: $LD_LIBRARY_PATH:/snap/snap-wx-simple/current/usr/lib/x86_64-linux-gnu/pulseaudio
```

I also added various pulseaudio packages to the stage-packages section of the snapcraft.yaml file.

In debugging, inside the lxd container used by snapcraft (which I entered using `lxc start snapcraft-snap-wx-simple` then `lxc exec snapcraft-snap-wx-simple -- /bin/bash`) I found the pulse library
```
sudo find / -name libpulsecommon-13.99.so
/root/prime/usr/lib/x86_64-linux-gnu/pulseaudio/libpulsecommon-13.99.so
/root/stage/usr/lib/x86_64-linux-gnu/pulseaudio/libpulsecommon-13.99.so
/root/parts/build-the-python-stuff-please/install/usr/lib/x86_64-linux-gnu/pulseaudio/libpulsecommon-13.99.so
```
which helped me to find the correct path to add to the LD_LIBRARY_PATH environment variable.
