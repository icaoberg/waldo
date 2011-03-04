from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
import waldo.subcellular.models
import waldo.subcellular.load
import waldo.subcellular.retrieve
from waldo.translations.services import translate

_testdir = 'tests/data/'

def test_subcellular_retrieve():
    ensembl = 'ENSG00000000003'
    uid = 'HPA000992'

    engine = create_engine('sqlite://')
    metadata = waldo.subcellular.models.Base.metadata
    metadata.bind = engine
    metadata.create_all()
    sessionmaker_ = sessionmaker(engine)
    waldo.subcellular.load.load(_testdir, sessionmaker_)
    session = sessionmaker_()
    locations = waldo.subcellular.retrieve.retrieve_location_annotations(ensembl, session)
    assert len(locations) == 2

test_subcellular_retrieve()
