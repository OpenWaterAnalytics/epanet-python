

import pytest

from epanet.output import OutputMetadata
from epanet.output import output as oapi


def test_outputmetadata():
    om = OutputMetadata(None)
    
    for attr in oapi.LinkAttribute:
        temp = om.get_attribute_metadata(attr)
    