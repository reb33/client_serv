from datetime import datetime

from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime, func, delete
from sqlalchemy.orm import declarative_base, sessionmaker, Session



Base = declarative_base()


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    login = Column(String)
    last_login = Column(DateTime)
    information = Column(String)

    def __init__(self, login, login_time, information=None):
        self.login = login
        self.last_login = login_time
        self.information = information


# Класс - отображение таблицы активных пользователей:
class ActiveUsers(Base):
    __tablename__ = 'active_users'
    id = Column(Integer, primary_key=True)
    client_id = Column(ForeignKey('clients.id'))
    ip_address = Column(String)
    port = Column(Integer)
    login_time = Column(DateTime)

    def __init__(self, client_id, ip_address, port, login_time) -> None:
        self.client_id = client_id
        self.ip_address = ip_address
        self.port = port
        self.login_time = login_time


# Класс отображение таблицы истории действий
class ClientStatistics(Base):
    __tablename__ = 'client_statistics'
    id = Column(Integer, primary_key=True)
    client_id = Column(ForeignKey('clients.id'))
    sent = Column(Integer)
    accepted = Column(Integer)

    def __init__(self, client_id, sent, accepted) -> None:
        self.client_id = client_id
        self.sent = sent
        self.accepted = accepted


class ClientHistory(Base):
    __tablename__ = 'client_history'
    id = Column(Integer, primary_key=True)
    id_client = Column(ForeignKey('clients.id'))
    time_login = Column(DateTime, server_default=func.now())
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

    def __init__(self, file_name) -> None:
        engine = create_engine(f'sqlite:///{file_name}', echo=True, connect_args={'check_same_thread': False})
        session = sessionmaker(bind=engine)
        self.sess: Session = session()
        Base.metadata.create_all(engine)

    def login_client(self, name, socket, time=None):
        client = self.sess.query(Client).filter_by(login=name).first()
        if client is None:
            client = Client(name, time)
            self.sess.add(client)
            self.sess.commit()
        else:
            client.last_login = time
            self.sess.commit()
        ip, port = socket.getpeername()
        self.sess.add(ClientHistory(client.id, ip, time))
        self.sess.add(ActiveUsers(client.id, ip, port, time))
        self.sess.commit()

    def logout_client(self, name):
        client = self.sess.query(Client).filter_by(login=name).first()
        active_user = self.sess.query(ActiveUsers).filter_by(client_id=client.id).first()
        self.sess.delete(active_user)
        self.sess.commit()

    def save_contact(self, client_name_from, client_name_to):
        client_from = self.sess.query(Client).filter_by(login=client_name_from).first()
        client_to = self.sess.query(Client).filter_by(login=client_name_to).first()
        if client_from and client_to:
            self.sess.add(ContactList(client_from.id, client_to.id))
            self.sess.commit()

    def add_message(self, client_name_from, client_name_to):
        client_from = self.sess.query(Client).filter_by(login=client_name_from).first()
        client_to = self.sess.query(Client).filter_by(login=client_name_to).first()
        if client_from and client_to:
            client_stat_from = self.sess.query(ClientStatistics).filter_by(client_id=client_from.id).first()
            if client_stat_from:
                client_stat_from.sent += 1
            else:
                self.sess.add(ClientStatistics(client_from.id, 1, 0))
            client_stat_to = self.sess.query(ClientStatistics).filter_by(client_id=client_to.id).first()
            if client_stat_to:
                client_stat_to.accepted += 1
            else:
                self.sess.add(ClientStatistics(client_to.id, 0, 1))
            self.sess.commit()

    def del_contact(self, client_name_from, client_name_to_del):
        client_from = self.sess.query(Client).filter_by(login=client_name_from).first()
        client_to_del = self.sess.query(Client).filter_by(login=client_name_to_del).first()
        if client_from and client_to_del:
            self.sess.delete(ContactList(client_from.id, client_to_del.id))
            self.sess.commit()

    def get_contracts(self, client_name):
        return self.sess.query(Client).filter_by(login=client_name).all()

    def active_users_list(self):
        query = self.sess.query(
            Client.login,
            ActiveUsers.ip_address,
            ActiveUsers.port,
            ActiveUsers.login_time
        ).join(Client)
        return query.all()

    def message_history(self):
        queue = self.sess.query(
            Client.login,
            Client.last_login,
            ClientStatistics.sent,
            ClientStatistics.accepted,
        ).join(ClientStatistics)
        return queue.all()

    def clear_active_users(self):
        self.sess.execute(delete(ActiveUsers))
        self.sess.commit()


# if __name__ == '__main__':
#     ServerDB('server_db.db3').clear_active_users()
