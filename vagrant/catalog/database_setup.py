import sys
# helpful for mapper code
from sqlalchemy import Column, ForeignKey, Integer, String
#will use in configuration and class code
from sqlalchemy.ext.declarative import declarative_base
# to create foreign key relationship to be used w/ mapper
from sqlalchemy.orm import relationship
#will use in configuration code at the end
from sqlalchemy import create_engine

# creates instance of imported class called base letting SQL know that our classes are special classes that correspond to tables in our database
Base = declarative_base()

class Region(Base):
    __tablename__='region'
    # region name
    name = Column(String(80), nullable = False)
    # each region has an id
    id = Column(Integer, primary_key = True)


# class name will be in camel case
class College(Base):
    __tablename__='college'
    # name of college
    name = Column(String(80), nullable = False)
    # college id
    college_id = Column(Integer, primary_key = True)
    # picture of college
    image_filename = Column(String(100))
    # location
    location = Column(String(200))
    # phone number
    phone_number = Column(String(20))
    # type of college
    college_type = Column(String(100))
    # client notes
    notes = Column(String(9999))
    # id of region college is in
    college_region_id = Column(Integer, ForeignKey('region.id'))
    # get more info from corresponding region
    college_region = relationship(Region)

    @property
    def serialize(self):
        # returns object data in easily serializeable format
        return {
        'name': self.name,
        'college_id': self.college_id,
        'region': self.region,
        'location': self.location,
        'phone_number': self.phone_number,
        'college_type': self.college_type,
        'notes': self.notes
        }


#####################################################################   Insert At End Of File  #####################################################################

# create instance of create_engine class and pt to database we will use
engine = create_engine('sqlite:///colleges.db')
# adds classes we create as tables in our database
Base.metadata.create_all(engine)
