
# Nayuta no Kiseki / Nayuta: Endless Trails English Translation Edit

<!-- TOC -->
- [Introduction](#introduction)
- [Patching Instructions](#patching-instructions)
- [Known Issues](#known-issues)
- [How do I use the files in this repo?](#how-do-i-use-the-files-in-this-repo)
<!-- /TOC -->

<img src="https://i.imgur.com/1gWUK3w.jpg" width="360" height="204"> <img src="https://i.imgur.com/TT9smIn.jpg" width="360" height="204">


[More comparison screenshots](https://imgur.com/a/yJB1fTj). These are mostly one-liners that were particularly non-sensical. There shouldn't be any major spoilers if you're interested in avoiding them.

---
## Introduction

I wasn't happy with the [existing Nayuta no Kiseki English fantranslation](https://heroesoflegend.org/forums/viewtopic.php?f=22&t=73), so I used their [publicly available tools](https://heroesoflegend.org/forums/viewtopic.php?f=22&t=340) to make my own edit.


Initially I only wanted to only fix various inconsistencies, nonsensical lines, and the awkward direct-from-Japanese punctuation and formatting. Since I can read zero Japanese, I started out by using Google Translate and Linguee for help on trying to gauge what the more confusing lines were even trying to say, and editing the rest of the English lines myself.

But in addition to some lines simply not making any sense, I later noticed others had made some modicum of sense, but the online translators (especially after discovering DeepL, which lets you fiddle with alternative translations to reword sentences) gave results that make much *more* sense than the original. It seems that knowledge of the context is something that the original English writers were missing when writing much of the lines. I ended up editing the text to whatever *I*, as a native US English speaker, subjectively think might sound better, taking into account the original translation, any new machine translation(s), and what I knew about the context of the scene.

But I'm not a big creative writer, and again, don't know Japanese, so maybe I just made everything worse. Personally, I think it still might stick closer to literal Japanese compared to most previous official localizations, but now I believe it to be actually comprehensible.

I would appreciate reporting of any issues: technical bugs, glaring mistranslations, lore inconsistencies, or even just general language weirdness and typos. I did a playthrough or two with my changes and fixed a number of mistakes, but it is possible that I missed some. There are a few remaining [issues](#known-issues). 

If you're interested in more detail on the changes I made, you can look at my [script notes](./notes.md) file (definitely spoilers to be found here). If you're *really* interested, you can easily view almost all the text changes from the original at once [here](https://github.com/dackst/nayuta/compare/a6cecc6651f386ab3fabcab64cf440e021fa99bd...original).


## Patching Instructions
1. Download an xdelta file from latest [release](https://github.com/dackst/nayuta/releases). Choose clean.xdelta to apply the patch to an unmodified Japanese ISO, or choose 4.15.xdelta to apply to an ISO patched with version 4.15 of the previous fan-translation.
2. Apply your respective xdelta patch to your respective iso. If on Windows, the easiest thing to do would probably be to use [xdeltaUI](https://www.romhacking.net/utilities/598/).

   Otherwise, if you have xdelta3 installed elsewhere, you should also be able to run something similar to this with the desired filenames swapped in:
```
xdelta3 -ds original.iso patch.xdelta patched.iso
```


### MD5 Checksums
* Clean Japanese ISO : `02adefbdef8197cca872268d5c01b277`
* ISO patched with flame's 4.15 release: `6cc975153b7998db4242baa17eb8d276`
* ISO patched with this current release (1.0.3): `df2a18ce939cee74863bc5b0910b5b72`


## Known Issues

These are all issues that exist in the original fantranslation that I don't know how or care enough to try to fix myself.

* boss and new area intro graphics still untranslated
* erasing save data from in-game menu doesn't work
* there is some strange text spacing in some longer spell and item descriptions
* long achievement names are cut off in the notification box when unlocking them, e.g. "<armor of anhillat"
  * the above two *could* be solved by shortening them, but I'm not willing to butcher them further
* characters that use idiosyncratic manners of speaking in Japanese probably still don't here
  * E.g. Geo is supposed to [sound like an old man](https://legendofheroes.fandom.com/wiki/Lychnis_Gio) (characters even comment on it several times in-game), Eris is supposed to sound [domineering](https://legendofheroes.fandom.com/wiki/Song_Priestess_Elislette) or sarcastic. Algol and Nemeas are definitely supposed to sound unique too
  * Noi has her own verbal tic with the way she ends sentences in Japanese that is lost
  * things like slang or shifts in politeness or tone are probably still not accurately conveyed




## How do I use the files in this repo?

The original tools require Windows and Python 3. They seem to ["work"](./notes.md#why-not-just-use-flames-tools-directly) just as well in Wine if you install a Windows version of Python in a wineprefix. With the changes made in this repo, the Python scripts for the dumping and inserting of binary files should no longer require Windows or Wine, but the beginning extraction step and the final rebuilding step still do.

You should have access to a clean Nayuta no Kiseki iso. Some of my [workarounds](https://github.com/dackst/nayuta/blob/master/notes.md#solutions) also require access to a [version 4.15 patched](https://heroesoflegend.org/forums/viewtopic.php?f=22&t=73) translated iso.

1. Download [flame's 2017 tools](https://heroesoflegend.org/forums/viewtopic.php?f=22&t=340) and set up an environment with a clean Japanese iso (Step 1 in the readme.txt included with the tools):
    1. Drag your iso over `_extract_new.bat`, or run `python extract.py nayuta.iso ISO`, where `nayuta.iso` is the name of your file.
    2. Run `setup.py`
2. Copy the `PSP_GAME/USRDIR/pack` and `PSP_GAME/USRDIR/visual/event` from within the 4.15 patched ISO and replace their equivalents within the `ISO` folder in the environment set up from the previous step. Open the patched 4.15 ISO by mounting it with your OS or file explorer, or with UMDGen, 7-Zip, or anything else that works, really.
3. Copy and overwrite the files in this repository into the environment. Overwrite files if necessary. Modify text or images to your liking. 
4. Reinsert text by running using the insertion Python scripts from within each respective folder. With my changes, the dump scripts must be run at least once beforehand.
5. Copy the new files to their correct locations. I would avoid using flame's `copy_text` script, since it led to part of one of the issues I describe [here](./notes.md#why-not-just-use-flames-tools-directly). You can use `copy_all.py` if you don't want to do it manually.
    * If you made modifications to files that weren't modified before, you might have to run the pack editing part on a relevant file for your changes to appear. See the "final boss attack name texture" part of my `copy_all.py` for an example.
6. Run `_build.bat` to build the new ISO with your changes, named `output.iso`.

   * You should be able to do steps 4-6 in one go with `build_all.bat` or `build_all.sh`





