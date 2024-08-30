# Import required modules
import pytest
from datetime import datetime, timedelta
from data.src.synthdataclasses import CustomerSynthData, ProductSynthData, StoreSynthData, LoyaltySynthData, CampaignSynthData, OrdersSynthData

@pytest.fixture(scope="session")
def customer_test_data():
    return CustomerSynthData()

@pytest.fixture(scope="session")
def product_test_data():
    return ProductSynthData()

@pytest.fixture(scope="session")
def store_test_data():
    return StoreSynthData()

@pytest.fixture(scope="session")
def loyalty_test_data():
    return LoyaltySynthData()

@pytest.fixture(scope="session")
def campaign_test_data():
    return CampaignSynthData()

@pytest.fixture(scope="session")
def orders_test_data():
    return OrdersSynthData()

@pytest.fixture(scope="session")
def customer_data():
    return [
        {
            "CUST_ID": 1,
            "FIRST_NAME": 'John',
            "LAST_NAME": 'Smith',
            "EMAIL": 'fake_email_1@example.com',
            "PHONE": '111-111-1111',
            "DOB": '1990-12-01',
            "MARITAL_STATUS": 'Single',
            "ADDRESS": '111 W First St',
            "CITY": 'Madeupsville',
            "COUNTY": 'Madeupcounty',
            "STATE_PROVINCE": 'XY',
            "POSTAL_CODE": '11111',
            "COUNTRY": 'RW',
            "IS_ACTIVE": True,
            "CREATED_AT": datetime.now(),
            "UPDATED_AT": None,
            "DELETED_AT": None,
        },
        {
            "CUST_ID": 2,
            "FIRST_NAME": 'Jane',
            "LAST_NAME": 'Doe',
            "EMAIL": 'fake_email_2@example.com',
            "PHONE": '222-222-2222',
            "DOB": '1995-02-01',
            "MARITAL_STATUS": 'Married',
            "ADDRESS": '222 E Second St',
            "CITY": 'Madeupsville',
            "COUNTY": 'Madeupcounty',
            "STATE_PROVINCE": 'XY',
            "POSTAL_CODE": '22222',
            "COUNTRY": 'RW',
            "IS_ACTIVE": True,
            "CREATED_AT": datetime.now(),
            "UPDATED_AT": datetime.now() + timedelta(0, 500),
            "DELETED_AT": None,
        },
        {
            "CUST_ID": 3,
            "FIRST_NAME": 'Brian',
            "LAST_NAME": 'Jackson',
            "EMAIL": 'fake_email_3@example.com',
            "PHONE": '333-333-3333',
            "DOB": '2000-06-15',
            "MARITAL_STATUS": 'Divorced',
            "ADDRESS": '333 W Third St',
            "CITY": 'Madeupsville',
            "COUNTY": 'Madeupcounty',
            "STATE_PROVINCE": 'XY',
            "POSTAL_CODE": '33333',
            "COUNTRY": 'RW',
            "IS_ACTIVE": True,
            "CREATED_AT": datetime.now(),
            "UPDATED_AT": datetime.now() + timedelta(0, 500),
            "DELETED_AT": datetime.now() + timedelta(0, 10000),
        },
    ]

class TestCustomerSynthData:
    """Class to test the CustomerSynthData class"""

    def test_generate_data_length(self, customer_test_data):
        """
        Test that the generate_data method creates the correct number of records.
        Args:
            customer_test_data (CustomerSynthData): The test data class instance.
        Asserts:
            The length of the generated data matches the number of records requested.
        """
        num_records = 5
        customer_test_data.generate_data(num_records)
        assert len(customer_test_data.data) == num_records

    def test_generate_data_structure(self, customer_test_data):
        """
        Test that the generated data has the correct structure.
        Args:
            customer_test_data (CustomerSynthData): The test data class instance.
        Asserts:
            Each record in the generated data contains all required keys.
        """
        num_records = 1
        customer_test_data.generate_data(num_records)
        generated_data = customer_test_data.data
        assert len(generated_data) == num_records
        required_keys = [
            "CUST_ID", "FIRST_NAME", "LAST_NAME", "EMAIL", "PHONE",
            "DOB", "MARITAL_STATUS", "ADDRESS", "CITY", "COUNTY",
            "STATE_PROVINCE", "POSTAL_CODE", "COUNTRY", "IS_ACTIVE",
            "CREATED_AT", "UPDATED_AT", "DELETED_AT"
        ]
        for record in generated_data:
            assert all(key in record for key in required_keys)

    def test_generate_zero_records(self, customer_test_data):
        """
        Test that generating zero records results in an empty data list.
        Args:
            customer_test_data (CustomerSynthData): The test data class instance.
        Asserts:
            The generated data list is empty when zero records are requested.
        """
        num_records = 0
        customer_test_data.generate_data(num_records)
        generated_data = customer_test_data.data
        assert len(generated_data) == 0

class TestProductSynthData:
    """Class to test the ProductSynthData class"""

    def test_generate_data_length(self, product_test_data):
        """
        Test that the generate_data method creates the correct number of records.
        Args:
            product_test_data (ProductSynthData): The test data class instance.
        Asserts:
            The length of the generated data matches the number of records requested.
        """
        num_records = 5
        product_test_data.generate_data(num_records)
        assert len(product_test_data.data) == num_records

    def test_generate_data_structure(self, product_test_data):
        """
        Test that the generated data has the correct structure.
        Args:
            product_test_data (ProductSynthData): The test data class instance.
        Asserts:
            Each record in the generated data contains all required keys.
        """
        num_records = 1
        product_test_data.generate_data(num_records)
        generated_data = product_test_data.data
        assert len(generated_data) == num_records
        required_keys = [
            "PRODUCT_ID",
            "PRODUCT_NAME",
            "PRODUCT_DESCRIPTION",
            "PRODUCT_CATEGORY",
            "PRODUCT_SUBCATEGORY",
            "PRODUCT_PRICE",
            "PRODUCT_QTY",
            "IS_ACTIVE",
            "COUNTRY",
            "CREATED_AT",
            "UPDATED_AT",
            "DELETED_AT",
        ]
        for record in generated_data:
            assert all(key in record for key in required_keys)

    def test_generate_zero_records(self, product_test_data):
        """
        Test that generating zero records results in an empty data list.
        Args:
            product_test_data (ProductSynthData): The test data class instance.
        Asserts:
            The generated data list is empty when zero records are requested.
        """
        num_records = 0
        product_test_data.generate_data(num_records)
        generated_data = product_test_data.data
        assert len(generated_data) == 0

class TestStoreSynthData:
    """Class to test the StoreSynthData class"""

    def test_generate_data_length(self, store_test_data):
        """
        Test that the generate_data method creates the correct number of records.
        Args:
            store_test_data (StoreSynthData): The test data class instance.
        Asserts:
            The length of the generated data matches the number of records requested.
        """
        num_records = 5
        store_test_data.generate_data(num_records)
        assert len(store_test_data.data) == num_records

    def test_generate_data_structure(self, store_test_data):
        """
        Test that the generated data has the correct structure.
        Args:
            store_test_data (StoreSynthData): The test data class instance.
        Asserts:
            Each record in the generated data contains all required keys.
        """
        num_records = 1
        store_test_data.generate_data(num_records)
        generated_data = store_test_data.data
        assert len(generated_data) == num_records
        required_keys = [
            "STORE_ID",
            "STORE_NAME",
            "STORE_TYPE",
            "ADDRESS",
            "CITY",
            "STATE_PROVINCE",
            "POSTAL_CODE",
            "COUNTRY",
            "PHONE",
            "EMAIL",
            "IS_ACTIVE",
            "STORE_MANAGER",
            "CREATED_AT",
            "UPDATED_AT",
            "DELETED_AT",
        ]
        for record in generated_data:
            assert all(key in record for key in required_keys)

    def test_generate_zero_records(self, store_test_data):
        """
        Test that generating zero records results in an empty data list.
        Args:
            store_test_data (StoreSynthData): The test data class instance.
        Asserts:
            The generated data list is empty when zero records are requested.
        """
        num_records = 0
        store_test_data.generate_data(num_records)
        generated_data = store_test_data.data
        assert len(generated_data) == 0

