import re
from bs4 import BeautifulSoup
import requests
import mysql.connector as mc
from sklearn import tree


def guess_price():
    while True: 
        print('Please enter required information down below.')
        car_brand = input('Brand Name: ').strip().lower()
        car_model = input('Car Model(if there is no specific model just press "Enter"): ').strip().lower()
        car_year = int(input('Manufacture year(ex: 2018): ').strip())
        car_accideent = int(input('Number of accidents(only enter numbers): ').strip())
        car_mileage = int(input('Mileage(ex: 12300): ').strip())
        if car_model: 
            brand = '-'.join(car_brand.split()) # chon betoonim too url bezarim (mercedes benz -> mercedes-benz)
            model = '-'.join(car_model.split()) # # chon betoonim too url bezarim ( c class -> c-class)
            req = requests.get(f'https://www.truecar.com/used-cars-for-sale/listings/{brand}/{model}')
        else:
            brand = '-'.join(car_brand.split())
            req = requests.get(f'https://www.truecar.com/used-cars-for-sale/listings/{brand}') # age model khasi mad nazar nabood hame model haye oon brand ro search mikone

        soup = BeautifulSoup(req.text, 'html.parser')

        name_test = soup.find_all('div', attrs={'class': 'heading-4'}) # age brand ya model eshtebah bashad too site ye error mide va in bakhsh baraye ineke bebinim error mide ya na
        for i in name_test:
            nametest = re.sub(r'\s+', ' ', i.text)
        if 'out' not in nametest:
            break # age error nade az loop kharej mishe mire section ba'adi
        else:
            print('Car brand or car model is incorrect!')
            continue # age brand ya model eshteba bashe error mide va bar migarde aval loop ta dobare esm haro begire
        
    ad_price = soup.find_all('div', attrs={'data-test': 'vehicleCardPricingBlockPrice'})
    ad_mileage = soup.find_all('div', attrs={'data-test': 'vehicleMileage'})
    ad_accident = soup.find_all('div', attrs={'data-test': 'vehicleCardCondition'})
    ad_year = soup.find_all('div', attrs={'data-test': 'vehicleCardYearMakeModel'})

    x = list()
    y = list()
    for i in range(len(ad_price)):
        p = ad_price[i]
        m = ad_mileage[i]
        yr = ad_year[i]
        ac = ad_accident[i]
        price = int(''.join(re.findall(r'([0-9]+)',p.text))) # chon to site beyne adad "," gozashte(12,345), az method join va "()" too regex estefade kardam ta "," ro hazf konam
        mileage = int(''.join(re.findall(r'([0-9]+)',m.text)))
        year = int(re.findall(r'[0-9]{4}',yr.text)[0])
        if ac.text[0] == "N": # to site zade "no accident" va man oon "no" ro be 0 tabdil kardam
            accident = 0
        else:
            accident = int(ac.text[0])
        x.append([mileage, year, accident])
        y.append(price)

    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(x, y)

    awns = clf.predict([[car_mileage, car_year, car_accideent]])
    print(f'Your car is worth about ${awns[0]}.')

def car_price():
    while True: 
        print('Please enter required information down below.')
        car_brand = input('Brand Name: ').strip().lower()
        car_model = input('Car Model(if there is no specific model just press "Enter"): ').strip().lower()
        if car_model: 
            brand = '-'.join(car_brand.split()) # chon betoonim too url bezarim (mercedes benz -> mercedes-benz)
            model = '-'.join(car_model.split()) # # chon betoonim too url bezarim ( c class -> c-class)
            req = requests.get(f'https://www.truecar.com/used-cars-for-sale/listings/{brand}/{model}')
        else:
            brand = '-'.join(car_brand.split())
            req = requests.get(f'https://www.truecar.com/used-cars-for-sale/listings/{brand}') # age model khasi mad nazar nabood hame model haye oon brand ro search mikone

        soup = BeautifulSoup(req.text, 'html.parser')

        name_test = soup.find_all('div', attrs={'class': 'heading-4'}) # age brand ya model eshtebah bashad too site ye error mide va in bakhsh baraye ineke bebinim error mide ya na
        for i in name_test:
            nametest = re.sub(r'\s+', ' ', i.text)
        if 'out' not in nametest:
            break # age error nade az loop kharej mishe mire section ba'adi
        else:
            print('Car brand or car model is incorrect!')
            continue # age brand ya model eshteba bashe error mide va bar migarde aval loop ta dobare esm haro begire
        
    ad_price = soup.find_all('div', attrs={'data-test': 'vehicleCardPricingBlockPrice'})
    ad_mileage = soup.find_all('div', attrs={'data-test': 'vehicleMileage'})
    ad_accident = soup.find_all('div', attrs={'data-test': 'vehicleCardCondition'})
    ad_year = soup.find_all('div', attrs={'data-test': 'vehicleCardYearMakeModel'})

    data = list()
    for i in range(len(ad_price)):
        p = ad_price[i]
        m = ad_mileage[i]
        yr = ad_year[i]
        ac = ad_accident[i]
        price = int(''.join(re.findall(r'([0-9]+)',p.text))) # chon to site beyne adad "," gozashte(12,345), az method join va "()" too regex estefade kardam ta "," ro hazf konam
        mileage = int(''.join(re.findall(r'([0-9]+)',m.text)))
        year = int(re.findall(r'[0-9]{4}',yr.text)[0])
        if ac.text[0] == "N": # to site zade "no accident" va man oon "no" ro be 0 tabdil kardam
            accident = 0
        else:
            accident = int(ac.text[0])
        data.append([price, mileage, year, accident])
    
    print('Data has been collected. Now please enter the database information down below.')
    db_name = input('database: ')
    db_user = input('user: ')
    db_pw = input("password(if there is no password, just press 'Enter'):")

    cnx = mc.connect(user=db_user, password=db_pw, host='127.0.0.1', database=db_name)
    cursor = cnx.cursor()

    while True:
        question = input('Do you want to store data in a new table?("yes" ya "no")(table must have 6 rows): ').lower()
        if question == 'yes':
            question = True # tabdil be boolean mishe ta vaghti az loop in question kharej shodim, ba check kardan True ya False budan anha tasmim begirim
            break
        elif question == 'no':
            question = False
            break
        else : # age user chizi joz 'yes' ya 'no' vared konad, barname ekhtar midahad va dobare soal miporsad
            print('Pleas only enter "yes" or "no".')
            continue
    if question: # age user 'yes' bege, esm table ro az user migirim va ba oon esm yek table jadid dorost mikonim
        db_table = input('Enter name of new table: ')
        cursor.execute(f'CREATE TABLE {db_table} (brand varchar(20) not null, model varchar(20) not null, price varchar(20) not null, mileage varchar(20) not null, year varchar(6) not null, accidents varchar(3) not null)')
        cnx.commit() # "not null"  baraye jologiri az duplicates
    else:
        db_table = input('Enter name of the table: ')

    for item in data:
        cursor.execute(f"INSERT IGNORE INTO {db_table} VALUES ('{car_brand}', '{car_model}', '{item[0]}', '{item[1]}','{item[2]}', '{item[3]}')") # "INSERT IGNORE"  baraye jologiri az duplicates
        cnx.commit()

    print('Data have stored completely')

def find_car():
    min_price = int(input('Minimum price: '))
    max_price = int(input('maximum price: '))

    print('Now please enter the database information down below.')
    db_name = input('database: ')
    db_user = input('user: ')
    db_pw = input("password(if there is no password, just press 'Enter'):")
    
    cnx = mc.connect(user=db_user, password=db_pw, host='127.0.0.1', database=db_name)
    cursor = cnx.cursor()

    while True:
        question = input('Do you want to store data in a new table?("yes" ya "no")(table must have 6 rows): ').lower()
        if question == 'yes':
            question = True # tabdil be boolean mishe ta vaghti az loop in question kharej shodim, ba check kardan True ya False budan anha tasmim begirim
            break
        elif question == 'no':
            question = False
            break
        else : # age user chizi joz 'yes' ya 'no' vared konad, barname ekhtar midahad va dobare soal miporsad
            print('Pleas only enter "yes" or "no".')
            continue
    if question: # age user 'yes' bege, esm table ro az user migirim va ba oon esm yek table jadid dorost mikonim
        db_table = input('Enter name of new table: ')
        cursor.execute(f'CREATE TABLE {db_table} (brand varchar(20) not null, model varchar(20) not null, price varchar(20) not null, mileage varchar(20) not null, year varchar(6) not null, accidents varchar(3) not null)')
        cnx.commit() # "not null"  baraye jologiri az duplicates
    else:
        db_table = input('Enter name of the table: ')

    print('It might take some time to collect data from the actual website! please be patient!')

    data = list()
    for i in range(1, 31):
        req = requests.get(f'https://www.truecar.com/used-cars-for-sale/listings/?page={i}') # ta 30 safhe avalo search mikone
        soup = BeautifulSoup(req.text, 'html.parser')

        ad_price = soup.find_all('div', attrs={'data-test': 'vehicleCardPricingBlockPrice'})
        ad_mileage = soup.find_all('div', attrs={'data-test': 'vehicleMileage'})
        ad_accident = soup.find_all('div', attrs={'data-test': 'vehicleCardCondition'})
        ad_year_brand_model = soup.find_all('div', attrs={'data-test': 'vehicleCardYearMakeModel'})

        for i in range(len(ad_price)):
            p = ad_price[i]
            ma = ad_mileage[i]
            ybm = ad_year_brand_model[i]
            ac = ad_accident[i]

            brand = ybm.text.split()[1]
            model = ' '.join(ybm.text.split()[2:])
            price = int(''.join(re.findall(r'([0-9]+)',p.text))) # chon to site beyne adad "," gozashte(12,345), az method join va "()" too regex estefade kardam ta "," ro hazf konam
            mileage = int(''.join(re.findall(r'([0-9]+)',ma.text)))
            year = int(re.findall(r'[0-9]{4}',ybm.text)[0])
            if ac.text[0] == "N": # to site zade "no accident" va man oon "no" ro be 0 tabdil kardam
                accident = 0
            else:
                accident = int(ac.text[0])

            data.append([brand, model, price, mileage, year, accident])

    for item in data:
        cursor.execute(f"INSERT IGNORE INTO {db_table} VALUES ('{item[0]}', '{item[1]}', '{item[2]}', '{item[3]}','{item[4]}', '{item[5]}')") # "INSERT IGNORE"  baraye jologiri az duplicates
        cnx.commit()

    cursor.execute(f'SELECT * FROM {db_table} WHERE price <= {max_price} AND price >= {min_price}')

    if not cursor:
        print('There is no car in this price range!')
    else:
        print(' brand         | model                | price   | mileage | year | accidents ')
        print('---------------+----------------------+---------+---------+------+-----------')
        for item in cursor:
            print(f' {item[0]:<14}| {item[1]:<21}| ${item[2]:<7}| {item[3]:<8}| {item[4]:<5}| {item[5]}')


while True:
    print('''Please choose a number from the menu below.
    1. Estimate the value of your car
    2. The best prices to buy the car you want
    3. Cars at your desired price
    0. Exit''')
    try:
        user = int(input('>'))
    except ValueError:
        print('Only numbers from 0 to 3 are allowed!!!')
        continue
    
    if user == 1:
        guess_price()
    elif user == 2:
        car_price()
    elif user == 3:
        find_car()
    elif user == 0:
        print('GoodBye!')
        break
    else:
        print('Only numbers from 0 to 3 are allowed!!!')
        continue
