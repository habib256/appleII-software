#include "hgr_rle.h"

static int read_byte(FILE* input)
{
    return fgetc(input);
}

int hgr_rle_decode_file(FILE* input, unsigned char* dst,
                        unsigned int dst_size)
{
    static const unsigned char magic[4] = { 'H', 'G', 'R', 'R' };
    unsigned int produced = 0;
    unsigned int expected;
    unsigned int i;
    int token;
    int value;

    if (!input || !dst || dst_size != HGR_RLE_DECODED_SIZE) {
        return 0;
    }

    for (i = 0; i < 4; ++i) {
        if (read_byte(input) != magic[i]) {
            return 0;
        }
    }
    if (read_byte(input) != 1 || read_byte(input) != 0) {
        return 0;
    }
    value = read_byte(input);
    if (value == EOF) {
        return 0;
    }
    expected = (unsigned int)value;
    value = read_byte(input);
    if (value == EOF) {
        return 0;
    }
    expected |= (unsigned int)value << 8;
    if (expected != dst_size) {
        return 0;
    }

    while (produced < expected) {
        unsigned int count;
        token = read_byte(input);
        if (token == EOF) {
            return 0;
        }
        if (token & 0x80) {
            count = (unsigned int)(token & 0x7f) + 3u;
            value = read_byte(input);
            if (value == EOF || count > expected - produced) {
                return 0;
            }
            while (count-- != 0u) {
                dst[produced++] = (unsigned char)value;
            }
        } else {
            count = (unsigned int)token + 1u;
            if (count > expected - produced) {
                return 0;
            }
            while (count-- != 0u) {
                value = read_byte(input);
                if (value == EOF) {
                    return 0;
                }
                dst[produced++] = (unsigned char)value;
            }
        }
    }
    return 1;
}
