# Website image catalog schema

Each record represents either a file served from the repository's `assets/`
directory or an externally hosted image.

```ts
export type WebsiteImageOrientation = "landscape" | "portrait" | "square";

export interface WebsiteImage {
  id: string;
  src: string;
  category: string;
  orientation: WebsiteImageOrientation;
  tags: string[];
  bestFor: string[];
  mood: string[];
  alt: string;
  focalPoint: {
    x: number;
    y: number;
  };
}
```

## Field decisions

- `id`: stable, unique kebab-case handle based on the subject and setting.
- `src`: `/assets/...` for local files or the unchanged full `https://...` URL
  for remote images. Keep meaningful remote query parameters.
- `category`: one broad retrieval group such as `resort`, `food`, `people`,
  `product`, `architecture`, or a project-specific taxonomy already in use.
- `orientation`: use `square` when dimensions are equal or effectively square;
  otherwise compare width and height.
- `tags`: concrete subjects, setting, visual features, industry, and likely
  search phrases. Prefer roughly 5-12 useful phrases over near-duplicates.
- `bestFor`: plausible placements such as `hero`, `banner`, `card`, `editorial`,
  `background`, `gallery`, `thumbnail`, or `feature`.
- `mood`: 2-6 visually supported qualities such as `calm`, `luxury`, `warm`,
  `playful`, `corporate`, or `dramatic`.
- `alt`: natural description of visible, relevant content. Decorative images
  may use an empty string only when the project intentionally treats them as
  decorative.
- `focalPoint`: integer or decimal percentages in the inclusive range 0-100,
  measured from the top-left corner.

## Example

```ts
{
  id: "luxury-hotel-lobby-modern-city-view-01",
  src: "https://images.unsplash.com/photo-1587702068694-a909ef4aa346?q=80&w=687&auto=format&fit=crop",
  category: "resort",
  orientation: "portrait",
  tags: [
    "luxury hotel",
    "hotel lobby",
    "modern interior",
    "city view",
    "floor-to-ceiling windows",
    "hospitality",
  ],
  bestFor: ["hero", "editorial", "card", "banner"],
  mood: ["luxury", "corporate", "exclusive", "urban"],
  alt: "Modern luxury hotel lobby with designer seating, floor-to-ceiling windows and an urban city view",
  focalPoint: {
    x: 52,
    y: 60,
  },
},
```

Follow an existing catalog's export name and style. For a new catalog, declare
the types above and export an empty starter array:

```ts
export const websiteImages: WebsiteImage[] = [];
```
