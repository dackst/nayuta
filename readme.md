
# Nayuta no Kiseki English Translation Edit

<!-- TOC -->
- [Introduction](#introduction)
- [Patching Instructions](#patching-instructions)
- [Known Issues](#known-issues)
- [How do I use the files in this repo?](#how-do-i-use-the-files-in-this-repo)
<!-- /TOC -->


![before](https://i.imgur.com/1gWUK3w.jpg)
![after](https://i.imgur.com/TT9smIn.jpg)

[More comparison screenshots](https://imgur.com/a/yJB1fTj). These are mostly one-liners that were particularly non-sensical. There shouldn't be any major spoilers if you're interested in avoiding them.

---
## Introduction

I wasn't happy with the [existing Nayuta no Kiseki English fantranslation](https://heroesoflegend.org/forums/viewtopic.php?f=22&t=73), so I used their [publicly available tools](https://heroesoflegend.org/forums/viewtopic.php?f=22&t=340) to make my own edit.


Initially I only wanted to only fix various inconsistencies, nonsensical lines, and the awkward direct-from-Japanese punctuation and formatting. Since I can read zero Japanese, I started out by using Google Translate and Linguee for help on rewriting the more confusing lines, and editing the rest myself.

In addition to some lines simply not making any sense, I noticed others had made some modicum of sense, but the online translators (especially after discovering DeepL, which lets you pick out alternative translations) gave results that make much *more* sense than the original. It seems that knowledge of the context is something that the original English writers were missing for much of the lines. As I went on, I ended up retranslating (and subsequently editing) pretty much the whole script to what *I* think sounds more natural to a native US English speaker. Lines are edited from the original to various degrees: some parts may be kept, other parts are entirely rewritten.

But I'm not a big creative writer, and again, don't know Japanese, so maybe I just made everything worse. At least I ran my English script through a spelling and grammar checker to catch obvious typos and errors, unlike the original. Personally, I think it still might stick slightly closer to the literal Japanese compared to most previous official localizations of Falcom games, but now I believe it to be actually comprehensible. 

I would appreciate reporting of any issues or general language weirdness. I played through a new game plus with my script and fixed a number of less-obvious mistakes, but it is possible that I missed some. There are a few [issues](#Known-Issues) I've found that I don't know how to fix.

If you're interested in more detail on the changes I made, you can look at my [script notes](./notes.md) file (definitely spoilers to be found here), or look directly at the file history in this repository. You can easily view almost all the changes at once [here](https://github.com/dackst/nayuta/commit/2e5b5c5db7d33fb19f7d38e6ba8c0a8826a07419).

<!-- or you can [compare]((https://github.com/dackst/nayuta/compare/original...master)) any of the changed files directly to their originals in this repo. 
broken ever since I moved files around
-->

## Patching Instructions
1. Download an xdelta file from latest [release](https://github.com/dackst/nayuta/releases). Choose clean.xdelta to apply the patch to an unmodified Japanese ISO, or choose 4_15.xdelta to apply to an ISO patched with version 4.15 of the previous fan-translation.
2. Apply your respective xdelta patch to your respective iso. If on Windows, the easiest thing to do would probably be to use [xdeltaUI](https://www.romhacking.net/utilities/598/).

   Otherwise, if you have xdelta3 installed elsewhere, you should also be able to run something similar to this with the desired filenames swapped in:
```
xdelta3 -dfs original.iso patch.xdelta3 patched.iso
```


### MD5 Checksums
* Clean Japanese ISO : `02adefbdef8197cca872268d5c01b277`
* ISO patched with flame's 4.15 release: `6cc975153b7998db4242baa17eb8d276`
* ISO patched with this current release: `3d17f08af098667722f348cf6c47b3b0`


## Known Issues

### Issues in this version 
These issues don't seem to exist in the original 4.15 fan translation release. I think they may be due to problems with the released tools? See [here](./notes.md/#Why-not-just-use-flame's-tools-directly) for more info.
* unable to speak to Mishy before chapter 5
  * The new game+ sidequest involving Mishy starts partway into chapter 5, so it is unaffected. However, the special Mishy achievement requires talking to him at every opportunity, so that achievement is unable to be completed.
    * If you really want to have a go at that achievement, you can save whenever you find Mishy, and reload with a clean/4.15 patched ISO to talk to him.
* there are some extra stray lines of text in Japanese when reading the tablet at the end of Volans' sidequest. 

### Issues from original fantranslation that I don't know how/care enough to try to fix myself
* ingredient location text (press △ on the cooking screen) cannot be changed from the original fan translation, which still shows some partially Japanese text
* boss and new area intro graphics still untranslated
* erasing save data from in-game menu doesn't work
* there is some strange text spacing in certain spell descriptions
* long achievement names are cut off in the notification box when unlocking them, e.g. "<armor of anhillat"
  * the achievement notification box is tiny. I'm not willing to butcher the names further in order to make them fit
* characters that use idiosyncratic manners of speaking in Japanese probably still don't here
  * E.g. Geo is supposed to [sound like an old man](https://legendofheroes.fandom.com/wiki/Lychnis_Gio) (characters even comment on it several times in-game), Eris is supposed to sound [domineering](https://legendofheroes.fandom.com/wiki/Song_Priestess_Elislette) or sarcastic. I think Algol is supposed to use archaic speech patterns, and Nemeas is like a schoolteacher or something?




## How do I use the files in this repo?

The original tools require Windows and Python 3. They seem to ["work"](./notes.md#why-not-just-use-flames-tools-directly) just as well in Wine if you install a Windows version of Python in a wineprefix. With the changes made in this repo, the Python scripts for the dumping and inserting of binary files should no longer require Windows or Wine, but the beginning extraction step and the final rebuilding step still do.

1. Download [flame's 2017 tools](https://heroesoflegend.org/forums/viewtopic.php?f=22&t=340) and set up an environment with a clean Japanese iso (Step 1 in the readme.txt included with the tools):
    1. Drag your iso over `_extract_new.bat`
    2. Run `setup.py`
  
   You should also have both a clean Nayuta no Kiseki iso and [version 4.15 patched](https://heroesoflegend.org/forums/viewtopic.php?f=22&t=73) translated iso.

2. Remove the `ISO/USRDIR/pack` and `ISO/USRDIR/visual/event` folders in the environment from the previous step and replace them with their respective folders found from within the 4.15 patched ISO. Open the patched 4.15 ISO by mounting it with your OS or file explorer, or with UMDGen, 7-Zip, or anything else that works, really.
3. Copy and overwrite the files in this repository into the environment. Overwrite files if necessary. Modify text or images to your liking. 
4. Reinsert text by running using the insertion Python scripts from within each respective folder. With my changes, the dump scripts must be run at least once beforehand.
5. Copy the new files to their correct locations. I avoided using flame's scripts, since they modified other files in a way that didn't seem to completely work.
6. Run `_build.bat` build the new ISO with your changes, named `output.iso`.

   * You should be able to do steps 4-6 in one go with `build_all.bat` or `build_all.sh`





