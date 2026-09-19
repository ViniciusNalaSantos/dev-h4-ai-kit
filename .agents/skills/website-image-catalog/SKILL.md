---
name: website-image-catalog
description: Set up and maintain an AI-readable website image library using a repository-level assets folder, AGENTS.md guidance, and website-images.ts metadata. Use when adding, removing, reviewing, or cataloging local website images or external image URLs.
---

# Website Image Catalog

Keep website imagery discoverable without forcing future agents to repeatedly
search for, open, and reinterpret every image.

## Set up the repository

At the beginning of the first image-library task in a repository, perform the
setup directly with the available file-editing tools:

1. Find the repository root and read every applicable `AGENTS.md` before
   editing.
2. Create the root `assets/` directory if it is absent. Add `assets/.gitkeep`
   only when the directory would otherwise be empty, so Git can retain it.
3. Search the repository for `website-images.ts`. If exactly one exists, use
   it in place and preserve its module shape. If none exists, create it at the
   repository root using the types in
   [references/catalog-schema.md](references/catalog-schema.md) and export an
   empty `websiteImages` array. If multiple files exist, determine which one
   belongs to the website in scope rather than creating another.
4. Create or update the root `AGENTS.md` without replacing unrelated
   instructions. Add a concise `Website image library` section that links to
   `assets/` and the actual repository-relative location of
   `website-images.ts`, and instructs future agents to use this skill whenever
   imagery changes. Do not duplicate the section on later runs.

Use relative Markdown links in `AGENTS.md`, for example:

```markdown
## Website image library

- Store local website images in [`assets/`](assets/).
- Find image metadata in [`website-images.ts`](website-images.ts).
- Use `$website-image-catalog` whenever local images or external image URLs
  change.
```

Do not run or create a helper script for this setup. The agent must inspect the
project, make the edits itself, and verify the resulting files.

## Reconcile the catalog

Before editing the catalog:

1. Find the repository root and the applicable `AGENTS.md` instructions.
2. Locate `website-images.ts`; do not create a competing catalog if one exists.
3. Run `git status --short --untracked-files=all -- assets/ website-images.ts`
   to identify additions, modifications, renames, and deletions.
4. When the catalog is new or incomplete, also enumerate all image files under
   `assets/`, including already tracked files. Git status alone is not a full
   inventory.
5. Open each new or changed local image with an image-viewing tool. Use actual
   dimensions and visible content; do not invent visual metadata from a
   filename. Inspect an external image URL when the user adds one or asks for
   it to be cataloged.
6. Read [references/catalog-schema.md](references/catalog-schema.md), then add
   or update only the affected entries.
7. Re-run Git status and type-check or format the TypeScript file with the
   project's existing tooling when available.

Preserve stable IDs and human-curated metadata for unchanged entries. When a
local asset is renamed, update its `src` but keep its ID unless the ID is now
misleading. Remove a local entry when its asset was deleted. Git cannot detect
changes to remote images, so only alter URL-backed entries when explicitly
in scope.

## Catalog quality

- Local `src` values use root-relative web paths such as
  `/assets/hotel/lobby.webp`; external images retain their full `https://` URL.
- Make IDs unique, stable, descriptive kebab-case identifiers. Do not encode
  temporary dimensions or query parameters in an ID.
- Derive `orientation` from dimensions: `landscape`, `portrait`, or `square`.
- Write concise, accessibility-quality alt text describing visible content and
  relevant context. Avoid phrases such as "image of" and do not keyword-stuff.
- Use specific search-oriented tags, a small set of realistic placements in
  `bestFor`, and visually supported emotional qualities in `mood`.
- Express `focalPoint` as percentages from the top-left. Center is `{ x: 50,
  y: 50 }`. Place it on the subject or composition area that responsive crops
  should preserve.
- Match the existing module's exports, formatting, and types. Do not rewrite
  unrelated entries merely to enforce the starter template.

Report which entries were added, updated, removed, or left uncertain after the
catalog edit.
