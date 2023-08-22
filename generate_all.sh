#!/bin/bash

# This builds the entire website, by grabbing all of the content and building
# their pages, creating the optimized stylesheet, building an awful (FIXME) table
# of contents, and placing everything accordingly.
# The Python script requires htmlmin, Pillow, bs4, css-html-js-minify, and colorama.

OIFS=$IFS
IFS='/'

# Initialize the index HTML document
mkdir -p out
echo "<!DOCTYPE html>" > out/index.html
echo "<title>CoD Map Pool</title>" >> out/index.html
echo "<h1>This is a temporary index of all page content, the actual mod pages look better (promise)!</h1>" >> out/index.html
echo "<ul>" >> out/index.html

# Get every directory in content/
for d in content/*/ ; do
    read -r -a dirs <<< "$d"

    # Run the script with found content
    python generate_page.py ${dirs[1]}

    # Parse the outfile
    IFS='+'
    read -r -a content < out.txt
    IFS='/'

    # Add to the index list
    echo "<li><a href=\"${dirs[1]}/index.html\">${content[0]}</a>: ${content[1]}</li>" >> out/index.html
done

# Bring the assets in
mkdir -p out/assets
cp template_source/assets/* out/assets/

# Optimize CSS and JavaScript files for size
css-html-js-minify --overwrite out/

IFS=$OIFS
