from enum import Enum

# Define the supported data stores
class Environments(Enum):
    DEV = 1
    PROD = 2
    BOTH = 3