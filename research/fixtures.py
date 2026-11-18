"""Construct a minimal PE32 fixture with one RET instruction; never execute it."""
import struct


def harmless_pe(marker=0):
    data = bytearray(1024)
    data[:2] = b"MZ"
    struct.pack_into("<I", data, 60, 128)
    data[128:132] = b"PE\0\0"
    struct.pack_into("<HHIIIHH", data, 132, 0x14c, 1, 0, 0, 0, 224, 0x102)
    optional = 152
    struct.pack_into("<H", data, optional, 0x10b)
    struct.pack_into("<I", data, optional+4, 512)
    struct.pack_into("<III", data, optional+16, 4096, 4096, 8192)
    struct.pack_into("<III", data, optional+28, 0x400000, 4096, 512)
    struct.pack_into("<HH", data, optional+40, 4, 0)
    struct.pack_into("<HH", data, optional+48, 4, 0)
    struct.pack_into("<II", data, optional+56, 8192, 512)
    struct.pack_into("<H", data, optional+68, 3)
    struct.pack_into("<IIIIII", data, optional+72, 1048576, 4096, 1048576, 4096, 0, 16)
    section = optional+224
    data[section:section+8] = b".text\0\0\0"
    struct.pack_into("<IIII", data, section+8, 1, 4096, 512, 512)
    struct.pack_into("<I", data, section+36, 0x60000020)
    data[512] = 0xc3
    data[-1] = marker
    return bytes(data)
