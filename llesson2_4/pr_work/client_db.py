from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import declarative_base, sessionmaker, Session

Base = declarative_base()


class ClientContacts(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class MessageHistory(Base):
    __tablename__ = 'message_history'
    id = Column(Integer, primary_key=True)
    from_user = Column(String)
    to_user = Column(String)
    message = Column(Text)
    datetime = Column(DateTime(timezone=True), server_default=func.now())


class ClientDB:

    def __init__(self, account):
        self.account = account
        engine = create_engine(
            f'sqlite:///client_{account}.db3',
            echo=True,
            pool_recycle=7200,
            connect_args={'check_same_thread': False}
        )
        Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)
        self.sess: Session = session()

    def add_contact(self, contact):
        insert_seq = insert(ClientContacts).values({'name': contact}).on_conflict_do_nothing()
        self.sess.execute(insert_seq)
        self.sess.commit()

    def del_contact(self, contact):
        self.sess.query(ClientContacts).filter_by(name=contact).delete()
        self.sess.commit()

    def add_message(self, from_user, to_user, message, date=None):
        self.sess.add(MessageHistory(from_user=from_user, to_user=to_user, message=message, datetime=date))
        self.sess.commit()


# if __name__ == '__main__':
#     clientdb = ClientDB('test')
#     clientdb.add_contact('cli')
#     clientdb.add_contact('cli2')
#     clientdb.add_message('test', 'cli', 'Hey man')
#     clientdb.del_contact('cli2')
