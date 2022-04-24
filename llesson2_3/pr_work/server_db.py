from datetime import datetime

from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session

engine = create_engine('sqlite:///server_db.db3', echo=True)

Base = declarative_base()


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    login = Column(String)
    information = Column(String)

    def __init__(self, login, information=None):
        self.login = login
        self.information = information


class ClientHistory(Base):
    __tablename__ = 'client_history'
    id = Column(Integer, primary_key=True)
    id_client = Column(ForeignKey('clients.id'))
    time_login = Column(DateTime, server_default=text('NOW()'))
    ip_address = Column(String)

    def __init__(self, id_client, ip_address, time_login=None) -> None:
        self.id_client = id_client
        self.time_login = time_login or datetime.now()
        self.ip_address = ip_address


class ContactList(Base):
    __tablename__ = 'contact_list'
    id = Column(Integer, primary_key=True)
    id_owner = Column(ForeignKey('clients.id'))
    id_client = Column(ForeignKey('clients.id'))

    def __init__(self, id_owner, id_client) -> None:
        self.id_owner = id_owner
        self.id_client = id_client


class ServerDB:

    def __init__(self) -> None:
        session = sessionmaker(bind=engine)
        self.sess: Session = session()

    def save_client(self, name, socket, time=None):
        client = self.sess.query(Client).filter_by(login=name).first()
        client = client if client is not None else Client(name)
        self.sess.add(client)
        self.sess.commit()
        self.sess.add(ClientHistory(client.id, socket.getpeername()[0], time))
        self.sess.commit()

    def save_contact(self, client_name_from, client_name_to):
        client_from = self.sess.query(Client).filter_by(login=client_name_from).first()
        client_to = self.sess.query(Client).filter_by(login=client_name_to).first()
        if client_from and client_to:
            self.sess.add(ContactList(client_from.id, client_to.id))
            self.sess.commit()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
