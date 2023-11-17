# --- Importing libraries ---
import pandas as pd
from faker import Faker
import random
import os
from datetime import datetime, timedelta
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, ForeignKey
random.seed(42)

# Generator various DataFrames
def generator_main_dfs(num_cities: int,                    
                       num_companies: int,                 
                       max_clients_num_one_company: int,    
                       max_contracts_num_one_client: int,   
                       num_managers: int,                 
                       years: int,                        
                       max_day_delta_start_date: int,      
                       min_work_duration: int,              
                       max_work_duration: int,              
                       max_day_delta_paying: int            
                       ) -> tuple:           
    
    """
    Generates various DataFrames for companies, customers, services, contracts and managers.

    Arguments:
    - num_cities (int): Number of customer cities.
    - num_companies (int): The number of companies of the clients.
    - max_clients_num_one_company (int): Maximum number of clients from one company.
    - max_contracts_num_one_client (int): Maximum number of contracts for one client.
    - num_managers (int): The number of managers from the consulting agency.
    - years (int): The length of time the consulting agency has been in operation in years.
    - max_day_delta_start_date (int): The maximum difference in days between the signing of the contract and the start of the action.
    - min_work_duration (int): Minimum work duration in days (time difference between start and end).
    - max_work_duration (int): Maximum work duration in days (time difference between start and end).
    - max_day_delta_paying (int): Maximum difference in days between the end of the job and the payment date.

    Returns a tuple of DataFrames for companies, clients, services, contracts, and managers.
    """

    # --- Generating list of clients' cities ---
    fake = Faker('en_GB')
    available_cities = []
    for _ in range(num_cities):
        city = fake.city()
        available_cities.append(city)

    # --- Main Paths ---
    script_directory = os.path.dirname(os.path.abspath(__file__)) # Script path
    data_directory = os.path.join(os.path.dirname(script_directory), "data")    # data folder path
    gen_data_directory = os.path.join(os.path.dirname(script_directory), "generated_data")  # generated_data folder path



    # --- Generating company DataFrame
    df_company = pd.read_csv(data_directory+'\AllCompanyNames.csv', encoding='cp1251')
    df_sampled = df_company.sample(n=num_companies) #.rename(columns={'CompanyName': 'Company'})   # Choice cities with current amount
    df_n_rows = df_sampled.shape[0]



    # Creating result DataFrame of companies
    df_company = df_sampled  # pd.concat([df_sampled['CompanyName'], df_adress_city)], axis=1).rename(columns={'CompanyName': 'Company'}).reset_index()
    df_company['CompanyID'] = range(1, len(df_company) + 1)
    df_company=df_company.drop(columns=["IncorporationDate","SIC"], axis=1)
    df_company = df_company[['CompanyID', 'CompanyName']].reset_index(drop=True)
    # Saving companies DF to .csv file in generated_data folder
    df_company.to_csv(gen_data_directory + '\company.csv')



    # --- Generating 1st part of clients DataFrame
    # Repetition of company lines for several clients from one company
    indices = []
    df_clients = df_company
    for i, row in df_company.iterrows():
        indices.extend([i] * random.randint(1, max_clients_num_one_company))  # Repeat the line index 
    # Retrieve rows by indices
    df_clients = df_clients.loc[indices].reset_index(drop=True).sort_values(by='CompanyName')
    num_clients = len(df_clients)   # Number of clients

    num_people = num_clients + num_managers

    # --- Generating array of full names for clients and managers ---
    # Read lines from a file and save them into an array
    with open(data_directory + '\\' + 'surname.txt', 'r', encoding='utf-8') as file:
        surnames_array = file.readlines()
    with open(data_directory + '\\' + 'name.txt', 'r', encoding='utf-8') as file:
        names_array = file.readlines()

    # Defining array dimensions
    names_array_len = len(names_array)
    surnames_array_len = len(surnames_array)

    full_names=set() # Ensures the uniqueness of the name
    while len(full_names) < num_people:
        # Selecting a random first and last name + removing unnecessary characters
        name = names_array[random.randint(0, names_array_len-1)].strip()
        surname = surnames_array[random.randint(0, surnames_array_len-1)].strip()
        full_names.add(name + ' ' + surname)
    full_names = list(full_names)

    # --- Generating array of phone numbers for clients and managers ---
    phone_numbers = set()
    while len(phone_numbers) < num_people: # Ensures the uniqueness of phone number
        area_code = random.randint(200, 999)        # Generate a three-digit area code
        exchange_code = random.randint(200, 999)    # Generation of a three-digit exchange code
        line_number = random.randint(1000, 9999)    # Generate a four-digit line number
        # Formatting the number to a standard format
        phone_number = f"({area_code}) {exchange_code}-{line_number}"
        phone_numbers.add(phone_number)
    phone_numbers = list(phone_numbers)
    # Among all, the first part of the arrays is for customers
    # The second part is for managers
    clients_full_names = full_names[:num_clients]
    managers_full_names = full_names[num_clients:num_people]
    clients_phone_numbers = phone_numbers[:num_clients]
    managers_phone_numbers = phone_numbers[num_clients:num_people]


    fake = Faker()
    columns = ['Address', 'City']
    address_client = []
    city_client = []
    # Generating adress and city of company
    for _ in range(num_clients):
        address = fake.street_address()
        city = random.choice(available_cities)
        city_client.append(city)
        address_client.append(address)
    # --- Filling in the 2nd part of clients DataFrame ---
    df_clients['ClientID'] = range(1, num_clients + 1)
    df_clients['ClientName'] = clients_full_names
    df_clients['City'] = city_client
    df_clients['Address'] = address_client
    df_clients['ClientPhone'] = clients_phone_numbers
    df_clients=df_clients.reset_index(drop=True)
    # Saving companies DF to .csv file in generated_data folder
    df_clients.to_csv(gen_data_directory + '\clients.csv')

    # --- Generating service DataFrame
    df_service = pd.read_csv(data_directory+'\service_ex.csv', sep=';')
    # Saving service DF to .csv file in generated_data folder
    df_service.to_csv(gen_data_directory + '\service.csv')

    # --- Generating type service DataFrame
    df_type_service = pd.read_csv(data_directory+'\service_type_ex.csv', sep=';')
    # Saving service DF to .csv file in generated_data folder
    df_type_service.to_csv(gen_data_directory + '\\type_service.csv')

    # # --- Generating service DataFrame
    # with open(data_directory + '\\' + 'service.txt', 'r', encoding='utf-8') as file:
    #     service_array = file.readlines()
    # services = [s.strip() for s in service_array]
    # df_service = pd.DataFrame(services, columns=['TypeService'])
    # df_service['ServiceID'] = range(1, len(service_array) + 1)
    # df_service = df_service[['ServiceID', 'TypeService']].reset_index(drop=True)
    # # Saving service DF to .csv file in generated_data folder
    # df_service.to_csv(gen_data_directory + '\service.csv')

    num_df_type_service = len(df_type_service)
    num_df_service = len(df_service)
    # --- Generating contracts DataFrame
    df_contracts = df_clients.drop(['City', 'Address'], axis=1)
    df_random = df_contracts.sample(frac=1).reset_index(drop=True) # Mix the rows
    # Repetition of client line for several contarts from one client
    indices = []
    for i, row in df_contracts.iterrows():
        indices.extend([i] * random.randint(1, max_contracts_num_one_client))  # Repeat the line index 
    df_contracts = df_random.loc[indices].reset_index(drop=True)

    num_contracts = len(df_contracts)
    

    # --- Generating dates for conrats
    type_service_ids = []
    service_ids = []
    signing_dates = []
    start_dates = []
    end_dates = []
    payment_dates = []
    contract_amounts = []
    
    for _ in range(num_contracts):
        # Generation ServiceId
        type_service_id = random.randint(1, num_df_type_service)
        filtered_df = df_service[df_service['TypeServiceID'] == type_service_id]
        service_id = filtered_df.sample(n=1)['ServiceID'].iloc[0] if not filtered_df.empty else None

        # service_id = random.randint(1, len(service_array)+1)
        # Generation of signature date within the last 'years' years
        signing_date = datetime.now().date() - timedelta(days=random.randint(0, 365 * years))

        # Generation of work start date subject 
        # to a max_day_delta_start_date-day limitation after signing
        start_date = signing_date + timedelta(days=random.randint(1, max_day_delta_start_date))

        # Generation of the completion date, taking into account the limitation 
        # of min_work_duration-max_work_duration days after the start of work
        end_date = start_date + timedelta(days=random.randint(min_work_duration, max_work_duration))

        # Generation of the payment date taking into account the limitation 
        # of max_day_delta_paying days after completion of works
        payment_date = end_date + timedelta(days=random.randint(0, max_day_delta_paying))

        # Generation of the contract amount taking into account normal distribution
        mean_amount = 5100  # Mean value
        std_deviation = 2500  # Standard deviation
        contract_amount = round(np.random.normal(mean_amount, std_deviation), -1)
        contract_amount = max(550, min(10000, contract_amount))  # Restricted to a range of $750 to $10,000

        type_service_ids.append(type_service_id)
        service_ids.append(service_id)
        # signing_dates.append(signing_date.strftime("%Y-%m-%d"))
        # start_dates.append(start_date.strftime("%Y-%m-%d"))
        # end_dates.append(end_date.strftime("%Y-%m-%d"))
        # payment_dates.append(payment_date.strftime("%Y-%m-%d"))
        # signing_dates.append(datetime.strptime(signing_date.strftime("%Y-%m-%d"), '%Y-%m-%d'))
        signing_dates.append(signing_date)
        start_dates.append(start_date)
        end_dates.append(end_date)
        payment_dates.append(payment_date)
        contract_amounts.append(contract_amount)

    # Filling the fields of the contract dataframe
    df_contracts['TypeServiceID'] = type_service_ids 
    df_contracts['ServiceID'] = service_ids
    df_contracts['SigningDate'] = pd.to_datetime(signing_dates)
    df_contracts['StartDate'] = pd.to_datetime(start_dates)
    df_contracts['EndDate'] = pd.to_datetime(end_dates)
    df_contracts['PayDate'] = pd.to_datetime(payment_dates)
    df_contracts['Price'] = contract_amounts

    df_contracts = df_contracts.sort_values(by='SigningDate').reset_index(drop=True)
    df_contracts['ContractID'] = range(1, num_contracts + 1)

    manager_ids = range(1, num_managers+1)
    full_length = len(manager_ids)
    target_length = len(df_contracts)
    repetitions = target_length // full_length
    remainder = target_length % full_length

    repeated_manager_ids = list(manager_ids) * repetitions
    trimmed_manager_ids = repeated_manager_ids + list(manager_ids[:remainder])
    df_contracts['ManagerID'] = trimmed_manager_ids

    # Saving contract DF to .csv file in generated_data folder
    df_contracts.to_csv(gen_data_directory + '\contracts.csv')

    # --- Generating Dataframe of managers
    df_managers = pd.DataFrame(managers_full_names, columns=['ManagerName'])
    df_managers['ManagerPhone'] = managers_phone_numbers
    df_managers['ManagerID'] = range(1, num_managers+1)
    df_managers = df_managers[['ManagerID', 'ManagerName', 'ManagerPhone']].reset_index(drop=True)
    df_managers.to_csv(gen_data_directory + '\managers.csv')


    return df_company, df_clients, df_type_service, df_service, df_managers, df_contracts



def generator_scan_contracts(df_contracts: pd.DataFrame, df_service: pd.DataFrame) -> None:
    """
    Generates contract scans based on transferred data from dataframes.

    Arguments:
    df_contracts (pd.DataFrame): A dataframe with information about contracts.
    df_service (pd.DataFrame): DataFrame with information about the services provided.

    Return Value:
    None: The function returns no values, it generates contract scans based on the data passed in.
    """
    # --- Main Paths ---
    script_directory = os.path.dirname(os.path.abspath(__file__)) # Script path
    data_directory = os.path.join(os.path.dirname(script_directory), "data")    # data folder path
    gen_data_directory = os.path.join(os.path.dirname(script_directory), "generated_data\scan_contract")  # generated_data folder path
    def create_contract(fields, index):
        # Loading a contract template
        contract_template = Image.open(f'{data_directory}\\default.jpg')  

        # Выбор шрифта и его размера
        font = ImageFont.truetype('arial.ttf', size=10) 

        # Create an ImageDraw object for image editing
        draw = ImageDraw.Draw(contract_template)

        # Set the position and text for each field
        text_positions = {
            'Signing date': (400, 100),
            'Contract ID': (270, 130),
            'Service': (20, 300),
            'Company name': (20, 320),
            'Client name': (320, 400),
            'Phone number': (320, 420),
            'Start date': (320, 440),
            'End date': (320, 460),
            'Pay date': (320, 480),
            'Price': (320, 500)
        }

        # Add the text of specified fields to the image
        for field, position in text_positions.items():
            if field in fields:
                draw.text(position, f"{field}: {fields[field]}", font=font, fill='black')

        # Saving the modified image to a file with a unique name for each line
        # Compression with quality parameter added
        contract_template.save(f'{gen_data_directory}\contract_{fields["Contract ID"]}.jpg', quality=80)  

    merged_df = pd.merge(df_contracts, df_service, on=['ServiceID', 'TypeServiceID'], how='inner')
    
    for index, row in merged_df.iterrows():
        # Create a dictionary for each line of the dataframe, which is passed to the create_contract function
        contract_fields = {
            'Signing date': row['SigningDate'],
            'Contract ID': row['ContractID'],
            'Service': row['Service'],
            'Company name': row['CompanyName'],
            'Client name': row['ClientName'],
            'Phone number': row['ClientPhone'],
            'Start date': row['StartDate'],
            'End date': row['EndDate'],
            'Pay date': row['PayDate'],
            'Price': str(row['Price']) + '$'
        }
        create_contract(contract_fields, index)


def create_database(
    df_company: pd.DataFrame, 
    df_clients: pd.DataFrame, 
    df_type_service: pd.DataFrame, 
    df_service: pd.DataFrame, 
    df_managers: pd.DataFrame, 
    df_contracts: pd.DataFrame
) -> None:
    
    """
    Creates a SQLite database and populates it with information from the passed dataframes.

    Arguments:
    df_company (pd.DataFrame): A dataframe with information about companies.
    df_clients (pd.DataFrame): DataFrame with information about customers.
    df_type_service (pd.DataFrame): A dataframe with information about service types.
    df_service (pd.DataFrame): DataFrame with information about the services provided.
    df_managers (pd.DataFrame): DataFrame with information about the managers.
    df_contracts (pd.DataFrame): A dataframe with information about contracts.

    Return Value:
    None: The function returns no values, only creates the database and populates it with data from the dataframes.
    """
    absolute_path = os.path.abspath(os.path.join(os.getcwd(), '../databases/EGA_database.db'))

    # Replacing backslashes with forward slashes to create a SQLite database URL
    absolute_path = "sqlite:///" + absolute_path.replace("\\", "/")
	# Connection to database
    
    engine = create_engine(f'sqlite:///d:/Repositories/EGA_consult/databases/EGA_database.db')
	# Def tables in DB
    metadata = MetaData()
    company = Table('Company', metadata,
		Column('CompanyID', Integer, primary_key=True),
		Column('CompanyName', String)
	)
	
    clients = Table('Clients', metadata,
		Column('ClientID', Integer, primary_key=True),
		Column('CompanyID', Integer, ForeignKey('Company.CompanyID')),
		Column('CompanyName', String),
		Column('ClientName', String),
        Column('City', String),
        Column('Address', String),
		Column('ClientPhone', String)
	)
	
    type_service = Table('TypeService', metadata,
		Column('TypeServiceID', Integer, primary_key=True),
		Column('TypeService', String)
	)
	
    service = Table('Service', metadata,
		Column('ServiceID', Integer, primary_key=True),
		Column('TypeServiceID', Integer, ForeignKey('TypeService.TypeServiceID')),
		Column('Service', String)
	)
	
    managers = Table('Managers', metadata,
		Column('ManagerID', Integer, primary_key=True),
		Column('ManagerName', String),
		Column('ManagerPhone', String)
	)
	
    contracts = Table('Contracts', metadata,
		Column('ContractID', Integer, primary_key=True),
		Column('CompanyID', Integer, ForeignKey('Company.CompanyID')),
		Column('ClientID', Integer, ForeignKey('Clients.ClientID')),
		Column('TypeServiceID', Integer, ForeignKey('TypeService.TypeServiceID')),
		Column('ServiceID', Integer, ForeignKey('Service.ServiceID')),
		Column('SigningDate', Date),
		Column('StartDate', Date),
		Column('EndDate', Date),
		Column('PayDate', Date),
		Column('Price', Integer),
		Column('ManagerID', Integer, ForeignKey('Managers.ManagerID'))
	)
	# Create tables in DB
    metadata.create_all(engine)
	
	
	# DataFrames to dictionaries
    records_df_company = df_company.to_dict(orient='records')
    records_df_clients = df_clients.to_dict(orient='records')
    records_df_type_service = df_type_service.to_dict(orient='records')
    records_df_service = df_service.to_dict(orient='records')
    records_df_managers = df_managers.to_dict(orient='records')
    records_df_contracts = df_contracts.to_dict(orient='records')
	
	# Open connection with DB
    with engine.connect() as connection:
		# Start transaction
        transaction = connection.begin()
        try:
			# Inseert data from DataFrames to Tables
            connection.execute(company.insert(), records_df_company)
            connection.execute(clients.insert(), records_df_clients)
            connection.execute(type_service.insert(), records_df_type_service)
            connection.execute(service.insert(), records_df_service)
            connection.execute(managers.insert(), records_df_managers)
            connection.execute(contracts.insert(), records_df_contracts)
	
            transaction.commit()
        except Exception as e:
			# Catch Error
            transaction.rollback()
            print(f"Error: {e}")