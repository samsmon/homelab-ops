import struct

fp = "/mnt/hdd-backup/music/Lossless/Vtuber/La Prière ~/純情アンビバレンス/純情アンビバレンス.flac"

with open(fp, 'rb') as f:
    hdr = f.read(4)
    print("header:", hdr)
    while True:
        bh = f.read(4)
        if not bh:
            break
        is_last = (bh[0] & 0x80) != 0
        btype = bh[0] & 0x7F
        blen = (bh[1] << 16) | (bh[2] << 8) | bh[3]
        print(f"block type: {btype}, length: {blen}, is_last: {is_last}")
        if btype == 4:
            data = f.read(blen)
            vlen = struct.unpack('<I', data[0:4])[0]
            vendor = data[4:4+vlen].decode('utf-8', errors='ignore')
            print("vendor:", vendor)
            pos = 4 + vlen
            num = struct.unpack('<I', data[pos:pos+4])[0]
            print("num comments:", num)
            pos += 4
            for i in range(num):
                clen = struct.unpack('<I', data[pos:pos+4])[0]
                pos += 4
                cstr = data[pos:pos+clen].decode('utf-8', errors='ignore')
                pos += clen
                print(f"  comment {i}: {cstr}")
            break
        else:
            f.seek(blen, 1)
        if is_last:
            break
