# Hexcrawl Mapper

A single-file browser tool for laying a hex grid over any map image and keying notes to the hexes. No server, no build step, no dependencies — one HTML file that runs from a URL or straight off disk.

**Live:** https://getoffmaccloud.github.io/greyhawk-hexcrawl/

Built for the *A Tourist In Greyhawk* campaign and the Ritterstadt West Marches, but nothing in it is campaign-specific except the calibration anchor described below.

---

## Quick start

1. **Load map** — pick any image file. It's held in your browser, never uploaded.
2. **Align the grid** — *Hex size*, *Shift* (X/Y offset), and orientation (*Flat top* / *Pointy top*) until the hexes sit where you want them.
3. **Click a hex** — the note editor opens. Give it a title, body, a marker colour or an icon, and save.
4. **Turn on Autosave** — see [Your data](#your-data). Do this before you've done enough work to be sad about losing.

---

## Controls

| Action | How |
|---|---|
| Pan | Drag the canvas |
| Zoom | Scroll wheel (0.05×–12×) |
| Open a hex note | Click the hex |
| Save note | **Ctrl/Cmd+Enter**, or the Save button |
| Close editor | **Esc** |
| Undo | **Ctrl/Cmd+Z** |
| Redo | **Ctrl/Cmd+Shift+Z** or **Ctrl/Cmd+Y** |
| Find a note | The search box filters the note list |

Coordinates appear in the badge as `col,row`. The *coords* and *terrain* checkboxes toggle labels and pipeline terrain tinting on the canvas.

## Markers

Six preset marker colours, or any icon you've imported:

| Swatch | Hex |
|---|---|
| Gold | `#d4a24e` |
| Green | `#7fb069` |
| Blue | `#6a9fd4` |
| Red | `#d47b6a` |
| Violet | `#b58ad4` |
| Bone | `#e0e0e0` |

The colours carry no built-in meaning — assign your own and write the key into the map's own notes so it survives you forgetting.

---

## Exports

| Button | Produces |
|---|---|
| **Export** | The full state bundle as JSON — notes, settings, icons. This is your backup. |
| **Obsidian note** | A note formatted for a local vault |
| **Publish note** | A note formatted for the Obsidian Publish site |
| **Web map** | A standalone interactive HTML map with the base image baked in |
| **Hex notes** | Per-hex note files |

**Import** takes an exported JSON bundle back in. **Pipeline** takes a JSON file from the map-generation toolchain, which is what feeds the *terrain* tinting.

### Calibration

*Hex notes* needs to know where your local grid sits in world coordinates. The first time you use it, the tool asks you to click the **Ritterstadt hex (D5)** on your map, and remembers the anchor from then on.

**Alt+click** any export button to redo that calibration — useful after you've re-aligned the grid or swapped the base image.

---

## Your data

Everything lives in your browser, tied to the exact address the tool is open at:

- **Notes and settings** — `localStorage`, key `hexcrawl-state`
- **Base map image** — IndexedDB, database `hexcrawl`, store `kv`

Two consequences worth internalising:

**Clearing site data wipes everything.** So does switching browsers, switching machines, or using a private window. There is no account and no cloud copy.

**The hosted and local copies do not share state.** `https://getoffmaccloud.github.io/…` and a `file:///` copy on your disk are different browser origins, so each keeps its own separate notes and its own separate map image. Moving between them means exporting from one and importing into the other.

### Autosave

The **Autosave…** button asks for a real file on disk and writes the bundle to it as you work. This is the durable option and the one to prefer — treat *Export* as the manual fallback rather than the primary backup.

It uses the File System Access API, so it's available in Chrome and Edge but not Firefox or Safari. In those browsers, use **Export** and do it deliberately.

---

## Related

The **Web map** export is what produced [Ritterstadt-Marches-Map](https://github.com/GetOffMacCloud/Ritterstadt-Marches-Map) — this repo is the tool, that one is a published artifact of it.

## Credits

The tool contains no map art. Base images are supplied by the user at runtime and are never committed here.

Maps of the Flanaess used with this tool are the work of **Anna B. Meyer** (ghmaps.net), released under CC BY — credit her wherever one of her maps is redistributed.

Greyhawk is a trademark of Wizards of the Coast. This is unofficial fan work, not for sale.
