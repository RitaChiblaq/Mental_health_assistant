import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from BE.models.user import User
from BE.models.user_profile import UserProfile
from BE.models.chat_history import ChatHistory
from BE.models.recommendation import Recommendation
from BE.database.db_setup import Base
from BE.config import DATABASE_URI


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(DATABASE_URI)
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()

    def test_add_user(self):
        new_user = User(name='John Doe', email='john.doe@example.com', password_hash='hashed_password')
        self.session.add(new_user)
        self.session.commit()
        user = self.session.query(User).filter_by(email='john.doe@example.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.name, 'John Doe')

    def test_add_user_profile(self):
        user = self.session.query(User).filter_by(email='john.doe@example.com').first()
        user_profile = UserProfile(user_id=user.user_id, preferences={'theme': 'dark'},
                                   mental_health_goals={'goal': 'reduce stress'})
        self.session.add(user_profile)
        self.session.commit()
        profile = self.session.query(UserProfile).filter_by(user_id=user.user_id).first()
        self.assertIsNotNone(profile)
        self.assertEqual(profile.preferences['theme'], 'dark')

    def test_add_chat_history(self):
        user = self.session.query(User).filter_by(email='john.doe@example.com').first()
        chat = ChatHistory(user_id=user.user_id, message='I feel sad', response='I understand. Can you tell me more?',
                           timestamp=datetime.now(), emotion='sad')
        self.session.add(chat)
        self.session.commit()
        chats = self.session.query(ChatHistory).filter_by(user_id=user.user_id).all()
        self.assertGreater(len(chats), 0)
        self.assertEqual(chats[0].message, 'I feel sad')

    def test_add_recommendation(self):
        user = self.session.query(User).filter_by(email='john.doe@example.com').first()
        recommendation = Recommendation(user_id=user.user_id, recommendation={'text': 'Try meditation'},
                                        timestamp=datetime.now())
        self.session.add(recommendation)
        self.session.commit()
        recs = self.session.query(Recommendation).filter_by(user_id=user.user_id).all()
        self.assertGreater(len(recs), 0)
        self.assertEqual(recs[0].recommendation['text'], 'Try meditation')

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(cls.engine)
        cls.session.close()


if __name__ == '__main__':
    unittest.main()