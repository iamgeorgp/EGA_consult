import gen_funcs2

num_cities = 30         # Amount of clients' cities
num_companies = 1200      # Amount of clients' companies
max_clients_num_one_company = 3 # For generating for one company several clients from 1 to ...
max_contracts_num_one_client = 3 # For generating for one client several contracts from 1 to ...
num_managers = 82   # Amount of managers from consulting agency 
years = 6 # Duration of work of the consulting agency in years
max_day_delta_start_date = 21 # Day timedelta between signing contract and start date
# Duration of work (timedelta between start_date and end_date)
min_work_duration = 3
max_work_duration = 72
max_day_delta_paying = 14 # Max timedelta between end_date and payment_date

df_company, df_clients, df_type_service, df_service, df_managers, df_contracts = gen_funcs2.generator_main_dfs(
                       num_cities, 
                       num_companies, 
                       max_clients_num_one_company, 
                       max_contracts_num_one_client, 
                       num_managers, 
                       years,
                       max_day_delta_start_date,
                       min_work_duration,
                       max_work_duration,
                       max_day_delta_paying)

# gen_funcs2.generator_scan_contracts(df_contracts, df_service)

gen_funcs2.create_database(df_company, df_clients, df_type_service, df_service, df_managers, df_contracts)