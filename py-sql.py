

import pyodbc
import string
import random

conn = pyodbc.connect('driver=')

cur = conn.cursor()

# Helper function to check if the inputted string contains an apostrophe and fix it if it does
def checkapostrophe(string):
    apostrophe = False
    for x in string:
        if x == "'":
            apostrophe = True
            break
    if apostrophe:
        temp = []
        string = list(string)
        count = len(string)
        i=0
        while i < count:
            # Add a '' instead of a ' which is the correct way to put ' in sql
            if string[i] == "'":
                temp.append(string[i])
            temp.append(string[i])
            i = i+1
        string = "".join(temp)
    return string

############### Start ####################
print("Hi! Login so you can find businesses, make new friends, and leave reviews!\n")

# Ask for user ID and check for apostrophe
userid = input("Please enter your userID: ")
userid = checkapostrophe(userid)

SQLCommand = (f"select * from user_yelp where user_id = '{userid}' collate latin1_general_cs_as")
cur.execute(SQLCommand)
data = cur.fetchall()

# Infinite loop until existing user ID is entered
while True:
    if not data:
        print("This userID does not exist. Please try again. Remember your login is case sensitive!\n")
        userid = input("Please enter userID: ")
        userid = checkapostrophe(userid)
        
        SQLCommand = (f"select * from user_yelp where user_id = '{userid}' collate latin1_general_cs_as")
        cur.execute(SQLCommand)
        data = cur.fetchall()
    
    else:
        print("\nWelcome! You are now logged in!")
        break

# Main infinite loop that will keep running until the terminal is closed
while True: 
    # Loop will contine until 1, 2, 3, 4, or 5 are entered
    while True:
        print("\nMain Menu:")
        menu = input("Select 1 (Search Business), 2 (Search User), 3 (Make a Friend), or 4 (Write a Review): ")
        if menu in ("1", "2", "3", "4"):
            menu = int(menu)
            break
        else:
            print("Please try again. Only select integers from 1 to 4.\n")
    
    if menu == 1:
        ###### SEARCH BUSINESS ######
        print("\nYou have selected search business!")
        print("Please select the filters you would like as they come along!")
        print("If you do not want a certain filter follow these rules: select 1 for min stars, 5 for max stars, 'any' for city and empty for name")
        print("These instructions to skip will be shown when asking for an input as well!\n")

        # 2 loops that continue until the correct numbers are entered
        while True:
            try:
                minstars = float(input("Enter the MINIMUM stars for the business (int or decimal from 1-5, 1 is also used to skip this filter): "))
                if minstars >= 1 and minstars <= 5:
                    break
                else:
                    print("Please enter a number between 1 and 5. Try again.\n")
            except ValueError:
                print("Please enter a number. Try again.\n")

        while True:
            try:
                maxstars = float(input("Now enter MAXIMUM stars (int of decimal from 1-5, 5 is also used to skip this filter): "))
                if maxstars < minstars:
                    print("The maximum stars cannot be less than the minimum stars. Try again.\n")
                elif maxstars >= 1 and maxstars <= 5:
                    break
                else:
                    print("Please enter a number between 1 and 5. Try again.\n")
            except ValueError:
                print("Please enter a number. Try again.\n")

        # Enter city and business name (both will be checked for apostrophes)
        city = input("Enter city name (write 'any' if you want to skip this filer): ").lower()
        city = checkapostrophe(city)

        business_name = input("Enter business name (or part of it, press enter without any characters if you would like to skip this filter): ").lower()
        business_name = checkapostrophe(business_name)
        print()

        # Select filters in SQL depending on if any is inputted for city
        if city == "any":
            findbusiness = (f"select business_id, name, address, city, stars \
            from business where stars >= {minstars} and stars <= {maxstars} \
                and name like '%{business_name}%' order by name") 
        else:
            findbusiness = (f"select business_id, name, address, city, stars \
                from business where stars >= {minstars} and stars <= {maxstars} and city = '{city}' \
                    and name like '%{business_name}%' order by name")
        cur.execute(findbusiness)

        # Print them one by one or let the user know there is no results
        i = 1
        results = cur.fetchone()
        while results:
            print("Business #%d" %i)
            print("Business ID: " + str(results[0]))
            print("Business Name: " + str(results[1]))
            print("Address: " + str(results[2]))
            print("City: " + str(results[3]))
            print("Stars: " + str(results[4]))
            print()
            results = cur.fetchone()
            i = i + 1
        if i == 1:
            print("\nThere is nothing in the results with these filters:")
            print("Minimum stars: " + str(minstars))
            print("Maximum stars: " + str(maxstars))
            print("City: " + str(city))
            print("Name: " + str(business_name))
            print("You are going back to the main menu. Try again if you would like!")
        else:
            print("\nHere are all the businesses.")

    elif menu == 2:
        ###### THIS IS SEARCH USERS ######
        print("\nYou have selected search users!")
        print("Please enter the filters as they come along!\n")
        
        # Ask for name (or part of it) and check for apostrophes
        user_name = input("Enter name (or part of it, you can skip this filter by pressing enter without inputting any character): ").lower()
        user_name = checkapostrophe(user_name)
        
        # Loop until correct input for useful, funny, and cool
        while True:
            useful = input("Useful? (y/n or 'skip' to skip filter): ").lower()
            if useful in ("y", "n", "skip"):
                break
            else:
                print("Please try again. Make sure to only write y, n, or skip.\n")
        
        while True:
            funny = input("Funny? (y/n or 'skip' to skip filter): ").lower()
            if funny in ("y", "n", "skip"):
                break
            else:
                print("Please try again. Make sure to only write y, n, or skip.\n")
        
        while True:
            cool = input("Cool? (y/n or 'skip' to skip filter): ").lower()
            if cool in ("y", "n", "skip"):
                break
            else:
                print("Please try again. Make sure to only write y, n, or skip.\n")

        # If statements for different filters, need to take the skip's into account as well
        if useful == "skip" and funny == "skip" and cool == "skip":
            finduser = (f"select user_id, name, useful, funny, cool, yelping_since from user_yelp \
                where name like '%{user_name}%' order by name")
        elif useful == "skip" and funny == "skip":
            if cool == "y":
                finduser = (f"select user_id, name, useful, funny, cool, yelping_since from user_yelp \
                    where name like '%{user_name}%' and cool > 0 order by name")
            else:
                finduser = (f"select user_id, name, useful, funny, cool, yelping_since from user_yelp \
                    where name like '%{user_name}%' and cool = 0 order by name")
        elif useful == "skip" and cool == "skip":
            if funny == "y":
                finduser = (f"select user_id, name, useful, funny, cool, yelping_since from user_yelp \
                    where name like '%{user_name}%' and funny > 0 order by name")
            else:
                finduser = (f"select user_id, name, useful, funny, cool, yelping_since from user_yelp \
                    where name like '%{user_name}%' and funny = 0 order by name")
        elif funny == "skip" and cool == "skip":
            if useful == "y":
                finduser = (f"select user_id, name, useful, funny, cool, yelping_since from user_yelp \
                    where name like '%{user_name}%' and useful > 0 order by name")
            else:
                finduser = (f"select user_id, name, useful, funny, cool, yelping_since from user_yelp \
                    where name like '%{user_name}%' and useful = 0 order by name")
        elif useful == "skip":
            if funny == "y" and cool == "y":
                finduser = (f"select user_id, name, useful, funny, cool, yelping_since from user_yelp \
                    where name like '%{user_name}%' and funny > 0 and cool > 0 order by name")
            elif funny == "y" and cool == "n":
                finduser = (f"select user_id, name, useful, funny, cool, yelping_since from user_yelp \
                    where name like '%{user_name}%' and funny > 0 and cool = 0 order by name")
            elif funny == "n" and cool == "y":
                finduser = (f"select user_id, name, useful, funny, cool, yelping_since from user_yelp \
                    where name like '%{user_name}%' and funny = 0 and cool > 0 order by name")
            else:
                finduser = (f"select user_id, name, useful, funny, cool, yelping_since from user_yelp \
                    where name like '%{user_name}%' and funny = 0 and cool = 0 order by name")
        elif funny == "skip":
            if useful == "y" and cool == "y":
                finduser = (f"select user_id, name, useful, funny, cool, yelping_since from user_yelp \
                    where name like '%{user_name}%' and useful > 0 and cool > 0 order by name")
            elif useful == "y" and cool == "n":
                finduser = (f"select user_id, name, useful, funny, cool, yelping_since from user_yelp \
                    where name like '%{user_name}%' and useful > 0 and cool = 0 order by name")
            elif useful == "n" and cool == "y":
                finduser = (f"select user_id, name, useful, funny, cool, yelping_since from user_yelp \
                    where name like '%{user_name}%' and useful = 0 and cool > 0 order by name")
            else:
                finduser = (f"select user_id, name, useful, funny, cool, yelping_since from user_yelp \
                    where name like '%{user_name}%' and useful = 0 and cool = 0 order by name")
        elif cool == "skip":
            if useful == "y" and funny == "y":
                finduser = (f"select user_id, name, useful, funny, cool, yelping_since from user_yelp \
                    where name like '%{user_name}%' and useful > 0 and funny > 0 order by name")
            elif useful == "y" and funny == "n":
                finduser = (f"select user_id, name, useful, funny, cool, yelping_since from user_yelp \
                    where name like '%{user_name}%' and useful > 0 and funny = 0 order by name")
            elif useful == "n" and funny == "y":
                finduser = (f"select user_id, name, useful, funny, cool, yelping_since from user_yelp \
                    where name like '%{user_name}%' and useful = 0 and funny > 0 order by name")
            else:
                finduser = (f"select user_id, name, useful, funny, cool, yelping_since from user_yelp \
                    where name like '%{user_name}%' and useful = 0 and funny = 0 order by name")
        else:
            # If statements depending on if there were no skips for filters!
            if useful == "y" and funny == "y" and cool == "y":
                finduser = (f"select user_id, name, useful, funny, cool, yelping_since from user_yelp \
                    where name like '%{user_name}%' and useful > 0 and funny > 0 and cool > 0 order by name")
            elif useful == "n" and funny == "y" and cool == "y":
                finduser = (f"select user_id, name, useful, funny, cool, yelping_since from user_yelp \
                    where name like '%{user_name}%' and useful = 0 and funny > 0 and cool > 0 order by name")
            elif useful == "y" and funny == "n" and cool == "y":
                finduser = (f"select user_id, name, useful, funny, cool, yelping_since from user_yelp \
                    where name like '%{user_name}%' and useful > 0 and funny = 0 and cool > 0 order by name")
            elif useful == "y" and funny == "y" and cool == "n":
                finduser = (f"select user_id, name, useful, funny, cool, yelping_since from user_yelp \
                    where name like '%{user_name}%' and useful > 0 and funny > 0 and cool = 0 order by name")
            elif useful == "y" and funny == "n" and cool == "n":
                finduser = (f"select user_id, name, useful, funny, cool, yelping_since from user_yelp \
                    where name like '%{user_name}%' and useful > 0 and funny = 0 and cool = 0 order by name")
            elif useful == "n" and funny == "n" and cool == "y":
                finduser = (f"select user_id, name, useful, funny, cool, yelping_since from user_yelp \
                    where name like '%{user_name}%' and useful = 0 and funny = 0 and cool > 0 order by name")
            elif useful == "n" and funny == "y" and cool == "n":
                finduser = (f"select user_id, name, useful, funny, cool, yelping_since from user_yelp \
                    where name like '%{user_name}%' and useful = 0 and funny > 0 and cool = 0 order by name")
            else:
                finduser = (f"select user_id, name, useful, funny, cool, yelping_since from user_yelp \
                    where name like '%{user_name}%' and useful = 0 and funny = 0 and cool = 0 order by name")
        cur.execute(finduser)
        
        # Print all the results and state if there are 0
        i = 1
        result = cur.fetchone()
        a = []
        print()
        while result:
            print("User #%d" %i)
            print("User ID: " + str(result[0]))
            a.append(result[0])
            print("Name: " + str(result[1]))
            print("Useful: " + str(result[2]))
            print("Funny: " + str(result[3]))
            print("Cool: " + str(result[4]))
            print("Date Registered: " + str(result[5]))
            print()
            result = cur.fetchone()
            i = i + 1
        if i == 1:
            print("\nThere is nothing in the results with these filters:")
            print("Name: " + str(user_name))
            print("Useful: " + str(useful))
            print("Funny: " + str(funny))
            print("Cool: " + str(cool))
            print("You are headed back to the main menu! Please try again if you would like!")

        # Ask if user wants to be friends with any of the results
        if i > 1:
            check = True
            check2 = True
            while True:
                wouldyou = input("Would you like to be friends with anyone in this group? (y/n): ").lower()    
                if wouldyou in ("y", "n"):
                    if wouldyou == "y":
                        check = False
                        check2 = False
                    else:
                        print("\nThank you. Headed back to the menu now!")
                    break
                else:
                    print("Please try again. Only select y or n.\n")

            # Loop to check correct ID is inputted
            while check == False:
                test = str(input("Enter ID of friend: "))
                j=0
                while j<i-1:
                    if test == a[j]:
                        check = True
                        break
                    j=j+1

                if check == False:
                    print("\nSorry the ID is not in this list. Try again. ID is case sensitive.")
                    print("You can only be friends with someone in this list from this option.\n")
                    
                    # Ask if user would like to quit back to main menu
                    print("If you would like to befriend someone not on this list, quit back to the main menu.")
                    while True:
                        frm = input("Would you like to quit back to the main menu (y/n): ")
                        if frm in ("y", "n"):
                            if frm == "n":
                                print("\nOkay here is the list of user id's in this list again. Select one:")
                                for x in a:
                                    print(x)
                            else:
                                print("Quitting back to the main menu.")
                                check = True
                                check2 = True
                            break
                        else:
                            print("Please try again. Only input y or n.\n")

            # Make a friend inside of search users
            if check2 == False:
                existingfriend = (f"select * from friendship where user_id = '{userid}' \
                    and friend = '{test}'")
                cur.execute(existingfriend)
                alreadyfriends = cur.fetchall()
                if not alreadyfriends:
                    addfriend = ("INSERT INTO friendship(user_id, friend) VALUES (?,?)")
                    values = [userid, test]
                    cur.execute(addfriend, values)
                    conn.commit()
                    print("\nCongrats! You are now friends!")
                else:
                    print("You are already friends with them!")
    
    elif menu == 3:
        ###### MAKE A FRIEND ######
        print("\nYou have chosen to make a new friend!")
        runit = True
        
        # Loop until correct ID is inputted
        loopcheck = True
        count = 3
        while loopcheck:
            nfr = input("\nPlease enter the user ID of who you would like to be friends with: ")
            
            if userid.lower() == nfr.lower():
                print("You cannot be friends with yourself!")

                # Ask user if they want to quit back to main menu
                while True:
                    quit = input("\nWould you like to quit to the main menu (y/n): ")
                    if quit in ("y", "n"):
                        if quit == "y":
                            print("Headed back to the main menu!")
                            runit = False
                            loopcheck = False
                        break
                    else:
                        print("Please try again. Only input y or n.\n")
            
            else:
                nfr = checkapostrophe(nfr)
                SQLCommand = (f"select * from user_yelp where user_id = '{nfr}' collate latin1_general_cs_as")
                cur.execute(SQLCommand)
                data = cur.fetchall()

                if not data:
                    print("A user does not exist with this ID. ID is case sensitive.")
                    count = count + 1

                    # Ask user every 3 times ID is wrong if they want to quit to menu
                    if count >= 3:
                        if count == 4:
                            print("\nYou have the option to quit to menu. Moving forward, this option will show up every 3 times in a row the ID is wrong.")
                        else:
                            print("\nYou are given the option to quit to menu when the ID is wrong every 3 times.")
                        while True:
                            quit = input("Would you like to quit to the main menu (y/n): ")
                            if quit in ("y", "n"):
                                if quit == "y":
                                    print("Headed back to the main menu!")
                                    runit = False
                                    loopcheck = False
                                break
                            else:
                                print("Please try again. Only input y or n.\n")
                        count = 0
                else:
                    break
        
        # Try to add friends or give message if they already are
        if runit:
            existingfriend = (f"select * from friendship where user_id = '{userid}' \
                        and friend = '{nfr}'")
            cur.execute(existingfriend)
            alreadyfriends = cur.fetchall()
            if not alreadyfriends:
                addfriend = ("INSERT INTO friendship(user_id, friend) VALUES (?,?)")
                values = [userid, nfr]
                cur.execute(addfriend, values)
                conn.commit()
                print("\nCongrats! You are now friends!")
            else:
                print("You are already friends with them!")

    elif menu == 4:
        ###### WRITE A REVIEW #######
        print("\nYou have selected to review a business!")
        print("Follow the steps to submit a review.\n")
        
        # Ask for business name and loop if necessary
        cnt = 3
        runit2 = True
        loopcheck2 = True
        while loopcheck2:
            selectbusiness = input("Please enter business ID: ")
            selectbusiness = checkapostrophe(selectbusiness)
            checkbus = (f"select * from business where business_id = '{selectbusiness}' collate latin1_general_cs_as")
            cur.execute(checkbus)
            data2 = cur.fetchall()
            
            if not data2:
                cnt = cnt + 1
                print("This business ID does not exist. Please try again. ID is case sensitive.")
                # Give user option to quit to menu if incorrect every 3 times in a row
                if cnt >= 3:
                    if cnt == 4:
                        print("\nYou are given an option to quit to menu. This message will come every 3 times in a row the ID is wrong moving forward.")
                    else:
                        print("\nYou are given an option to quit to menu when getting the ID wrong every 3 times.")
                    while True:
                        quit = input("Would you like to quit to the main menu (y/n): ")
                        if quit in ("y", "n"):
                            if quit == "y":
                                print("Headed back to the main menu!")
                                runit2 = False
                                loopcheck2 = False
                            break
                        else:
                            print("Please try again. Only input y or n.\n")
                    cnt = 0
                print()
            else:
                break

        if runit2:
            # Loop until correct numbers are entered
            while True:
                newstars = input("Enter stars (only integers 1-5): ")
                if newstars in ("1", "2", "3", "4", "5"):
                    newstars = int(newstars)
                    break
                else:
                    print("Please try again. Only select integers from 1 to 5.\n")

            # Loop to generate a review ID until one does not already exist (very unlikely it is ever the same!)
            while True:
                letters = string.ascii_lowercase
                uppletters = string.ascii_uppercase
                dig = string.digits
                revid = ''.join(random.choice(letters + uppletters + dig) for i in range(22))
                checkrevid = (f"select * from review where review_id = '{revid}'")
                cur.execute(checkrevid)
                data3 = cur.fetchall()

                if not data3:
                    break

            # Submit the review as review, user, business, and stars have been selected
            # Don't need to worry about date because review table's default will grab current date by itself
            # Trigger will take care of updating stars and review count for the business
            revbusiness = ("INSERT INTO review(review_id, user_id, business_id, stars) VALUES (?,?,?,?)")
            val = [revid, userid, selectbusiness, newstars]
            cur.execute(revbusiness, val)
            conn.commit()
            print("\nCongrats! Your review has been posted!")

conn.close()
