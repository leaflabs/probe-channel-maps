"""
ProbeMapUtils.py, CKC 20160427

Utilities for generating and working with probe channel maps.

Example usage:
>>> from ProbeMapUtils import *
>>> chip2conn = { 0:0, 1:1  }
>>> generate_level2_mapping('64chan/probeMap_64_level1.p', chip2conn, '64chan/probeMap_64_level2.p')
"""

import pickle, os

# chipChan is the channel number local to the chip
ffcTrace2chipChan = {
    0:28,
    1:23,
    2:29,
    3:22,
    4:30,
    5:21,
    6:31,
    7:20,
    8:27,
    9:19,
    10:26,
    11:18,
    12:25,
    13:17,
    14:24,
    15:16,
    #16:ref,
    17:15,
    18:7,
    19:14,
    20:6,
    21:13,
    22:5,
    23:12,
    24:4,
    25:11,
    26:0,
    27:10,
    28:1,
    29:9,
    30:2,
    31:8,
    32:3,
}

def chip2willow(chip, ffcTrace):
    return 32*chip + ffcTrace2chipChan[ffcTrace]

def generate_level2_mapping(level1_picklefile, chip2conn, level2_picklefile):
    """
    chip2conn should be a dictionary containing key:value pairs as chip:conn
    (see README.md for definitions of these variables)
    """
    level1_map = pickle.load(open(level1_picklefile, 'rb'))
    nshanks = level1_map['nshanks']
    nrows = level1_map['nrows']
    ncols = level1_map['ncols']
    level2_map = {}
    conn2chip = {v:k for k,v in chip2conn.items()}
    for shank in range(nshanks):
        for row in range(nrows):
            for col in range(ncols):
                conn, ffcTrace = level1_map[shank,row,col]
                chip = conn2chip[conn]
                willowChan = chip2willow(chip, ffcTrace)
                level2_map[(shank,row,col)] = willowChan
    # metadata
    level2_map['nshanks'] = nshanks
    level2_map['nrows'] = nrows
    level2_map['ncols'] = ncols
    level2_map['chip2conn'] = chip2conn
    # export
    pickle.dump(level2_map, open(level2_picklefile, 'wb'))

def print_chip2conn(level2_pickle):
    level2_map = pickle.load(open(level2_pickle, 'rb'))
    chip2conn = level2_map['chip2conn']
    print ''
    for chip,conn in chip2conn.items():
        print 'Chip %d connects to connector %d' % (chip,conn)
    print ''

def generate_text_file_level1(level1_picklefile, outfile):
    level1_map = pickle.load(open(level1_picklefile, 'rb'))
    nshanks = level1_map['nshanks']
    nrows = level1_map['nrows']
    ncols = level1_map['ncols']
    with open(outfile, 'w') as f:
        f.write('# generated from %s\n' % os.path.basename(level1_picklefile))
        f.write('# nshanks = %d\n' % nshanks)
        f.write('# nrows = %d\n' % nrows)
        f.write('# ncols = %d\n' % ncols)
        f.write('# The following data is in the format:\n')
        f.write('#   shank row col    connector ffcTrace\n')
        f.write('# (see probe-channel-maps/READEME.md for a definition of these coordinates)\n')
        for shank in range(nshanks):
            for row in range(nrows):
                for col in range(ncols):
                    conn, ffcTrace = level1_map[shank,row,col]
                    f.write('%d %d %d    %d %d\n' % (shank, row, col, conn, ffcTrace))
    

def generate_text_file_level2(level2_picklefile, outfile):
    level2_map = pickle.load(open(level2_picklefile, 'rb'))
    nshanks = level2_map['nshanks']
    nrows = level2_map['nrows']
    ncols = level2_map['ncols']
    with open(outfile, 'w') as f:
        f.write('# generated from %s\n' % os.path.basename(level2_picklefile))
        f.write('# nshanks = %d\n' % nshanks)
        f.write('# nrows = %d\n' % nrows)
        f.write('# ncols = %d\n' % ncols)
        f.write('# chip2conn = %s\n' % str(level2_map['chip2conn']))
        f.write('# The following data is in the format:\n')
        f.write('#   shank row col    willowChan\n')
        f.write('# (see probe-channel-maps/READEME.md for a definition of these coordinates)\n')
        for shank in range(nshanks):
            for row in range(nrows):
                for col in range(ncols):
                    willowChan = level2_map[shank,row,col]
                    f.write('%d %d %d    %d\n' % (shank, row, col, willowChan))

