# Print Jar Labels
Print configurable amount of labels through swift publisher, with minimal user interaction.

## Why
At [Smith and Truslow](https://smithandtruslow.com), we sell jars of spices, and those jars have labels on them. Every so often, we have to print an absolute ton of labels - and not just 1000 of a certain kind, but 20 of this, 6 of that, etc. This is incredibly tedious to do by hand. 


## What
This program takes as input a CSV with columns for the item SKU, an english description of the item, and the number of labels to print, and goes through and prints all of them, assuming the label path == `LABELS_FOLDER / f{SKU}.spub`. It needs python3.10+, applescript, and Swift Publisher 5. It prints on a Primera Color Label LX2000.


## Adapting this
You probably do not work here, and your use case is different. Get the applescript running for a single label, where you've provided the path and number to print. I have found automator's "record" action to be useful to find the proper snippets. Then, either adapt the python code or write a new wrapper.
