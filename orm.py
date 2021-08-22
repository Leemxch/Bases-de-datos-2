import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

engine = sa.create_engine('mssql+pyodbc://(LocalDb)\MSSQLLocalDB/solutiondesigns?driver=SQL+Server+Native+Client+11.0', echo = False)
con = engine.connect()

'''Session = sessionmaker(bind=engine)
session = Session()
metadata = sa.MetaData()'''

Base = declarative_base()

class solutionsLog(Base):
    __tablename__ = 'sd_solutionslog'
    solutionlogid = sa.Column('solutionlogid', sa.Integer(),primary_key = True)
    posttime =  sa.Column('posttime', sa.DateTime() , nullable=False)
    actiontypeid = sa.Column('actiontypeid', sa.Integer(), nullable=False)
    solutionid = sa.Column('solutionid', sa.Integer(), nullable=False)

class action(Base):
    __tablename__ = 'sd_actiontypes'
    actiontypeid = sa.Column('actiontypeid', sa.Integer(),primary_key = True)
    name = sa.Column('name', sa.String(255), nullable=False)
    iconurl = sa.Column('iconurl', sa.String(255), nullable=False)

#Usable tables: solutionsLog, action
solutions = solutionsLog.__table__
actions = action.__table__
query = sa.select([solutions, actions])
query = query.select_from(solutions.join(
                                        actions,
                                        solutions.columns.actiontypeid == actions.columns.actiontypeid))
res = con.execute(query)
test = res.fetchall()
for i in range(0,10):
    print(test[i])
