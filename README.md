Recipe Markdown
===============

[![Build Status](https://travis-ci.org/andreasWallner/recipe-markdown.svg?branch=master)](https://travis-ci.org/andreasWallner/recipe-markdown)

We aim to create a bunch of tool for easy entry recipes using a language somewhat inspired by markdown.
The files themselves are simple text files, which are parsed using python and transformed into
other descriptions for display purposes.

At the moment there is support for conversion into XML, HTML (via XSLT). There is also support for Latex output.

The markdown format is designed for a special recipe formatting, but is also usable for "normal" recipes.
In a classic recipe one would have a block of ingredients, and then a number of steps to perform to cook the dish.
In the intended format, steps are grouped with the ingredients needed for those particular steps. The format is
inspired by the recipes used in the cookbook 'Modernist cuisine'.

We prefer the format because it seems clearer, enables one to use much shorter descriptions, and to some degree also
prevents common mistakes like ingredients missing in either the instructions or the ingredient list.

Usage Pattern
-------------

The usage idea is to handle recipes in a souce controls system (we use git atm). When pushing new recipes/changes
to the repository, the needed conversion results are update/created and made available online.

Markdown format
---------------

The format is line-based, every 'information' has to be on a seperate line.
The markdown format contains five types of information:
- metadata
- ingredients
- steps
- note
- wait phases

The metadata block is located at the beginning of the recipe block, ingredients
and steps are mixed because of the intended output format. Ingredients for a
specific block come first, then the steps to perform with the mentioned
ingredients. A note is similar to a step, but contains additional advice and is not numbered.
Wait phases are steps in the recipe that primarily contain of
waiting. Furthermore, the recipe can be separated into different parts.

Currently metadata may contain the following tags:
- !title (name of the recipe)
- !size (how many people can you feed)
- !author (writer of the recipe)
- !source (original source of the recipe)
- !img (on-disk image file; one image per !img tag)

Metadata is written with a leading '!', followed by the type of metadata, a
colon and the value.  After the first metadata line, all lines that can not be
interpreted as anything else will also be considered metadata.
A '!' also has to be used to mark the beginning of a new recipe (since the metadata
has to be at the beginning of the recipe, the first metadata line is sufficient
for this).

Currently for images to be displayed they have to be placed in the same folder the output files will be generated for. This currently poses a problem if you use a git repository and want the files to be generated outside the repo.

Then the recipe itself follows.

Lines with ingredients are started with a '*'. After the star, one can either
write the amount, unit and ingredient (e.g. 4tsp sugar) name, amount and name
(e.g. 4 eggs), or just the ingredient if an amount is not neccesary (e.g.
salt). The unit has to follow the amount directly, without whitespace
in between. In cases when this is not sufficient, squared brackets around the
unit can be used to separate the components in an explicit way (e.g. 1 [heaped tbsp.] sugar).

Steps are started with a '-', followed by the instruction. For notes, '--' is used.

WaitPhase blocks start with a '+' and a '#' is used to start a new part.

Example
-------

As an example, a simple recipe for a quiche lorraine:

    !title: Quiche Lorraine
    !size: 1 28cm quiche pan
    !author: uhu01
    !source: 
    !img: very_nice_image.png

    This would be the description for this very nice recipe, which is actually
    legit and can be cooked like this.
    
    * 200g speck
    * 3pcs onion
    - cut speck into cubes, onion into rings
    - brown both together and let cool
    
    * 3pcs egg
    * 250ml heavy cream
    * 125g Gruyère
    - whisk egg and cream together
    - grate Gruère, add to cream
    - add speck mixture to cream
    
    * shortcrust pastry
    - line dish with pastry
    - fill pastry with the mixture
    - bake in the preheated oven at 180°C, for 30 to 35 minutes

Installation
------------
While all scripts can be run without installation from the bin/ directory, the
recommended way is to install the module via pip.

- checkout the recipe-markdown code
- inside the recipe-markdown directory, run `pip3 install .` (including the dot!)

Installation of the Git Commit Hook
-------------------------------

Installation is pretty simple if you are using a standard git repository.
If you manage your repositories with gitolite replace the 4th step with the
actions appropriate for your version of gitolite (see gitolite docs).

- checkout the recipe-markdown code (e.g. to /opt)
- if necessary, make bin/update-hook executable
- create a new repository to hold your recipes
- in this repositories hooks folder, create a link named "update" that links to
  bin/update-hook
- copy settings\_template.py to the hooks folder and rename it to settings.py
- edit settings.py to suite your needs
- use recipe-markdown by pushing recipes into the repository

Fixing Problems
---------------

If there was a problem and some recipes are not correctly updated anymore
consider running bin/reprocess-all in the hooks directory of the repository.

It will delete all created XML files and the index and generate them anew from
the rmd files at the current repository HEAD.
