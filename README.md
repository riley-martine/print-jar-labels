# Print Jar Labels
Print configurable amount of labels through swift publisher, with minimal user interaction.

## Why
At [Smith and Truslow](https://smithandtruslow.com), we sell jars of spices, and those jars have labels on them. Every so often, we have to print an absolute ton of labels - and not just 1000 of a certain kind, but 20 of this, 6 of that, etc. This is incredibly tedious to do by hand.
 
![organic-cinnamon(1)(1)](https://user-images.githubusercontent.com/10540915/167214496-d52e5929-15d6-45e5-b0e1-e817948d2917.png)

## What
This program automates the repetitive task of opening a label file, looking up how much to print, printing that many, and repeating. It takes as input a CSV with columns for the item SKU, an english description of the item, and the number of labels to print, and goes through and prints all of them, assuming the label path == `LABELS_FOLDER / f{SKU}.spub`. It needs python3.10+, applescript, and Swift Publisher 5. It prints on a [Primera Color Label LX2000](https://www.primera.com/lx2000downloads) (Discontinued).

It does this by opening the label in [Swift Publisher 5](https://www.swiftpublisher.com/), and actually clicking on the proper dropdowns (File->Print; Select Printer; Input number of copies; Set paper size; Print; Close).

![output](https://user-images.githubusercontent.com/10540915/167216569-3ff7051b-0e9b-4fed-a621-98f67c05fbe2.gif)

## Adapting this
You probably do not work here, and your use case is different. The central idea should work for anyone on MacOS who must regularly print a variable number of a large quantity of documents. Get the applescript running for a single file, where you've provided the path and number to print. (Run with `osascript -e printsmall.applescript`.) I have found automator's "record" action to be useful to find the proper snippets. Then, either adapt the python code or write a new wrapper.

## Usage
Be sure you will not need to print any specific label in the near future, as the printer will be occupied for a while.

Do a test print. Print 6 of any label. Check if it is aligned, if it is not, fix it. (LX2000 app->Label offsets). Check that the printer prints 6 and then cuts (not 4 and then cuts and then 2). If not, fix it.

Open Terminal.app, cd to the code directory, type `python3.10 print_jar_labels_variable.py`, and hit enter.

Follow the prompts onscreen. Note any errors, remediate if desired.

Every now and then, replace the empty roll with a new roll of labels. Ensure alignment is alright - it may correct itself or drift, so watch the first 18 or so. You will want to pause the printer, adjust alignment, and resume. This will unfortunately mess up the cut location, and you'll have 5 of one SKU + 1 of another per cut, or 4+2. I have not found a way to insert a new item at the head of the print queue, this would fix the problem.

If you need to edit the amount of labels printed per jar, edit the csv file whose location is defined in the variable `JAR_QUANTITIES`. It has a 3 column format - sku,description,target.
