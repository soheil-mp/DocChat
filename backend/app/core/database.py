class Database:
    db = None

    @classmethod
    def initialize(cls, database):
        """Initialize the global database instance"""
        cls.db = database

    @classmethod
    def get_database(cls):
        """Get the current database instance"""
        if not cls.db:
            raise ValueError("Database not initialized")
        return cls.db 