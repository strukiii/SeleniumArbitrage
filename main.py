import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, InvalidSessionIdException, StaleElementReferenceException
import time
from difflib import SequenceMatcher, get_close_matches

#browserPath = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'
browserPath = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
driverPath = 'C:/Program Files (x86)/chromedriver.exe'
ignored_exceptions = (NoSuchElementException,
                      StaleElementReferenceException, InvalidSessionIdException)


remapping = {'Mississippi': 'Ole Miss'}


def check10BetSessionExpired(tenBetDriver):
    try:
        popup = WebDriverWait(tenBetDriver, 2, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="rj-popup-message-root"]/div/sb-resp-popup-portal/sb-resp-popup-content/div[2]/div/div/div[1]')))
        tenBetDriver.refresh()
        return True
    except:
        return False


def login10Bet(tenBetDriver):
    try:
        #print('logging in')
        login = WebDriverWait(tenBetDriver, 2, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="hr-mid-Top_ResponsiveHeader_49672-page-header-right7"]/a')))
        login.click()
        time.sleep(1)
        unInput = WebDriverWait(tenBetDriver, 10, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="Center_LoginResponsiveBlock_51091-responsive-login-name-input"]')))
        unInput.clear()
        unInput.send_keys('omgagopher@gmail.com')
        time.sleep(0.5)
        pwInput = WebDriverWait(tenBetDriver, 10, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="Center_LoginResponsiveBlock_51091-responsive-login-password-input"]')))
        pwInput.clear()
        pwInput.send_keys('Moneyprinter123!@#')
        time.sleep(0.5)
        # rememberMe = tenBetDriver.find_element(
        #    By.XPATH, '//*[@id="html-container-Center_LoginResponsiveBlock_51091"]/div/div/div[7]/div/div[2]/label/div')
        # rememberMe.click()
        time.sleep(0.5)
        loginButton = tenBetDriver.find_element(
            By.XPATH, '//*[@id="Center_LoginResponsiveBlock_51091-submit-button"]')
        loginButton.click()
        time.sleep(3)
    except:
        return
        #print("login failed")


def checkNotBanned10Bet(profileNum, tenBetDriver):
    try:
        banned = WebDriverWait(tenBetDriver, 2, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h1')))
        if (banned.text == 'Access Denied'):
            tenBetDriver.close()
            profileNum = profileNum + 1
            f = open("profilenum.txt", "w")
            f.write(str(profileNum))
            f.close()
            tenBetOptions = uc.ChromeOptions()
            tenBetOptions.add_argument(
                f'--user-data-dir=c:\\temp\\profile{profileNum}')
            tenBetOptions.add_argument(
                '--no-first-run --no-service-autorun --password-store=basic')
            tenBetDriver = uc.Chrome(
                use_subprocess=True, browser_executable_path=browserPath, options=tenBetOptions)
            time.sleep(3)
            tenBetDriver.get('https://www.10bet.com/sports/')
            login10Bet(tenBetDriver)
            print('removed')
            return True
    except Exception as E:
        return False


def loginPinnacle(pinnacleDriver):
    try:
        unInput = WebDriverWait(pinnacleDriver, 2, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[1]/div[1]/div[3]/div[2]/div/div/div[2]/div/div/input')))
        unInput.clear()
        unInput.send_keys('omgagopher@gmail.com')
        time.sleep(0.5)
        pwInput = WebDriverWait(pinnacleDriver, 10, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[1]/div[1]/div[3]/div[2]/div/div/div[3]/div/div/input')))
        pwInput.clear()
        pwInput.send_keys('Desbois1233%')
        time.sleep(0.5)
        loginButton = pinnacleDriver.find_element(
            By.XPATH, '/html/body/div[2]/div/div[1]/div[1]/div[3]/div[2]/div/div/div[4]/button')
        loginButton.click()
        time.sleep(0.5)
        pinnacleDriver.find_element(
            By.XPATH, '/html/body/div[3]/div/div/div[1]').click()
    except Exception as E:
        # print(E)
        return


def getArbitrageInfo(currEle):
    betDict = {}
    spans = currEle.find_elements(By.TAG_NAME, 'span')
    oddsDiv = currEle.find_element(
        By.XPATH, '//*[@id="kt_content"]/div[2]/div/div/div/div/div[2]/div/div/table/tbody/tr/td[6]/span')
    oddsDivs = oddsDiv.find_elements(By.TAG_NAME, 'div')
    betDict['profit'] = spans[2].text
    betDict['time'] = spans[3].text
    betDict['name'] = spans[4].text

    for i in range(2):
        booksArr = []
        odds = oddsDivs[i].find_element(By.TAG_NAME, 'span').text
        books = oddsDivs[i].find_elements(By.TAG_NAME, 'img')
        for book in books:
            booksArr.append(book.get_attribute('alt'))
        betDict[f'book{i}'] = booksArr
        betDict[f'odds{i}'] = odds

    #betDict['odds1'] = spans[5].text.split('\n')[1]
    #betDict['odds2'] = spans[6].text
    betDict['betType'] = spans[8].text

    return betDict


def initBets(profileNum, currBets, prevBets, tenBetDriver, pinnacleDriver):
    currBets.sort(key=lambda x: x['profit'], reverse=True)

    for bet in currBets:
        bet['profit'] = bet['profit'].split('%')[0]

        login10Bet(tenBetDriver)
        loginPinnacle(pinnacleDriver)
        checkNotBanned10Bet(profileNum, tenBetDriver)
        if (check10BetSessionExpired(tenBetDriver)):
            time.sleep(5)

        if (bet not in prevBets and float(bet['profit']) > 0):
            searchInputs = [bet['name'].split('vs')[0].split(
            )[-1], bet['name'].split('vs')[-1].split()[-1]]
            fullTeams = [bet['name'].split(
                'vs')[0], bet['name'].split('vs')[1]]

            print(bet)
            print()
            findBets(searchInputs, fullTeams, tenBetDriver, pinnacleDriver)
            placeBets(fullTeams, bet, tenBetDriver, pinnacleDriver)
            #placeBets(fullTeams, bet, tenBetDriver, pinnacleDriver)
            # if ('OddsJam' in bet['book0'] and '10bet' in bet['book1']):

            # elif ('10bet' in bet['book0'] and 'OddsJam' in bet['book1']):
            #    findBets(searchInputs, fullTeams, tenBetDriver, pinnacleDriver)
            #    placeBets(fullTeams, bet, tenBetDriver,
            #              pinnacleDriver, bet['odds0'])
            '''
            if (bet['book1'] == 'OddsJam'):
                searchBar = WebDriverWait(pinnacleDriver, 1, ignored_exceptions=ignored_exceptions).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="search"]')))
                print(searchBar)
                searchBar.send_keys(searchInput)
                print('sent keys:' + searchInput)
                searchBar.submit()
                time.sleep(0.1)
                pinnacleDriver.get('https://www.pinnacle.com/en/')
            else:
            '''


def init(profileNum, oddsJamOptions, tenBetOptions, pinnacleOptions):
    oddsJamOptions.add_argument('--user-data-dir=c:\\temp\\profile2')
    oddsJamOptions.add_argument(
        '--no-first-run --no-service-autorun --password-store=basic')
    tenBetOptions.add_argument(
        f'--user-data-dir=c:\\temp\\profile{profileNum}')
    tenBetOptions.add_argument(
        '--no-first-run --no-service-autorun --password-store=basic')
    pinnacleOptions.add_argument('--user-data-dir=c:\\temp\\profile4')
    pinnacleOptions.add_argument(
        '--no-first-run --no-service-autorun --password-store=basic')


def placePinnacleBet(searchInputs, fullTeams, pinnacleDriver):
    # time.sleep(120)
    WebDriverWait(pinnacleDriver, 10, ignored_exceptions=ignored_exceptions).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/main/div/div[3]/div/div/div[3]')))
    results = pinnacleDriver.find_elements(
        By.CSS_SELECTOR, '#root > div > div.style_container__3Xbio > main > div > div:nth-child(3) > div > div > div.style_row__1G55Y.style_lastRow__2l3ez')

    for result in results:
        team1 = result.find_element(
            By.CSS_SELECTOR, '#root > div > div.style_container__3Xbio > main > div > div:nth-child(3) > div > div > div.style_row__1G55Y.style_lastRow__2l3ez > div.style_col__1tqq-.style_colGame__1xrUv.overflow-visible > a > div.style_participants__fQV9D > div:nth-child(1) > span').text
        team2 = result.find_element(
            By.CSS_SELECTOR, '#root > div > div.style_container__3Xbio > main > div > div:nth-child(3) > div > div > div.style_row__1G55Y.style_lastRow__2l3ez > div.style_col__1tqq-.style_colGame__1xrUv.overflow-visible > a > div.style_participants__fQV9D > div:nth-child(2) > span').text
        if ((team1 in fullTeams[0] or team2 in fullTeams[0]) and (team1 in fullTeams[1] or team2 in fullTeams[1])):
            print(team1)
            print(team2)
            result.click()
            # time.sleep(3)
            allButton = WebDriverWait(pinnacleDriver, 10, ignored_exceptions=ignored_exceptions).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[2]/main/div[2]/div/div/div/button[1]')))
            allButton.click()
            # time.sleep(120)
            break


def findBets(searchInputs, fullTeams, tenBetDriver, pinnacleDriver):
    searchBar10Bet = WebDriverWait(tenBetDriver, 4, ignored_exceptions=ignored_exceptions).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="rj-bet-search-field"]')))
    searchBarPinnacle = WebDriverWait(pinnacleDriver, 4, ignored_exceptions=ignored_exceptions).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="search"]')))
    time.sleep(1)
    searchBarPinnacle.clear()
    searchBarPinnacle.send_keys(searchInputs[1])
    searchBarPinnacle.submit()

    found10Bet = False

    searchBar10Bet.send_keys(searchInputs[1])
    searchResultsContainer10Bet = WebDriverWait(tenBetDriver, 10, ignored_exceptions=ignored_exceptions).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="Left_BetSearchReactBlock_70734"]/sb-comp/div/div[2]/div')))
    time.sleep(1)

    searchResultsContainerPinnacle = WebDriverWait(pinnacleDriver, 10, ignored_exceptions=ignored_exceptions).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/main/div/div[2]/ul')))
    resultsDivsPinnacle = searchResultsContainerPinnacle.find_elements(
        By.CLASS_NAME, "style_listItem__pMz0S")

    searchResultsTeam1 = searchResultsContainer10Bet.find_elements(
        By.CLASS_NAME, "rj-bet-search__team-one")
    searchResultsTeam2 = searchResultsContainer10Bet.find_elements(
        By.CLASS_NAME, "rj-bet-search__team-two")

    for i in range(len(searchResultsTeam1)):
        team1 = searchResultsTeam1[i].text
        team2 = searchResultsTeam2[i].text

        if ((searchInputs[0] in team1 and searchInputs[1] in team2) or (searchInputs[0] in team2 and searchInputs[1] in team1)):
            parent = searchResultsTeam1[i].find_element(By.XPATH, '..')
            time.sleep(1)
            parent.click()
            found10Bet = True
            break

    if (not found10Bet):
        searchBar10Bet.clear()
        searchBar10Bet.send_keys(searchInputs[0])
        searchResultsContainer10Bet = WebDriverWait(tenBetDriver, 10, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="Left_BetSearchReactBlock_70734"]/sb-comp/div/div[2]/div')))
        time.sleep(1)

        searchResultsContainerPinnacle = WebDriverWait(pinnacleDriver, 10, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/main/div/div[2]/ul')))
        resultsDivsPinnacle = searchResultsContainerPinnacle.find_elements(
            By.CLASS_NAME, "style_listItem__pMz0S")

        searchResultsTeam1 = searchResultsContainer10Bet.find_elements(
            By.CLASS_NAME, "rj-bet-search__team-one")
        searchResultsTeam2 = searchResultsContainer10Bet.find_elements(
            By.CLASS_NAME, "rj-bet-search__team-two")

        for i in range(len(searchResultsTeam1)):
            team1 = searchResultsTeam1[i].text
            team2 = searchResultsTeam2[i].text

            if ((searchInputs[0] in team1 and searchInputs[1] in team2) or (searchInputs[0] in team2 and searchInputs[1] in team1)):
                parent = searchResultsTeam1[i].find_element(By.XPATH, '..')
                time.sleep(1)
                parent.click()
                found10Bet = True
                break

    foundPinn = False

    for i in range(len(resultsDivsPinnacle)):
        resultText = resultsDivsPinnacle[i].find_element(
            By.CSS_SELECTOR, 'span').text

        if (resultText in fullTeams[1]):
            # time.sleep(120)
            toClick = resultsDivsPinnacle[i].find_element(
                By.CSS_SELECTOR, 'a')
            time.sleep(0.5)
            toClick.click()
            time.sleep(0.5)
            foundPinn = True
            #placePinnacleBet(searchInputs, fullTeams, pinnacleDriver)
            break

    if (not foundPinn):
        searchBarPinnacle.clear()
        searchBarPinnacle.send_keys(searchInputs[0])
        searchBarPinnacle.submit()
        searchResultsContainerPinnacle = WebDriverWait(pinnacleDriver, 10, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/main/div/div[2]/ul')))
        resultsDivsPinnacle = searchResultsContainerPinnacle.find_elements(
            By.CLASS_NAME, "style_listItem__pMz0S")

        for i in range(len(resultsDivsPinnacle)):
            resultText = resultsDivsPinnacle[i].find_element(
                By.CSS_SELECTOR, 'span').text

            if (resultText in fullTeams[0]):
                toClick = resultsDivsPinnacle[i].find_element(
                    By.CSS_SELECTOR, 'a')
                time.sleep(0.5)
                toClick.click()
                time.sleep(0.5)
                foundPinn = True
                #placePinnacleBet(searchInputs, fullTeams, pinnacleDriver)
                break

    # time.sleep(1)
    # pinnacleDriver.get('https://www.pinnacle.com/en/')
    # tenBetDriver.get('https://www.10bet.com/sports/')


def placeBets(fullTeams, bet, tenBetDriver, pinnacleDriver):
    # time.sleep(6969)
    tenUls = WebDriverWait(tenBetDriver, 10, ignored_exceptions=ignored_exceptions).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#event-view-Center_EventViewResponsiveBlock_49766 > ul')))
    strippedBetName = bet['betType'].translate(str.maketrans('', '', '(),'))
    #strippedBetNameList = strippedBetName.split()
    marketsSimilarScores = {}
    closest = 0

    tenMarkets = []
    for _ in range(len(tenUls)):
        localLis = WebDriverWait(tenBetDriver, 10, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#event-view-Center_EventViewResponsiveBlock_49766 > ul li')))
        for li in localLis:
            tenMarkets.append(li)

    for i in range(len(tenMarkets)):
        try:
            marketType = tenMarkets[i].find_element(
                By.CLASS_NAME, 'toggleableHeadline-text').text

            s = SequenceMatcher(a=marketType, b=strippedBetName).ratio()
            # for word in strippedBetNameList:
            #    if word in marketType:
            #        wordsSimilar += 1
            # time.sleep(6969)

            if (s >= closest):
                eventButtons = tenMarkets[i].find_elements(
                    By.TAG_NAME, 'button')
                if (len(eventButtons) == 0):
                    tenMarkets[i].click()
                    eventButtons = tenMarkets[i].find_elements(
                        By.TAG_NAME, 'button')

                buttonDescriptions = {}
                for j in range(len(eventButtons)):
                    buttonDescription = []
                    buttonDescription.append(eventButtons[j].find_element(
                        By.CSS_SELECTOR, '.bet-button-title.bet-title-team-name').text)
                    buttonDescription.append(eventButtons[j].find_element(
                        By.CSS_SELECTOR, '.bet-button-title.bet-title-hcap-points').text)
                    buttonDescription.append(eventButtons[j].find_element(
                        By.CSS_SELECTOR, '.bet-odds-number').text)
                    buttonDescriptions[f'{j}'] = ' '.join(buttonDescription)

                marketsSimilarScores[f'{i}'] = {
                    'wordsSimilar': s, 'marketType': marketType, 'description': buttonDescriptions}
                closest = s

        except Exception as E:
            # print(E)
            #print('place bets failed')
            pass
    #market = get_close_matches(bet['betType'], marketsText)
    # print(market)
    # print(marketsText)
    #candidateEvents = []

    # for tup in marketsSimilarScores:
    #    if tup[wordsSimilar] == closest:
    #        candidateEvents.append(tup['marketType'])

    # print()

    # Go through the buttons, if the odds are in here thats our pick

    for index in marketsSimilarScores:
        # print(marketsSimilarScores[index]['marketType'])
        # print(marketsSimilarScores[index]['wordsSimilar'])
        print(marketsSimilarScores[index])
        '''
        for button in marketsSimilarScores[index]['description']:
            # print(oddsTenBet)
            # print(button)
            # print(marketsSimilarScores[index]['description'][button])
            if oddsTenBet in marketsSimilarScores[index]['description'][button]:
                print("WINNER GAGNOT")
                print(marketsSimilarScores[index]['description'][button])
                print(marketsSimilarScores[index]['marketType'])
    '''

    #
    print('done')
    tenBetDriver.get('https://www.10bet.com/sports/')
    return


def main():
    prevBets = []
    currBets = []

    # Biiiiig band aid
    f = open("profilenum.txt", "r")
    profileNum = int(f.read())
    f.close()

    oddsJamOptions = uc.ChromeOptions()
    tenBetOptions = uc.ChromeOptions()
    pinnacleOptions = uc.ChromeOptions()
    init(profileNum, oddsJamOptions, tenBetOptions, pinnacleOptions)

    oddsJamDriver = uc.Chrome(
        use_subprocess=True, browser_executable_path=browserPath, options=oddsJamOptions)
    oddsJamDriver.get('https://oddsjam.com/arbitrage')
    print('\n' + oddsJamDriver.current_url + '\n')

    tenBetDriver = uc.Chrome(
        use_subprocess=True, browser_executable_path=browserPath, options=tenBetOptions)
    tenBetDriver.get('https://www.10bet.com/sports/')
    print('\n' + tenBetDriver.current_url + '\n')

    pinnacleDriver = uc.Chrome(
        use_subprocess=True, browser_executable_path=browserPath, options=pinnacleOptions)
    pinnacleDriver.get('https://www.pinnacle.com/en/')
    print('\n' + pinnacleDriver.current_url + '\n')

    while 1:
        # time.sleep(1)

        currBets = []
        flag = True
        try:
            elements = WebDriverWait(oddsJamDriver, 10, ignored_exceptions=ignored_exceptions).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr')))
        except Exception as E:
            print(E)
            print('wait failed')
            continue

        for webElement in elements:
            try:
                bet = getArbitrageInfo(webElement)
                currBets.append(bet)
            except Exception as E:
                flag = False
                # print(E)
                #print('scraping oddsjam failed')
                continue

        initBets(profileNum, currBets, prevBets, tenBetDriver, pinnacleDriver)

        if (flag):
            for bet in currBets:
                prevBets.append(bet)

        time.sleep(5)
        oddsJamDriver.get('https://oddsjam.com/arbitrage')

    time.sleep(100)


if __name__ == "__main__":
    main()
