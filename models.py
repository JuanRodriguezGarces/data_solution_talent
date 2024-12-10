from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Tabla `users`
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(255), nullable=True)
    identification_number = Column(String(20), nullable=True, unique=True)
    slug = Column(String(255), unique=True, nullable=True)
    video = Column(Text, nullable=True)
    email = Column(String(255), unique=True, nullable=True)
    gender = Column(String(1), nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    #resumes = relationship("Resume", back_populates="user")
    #profiles = relationship("Profile", back_populates="user")

# Tabla `resumes`
class Resume(Base):
    __tablename__ = 'resumes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=True)
    name = Column(String(255), nullable=True)
    type = Column(String(50), nullable=True)
    video = Column(Text, nullable=True)
    views = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=True)

    #user = relationship("User", back_populates="resumes")

# Tabla `profiles`
class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=True)
    onboarding_goal = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    views = Column(Integer, nullable=True)

    #user = relationship("User", back_populates="profiles")

# Tabla `challenges`
class Challenge(Base):
    __tablename__ = 'challenges'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=True)
    opencall_objective = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=True)
