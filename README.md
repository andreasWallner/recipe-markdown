Recipe Markdown
===============

We aim to create a bunch of tool for easy entry recipes using a language somewhat inspired by markdown.
The files themselves are simple text files, which are parsed using python and transformed into
other descriptions for display purposes.

At the moment there is support for conversion into XML, HTML (via XSLT). There is also support for Latex output.

The markdown format is designed for a special recipe formatting, but is also usable for "normal" recipes.
In a classic recipe one would have a block of ingredients, and then a number of steps to perform to cook the dish.
In the intended format, steps are grouped with the ingredients needed for those particular steps. The format is
inspired by the recipes used in the cookbook 'Modernist cuisine'.

We prefer the format because it seems clearer, enables one to use much shorter descriptions, and to some degree also
prevent common mistakes like ingredients missing in either the instructions or the ingredient list.

Usage Pattern
-------------

The usage idea is to handle recipes in a souce controls system (we use git atm). When pushing new recipes/changes
to the repository, the needed conversion results are update/created and made available online.

Markdown format
---------------

The format is line-based, every 'information' has to be on a seperate line.
The markdown format contains three types of information:
- metadata
- ingredients
- steps

The metadata block is located at the beginning of the recipe block, ingredients and steps are mixed because
if the intended output format. Ingredients for a specific block come first, then the steps to perform with the
mentioned ingredients.

Currently metadata may contain
- title / name
- size (how many people can you feed)
- author (writer of the recipe)
- source (original source of the recipe)

Metadata is written with a leading '!', followed by the type of metadata, a colon and the value.

Then the recipe itself follows.

Lines with ingredients are started with a '#'. After the hash, one can either write the amount, unit and ingredient
name, or just the ingredient if an amount is not neccesary (e.g. salt).

Steps are started with a '\*', followed by the instruction.

Example
-------

As an example, a simple recipe for a quiche lorraine:

    ! title: Quiche Lorraine

    # 200g speck
    # 3pcs onion
    * cut speck into cubes, onion into rings
    * brown both together and let cool
    
    # 3pcs egg
    # 250ml heavy cream
    # 125g Gruyère
    * whisk egg and cream together
    * grate Gruère, add to cream
    * add speck mixture to cream
    
    # shortcrust pastry
    * line dish with pastry
    * fill pastry with the mixture
    * bake in the preheated oven at 180°C, for 30 to 35 minutes
