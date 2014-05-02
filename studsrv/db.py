from sqlalchemy import create_engine
from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.declarative import declarative_base



engine = create_engine('sqlite:////tmp/test.db',
                       convert_unicode = True,
                       echo = True,
                       echo_pool = False)

session = scoped_session(sessionmaker(autocommit = False,
                                      autoflush = False,
                                      bind = engine))

Base = declarative_base()
Base.query = session.query_property()



class Project(Base):
  __tablename__ = 'projects'
  
  id = Column(String(63),
              unique = True,
              primary_key = True)
  
  image = Column(String(255),
                 nullable = False)
  
  description = Column(Text(),
                       nullable = False)
  
  public = Column(Boolean(),
                  default = True,
                  nullable = False)
  
  container_id = Column(String(255),
                        nullable = False)
  
  created = Column(DateTime,
                   default = func.now(),
                   nullable = False)
  
  enabled = Column(Boolean(),
                   default = True,
                   nullable = False)

  blocked = Column(Text(),
                   default = None,
                   nullable = True)
  
  admins = relationship('Admin',
                        collection_class = attribute_mapped_collection('id'),
                        backref = 'project',
                        cascade = 'all, delete-orphan')



class Admin(Base):
  __tablename__ = 'admins'
  
  id = Column(String(256),
              nullable = False,
              primary_key = True)
  
  project_id = Column(String(256),
                      ForeignKey(Project.id),
                      nullable = False,
                      primary_key = True)



# Creates the database schema
Base.metadata.create_all(bind = engine)
