
# Nayuta no Kiseki / Nayuta: Endless Trails English Translation Edit

<!-- TOC -->
- [Introduction](#introduction)
- [Patching Instructions](#patching-instructions)
- [Known Issues](#known-issues)
- [How do I use the files in this repo?](#how-do-i-use-the-files-in-this-repo)
- [Credits](#credits)
<!-- /TOC -->

<img src="https://i.imgur.com/1gWUK3w.jpg" width="360" height="204"> <img src="https://i.imgur.com/TT9smIn.jpg" width="360" height="204">


[More comparison screenshots](https://imgur.com/a/yJB1fTj). These are mostly one-liners that were particularly non-sensical. There shouldn't be any major spoilers if you're interested in avoiding them.

---
## Introduction

I wasn't happy with the English in the [existing Nayuta no Kiseki fantranslation](https://heroesoflegend.org/forums/viewtopic.php?f=22&t=73), so I used their [publicly available tools](https://heroesoflegend.org/forums/viewtopic.php?f=22&t=340) to make my own edit.


Initially I only wanted to only fix various inconsistencies, nonsensical lines, and the awkward direct-from-Japanese punctuation and formatting. Since I can read zero Japanese, I started out by using Google Translate and Linguee for help on trying to gauge what the more confusing parts were even trying to say, and editing the rest of the English myself.

But in addition to some parts simply not making any sense, I later noticed others had made some modicum of sense, but the online translators (especially after discovering DeepL, which lets you fiddle with alternative translations to reword sentences) gave results that make much *more* sense than the original. It seems that knowledge of the context is something that the original English writers were missing when writing much of the dialogue. I ended up also editing the rest of the text to whatever *I*, as a native US English speaker, subjectively think might sound better, taking into account the original translation, any new machine translation(s), and what I knew about the context of the scene.

But I'm not a big creative writer, so I think it still might stick closer to literal Japanese compared to most previous official localizations: lines with simple phrases or sounds in Japanese like *eh* or *naruhodo* are replaced with simple phrases or sounds in English, rather something potentially more expressive, meaningful, or entertaining. However, now I believe the English to be actually comprehensible. For instance, *yappari* is no longer almost always 'as expected,' even when one of the [many alternatives](https://en.wiktionary.org/wiki/やはり) or similar English phrases make more sense. But again, I don't even know Japanese, so maybe I just made everything worse, especially for anything more nuanced.

I would appreciate reporting of any issues: technical bugs, glaring mistranslations, lore inconsistencies, or even just general English weirdness and typos. I did a playthrough or two with my changes and fixed a number of mistakes, but it is possible that I missed some. There are a few remaining [issues](#known-issues). 

Go to the [release page](https://github.com/dackst/nayuta/releases) for a changelog. If you're interested in more detail on the changes made from the original project, you can look at the [script notes](./notes.md) file. If you're *really* interested, you can easily view almost all the text changes from the original at once [here](https://github.com/dackst/nayuta/compare/a6cecc6651f386ab3fabcab64cf440e021fa99bd...original).


## Patching Instructions
1. Download an xdelta file from latest [release](https://github.com/dackst/nayuta/releases). Choose clean.xdelta to apply the patch to an unmodified Japanese ISO, or choose 4.15.xdelta to apply to an ISO patched with version 4.15 of the previous fan-translation.
2. Apply your respective xdelta patch to your respective iso. If on Windows, the easiest thing to do would probably be to use [xdeltaUI](https://www.romhacking.net/utilities/598/):

    1. Click **Open...** next to **Patch:** and select the xdelta file you downloaded.
    2. Click **Open..** next to **Source File:** and select the corresponding ISO disk image.
    3. Click **...** next to **Output File:** to specify the name and location of the new patched ISO disk image. The new name should end in ".iso" or ".ISO" in order to be recognized by PSP CFWs and emulators. [Here is an example](https://i.imgur.com/6Z65wjP.png) with all the inputs filled in. Your exact names and locations are likely to be different.
    4. Click **Patch** and wait for the new file to be generated. This may take a while and cause the program to appear to stop responding.

   Otherwise, if you have xdelta3 installed elsewhere, you should also be able to run something similar to this with the desired filenames swapped in:
```
xdelta3 -ds original.iso patch.xdelta patched.iso
```


### MD5 Checksums

* Clean Japanese ISO : `02adefbdef8197cca872268d5c01b277`
* ISO patched with flame's 4.15 release: `6cc975153b7998db4242baa17eb8d276`
* ISO patched with this current release (1.06): `3261389b793c4d81a2c42687b9f54ae6`


## Known Issues

These are all issues that exist in the original fantranslation that I don't know how or care enough to try to fix myself.

* boss and new area intro graphics still untranslated ([example](https://i.imgur.com/xizzVel.jpg))
* erasing save data from in-game menu doesn't work
* strange text spacing in some (but not all) longer spell and item descriptions ([example](https://i.imgur.com/Crf076h.jpg))
* long achievement names are cut off in the notification box when unlocking them, e.g. "armor of anhillat"
  * the above two *could* be solved by shortening them, but I'm not willing to butcher them further
* characters that use idiosyncratic manners of speaking in Japanese probably still don't here
  * E.g. Geo is supposed to [sound like an old man](https://legendofheroes.fandom.com/wiki/Lychnis_Gio) (characters even comment on it several times in-game), Eris is supposed to sound [domineering](https://legendofheroes.fandom.com/wiki/Song_Priestess_Elislette) or sarcastic. Algol and Nemeas are definitely supposed to sound unique too
  * Noi has her own verbal tic with the way she ends sentences in Japanese that is lost
  * things like slang or shifts in politeness or tone are probably still not accurately conveyed




## How do I use the files in this repo?

This repository contains modifications of [flame's 2017 tools](https://heroesoflegend.org/forums/viewtopic.php?f=22&t=340) for modifying the text and images in Nayuta no Kiseki, as well as modifications of the English text and images dumped from version 4.15 of original project from 2016.

The original tools require a Windows installation of Python 3 to ["work"](./notes.md#why-not-just-use-flames-tools-directly). With the changes made in this repo, all of the non-working parts of these tools should be fixed. Also, the Python scripts for the dumping and inserting of binary files no longer require a Windows-based version of Python, but the beginning extraction/setup scripts and the final rebuilding scripts still do.

You should have access to a clean Nayuta no Kiseki iso.

1. Download and extract [the original tools](https://heroesoflegend.org/forums/viewtopic.php?f=22&t=340) and paste the [contents of this repository](https://github.com/dackst/nayuta/archive/master.zip) into the extracted folder. Overwrite files if necessary.
2. Set up an environment with a clean Japanese iso (Step 1 in the readme.txt included with the tools):
    1. Drag your iso over `_extract_new.bat`, or run `python extract.py nayuta.iso ISO`, where `nayuta.iso` is the name of your file.
    2. Run `setup.py`
3. Modify files to your liking. See flame's `readme.txt` for more on this.
4. Reinsert text by running using the insertion Python scripts from within each respective folder.
5. Copy the new files to their correct locations. Use `copy_all.py` instead of flame's individual `copy_*.py` scripts.
    * If you made modifications to files that weren't modified before, you *might* have to run the pack editing function in `copy_all.py` on a relevant file for your changes to appear. See the "final boss attack name texture" section of `copy_all.py` for an example.
6. Run `_build.bat` to build the new ISO with your changes, named `output.iso`.

   * You should be able to do steps 4-6 in one go with `build_all.bat` or `build_all.sh`


## Credits

Based on the work of a previous fan translation project:

* Flame - Project leader, main programmer, translator
* SkyeWelse - images
* naachan - translation assistance - helped with boss, character and location names
* Kelebek - programming assistance
* CUE - programming assistance
* zero_g_monkey - programming assistance (images)
* M_bot - image programming

This project:
* Wandering-Heiho - video editing, image editing assistance

Also thanks to anyone who [reported](https://github.com/dackst/nayuta/issues) any specific issues.


