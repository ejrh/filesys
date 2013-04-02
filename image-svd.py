from database import Connection
import numpy
import Image


FEATURES = [
    'ravg',
    'gavg',
    'bavg',
    'savg',
    'lavg',
    'rsd',
    'gsd',
    'bsd',
    'ssd',
    'lsd',
    'rlavg',
    'glavg',
    'blavg',
]


def main():
    """print 'Connecting'
    db = Connection()
    db.connect()
    
    print 'Reading image data'
    feature_list = ', '.join(FEATURES)
    db.execute(""SELECT %s FROM image"" % feature_list)
    
    print 'Populating array'
    arr = []
    for r in db.fetchall():
        a = []
        for f in FEATURES:
            a.append(r[f])
        arr.append(a)"""
    
    FEATURES = ['x', 'y']
    arr = [
        [0.1, 0.1],
        [0.2, 0.2],
        [0.3, 0.3],
    ]
    
    print 'Calculating principal components'
    data = numpy.array(arr)
    means = numpy.mean(data, axis=0)
    data2 = data - means
    cov = numpy.cov(data2, rowvar=0)
    w,v = numpy.linalg.eig(cov)
    ss = sorted(zip(w, v), reverse=True)
    w,v = zip(*ss)
    w = numpy.array(w)
    v = numpy.array(v)
    
    print 'Principal Components:'
    print '            ' + ', '.join('%05s' % x for x in FEATURES)
    for strength, vector in zip(w, v):
        print '%6.3f -> [%s]' % (strength, ','.join('%6.3f' % x for x in vector))
    
    print 'Projecting data'
    sds = numpy.sqrt(cov.diagonal())
    zscores = data2 / sds
    data3 = numpy.dot(zscores, v.transpose())
    
    mins = numpy.min(data3, axis=0)
    maxs = numpy.max(data3, axis=0)
    spans = maxs - mins
    
    """
    print 'Creating image'
    width = height = 4096
    im = Image.new('RGB', (width, height))
    for v,v2 in zip(data3, data):
        v = (v - mins)/spans
        px = int(v[0] * (width - 1))
        py = int(v[1] * (height - 1))
        #r = int(v2[0]*255)
        #g = int(v2[1]*255)
        #b = int(v2[2]*255)
        r = int(v[2]*255)
        g = int(v[3]*255)
        b = int(v[4]*255)
        im.putpixel((px, py), (r, g, b))
    im.save('svd.png')"""
    
    """for v,v2 in zip(data3, data):
        v = (v - mins)/spans
        print ""sphere { <%0.6f,%0.6f,%0.6f>, 0.0001 pigment { <%0.6f,%0.6f,%0.6f> } }"" % tuple(v[:6])
    """

if __name__ == "__main__":
    main()
