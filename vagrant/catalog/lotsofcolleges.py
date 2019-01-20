from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import College, Region, Base
engine = create_engine('sqlite:///colleges.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# West Region
West = Region(name = "West")
session.add(West)
session.commit()
# Midwest Region
Midwest = Region(name = "Midwest")
session.add(Midwest)
session.commit()
# North Region
North = Region(name = "North")
session.add(North)
session.commit()
# South Region
South = Region(name = "South")
session.add(South)
session.commit()
