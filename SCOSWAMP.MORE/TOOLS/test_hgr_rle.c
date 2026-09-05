#include "hgr_rle.h"

#include <assert.h>
#include <stdio.h>
#include <string.h>

static FILE* stream_from(const unsigned char* bytes, size_t size)
{
    FILE* f = tmpfile();
    assert(f != NULL);
    assert(fwrite(bytes, 1, size, f) == size);
    rewind(f);
    return f;
}

static void test_repeat_page(void)
{
    unsigned char stream[8 + 126 * 2 + 5];
    unsigned char page[HGR_RLE_DECODED_SIZE];
    size_t i;
    memcpy(stream, "DHRR\1\0\0\100", 8);
    for (i = 0; i < 126; ++i) {
        stream[8 + i * 2] = 0xff;     /* 130 copies */
        stream[9 + i * 2] = 0x5a;
    }
    stream[8 + 126 * 2] = 3;         /* final four literal bytes */
    memset(stream + 9 + 126 * 2, 0x5a, 4);
    {
        FILE* f = stream_from(stream, sizeof(stream));
        assert(hgr_rle_decode_file(f, page, sizeof(page)) == 1);
        fclose(f);
    }
    for (i = 0; i < sizeof(page); ++i) assert(page[i] == 0x5a);
}

static void test_literal_page(void)
{
    unsigned char stream[8 + 128 * 129];
    unsigned char page[HGR_RLE_DECODED_SIZE];
    size_t i, p = 8;
    memcpy(stream, "DHRR\1\0\0\100", 8);
    for (i = 0; i < 128; ++i) {
        size_t n;
        stream[p++] = 127;
        for (n = 0; n < 128; ++n) stream[p++] = (unsigned char)(i + n);
    }
    {
        FILE* f = stream_from(stream, p);
        assert(hgr_rle_decode_file(f, page, sizeof(page)) == 1);
        fclose(f);
    }
    assert(page[0] == 0 && page[127] == 127 && page[128] == 1);
}

static void test_rejections(void)
{
    unsigned char page[HGR_RLE_DECODED_SIZE];
    unsigned char bad_magic[] = "BADR\1\0\0\100";
    unsigned char truncated[] = "DHRR\1\0\0\100\177";
    unsigned char overflow[] = "DHRR\1\0\0\100\377\0";
    FILE* f = stream_from(bad_magic, sizeof(bad_magic) - 1);
    assert(hgr_rle_decode_file(f, page, sizeof(page)) == 0); fclose(f);
    f = stream_from(truncated, sizeof(truncated) - 1);
    assert(hgr_rle_decode_file(f, page, sizeof(page)) == 0); fclose(f);
    f = stream_from(overflow, sizeof(overflow) - 1);
    assert(hgr_rle_decode_file(f, page, sizeof(page)) == 0); fclose(f);
    f = stream_from((const unsigned char*)"DHRR\1\0\0\100", 8);
    assert(hgr_rle_decode_file(f, page, 4096) == 0); fclose(f);
}

int main(void)
{
    test_repeat_page();
    test_literal_page();
    test_rejections();
    puts("dhgr_rle: PASS");
    return 0;
}
