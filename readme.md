
# Nayuta no Kiseki English Translation Edit

![before](https://i.imgur.com/1gWUK3w.jpg)
![after](https://i.imgur.com/TT9smIn.jpg)


I wasn't happy with the [existing Nayuta no Kiseki English fantranslation](https://heroesoflegend.org/forums/viewtopic.php?f=22&t=73), so I used their [publicly available tools](https://heroesoflegend.org/forums/viewtopic.php?f=22&t=340) to make my own edit. You can see more comparison screenshots of one-liners that I thought were particularly non-sensical [here](https://imgur.com/a/yJB1fTj). There shouldn't be any major spoilers if you're interested in avoiding them.

Initially I only wanted to only fix various inconsistencies, nonsensical lines, and the awkward direct-from-Japanese punctuation and formatting. Since I can read zero Japanese, I started out by using Google Translate and Linguee for help on rewriting the more confusing lines, and editing the rest myself.

In addition to some lines simply not making any sense, I noticed others had made some modicum of sense, but the online translators (especially after discovering DeepL, which lets you pick out alternative translations) gave results that make much *more* sense than the original. It seems that knowledge of the context is something that the original English writers were missing for much of the lines. As I went on, I ended up retranslating (and subsequently editing) pretty much the whole script to what *I* think sounds more natural to a native US English speaker. Lines are edited from the original to various degrees: some parts may be kept, other parts are entirely rewritten.

But I'm not a big creative writer, and again, don't know Japanese, so maybe I just made everything worse. At least I ran my English script through a spelling and grammar checker to catch obvious typos and errors, unlike the original. Personally, I think it still might stick slightly closer to the literal Japanese compared to most previous official localizations of Falcom games, but now I believe it to be actually comprehensible. 

I would appreciate reporting of any issues or general language weirdness. I played through a new game plus with my script and fixed a number of less-obvious mistakes, but it is possible that I missed some. There are a few [issues](#Known-Issues) I've found that I don't know how to fix.

If you're interested in more detail on the changes I made, you can look at my [script notes](./notes.md) file (definitely spoilers to be found here), or look directly at the file history in this repository. You can easily view almost all the changes at once [here](https://github.com/dackst/nayuta/commit/2e5b5c5db7d33fb19f7d38e6ba8c0a8826a07419).

<!-- or you can [compare]((https://github.com/dackst/nayuta/compare/original...master)) any of the changed files directly to their originals in this repo. 
broken ever since I moved files around
-->

## Patching instructions
1. Download an xdelta file from latest release. Choose clean.xdelta to apply the patch to an unmodified Japanese ISO, or choose 4_15.xdelta to apply to an ISO patched with version 4.15 of the previous fan-translation.
2. Apply your respective xdelta patch to your respective iso. If on Windows, the easiest thing to do would probably be to use [xdeltaUI](https://www.romhacking.net/utilities/598/).

   If you have xdelta3 installed elsewhere, you should also be able to run something similar to this with the desired filenames swapped in:
```
xdelta3 -dfs original.iso patch.xdelta3 patched.iso
```


### MD5 checksums
* Clean Japanese ISO : `02adefbdef8197cca872268d5c01b277`
* ISO patched with flame's 4.15 release: `6cc975153b7998db4242baa17eb8d276`
* ISO patched with this current release: `1216ffbaa84f1839f7bfdf922233c881`


## Known Issues

### Issues in this version 
These issues don't seem to exist in the original 4.15 fan translation release. I think they may be due to problems with the released tools? See [here](#Why-not-just-use-flame's-tools-directly?) for more info.
* unable to speak to Mishy in early chapters
  * The new game+ sidequest involving Mishy starts late enough to be unaffected, but the special Mishy achievement requires talking to him at every opportunity, so that achievement is unable to be completed.
* there are some extra stray lines of text in Japanese when reading the tablet at the end of Volans' sidequest. 

### Issues from original fantranslation that I don't know how/care enough to try to fix myself
* ingredient location text (press △ on the cooking screen) cannot be changed from the original fan translation, see [here](#Why-not-just-use-flame's-tools-directly?) for more
* erasing save data from in-game menu doesn't work
* there is some strange text spacing in certain spell descriptions
* text pop up when confusion is inflicted says "panic" instead. This inflicted confusion on me, the player, when I thought they were two different status effects.
* boss and new area intro graphics are still untranslated
* long achievement names are cut off in the notification box when unlocking them, e.g. "<armor of anhillat"
  * the achievement notification box is tiny. I'm not willing to butcher the names further in order to make them fit
* characters that use idiosyncratic manners of speaking in Japanese probably still don't here
  * E.g. Geo is supposed to [sound like an old man](https://legendofheroes.fandom.com/wiki/Lychnis_Gio) (characters even comment on it several times in-game), Eris is supposed to sound [domineering](https://legendofheroes.fandom.com/wiki/Song_Priestess_Elislette) or sarcastic. I think Algol is supposed to use archaic speech patterns, and Nemeas is like a schoolteacher or something?




## How do I use the files in this repo?

The original tools require Windows and Python 3. They seem to ["work"](#Why-not-just-use-flame's-tools-directly-on-a-clean-iso?) just as well in Wine if you install a Windows version of Python in a wineprefix. With the changes made in this repo, the Python scripts for the dumping and inserting of binary files should no longer require Windows or Wine, but the beginning extraction step and the final rebuilding step still do due to their use of bundled `.exe` files. 

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



#### Why not just use flame's tools directly?

Before I started, I extracted everything from an iso of the original fantranslation. The addresses of each line in the English script then did not match up with the addresses of each line of the Japanese script, breaking the script insertion, well, script. My changes to the tools were initially so that the addresses from the dumped Japanese files are used instead of the addresses of each line of the input files.

The translated graphics are included in with the released 2017 tools, except the chapter titles are missing. This leads to a common theme where the released tools only seem to *mostly* work as is. Even if I were to revert all of my changes and try to use them as <del>God</del>flame intended, doing something as simple as dumping and reinserting the Japanese script without changes or replacing all text with the string "AAAAA" creates a number of issues not present in the 4.15 fantranslation release:
  1. item/money received messages in cutscenes are broken (but not all?)
  2. Some text remains in their original Japanese forms: Nayuta and Noi's names (stored in `text/pc.tsv`), tutorial menus (from `text/helplib.tsv`), food ingredient locations (`text/foodarea.tsv`) and some dialogue (namely, those in `script/noi.tsv` and `script/system.tsv`).
  3. as mentioned before, chapter start/end graphics are still in Japanese
  3. The text about your next objective that appears when pressing select used flame's translation
  4. can't talk to Mishy in first few chapters: an exclamation point appears when approaching, but nothing happens when you try to interact

Clearly, there were undocumented shenanigans that went on in the original fantranslation, given that none of these issues exist in its final release.

The way I ultimately dealt with #1, #2, and #3 was to look at files from outside the 2017 tools:
  * translated graphics are included with flame's tools, but for some reason the chapter start/end graphics aren't present. I simply grabbed the files from the 4.15 release to replace the Japanese versions
  * copying `USRDIR/pack` folder from the 4.15 translation mostly solved #2. This seems to indicate something is wrong with the `copy_*.py` files. Along with copying your new files to the extracted ISO, they also are intended to modify the files in the `pack` folder so that your new files are read instead of a compressed Japanese version. This doesn't seem to actually be done for the files listed in #2. At least, this isn't done successfully. Like with #3, grabbing the working files from the `pack` folder in the 4.15 release seems to have solved this issue. However, any changes I make in the `foodarea` and `helplib` files are still not reflected, and they are now stuck using the text from the original fantranslation.
  * issue #1 does not exist if I simply do not run the script inserter, but obviously, that leaves me unable to insert any of my script changes. This seemed to indicate something was wrong the script inserter.
    * inserting the script files produced from the [Flame's earlier Python 2 script inserter](https://pastebin.com/vtVwq338) released in 2015 seemed to fix #1, but all non-ascii characters found throughout the script do not display correctly ingame (e.g. ─□×△☆～♪). The game also seems to crash or freeze after talking to certain people, like Orvus. These crashes still occurred even after I tried removing all non-ascii characters from the script.
    * I eventually discovered changing a 1 to a 3 in for the `0xC1` entry in the dictionary defined in the beginning of the Python 3 inserter fixed #1 without introducing the problems in the Python 2 version. The inserter in this repo should include this change.
 
For #4, the correct text will be used if the story is continued to the next objective. It appears this is not at all the fault of the tools, and the text for the current objective is loaded directly from your savefile.

Similar to how many characters tend to feel about Mishy, I still have no idea how to deal with #5, or why it's even there in the first place.

After testing some more, I would occasionally encounter some stray lines of Japanese text underneath my English text in long text boxes. I would usually be able to fix this by reformatting my English text to use an extra line. However, this also occurred when reading the message at the end of Volans' sidequest, but my attempts at fixing it only makes my English text get cut off, and even more Japanese appearing. Copying the original fantranslation's script here also doesn't seem to work.


