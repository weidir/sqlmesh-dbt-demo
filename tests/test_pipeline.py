# Import required modules
import pytest
from data.src.pipeline import SyntheticDataPipeline
from data.src.synthdataclasses import CustomerSynthData, ProductSynthData, StoreSynthData, LoyaltySynthData, CampaignSynthData, OrdersSynthData

@pytest.fixture(scope="session")
def test_data_types():
    return [CustomerSynthData, ProductSynthData, StoreSynthData, LoyaltySynthData, CampaignSynthData, OrdersSynthData]

@pytest.fixture(scope="session")
def test_data_pipeline(test_data_types):
    return SyntheticDataPipeline(data_types=test_data_types)


class TestSyntheticDataPipeline:
    """Class to test the SyntheticDataPipeline class"""

    def test_generate_length(self, test_data_pipeline, test_data_types):
        """
        Test that the generate method creates the correct number of records.
        Args:
            test_data_pipeline (SyntheticDataPipeline): The test data pipeline class.
            test_data_types (list): The types of test data to generate
        Asserts:
            The length of the generated data matches the number of records requested.
        """

        num_records = 5
        test_data_pipeline.generate(num_records)
        assert len(test_data_pipeline.data) == len(test_data_types)
        assert len(test_data_pipeline.data["CUSTOMERSYNTHDATA"].data) == num_records
