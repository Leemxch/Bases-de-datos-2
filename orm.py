# Intituto Tecnologico de Costa Rica                            Bases de datos 2
# 2018093728 - Paula Mariana Bustos Vargas
# 2019185076 - Max Richard Lee Chung

''' -------------------------------------------------------------------------------------------------
                                         Caso 1
----------------------------------------------------------------------------------------------------- '''

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

#Coneccion con la base de datos ('mssql+pyodbc://server/databsae?driver=SQL+Server+Native+Client+11.0')
#Echo sirve para visualizar las ejecuciones que realiza
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

#Tablas a usar: solutionsLog, action
#Se declaran las varaibles tablas cuya utilidad es para poder acceder a las clases instanciadas
#anteriormente, las cuales contienen el mapeo a la informacion de las tablas en sql y se utiliza
#el metodo .___table___ de sqlalchemy para tenerlas como formato tablas y manipularlas
solutions = solutionsLog.__table__
actions = action.__table__

# Query relacion 1 a N
# Replica un select con inner join
query = sa.select([solutions, actions])
query = query.select_from(solutions.join(
                                        actions,
                                        solutions.columns.actiontypeid == actions.columns.actiontypeid))
#Ejecucion del query
res = con.execute(query)
#Extrae toda la informacion de la tabla seleccionada 
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

engine = sa.create_engine('mssql+pyodbc://(LocalDb)\MSSQLLocalDB/solutiondesigns?driver=SQL+Server+Native+Client+11.0', 
                            echo = False,
                          
                            #El predeterminado es de 5 y comienza sin conecciones
                            # mayor numero de conexiones que se mantendran.  
                            pool_size = 2,

                            # El valor predeterminado es 10. Cuando esta -1 significa que no tiene limite
                            # Cuando la cantidad de conexiones sobrepasa la capacidad maxima del pool_size, se mantienen en espera, sin embargo, si la cantidad de conexiones sobrepasan el max_overflow, se desconectaran automaticamente
                            max_overflow = 3, 
                          
                   ''' número total de conexiones simultáneas = pool_size + max_overflow '''

                            # Es una funcion propia Pool. El valor predeterminado es -1. 
                            # El numero de segundos entre el reciclaje de la conexión, lo que significa que al finalizar el "checkout", si se supera este tiempo de espera, la conexión se cerrará y se reemplazará por una conexión recién abierta
                            pool_recycle = 150,

                            # El valor predeterminado es 30.0. 
                            # Es el número máximo de segundos de espera al recuperar un nueva conexión desde la piscina. Después de la cantidad de tiempo especificada, se lanzará una excepción.
                            pool_timeout = 50
                        )


''' -------------------------------------------------------------------------------------------------
------------------------------  Transaccion que afecta a más de una tabla  --------------------------
- ------------------------------------------------------------------------------------------------- '''

#Creamos la sesion para la transaccion virtual enlazada al engine con la configuracion del object pooling
Session = sessionmaker(bind=engine)

#Variable para mapear la insercion de datos a las tablas, este caso se da por la columna nombre(name)
nombre = 'pez18_prueba'

#Declaramos la instancia de la sesion con la configuracion del engine 
ses = Session()
#Hacemos insert a la tabla action y luego insert a la tabla solutions mapeando por medio del nombre
ses.add(action(name = nombre ,iconurl = 'some url'))
#El actiontypeid se consigue por medio de un subquery, donde se obtienen las filas con la condicion de que tengan el mismo nombre,
#luego se selecciona la primera fila y, como el resultado es una fila de una tabla, se saca el dato bajo el nombre de actiontypeid
ses.add(solutionsLog(posttime = '2021-08-22', actiontypeid = ses.query(actions).where(actions.columns.name == nombre).first().actiontypeid, solutionid = 4))
#Si no hubo error, se le hace commit y, si hay error, no se hace commit
ses.commit()
