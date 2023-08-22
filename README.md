# CoD Map Pool Content List

This repository holds the web generator for the [CoD Map Pool](https://motolegacy.github.io/map-pool), which is (yet another) Call of Duty 4 and World at War mod browser, but with a spec for downloads that is both Linux (Proton, WINE, PlayOnLinux) and Windows friendly.

## Submitting a Mod

Data for the mods used to create webpages are found in the [content directory](content/). Content must be limited to images and the `.JSON` data for your mod to be accepted. Content descriptions are in HTML syntax, and we [provide a stylesheet](template_source/assets/stylesheet.css) for you to use. Note that images submitted are compressed on web build to be bandwidth-friendly, and your downloads **MUST** be hosted on archive.org, the `download_name` syntax is what comes after `https://archive.org/download/` in the *direct download* URL. This is mandatory in order to assure preservation of hosted content.

## Building the page

`generate_all.sh` will build the entire website, and `generate_page.py <name>` will build an individual page. The following `pip` packages are required:

* htmlmin 
* Pillow
* bs4
* css-html-js-minify
* colorama

Pages will be dumped to `out/<name>/`.