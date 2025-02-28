import requests 


# FIRST EXERCISE

# MAIN STATEMENT:
#  GET THE TOTAL DRAWS IN A SPECIFIC YEAR OF FOOTBALL MATCHES
def get_total_matches(year:int):
    url = f"https://jsonmock.hackerrank.com/api/football_matches?year={year}"
    try:
        totalDraws = 0
        response = requests.get(url)
        if response.status_code == 200:
            gameGenerals = response.json()
            for i in range(gameGenerals['page'], gameGenerals['total_pages'] + 1):
                pagedUrl = f"https://jsonmock.hackerrank.com/api/football_matches?year={year}&page={i}"
                currentPageGames = requests.get(pagedUrl)
                if currentPageGames.status_code == 200:
                    gameDetails = currentPageGames.json()['data']
                    for game in gameDetails:
                        if game['team1goals'] == game['team2goals']:
                            totalDraws+= 1
            return totalDraws
    except requests.exceptions.RequestException as e:
        print("Error", e)




# SECOND EXERCISE
# MAIN STATEMENT:
# GET THE TOTAL OF GOALS OF A WINNER GIVEN A FOOTBALL COMPETITION AND YEAR
def get_total_winner_goals(year:int, competition):
    competitionsUrl = f"https://jsonmock.hackerrank.com/api/football_competitions?name={competition}&year={year}"
    
    try:
        response = requests.get(competitionsUrl)
        if response.status_code == 200:
            winner_team_name = response.json()['data'][0]['winner']
            print(winner_team_name)
            totalGoalsOfWinner = 0
            homeMatchesUrl = f"https://jsonmock.hackerrank.com/api/football_matches?competition={competition}&year={year}&team1={winner_team_name}"
            awayMatchesUrl = f"https://jsonmock.hackerrank.com/api/football_matches?competition={competition}&year={year}&team2={winner_team_name}"
            
            homeMatchesResponse = requests.get(homeMatchesUrl).json()
            awayMatchesResponse = requests.get(awayMatchesUrl).json()

            # Analyzing first page of both before looping throw pages
            for homeMatch in homeMatchesResponse['data']:
                totalGoalsOfWinner += int(homeMatch['team1goals'])
            for awayMatch in awayMatchesResponse['data']:
                totalGoalsOfWinner += int(awayMatch['team2goals'])
            
            # Since I already checked first page, I can start checking page 2 (if result has more than one)
            totalHomePages = homeMatchesResponse['total_pages']
            totalAwayPages = awayMatchesResponse['total_pages']
            
            # For both away and home matches, same logic applied for the same page

            # Looping throw home matches
            for i in range (2, totalHomePages + 1):
                pagedHomeMatchesUrl = f"https://jsonmock.hackerrank.com/api/football_matches?competition={competition}&year={year}&team1={winner_team_name}&page{i}"
                pagedHomeMatchesResponse = requests.get(pagedHomeMatchesUrl).json()

                for pagedHomeMatch in pagedHomeMatchesResponse['data']:
                    totalGoalsOfWinner += int(pagedHomeMatch['team1goals'])
           
           # Looping throw away matches
            for i in range(2, totalAwayPages + 1):
                pagedAwayMatchesUrl = f"https://jsonmock.hackerrank.com/api/football_matches?competition={competition}&year={year}&team2={winner_team_name}&page={i}"            
                pagedAwayMatchesResponse = requests.get(pagedAwayMatchesUrl).json()

                for pagedAwayMatch in pagedAwayMatchesResponse['data']:
                    totalGoalsOfWinner += int(pagedAwayMatch['team2goals'])
            
        
        return totalGoalsOfWinner

    except requests.exceptions.RequestException as e:
        print("Error", e)
        return None


print(get_total_winner_goals(2011, 'English Premier League'))