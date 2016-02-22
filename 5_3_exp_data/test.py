# pylint: disable=invalid-name, missing-docstring
import handler
import numpy as np

handler.download_data()
blocks = handler.get_data()

for block in blocks:
    for rec in block.recordingchannelgroups:
        print rec
