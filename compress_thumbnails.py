from database import Connection
from PIL import Image
from StringIO import StringIO

def compress(id, thumbnail):
    im = Image.open(StringIO(thumbnail))
    for k in im.info.keys():
        del im.info[k]
    ss = StringIO()
    im.save(ss, 'PNG')
    new_thumbnail = ss.getvalue()
    if len(new_thumbnail) < len(thumbnail):
        return new_thumbnail
    else:
        return None

def main():
    print 'Connecting'
    db = Connection()
    db.connect()

    print 'Compressing thumbnails'
    db.execute("""SELECT id FROM thumbnail""")
    for id, in db.cursor.fetchall():
        db.execute("""SELECT thumbnail FROM thumbnail WHERE id = %d""" % id)
        thumbnail, = db.cursor.fetchone()
        new_thumbnail = compress(id, thumbnail)
        if new_thumbnail:
            db.execute("""UPDATE thumbnail SET thumbnail = %(tn)s WHERE id = %(id)s""", {'tn': db.make_binary(new_thumbnail), 'id': id})
            db.commit()
            print 'Compressed thumbnail %d from %d bytes to %d bytes' % (id, len(thumbnail), len(new_thumbnail))

if __name__ == "__main__":
    main()
