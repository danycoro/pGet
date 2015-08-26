import sys
import os
import time
from urllib.request import urlopen
from urllib.request import Request

def a(url):
    file = url.split('/')[-1]
    u = urlopen(url)
    meta = u.info()
    file_size = int(meta.get_all("Content-Length")[0])

    file_dl = 0
    block_sz = 8192

    if os.path.exists(file) and file_size == os.path.getsize(file):
        print("The file '%s' already exist." % file)
        exit()

    elif os.path.exists(file) and file_size != os.path.getsize(file):
        print("Resuming Download")
        f = open(file, "ab")
        dld = os.path.getsize(file)
        print("Downloading: {} Bytes: {}".format(file, file_size))
        while True:
            buffer = u.read(dld)
            if not buffer:
                break
            req = Request(url)
            req.headers['Range'] = 'bytes=%s-%s' % (dld, file_size)
            buffer = urlopen(req).read()

            file_dl += len(buffer)
            f.write(buffer)
            remain = dld * 100./ file_size
            status = "\r%10d [%3.2f%%]" % (file_dl, file_dl * remain / file_size)
            status = status + chr(8)*(len(status)+1)

            time.sleep(1)
            sys.stdout.write(status)
            sys.stdout.flush()

        f.close()
        print("File: %s Downloaded Successfully" % (file))

        exit()

    f = open(file, 'wb')
    print("Downloading: {} Bytes: {}".format(file, file_size))

    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_dl += len(buffer)
        f.write(buffer)
        status = "\r%10d [%3.2f%%]" % (file_dl, file_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)

        time.sleep(1)
        sys.stdout.write(status)
        sys.stdout.flush()

    f.close()
    print("File: %s Downloaded Successfully" % (file))

a(sys.argv[1])
