from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///server_db.db3', echo=True)

Base = declarative_base()


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    login = Column(String)
    information = Column(String)

    def __init__(self, login, information):
        self.login = login
        self.information = information


class ClientHistory(Base):
    __tablename__ = 'client_history'
    id = Column(Integer, primary_key=True)
    id_client = Column(ForeignKey('clients.id'))
    time_login = Column(DateTime)
    ip_address = Column(String)

    def __init__(self, id_client, time_login, ip_address) -> None:
        self.id_client = id_client
        self.time_login = time_login
        self.ip_address = ip_address


class ContactList(Base):
    __tablename__ = 'contact_list'
    id = Column(Integer, primary_key=True)
    id_owner = Column(ForeignKey('clients.id'))
    id_client = Column(ForeignKey('clients.id'))

    def __init__(self, id_owner, id_client) -> None:
        self.id_owner = id_owner
        self.id_client = id_client


if __name__ == '__main__':
    Base.metadata.create_all(engine)
