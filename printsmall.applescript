use AppleScript version "2.4" -- Yosemite (10.10) or later
use scripting additions

set labelPrinter1 to 1
set file_path to "{file_path}"
set number_print to "{number_print}"

tell application "Swift Publisher 5"
	open file_path
	activate
	delay 2
	tell application "System Events"
		tell process "Swift Publisher 5"
			# Print
			click menu item 24 of menu 1 of menu bar item "File" of menu bar 1
			delay 0.5
			
			# Set correct printer
			set printerDrop to pop up button 1 of splitter group 1 of sheet 1 of window 1
			click printerDrop
			delay 0.5
			click menu item labelPrinter1 of menu 1 of printerDrop
			delay 0.5
			
			# Set number of copies
			set value of text field 1 of splitter group 1 of sheet 1 of window 1 to number_print
			delay 0.5
			set value of text field 1 of group 3 of splitter group 1 of sheet 1 of window 1 to "1"
			delay 0.5
			
			# Set paper size
			set sizeDrop to pop up button 3 of splitter group 1 of sheet 1 of window 1
			click sizeDrop
			delay 2
			click menu item "Small Jar 1.31 by 5.50 inches" of menu 1 of sizeDrop
			delay 0.5
			
			# Print and close
			click UI element "Print" of splitter group 1 of sheet 1 of window 1
			delay 2
			click menu item "Close" of menu 1 of menu bar item "File" of menu bar 1
		end tell
	end tell
end tell

return ""
