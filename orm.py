import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

#Coneccion con la base de datos
engine = sa.create_engine('mssql+pyodbc://(LocalDb)\MSSQLLocalDB/solutiondesigns?driver=SQL+Server+Native+Client+11.0', echo = False)
con = engine.connect()

'''Session = sessionmaker(bind=engine)
session = Session()
metadata = sa.MetaData()'''

#Espacio de la base, molde para preparar la instancia de la base
Base = declarative_base()

#Clase solutionsLog, representacion de la tabla sd_solutionslog
class solutionsLog(Base):
    __tablename__ = 'sd_solutionslog'
    solutionlogid = sa.Column('solutionlogid', sa.Integer(),primary_key = True)
    posttime =  sa.Column('posttime', sa.DateTime() , nullable=False)
    actiontypeid = sa.Column('actiontypeid', sa.Integer(), nullable=False)
    solutionid = sa.Column('solutionid', sa.Integer(), nullable=False)

#Clase action, representacion de la tabla sd_solutionslog
class action(Base):
    __tablename__ = 'sd_actiontypes'
    actiontypeid = sa.Column('actiontypeid', sa.Integer(),primary_key = True)
    name = sa.Column('name', sa.String(255), nullable=False)
    iconurl = sa.Column('iconurl', sa.String(255), nullable=False)

''' -------------------------------------------------------------------------------------------------
-----------------------------------------  Relacion 1 a N   -----------------------------------------
- ------------------------------------------------------------------------------------------------- '''

#Usable tables: solutionsLog, action
#Creacion y declaracion variables tablas, 

'''Se realizan para poder acceder a las clases instanciadas arriba 
    Las cuales tienen la informacion de las tablas de sql
    y se realizan por medio del metodo ___table___ de sqlalchemy
'''
solutions = solutionsLog.__table__
actions = action.__table__

# Query relacion 1 a N
query = sa.select([solutions, actions])
query = query.select_from(solutions.join(
                                        actions,
                                        solutions.columns.actiontypeid == actions.columns.actiontypeid))
#Ejecucion del query
res = con.execute(query)

test = res.fetchall()

#Representacion de las primeras 10 filas de la ejecucion del query
for i in range(0,10):
    print(test[i])

#Representacion de todos los resultados de la ejecucion del query
#Nota: solo quitar el comentario
'''
for i in test:
    print(i)
'''

''' -------------------------------------------------------------------------------------------------
-----------------------------------------  Object Pooling   -----------------------------------------
- ------------------------------------------------------------------------------------------------- '''



''' -------------------------------------------------------------------------------------------------
-----------------------------------------  Object Pooling   -----------------------------------------
- ------------------------------------------------------------------------------------------------- '''
