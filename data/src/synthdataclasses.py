# Import required libraries
from faker import Factory
from random import randint
from datetime import datetime, timedelta
from utils.progressbar import ProgressBar

# Import custom classes
from src.synthdata import SyntheticData


class CustomerSynthData(SyntheticData):
    """
    Class to create, store, and write fake customer master data
    """ 

    @ProgressBar()
    def generate_data(self, num_records: int):
        """
        Method to produce fake customer master data
        :param num_records: Number of records to generate
        :return: List of dictionaries containing the data
        """

        # Define the list of countries
        country_locale_map = {
            "US": "en_US", 
            "UK": "en_GB",
        }
        
        # Create a list to store the data
        data = []
        for i in range(num_records):
            
            # For the progress bar
            yield (i / num_records)

            # Randomly select a country
            country = list(country_locale_map.keys())[randint(0, len(country_locale_map) - 1)]

            # Create a faker object for the given country
            faker = Factory.create(country_locale_map[country])

            # Set certain fields based on the country
            if country == "US":
                state = faker.state_abbr()
                county = None
            else:
                state = None
                county = faker.county()

            # Randomly generate some fake data elements that other elements depend on
            created_at = faker.date_time_this_century()
            updated_at = created_at + timedelta(randint(1, 7), randint(60, 1000)) if faker.boolean(chance_of_getting_true=10) else None            
            is_active = faker.boolean(
                chance_of_getting_true=90
            )
            if not is_active:
                deleted_at = updated_at + timedelta(randint(1, 7), randint(60, 1000)) if updated_at is not None else created_at + timedelta(randint(1, 7), randint(60, 1000))
            else:
                deleted_at = None

            # Create a dictionary of the data
            data_dict = {
                "CUST_ID": i,
                "FIRST_NAME": faker.first_name(),
                "LAST_NAME": faker.last_name(),
                "EMAIL": faker.email(),
                "PHONE": faker.phone_number(),
                "DOB": faker.date_of_birth(minimum_age=18, maximum_age=100),
                "MARITAL_STATUS": faker.random_element(elements=("Single", "Married", "Divorced", "Widowed")),
                "ADDRESS": faker.address(),
                "CITY": faker.city(),
                "COUNTY": county,
                "STATE_PROVINCE": state,
                "POSTAL_CODE": faker.postcode(),
                "COUNTRY": country,
                "IS_ACTIVE": is_active,
                "CREATED_AT": created_at,
                "UPDATED_AT": updated_at,
                "DELETED_AT": deleted_at,
            }

            # Convert each element to a string
            for key, value in data_dict.items():
                data_dict[key] = str(value)
            
            # Append the data to the list of data dictionaries
            data.append(data_dict)
        self.data = data


class ProductSynthData(SyntheticData):
    """
    Class to create, store, and write fake product master data
    """

    @ProgressBar()
    def generate_data(self, num_records: int):
        """
        Method to produce fake product master data
        :param num_records: Number of records to generate
        :return: List of dictionaries containing the data
        """

        # Define the list of countries
        country_locale_map = {
            "US": "en_US", 
            "UK": "en_GB",
        }

        # Create a list to store the data
        data = []
        for i in range(num_records):

            # For the progress bar
            yield (i / num_records)

            # Randomly select a country
            country = list(country_locale_map.keys())[randint(0, len(country_locale_map) - 1)]

            # Create a faker object for the given country
            faker = Factory.create(country_locale_map[country])

            # Randomly generate some fake data elements that other elements depend on
            created_at = faker.date_time_this_century()
            updated_at = created_at + timedelta(randint(1, 7), randint(60, 1000)) if faker.boolean(chance_of_getting_true=10) else None            
            is_active = faker.boolean(
                chance_of_getting_true=90
            )
            if not is_active:
                deleted_at = updated_at + timedelta(randint(1, 7), randint(60, 1000)) if updated_at is not None else created_at + timedelta(randint(1, 7), randint(60, 1000))
            else:
                deleted_at = None

            # Create a dictionary of the data
            data_dict = {
                "PRODUCT_ID": 1000 + i,
                "PRODUCT_NAME": faker.word(),
                "PRODUCT_DESCRIPTION": faker.sentence(),
                "PRODUCT_CATEGORY": faker.random_element(elements=("Electronics", "Clothing", "Books")),
                "PRODUCT_SUBCATEGORY": faker.random_element(elements=("Smartphone", "Laptop", "T-Shirt", "Jeans", "Novel", "Textbook")),
                "PRODUCT_PRICE": randint(5, 1000) + randint(0, 99) / 100,
                "PRODUCT_QTY": randint(1, 2),
                "IS_ACTIVE": is_active,
                "COUNTRY": country,
                "CREATED_AT": created_at,
                "UPDATED_AT": updated_at,
                "DELETED_AT": deleted_at,
            }

            # Convert each element to a string
            for key, value in data_dict.items():
                data_dict[key] = str(value)

            # Append the data to the list of data dictionaries
            data.append(data_dict)
        self.data = data


class StoreSynthData(SyntheticData):
    """
    Class to create, store, and write fake store master data
    """

    @ProgressBar()
    def generate_data(self, num_records: int):
        """
        Method to produce fake store master data
        :param num_records: Number of records to generate
        :return: List of dictionaries containing the data
        """

        # Define the list of countries
        country_locale_map = {
            "US": "en_US", 
            "UK": "en_GB",
        }
        
        # Create a list to store the data
        data = []
        for i in range(num_records):

            # For the progress bar
            yield (i / num_records)

            # Randomly select a country
            country = list(country_locale_map.keys())[randint(0, len(country_locale_map) - 1)]

            # Create a faker object for the given country
            faker = Factory.create(country_locale_map[country])

            # Set certain fields based on the country
            if country == "US":
                state = faker.state_abbr()
            else:
                state = None

            # Randomly generate some fake data elements that other elements depend on
            created_at = faker.date_time_this_century()
            updated_at = created_at + timedelta(randint(1, 7), randint(60, 1000)) if faker.boolean(chance_of_getting_true=10) else None            
            is_active = faker.boolean(
                chance_of_getting_true=90
            )
            if not is_active:
                deleted_at = updated_at + timedelta(randint(1, 7), randint(60, 1000)) if updated_at is not None else created_at + timedelta(randint(1, 7), randint(60, 1000))
            else:
                deleted_at = None

            # Create a dictionary of the data
            data_dict = {
                "STORE_ID": 100 + i,
                "STORE_NAME": faker.word().capitalize(),
                "STORE_TYPE": faker.random_element(elements=("retail", "online", "pop_up", "franchise")).upper(),
                "ADDRESS": faker.address(),
                "CITY": faker.city(),
                "STATE_PROVINCE": state,
                "POSTAL_CODE": faker.postcode(),
                "COUNTRY": country,
                "PHONE": faker.phone_number(),
                "EMAIL": faker.email(),
                "IS_ACTIVE": is_active,
                "STORE_MANAGER": faker.name(),
                "CREATED_AT": created_at,
                "UPDATED_AT": updated_at,
                "DELETED_AT": deleted_at,
            }
            
            # Convert each element to a string
            for key, value in data_dict.items():
                data_dict[key] = str(value)

            # Append the data to the list of data dictionaries
            data.append(data_dict)
        self.data = data


class LoyaltySynthData(SyntheticData):
    """
    Class to create, store, and write fake loyalty program master data
    """

    @ProgressBar()
    def generate_data(self, num_records: int):
        """
        Method to produce fake loyalty program master data
        :param num_records: Number of records to generate
        :return: List of dictionaries containing the data
        """

        # Define the list of countries
        country_locale_map = {
            "US": "en_US", 
            "UK": "en_GB",
        }
        
        # Create a list to store the data
        data = []
        for i in range(num_records):

            # For the progress bar
            yield (i / num_records)

            # Randomly select a country
            country = list(country_locale_map.keys())[randint(0, len(country_locale_map) - 1)]

            # Create a faker object for the given country
            faker = Factory.create(country_locale_map[country])

            # Randomly generate some fake data elements that other elements depend on
            created_at = faker.date_time_this_century()
            updated_at = created_at + timedelta(randint(1, 7), randint(60, 1000)) if faker.boolean(chance_of_getting_true=10) else None
            is_active = faker.boolean(chance_of_getting_true=90)
            if not is_active:
                deleted_at = updated_at + timedelta(randint(1, 7), randint(60, 1000)) if updated_at is not None else created_at + timedelta(randint(1, 7), randint(60, 1000))
            else:
                deleted_at = None

            # Create a dictionary of the data
            data_dict = {
                "LOYALTY_ID": 1000 + i,
                # Randomly select a customer ID from the given customer test data
                "CUST_ID": self.foreign_data["CustomerSynthData"].data[randint(0, len(self.foreign_data["CustomerSynthData"].data) - 1)]["CUST_ID"],
                "PROGRAM_NAME": faker.word().capitalize(),
                "ENROLLMENT_TMSTP": faker.date_time_this_century(),
                "CURRENT_POINTS_BALANCE": randint(0, 100000),
                "TIER_LEVEL": faker.random_element(elements=("Gold", "Silver", "Bronze")).upper(),
                "CREATED_AT": created_at,
                "UPDATED_AT": updated_at,
                "DELETED_AT": deleted_at,
            }

            # Convert each element to a string
            for key, value in data_dict.items():
                data_dict[key] = str(value)
            
            # Append the data to the list of data dictionaries
            data.append(data_dict)
        self.data = data


class CampaignSynthData(SyntheticData):
    """
    Class to create, store, and write fake campaign program master data
    """

    @ProgressBar()
    def generate_data(self, num_records: int):
        """
        Method to produce fake campaign master data
        :param num_records: Number of records to generate
        :return: List of dictionaries containing the data
        """

        # Define the list of countries
        country_locale_map = {
            "US": "en_US", 
            "UK": "en_GB",
        }
        
        # Create a list to store the data
        data = []
        for i in range(num_records):

            # For the progress bar
            yield (i / num_records)

            # Randomly select a country
            country = list(country_locale_map.keys())[randint(0, len(country_locale_map) - 1)]

            # Create a faker object for the given country
            faker = Factory.create(country_locale_map[country])

            # Randomly generate some fake data elements that other elements depend on
            created_at = faker.date_time_this_century()
            start_date = created_at.date() + timedelta(randint(1, 7))
            end_date = start_date + timedelta(randint(100, 1000))
            updated_at = created_at + timedelta(randint(1, 7), randint(60, 1000)) if faker.boolean(chance_of_getting_true=10) else None
            is_active = faker.boolean(
                chance_of_getting_true=90
            )
            if not is_active:
                deleted_at = updated_at + timedelta(randint(1, 7), randint(60, 1000)) if updated_at is not None else created_at + timedelta(randint(1, 7), randint(60, 1000))
            else:
                deleted_at = None
            
            # Create a dictionary of the data
            data_dict = {
                "CAMPAIGN_ID": 1000 + i,
                "CAMPAIGN_NAME": faker.word().capitalize(),
                "CAMPAIGN_DESCRIPTION": faker.sentence(),
                "START_DATE": start_date,
                "END_DATE": end_date,
                "CAMPAIGN_TYPE": faker.random_element(elements=("email", "sms", "push", "in_app", "in_store")).upper(),
                "CHANNEL": faker.random_element(elements=("online", "in_store")).upper(),
                "CAMPAIGN_STATUS": faker.random_element(elements=("pending", "active", "completed")).upper(),
                "CREATED_AT": created_at,
                "UPDATED_AT": updated_at,
                "DELETED_AT": deleted_at,
            }

            # Convert each element to a string
            for key, value in data_dict.items():
                data_dict[key] = str(value)
            
            # Append the data to the list of data dictionaries
            data.append(data_dict)
        self.data = data


class OrdersSynthData(SyntheticData):
    """
    Class to create, store, and write fake order data
    """

    @ProgressBar()
    def generate_data(self, num_records: int):
        """
        Method to produce fake order data
        :param num_records: Number of records to generate
        :return: List of dictionaries containing the data
        """

        # Define the list of countries
        country_locale_map = {
            "US": "en_US", 
            "UK": "en_GB",
        }
        
        # Create a list to store the data
        data = []
        for i in range(num_records):

            # For the progress bar
            yield (i / num_records)

            # Randomly select a country
            country = list(country_locale_map.keys())[randint(0, len(country_locale_map) - 1)]

            # Create a faker object for the given country
            faker = Factory.create(country_locale_map[country])

            # Randomly generate some fake data elements that other elements depend on
            created_at = faker.date_time_this_century()
            order_tmstp = created_at - timedelta(0, randint(60, 1000))

            # Create an update timestamp with 10% probability
            updated_at = created_at + timedelta(randint(1, 7), randint(60, 1000)) if faker.boolean(chance_of_getting_true=10) else None

            # Pull out a random customer and product data dictionary
            customer_data = self.foreign_data["CustomerSynthData"].data[randint(0, len(self.foreign_data["CustomerSynthData"].data) - 1)]
            product_data = self.foreign_data["ProductSynthData"].data[randint(0, len(self.foreign_data["ProductSynthData"].data) - 1)]

            # Decide the unit price, purchase price based on the product price and quantity
            order_qty = randint(1, 10)
            order_total = order_qty * float(product_data["PRODUCT_PRICE"])

            # Decide channel randomly
            channel = faker.random_element(elements=("ONLINE", "IN_STORE")).upper()

            # Decide the campaign randomly
            campaign_data = self.foreign_data["CampaignSynthData"].data[randint(0, len(self.foreign_data["CampaignSynthData"].data) - 1)]
            campaign_id = campaign_data["CAMPAIGN_ID"] if datetime.strptime(campaign_data["START_DATE"], '%Y-%m-%d').date() <= created_at.date() <= datetime.strptime(campaign_data["END_DATE"], '%Y-%m-%d').date() else None

            # Create a dictionary of the data
            data_dict = {
                "ORDER_ID": 10000 + i,
                # Randomly select a customer ID from the given customer test data
                "CUST_ID": customer_data["CUST_ID"],
                # Randomly select a product ID from the given product test data
                "PRODUCT_ID": product_data["PRODUCT_ID"],
                # Randomly select a store ID from the given store test data
                "STORE_ID": None if channel == "ONLINE" else self.foreign_data["StoreSynthData"].data[randint(0, len(self.foreign_data["StoreSynthData"].data) - 1)]["STORE_ID"],
                "ORDER_TMSTP": order_tmstp,
                "ORDER_TOTAL": order_total,
                "ORDER_QTY": order_qty,
                "PAYMENT_METHOD": faker.random_element(elements=("credit_card", "debit_card", "cash", "paypal", "apple_pay", "google_pay")).upper(),
                "ORDER_STATUS": "COMPLETED" if channel == "IN_STORE" else faker.random_element(elements=("pending", "processing", "shipped", "delivered", "cancelled", "completed", "returned")).upper(),
                "PURCHASE_CHANNEL": channel,
                # Randomly select a campaign ID from the given campaign test data
                "CAMPAIGN_ID": campaign_id,
                "SHIP_ADDRESS": customer_data["ADDRESS"] if channel == "ONLINE" else None,
                "SHIP_CITY": customer_data["CITY"] if channel == "ONLINE" else None,
                "SHIP_STATE_PROVINCE": customer_data["STATE_PROVINCE"] if channel == "ONLINE" else None,
                "SHIP_POSTAL_CODE": customer_data["POSTAL_CODE"] if channel == "ONLINE" else None,
                "SHIP_COUNTRY": customer_data["COUNTRY"] if channel == "ONLINE" else None,
                "CREATED_AT": created_at,
                "UPDATED_AT": updated_at,
            }

            # Convert each element to a string
            for key, value in data_dict.items():
                data_dict[key] = str(value)
            
            # Append the data to the list of data dictionaries
            data.append(data_dict)
        self.data = data