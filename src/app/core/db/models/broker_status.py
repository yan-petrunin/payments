import enum

class BrokerStatus(str, enum.Enum):
    PENDING = "pending"
    PUBLISHED = "published"