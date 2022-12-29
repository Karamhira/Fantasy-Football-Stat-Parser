from urllib.request import urlopen
import pandas
from bs4 import BeautifulSoup


def fantasy_football():
    #Introduction
    print("\nWelcome to the NFL fantasy stats finder\nThis program will help you build the best possible fantasy team!!!")
    print("\nYou will have to answer a few questions and will get the Data in a Csv organized based on headers and the preffered order")

    #Getting the year that the user wants data from and  
    while True:
        year = str(input(
            "\nPlease enter what years stats you would like to see (Between 1990 and 2022)\nin the following format yyyy\n"))
        try: #Making sure the input given by user is a year, using try and except    
            if int(year) >= 1990 and int(year) <=2020:
                break 
            else:
                print('\nInvalid input, only years between 1990 and 2022')
        except : 
            print("\nPlease enter a valid input")
            
    #Manipulating the url based on the given year and will 
    url = f'https://www.pro-football-reference.com/years/{year}/fantasy.htm' 
    open = urlopen(url)
    soup = BeautifulSoup(open, features="html.parser")

    #Gathering all the headers of the table in the page
    #The for loops finds every table header column in the second row 
    # where the headers are located and extracts the html text using the 
    # get_text and using the .upper() method they are put into upercase
    headers = []
    for x in soup.findAll('tr')[1].findAll('th'):
        headers.append(x.getText().upper())
    headers = headers[1:]
    
    #Td, Att and Yds are three columns that are repeated in 2- 3 different
    #sub categories, using enumerate and for loop to find the the indexs of these columns
    # and add the appropriate subheading 
    td = [i for i, n in enumerate(headers) if n == 'TD']

    categories = ['P-', 'RE-', 'RU-', 'S-']
    
    for i in range(len(td)):
        headers[td[i]] = categories[i] + 'TD'

    Att = [i for i, n in enumerate(headers) if n == 'ATT']

    for i in range(len(Att)):
        headers[Att[i]] = categories[i]+'ATT'

    Yds = [i for i, n in enumerate(headers) if n == 'YDS']

    for i in range(len(Yds)):
        headers[Yds[i]] = categories[i]+'YDS'

    #Gathering all the rows  that are not classed as header rows
    rows = []
    # Find all table rows (tr) in the BeautifulSoup object
    # If the table row does not have a 'class' attribute or if 'thead' 
    # is not in the class attribute, it is appended to a list of rows
    for tr in soup.find_all('tr'):
        if tr.has_attr('class') == False or 'thead' not in tr['class']:
            rows.append(tr)
    
    #List of player stats
    player_stats = []
    
    
    for i in range(len(rows)):
        temp_row = []  # Empty list to store the player stats for a single row
        #For all the table cells (td) in the current row if, if the cell has 
        #text it is added to the list of player stats for the current row
        #else ("-") is appended to represent no information collected
        #Finally the temp player stat row is added to the plater_stats.
        for x in rows[i].findAll('td'):
            if x.getText() != '':
                temp_row.append(x.getText())
            else:
                temp_row.append('-')
        player_stats.append(temp_row)
    player_stats = player_stats[2::]

    #Creating pandas DataFrame object
    stats = pandas.DataFrame(player_stats, columns=headers)

    
    print("---------------------------")
    print('Data collected succesfully')
    print("---------------------------")
    
    #asking user if they want all the data or they want to filter
    while True:
        whole_data = input(
            "Would you like to filter the collected data or see all, enter filter/all\n")
        if whole_data.lower() == 'filter' or whole_data.lower() == 'all':
            break
        else:
            print("Invalid input: Please try again")
            
    if whole_data.lower() == 'all':
        stats.to_csv("all_stats.csv")
        return (f"File created as {'all_stats.csv'}")

    else:
        
        filter = True
        
        #For these the filters they will be applied at end once all user inputs are entered as doing them as we go can cause overlapps
        #Empty lists to store all the filters entered
        teams = []
        a_d = []
        positions=[]
        min_max=[]
        list_of_teams = []
        
        #creating list of teams for user to see later
        for i in stats['TM']:
            if i not in list_of_teams:
                list_of_teams.append(i)
        
        while filter:
            #List of commands
            print("\nWhich of the following options would you like, can mix them together, but only one filter at a time.")
            print("1. Filter by positions")
            print("2. Filter by a certain stat / Assending and desending order")
            print("3. Set filter minimums and maximums")
            print("4. Filter by a Team")
            print("5. End")
            option = input("\nEnter corresponding number: ")
            
            try:
                option = int(option)
            except :
                filter = True   
            
            if option == 5:
                filter = False
                break 
            
            # Positions -> Enter positions user wants in stats
            elif option == 1:
                end = False
                while not end: 
                    position = input("\nWhat position would you like filter out, Please only add one at a time\nFollowing options: QB, RB, TE, WR\n")
                    #check if input is valid else user can re-enter their input
                    if type(position) != str or  position.upper() not in ['QB', 'RB', 'TE', 'WR']:
                        print ('Invalid input please try again')
                        end = False
                    
                    else: 
                        positions.append(position.upper())
                        addmore = input("\nWould you like to add another Position y/n: ") #option to add more positions
                        if addmore.lower() == 'y':
                            end = False 
                        else:
                            end = True
                            break
            
            #sorting the rows by ordering a column given by user
            elif option == 2:
                #while loop that keeps running till user givers a valid input
                while True:
                    stat = input(f'\nWhat stat would u like to sort in assending or desending order\nOptions include{headers[1::]}\n')
                    
                    if stat.upper() in headers: #checkingg if valid
                        while True: #Another loop for this value so user does not have to re-enter previous value if they mess up this input
                            sort = input('\nAssending or Desending a/d: ')
                            if sort.lower() =='a' or sort.lower()=='d':
                                a_d =[stat.upper(), sort.lower()]#first element is the stat and second represents Asending or Desending.
                                break
                            else:
                                print("\nInvalid input please try again")
                        break
                    else:
                        print("\nInvalid input please try again")
            
            # Min/Max -> setting limits on columns 
            elif option == 3:
                opinion = False
                
                while not opinion:
	                #While loops for valid inputs 
                    while True:
                            stat = input(
                                f'\nWhat stat would u like to add the max/min too \nOptions include the following\n{headers[2::]}\n')
                            if stat.upper() in headers:
                                while True:
                                    limit = input(
                                        '\nIs this a max or min, enter max/min: ')
                                    if limit.lower() == 'max' or limit.lower() == 'min':
                                        break
                                    else:
                                        print('\nInvalid input')
                                sort = input('\nWhat is the min/max: ')
                                #appening a list, where the first element is the stat, second whether it is a max/min and third the condition
                                min_max. append( [stat.upper(), limit.lower(), sort] )
                                
                                break
                            
                            else:
                                print('\nInvalid input')
                    #asking if the user wants to add another  min/max filter
                    ask = input("\nWould you like to add another filter, y/n: ")
                    
                    if ask.lower() != 'y':
                        break
                    else : opinion = False
            #teams -> display players from certain teams 
            elif option ==4:
                while True:
                    #formated innput string so the list of teams created above can me displayed
                    team = input(
                        f"\nWhat team would you like to add to filters, Please enter a team as shown in the list \n\n{list_of_teams}\n")
                    
                    if team.upper() in list_of_teams:
                        teams.append(team.upper())
                        ask = input('Would you like to add another team? y/n: ')
                        if ask == 'y':
                            True
                        else:
                            break
                    else:
                        print('Invalid team please try again!!!')    
            #incase number is not between 1 and 5
            elif option < 1 or option > 5:
                print("Please only enter numbers between 1 and 5") 
        
        #no filter applied even after selecting filter mode
        if len(teams) == 0 and len(positions)==0 and len(min_max) ==0 and len(a_d)==0:
            return stats

        #Filtering the teams 
        if len(teams) == 0:#no teams in the list, display all teams
            stats = stats
        elif len(teams) >= 1:
            stats = stats[stats['TM'].isin(teams)]#Only keeps the rows which have a team in the list of filtered teams 
        
        #Positions
        if len(positions) == 0:  # no positions in the list, display all positions
            stats = stats
        elif len(positions) >= 1: 
            stats = stats[stats['FANTPOS'].isin(positions)]#only keeps the rows which have a team in the list of filtered positions 
        
        #min/max
        for ele in min_max: #runs for every nested list in min_max 
            if ele[1].lower() == 'max': #Checking if condtion is max if yes, only keeping rows that have stats below the max
                stats = stats[stats[ele[0]] <= ele[2]]
            else:
                stats = stats[stats[ele[0]] >= ele[2]]#Only keeping rows that have the stat higher than min
        
        #sort
        if len(a_d) == 2: 
            if a_d[1].lower() == 'd':#if second element is d then sorted in desending order
                stats = stats.sort_values(a_d[0], ascending=False)
            elif a_d[1].lower() == 'a':
                stats = stats.sort_values(a_d[0])#else decreasing
    
    #Creating filtered csv file and printing end remarks 
    print("\n-------------------------")
    print("Done filtering the data")
    stats.to_csv("filtered_stats.csv")
    print("-------------------------")
    return (f"File created as {'filtered_stats.csv'}")

print(fantasy_football())