import os

class Config:
    DATABASE_URI = os.getenv('DATABASE_URI',
                             'postgresql+psycopg2://postgres:admin@localhost/poke-db')
