# Hexcrawl Mapper

A single-file browser tool for laying a hex grid over any map image and keying notes to the hexes. No server, no build step, no dependencies — one HTML file that runs from a URL or straight off disk.

**Live:** https://getoffmaccloud.github.io/greyhawk-hexcrawl/

Built for the *A Tourist In Greyhawk* campaign and the Ritterstadt West Marches, but nothing in it is campaign-specific except the calibration anchor described below.

---

## Quick start

1. **Load map** — pick any image file. It's held in your browser, never uploaded.
2. **Align the grid** — *Hex size*, *Shift* (X/Y offset), and orientation (*Flat top* / *Pointy top*) until the hexes sit where you want them. Do this before calibrating.
3. **Calibrate** — see [Letter coordinates](#letter-coordinates). Until you do, hexes are labelled `04.05`, not `D5`.
4. **Click a hex** — the note editor opens. Title, body, marker colour or icon, save.
5. **Turn on Autosave** — see [Your data](#your-data). Do this before you've done enough work to be sad about losing.

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

The *coords* checkbox draws labels on the grid; the badge shows the hex under the cursor either way. *terrain* tints hexes using a loaded pipeline file.

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

## Letter coordinates

Out of the box the tool labels hexes `NN.NN` — zero-padded column and row in **tool space**, which depends entirely on where your grid happens to sit on the image. Letter coordinates like `D5` only exist once you've told the tool where it is in the world.

### How to calibrate

1. **Align the grid first.** The anchor is stored as a tool-space hex, so changing *Hex size* or *Shift* afterwards invalidates it and every letter shifts. Get the grid right, then calibrate.
2. **Alt+click** any export button — *Obsidian note*, *Publish note*, *Web map*, or *Hex notes*. (If you've never calibrated, a plain click on *Hex notes* also triggers it.)
3. The tool asks for the anchor. **Find Ritterstadt on the map image and click its hex.** It is not asking for a coordinate — the coordinate is what you're about to create.
4. Done. Every hex in range now carries a letter label, and the anchor persists.

Tick **coords** to see the labels drawn on the grid, or just hover — the badge reads:

```
Hex 04.05 · D5 · Darlene 104.62
```

**One quirk:** calibration was designed as a step inside exporting, so finishing it immediately runs whatever export you alt-clicked. If you only wanted coordinates, discard the file it produces.

### How the three grids reconcile

The anchor sets an offset, and everything else is arithmetic:

```
vault  = tool + (4 - anchor.col, 5 - anchor.row)     → Ritterstadt = 4,5 = D5
letter = chr(64 + vault.x) + vault.y                 → 4,5 → D5
Darlene = (vault.x + 100) . (vault.y + 57)           → 4,5 → 104.62
```

Offsets 100 and 57 live in `settings.darleneColOff` / `darleneRowOff`. If a pipeline file records an explicit Darlene coordinate for a hex, that value wins over the arithmetic.

**Hexes outside the vault grid keep showing `NN.NN` forever.** Letters require vault column 1–26 and row ≥ 1, and if a pipeline defines `cols`/`rows`, anything beyond it is not a vault hex. This is intended, not a calibration failure.

---

## Exports

| Button | Produces |
|---|---|
| **Export** | `<mapname>-notes.json` — the complete state bundle. See below. |
| **Obsidian note** | A Markdown note with `obsidian://` links, for a local vault |
| **Publish note** | A Markdown note pointing at your published wiki |
| **Web map** | A standalone interactive HTML map with the base image baked in |
| **Hex notes** | One Markdown file per hex, written into a folder you choose |

*Obsidian note*, *Publish note*, and *Web map* require a calibrated anchor. *Web map* also prompts for your wiki base URL, which it remembers.

**Import** takes an exported JSON bundle back in. **Pipeline** takes `map-data.json` from the map-generation toolchain, supplying terrain colours, regions, and recorded Darlene coordinates.

### Hex notes never overwrite

`Hex notes` checks whether a file already exists at each path and skips it rather than clobbering it, reporting how many were written and how many were left alone. Safe to re-run against a vault you've been hand-editing.

If the browser can't write to a folder directly, it falls back to a single `hex-notes-bundle.md` for you to split by hand.

---

## Your data

Everything lives in your browser, tied to the exact address the tool is open at.

- **IndexedDB** (database `hexcrawl`, store `kv`, key `state`) holds the **full** state — notes, settings, icons, and the base map image.
- **localStorage** (key `hexcrawl-state`) holds a deliberately degraded copy with the map image stripped out, as a fallback for when IndexedDB is unavailable.

So localStorage alone would restore your notes but lose your map. IndexedDB is the real store.

**Clearing site data wipes both.** So does switching browsers, switching machines, or using a private window. There is no account and no cloud copy.

**The hosted and local copies do not share state.** `https://getoffmaccloud.github.io/…` and a `file:///` copy on your disk are different browser origins, so each keeps entirely separate notes and images. Moving between them means exporting from one and importing into the other.

### The Export bundle is a complete backup

`Export` serialises the whole state object, and the base map image travels inside it as base64. Import that one file on any browser or machine and you get notes, settings, icons, and the map itself back in a single step. It is genuinely sufficient on its own.

### Autosave

**Autosave…** asks for a real file on disk and mirrors every save to it as you work. This is the durable option and the one to prefer — treat *Export* as the deliberate snapshot rather than the routine backup.

It uses the File System Access API, so it works in Chrome and Edge but not Firefox or Safari. In those, use *Export* and do it on purpose.

---

## Related

The **Web map** export is what produced [Ritterstadt-Marches-Map](https://github.com/GetOffMacCloud/Ritterstadt-Marches-Map) — this repo is the tool, that one is a published artifact of it.

## Credits

The tool contains no map art. Base images are supplied by the user at runtime and are never committed here.

Maps of the Flanaess used with this tool are the work of **Anna B. Meyer** (ghmaps.net), released under CC BY — credit her wherever one of her maps is redistributed.

Greyhawk is a trademark of Wizards of the Coast. This is unofficial fan work, not for sale.

---

## Sharing

Nothing syncs. Two people on the same URL are running two independent copies, and neither can see the other's notes. Sharing is always a deliberate act.

### What each thing carries

| You send | They get | Your notes travel? |
|---|---|---|
| The URL, or the HTML file | An empty mapper | No |
| **Player map** export | A read-only map plus their own local notes | Only those marked *Share with players* |
| **Web map** export | A clickable grid linking to your wiki | No — it uses POI tables, not your notes |
| **Export** bundle (`.json`) | Everything, importable | **All of them, including secrets** |

The Export bundle is the dangerous one. It has no filter — send it and you have sent every note you have written.

### Marking notes for players

Tick **Share with players** in the note editor. Only ticked notes are baked into the player map.

### Player map

**Player map** writes a standalone `player-map.html`: the base image, the hex grid with letter coordinates, and your shared notes as markers with titles and bodies. Upload it to `players/index.html` in this repo and your group opens it at `/players/`.

Players can write their own notes on it. Those live in their browser under `hexcrawl-player-<mapid>` and are visible to nobody else.

### Notes coming back

A player ticks *Offer this note to the DM*, presses **Send notes to the DM**, and gets a `HEXNOTES1:` code to send you however you normally talk.

Paste it into **Inbox** and press Read. Each note appears with its hex, its author, and Approve / Deny:

- **Approve** — the note lands on your map marked shared. If the hex already has a note, the player's text is appended with attribution rather than overwriting.
- **Deny** — it disappears from your queue. Their copy is untouched; they simply never see it on the shared map.

Approved notes reach the rest of the group **the next time you export the player map and upload it.** There is no server, so nothing is live. Re-export when you want the group's map to catch up.

### Caution

Import replaces state wholesale — `state = { ...state, ...p }` — so importing someone's bundle discards your own notes rather than merging them. Import calls `pushUndo()` first, so **Ctrl+Z immediately afterwards recovers them**, but only if you notice before doing anything else.
