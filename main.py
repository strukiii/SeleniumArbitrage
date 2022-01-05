import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, InvalidSessionIdException, StaleElementReferenceException
import time


bravePath = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'
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
        pwInput.send_keys('Doggy123!@#')
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
        banned = WebDriverWait(tenBetDriver, 4, ignored_exceptions=ignored_exceptions).until(
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
                use_subprocess=True, browser_executable_path=bravePath, options=tenBetOptions)

            tenBetDriver.get('https://www.10bet.com/sports/')
            print('removed')
            return True
    except Exception as E:
        print(E)
        return False


def loginPinnacle(pinnacleDriver):
    try:
        unInput = WebDriverWait(pinnacleDriver, 3, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="username"]')))
        unInput.clear()
        unInput.send_keys('omgagopher@gmail.com')
        time.sleep(0.5)
        pwInput = WebDriverWait(pinnacleDriver, 10, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
        pwInput.clear()
        pwInput.send_keys('Desbois1233%')
        time.sleep(0.5)
        loginButton = pinnacleDriver.find_element(
            By.XPATH, '//*[@id="root"]/div/div[1]/div[1]/div[3]/div[2]/div/div/div[4]/button')
        loginButton.click()
    except Exception as E:
        print(E)
        return


def getArbitrageInfo(currEle):
    spans = currEle.find_elements(By.TAG_NAME, 'span')
    imgs = currEle.find_elements(By.TAG_NAME, 'img')
    return {
        'profit': spans[2].text,
        'time': spans[3].text,
        'name': spans[4].text,
        'odds1': spans[5].text.split('\n')[1],
        'odds2': spans[6].text,
        'betType': spans[8].text,
        'book2': imgs[0].get_attribute('alt'),
        'book1': imgs[1].get_attribute('alt'),
    }


def placeBets(currBets, prevBets, tenBetDriver, pinnacleDriver):
    currBets.sort(key=lambda x: x['profit'], reverse=True)

    for bet in currBets:
        bet['profit'] = bet['profit'].split('%')[0]

        if (bet not in prevBets and float(bet['profit']) > 0):
            print(bet)
            searchInputs = [bet['name'].split('vs')[0].split(
            )[-1], bet['name'].split('vs')[-1].split()[-1]]
            fullTeams = [bet['name'].split(
                'vs')[0], bet['name'].split('vs')[1]]
            #placeTenBet(searchInputs, tenBetDriver)
            #placePinnacleBet(searchInputs, fullTeams, pinnacleDriver)
            placeBoth(searchInputs, fullTeams, tenBetDriver, pinnacleDriver)
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
    searchBar = WebDriverWait(pinnacleDriver, 4, ignored_exceptions=ignored_exceptions).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="search"]')))
    searchBar.clear()
    searchBar.send_keys(searchInputs[1])
    searchBar.submit()
    searchResultsContainer = WebDriverWait(pinnacleDriver, 10, ignored_exceptions=ignored_exceptions).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/main/div/div[2]/ul')))
    resultsDivs = searchResultsContainer.find_elements(
        By.CLASS_NAME, "style_listItem__pMz0S")

    found = False

    for i in range(len(resultsDivs)):
        resultText = resultsDivs[i].find_element(By.CSS_SELECTOR, 'span').text

        if (resultText in fullTeams[1]):
            # time.sleep(120)
            toClick = resultsDivs[i].find_element(
                By.CSS_SELECTOR, 'a')
            time.sleep(0.5)
            toClick.click()
            time.sleep(2)
            found = True
            break

    if (not found):
        searchBar.clear()
        searchBar.send_keys(searchInputs[0])
        searchBar.submit()
        searchResultsContainer = WebDriverWait(pinnacleDriver, 10, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/main/div/div[2]/ul')))
        resultsDivs = searchResultsContainer.find_elements(
            By.CLASS_NAME, "style_listItem__pMz0S")

        for i in range(len(resultsDivs)):
            resultText = resultsDivs[i].find_element(
                By.CSS_SELECTOR, 'span').text

            if (resultText in fullTeams[0]):
                toClick = resultsDivs[i].find_element(
                    By.CSS_SELECTOR, 'a')
                time.sleep(0.5)
                toClick.click()
                time.sleep(2)
                found = True
                break
    pinnacleDriver.get('https://www.pinnacle.com/en/')
    time.sleep(3)


def placeBoth(searchInputs, fullTeams, tenBetDriver, pinnacleDriver):
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
            time.sleep(2)
            foundPinn = True
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
                time.sleep(2)
                foundPinn = True
                break

    time.sleep(1)
    pinnacleDriver.get('https://www.pinnacle.com/en/')
    tenBetDriver.get('https://www.10bet.com/sports/')


def placeTenBet(searchInputs, tenBetDriver):
    searchBar = WebDriverWait(tenBetDriver, 4, ignored_exceptions=ignored_exceptions).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="rj-bet-search-field"]')))
    time.sleep(1)
    searchBar.send_keys(searchInputs[1])
    searchResultsContainer = WebDriverWait(tenBetDriver, 10, ignored_exceptions=ignored_exceptions).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="Left_BetSearchReactBlock_70734"]/sb-comp/div/div[2]/div')))
    time.sleep(1)
    searchResultsTeam1 = searchResultsContainer.find_elements(
        By.CLASS_NAME, "rj-bet-search__team-one")
    searchResultsTeam2 = searchResultsContainer.find_elements(
        By.CLASS_NAME, "rj-bet-search__team-two")

    for i in range(len(searchResultsTeam1)):
        team1 = searchResultsTeam1[i].text
        team2 = searchResultsTeam2[i].text

        if ((searchInputs[0] in team1 and searchInputs[1] in team2) or (searchInputs[0] in team2 and searchInputs[1] in team1)):
            parent = searchResultsTeam1[i].find_element(By.XPATH, '..')
            time.sleep(1)
            parent.click()
            break

    time.sleep(3)
    tenBetDriver.get('https://www.10bet.com/sports/')


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
        use_subprocess=True, browser_executable_path=bravePath, options=oddsJamOptions)
    oddsJamDriver.get('https://oddsjam.com/arbitrage')
    print('\n' + oddsJamDriver.current_url + '\n')

    tenBetDriver = uc.Chrome(
        use_subprocess=True, browser_executable_path=bravePath, options=tenBetOptions)
    tenBetDriver.get('https://www.10bet.com/sports/')
    print('\n' + tenBetDriver.current_url + '\n')

    pinnacleDriver = uc.Chrome(
        use_subprocess=True, browser_executable_path=bravePath, options=pinnacleOptions)
    pinnacleDriver.get('https://www.pinnacle.com/en/')
    print('\n' + pinnacleDriver.current_url + '\n')

    while 1:
        time.sleep(1)

        checkNotBanned10Bet(profileNum, tenBetDriver)
        if (check10BetSessionExpired(tenBetDriver)):
            time.sleep(5)

        login10Bet(tenBetDriver)
        currBets = []
        flag = True
        try:
            threadBody = WebDriverWait(oddsJamDriver, 10, ignored_exceptions=ignored_exceptions).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="kt_content"]/div[2]/div/div/div/div/div[2]/div/div/table/tbody')))
        except Exception as E:
            print(E)
            print('wait failed')
            continue

        elements = threadBody.find_elements(By.TAG_NAME, 'tr')
        for webElement in elements:
            try:
                bet = getArbitrageInfo(webElement)
                currBets.append(bet)
            except Exception as E:
                flag = False
                # print(E)
                continue

        placeBets(currBets, prevBets, tenBetDriver, pinnacleDriver)

        if (flag):
            prevBets = currBets

        time.sleep(5)
        oddsJamDriver.refresh()

    time.sleep(100)


if __name__ == "__main__":
    main()
