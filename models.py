from sqlalchemy import Column, Integer, String, select, Boolean
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "postgresql+asyncpg://school_logins_user:mXpppLVXokYQkU8Owz6G0iVWeOOcGzUv@dpg-cu97jet6l47c73d72m2g-a.oregon-postgres.render.com/school_logins"
# DATABASE_URL = "sqlite+aiosqlite:///database.sqlite3"
engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine)


# Base model
class Base(AsyncAttrs, DeclarativeBase):
    pass


# Login model
class Login(Base):
    __tablename__ = "logins"
    id = Column(Integer, autoincrement=True, primary_key=True)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, autoincrement=True, primary_key=True)
    tg_id = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    sending = Column(Boolean, nullable=True, default=False)


async def create_or_update_user(tg_id: str, name: str, sending: bool):
    async with async_session() as session:
        stmt = select(User).where(User.tg_id == tg_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if user:
            user.sending = sending
            await session.commit()
        else:
            new_user = User(tg_id=tg_id, name=name, sending=sending)
            session.add(new_user)
            await session.commit()


async def get_user():
    async with async_session() as session:
        stmt = select(User.tg_id).where(User.sending == True)
        result = await session.execute(stmt)
        users = result.scalars().all()
        return users

async def get_login():
    async with async_session() as session:
        stmt = select(Login)
        result = await session.execute(stmt)
        users = result.scalars().all()
        return users



async def create_login(login: str, password: str):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(Login).where(Login.login == login)
            )
            existing_login = result.scalar_one_or_none()

            if existing_login:
                existing_login.password = password
            else:
                new_login = Login(login=login, password=password)
                session.add(new_login)

            await session.commit()
            return existing_login if existing_login else new_login


async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
