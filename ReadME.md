Parmveer Dayal
CMPT 354 Project
ReadME File

How to run application:
I only had to pip install pyodbc. I am assuming everyone else has similar python files with just pyodbc so this should work. But if it is not try pip install pyodbc.

I did everything using the windows CSIL computers is ASB 9840 and it is python 3 (should be 3.11).

This file should run like a normal python file anyways. But I ran it in VSCode by hitting the play button 
and it worked just fine. I'm sure you will adjust this command depending on where you have this file saved. It will work just like a normal python file as long as pyodbc is pip installed.

The only things imported are pyodbc, string, and random. All these should work just fine.


How to use application:
When the file is first run, the application will ask for a login. This login will loop and keep asking for an existing user ID. This ID is also case sensitive so will only work when the ID is exactly the same.

Anytime it says (y/n) it is asking for yes or no. So please enter either 'y' or 'n'. Or it will ask again.

Once logged in, there will be a main menu with 4 options. This is the main loop of the applications and will never end unless the terminal is closed. Only integers 1 to 4 will be accepted. If something else is inputted it will keep looping until the correct number is inputted.

For search business, each filter will come up and each filter will give clear instructions on how the user can skip that filter. So to skip the filters enter 1 for min stars, 5 for max stars (because 1 and 5 are the min and max stars anyways), 'any' for city, and press enter without a character for name, respectively. The results will then be printed and if there is none then a message will let the user know. User will be sent back to the main menu after.

For search user, the same thing will happen for filters like business. To skip any filter just follow the instructions that come up before inputting a value. For name you just enter without a character and for the other 3 write 'skip' then enter. Also, to select those just enter 'y' or 'n'. Add a friend option will also be in here but it is only exclusive to the search results. Options to quit to the menu will be given as well.

For add friend, user can add anyone as long as user ID is existent. The ID is also case sensitive and will give the user options to quit to main menu if they try to add themselves (not possible) or get an ID wrong every 3 times in a row. If a user is added then it will add it to the friendship table and let user know. Also, will let user know if they are already friends. Will go back to main menu after.

Finally, for write a review, the ID inputted is case sensitive so it will only work when it is exactly correct. Otherwise, it will keep repeating until the correct ID is inputted. Will also give the user the option to quit to menu every 3 times they get an ID wrong. Will ask for stars after and star must be an int and between 1 to 5. Review will then be listed in the review table and stars will update thanks to the trigger. A message will be given to the user to let them know the review is submitted and then they will be sent back to the main menu.

All the instructions are listed when asking for inputs. Only ID's are case sensitive and will let the user know as well!