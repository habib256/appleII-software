#include "Cam16.h"

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <limits>
#include <string>
#include <vector>

namespace {

constexpr int kWidth = 280;
constexpr int kHeight = 192;
constexpr std::size_t kHgrBytes = 8192;

struct Rgb { std::uint8_t r, g, b; };

// Exact POM2 Le Chat Mauve / AppleWin Feline palette.
constexpr Rgb kPalette[2][4] = {
    {{0x00,0x00,0x00}, {0xaa,0x1a,0xd1}, {0x6f,0xe6,0x2c}, {0xff,0xff,0xff}},
    {{0x00,0x00,0x00}, {0x00,0x8a,0xb5}, {0xff,0x72,0x47}, {0xff,0xff,0xff}},
};

std::size_t hgrOffset(int x, int y)
{
    return static_cast<std::size_t>((y & 7) << 10)
         + static_cast<std::size_t>((y & 0x38) << 4)
         + static_cast<std::size_t>((y >> 6) * 40)
         + static_cast<std::size_t>(x / 7);
}

bool readFile(const std::filesystem::path& path, std::vector<std::uint8_t>& out)
{
    std::ifstream in(path, std::ios::binary);
    if (!in) return false;
    in.seekg(0, std::ios::end);
    const auto end = in.tellg();
    if (end < 0) return false;
    out.resize(static_cast<std::size_t>(end));
    in.seekg(0, std::ios::beg);
    return out.empty() || static_cast<bool>(in.read(
        reinterpret_cast<char*>(out.data()), static_cast<std::streamsize>(out.size())));
}

bool writeFile(const std::filesystem::path& path, const std::vector<std::uint8_t>& data)
{
    std::error_code ec;
    std::filesystem::create_directories(path.parent_path(), ec);
    std::ofstream out(path, std::ios::binary | std::ios::trunc);
    if (!out) return false;
    out.write(reinterpret_cast<const char*>(data.data()),
              static_cast<std::streamsize>(data.size()));
    return static_cast<bool>(out);
}

std::vector<std::uint8_t> encodeRle(const std::vector<std::uint8_t>& raw)
{
    std::vector<std::uint8_t> out{'H','G','R','R',1,0,0,0x20};
    std::size_t i = 0;
    while (i < raw.size()) {
        std::size_t run = 1;
        while (i + run < raw.size() && raw[i + run] == raw[i] && run < 130) ++run;
        if (run >= 3) {
            out.push_back(static_cast<std::uint8_t>(0x80u + run - 3));
            out.push_back(raw[i]);
            i += run;
            continue;
        }
        const std::size_t begin = i;
        i += run;
        while (i < raw.size() && i - begin < 128) {
            run = 1;
            while (i + run < raw.size() && raw[i + run] == raw[i] && run < 130) ++run;
            if (run >= 3) break;
            i += run;
        }
        out.push_back(static_cast<std::uint8_t>(i - begin - 1));
        out.insert(out.end(), raw.begin() + static_cast<std::ptrdiff_t>(begin),
                   raw.begin() + static_cast<std::ptrdiff_t>(i));
    }
    return out;
}

bool decodeRle(const std::vector<std::uint8_t>& in, std::vector<std::uint8_t>& raw,
               std::string& error)
{
    if (in.size() < 8 || !std::equal(in.begin(), in.begin() + 4, "HGRR") ||
        in[4] != 1 || in[5] != 0 || in[6] != 0 || in[7] != 0x20) {
        error = "invalid HGRR v1 header";
        return false;
    }
    raw.clear(); raw.reserve(kHgrBytes);
    std::size_t i = 8;
    while (raw.size() < kHgrBytes && i < in.size()) {
        const std::uint8_t token = in[i++];
        if (token & 0x80u) {
            const std::size_t count = (token & 0x7fu) + 3u;
            if (i >= in.size() || count > kHgrBytes - raw.size()) {
                error = "truncated or overflowing repeat run";
                return false;
            }
            raw.insert(raw.end(), count, in[i++]);
        } else {
            const std::size_t count = token + 1u;
            if (count > in.size() - i || count > kHgrBytes - raw.size()) {
                error = "truncated or overflowing literal run";
                return false;
            }
            raw.insert(raw.end(), in.begin() + static_cast<std::ptrdiff_t>(i),
                       in.begin() + static_cast<std::ptrdiff_t>(i + count));
            i += count;
        }
    }
    if (raw.size() != kHgrBytes || i != in.size()) {
        error = raw.size() != kHgrBytes ? "decoded size is not 8192" : "trailing data";
        return false;
    }
    return true;
}

std::vector<std::uint8_t> resampleCover(const std::uint8_t* src, int sw, int sh)
{
    std::vector<std::uint8_t> out(kWidth * kHeight * 3);
    const double scale = std::max(double(kWidth) / sw, double(kHeight) / sh);
    const double cropW = kWidth / scale, cropH = kHeight / scale;
    const double x0 = (sw - cropW) * 0.5, y0 = (sh - cropH) * 0.5;
    for (int y = 0; y < kHeight; ++y) {
        const double sy = y0 + (y + 0.5) / scale - 0.5;
        const int iy0 = std::clamp(static_cast<int>(sy), 0, sh - 1);
        const int iy1 = std::min(iy0 + 1, sh - 1);
        const double fy = std::clamp(sy - iy0, 0.0, 1.0);
        for (int x = 0; x < kWidth; ++x) {
            const double sx = x0 + (x + 0.5) / scale - 0.5;
            const int ix0 = std::clamp(static_cast<int>(sx), 0, sw - 1);
            const int ix1 = std::min(ix0 + 1, sw - 1);
            const double fx = std::clamp(sx - ix0, 0.0, 1.0);
            for (int c = 0; c < 3; ++c) {
                const double a = src[(iy0 * sw + ix0) * 4 + c] * (1.0 - fx)
                               + src[(iy0 * sw + ix1) * 4 + c] * fx;
                const double b = src[(iy1 * sw + ix0) * 4 + c] * (1.0 - fx)
                               + src[(iy1 * sw + ix1) * 4 + c] * fx;
                out[(y * kWidth + x) * 3 + c] = static_cast<std::uint8_t>(
                    std::clamp(a * (1.0 - fy) + b * fy, 0.0, 255.0) + 0.5);
            }
        }
    }
    return out;
}

std::vector<std::uint8_t> imageToHgr(const std::uint8_t* rgba, int sw, int sh)
{
    const auto rgb = resampleCover(rgba, sw, sh);
    std::vector<std::uint8_t> page(kHgrBytes, 0);
    std::array<hgrpaint::Cam16Ucs, 8> paletteCam{};
    for (int bank = 0; bank < 2; ++bank)
        for (int code = 0; code < 4; ++code) {
            const auto c = kPalette[bank][code];
            paletteCam[bank * 4 + code] = hgrpaint::srgb8ToCam16Ucs(c.r, c.g, c.b);
        }

    for (int y = 0; y < kHeight; ++y) {
        std::array<std::uint8_t, kWidth> bits{};
        std::array<std::uint8_t, 40> banks{};
        for (int col = 0; col < 40; ++col) {
            float bestBankCost = std::numeric_limits<float>::max();
            int bestBank = 0;
            std::array<std::uint8_t, 4> bestCodes{};
            for (int bank = 0; bank < 2; ++bank) {
                float bankCost = 0.0f;
                std::array<std::uint8_t, 4> codes{};
                int n = 0;
                const int left = col * 7;
                const int firstPair = (left + 1) / 2;
                const int lastPair = std::min(139, (left + 6) / 2);
                for (int pair = firstPair; pair <= lastPair; ++pair, ++n) {
                    const int x = pair * 2;
                    const int i0 = (y * kWidth + x) * 3;
                    const int i1 = i0 + 3;
                    const auto want = hgrpaint::srgb8ToCam16Ucs(
                        static_cast<std::uint8_t>((rgb[i0] + rgb[i1]) / 2),
                        static_cast<std::uint8_t>((rgb[i0+1] + rgb[i1+1]) / 2),
                        static_cast<std::uint8_t>((rgb[i0+2] + rgb[i1+2]) / 2));
                    float best = std::numeric_limits<float>::max();
                    int bestCode = 0;
                    for (int code = 0; code < 4; ++code) {
                        const auto& got = paletteCam[bank * 4 + code];
                        const float dJ = got.J - want.J, da = got.a - want.a, db = got.b - want.b;
                        const float cost = dJ*dJ + da*da + db*db;
                        if (cost < best) { best = cost; bestCode = code; }
                    }
                    bankCost += best;
                    codes[n] = static_cast<std::uint8_t>(bestCode);
                }
                if (bankCost < bestBankCost) {
                    bestBankCost = bankCost; bestBank = bank; bestCodes = codes;
                }
            }
            banks[col] = static_cast<std::uint8_t>(bestBank);
            int n = 0;
            const int left = col * 7;
            const int firstPair = (left + 1) / 2;
            const int lastPair = std::min(139, (left + 6) / 2);
            for (int pair = firstPair; pair <= lastPair; ++pair, ++n) {
                const int x = pair * 2;
                bits[x] = bestCodes[n] & 1u;
                bits[x + 1] = (bestCodes[n] >> 1) & 1u;
            }
        }
        for (int col = 0; col < 40; ++col) {
            std::uint8_t b = static_cast<std::uint8_t>(banks[col] << 7);
            for (int bit = 0; bit < 7; ++bit) b |= bits[col * 7 + bit] << bit;
            page[hgrOffset(col * 7, y)] = b;
        }
    }
    return page;
}

std::vector<std::uint8_t> renderHgr(const std::vector<std::uint8_t>& page)
{
    std::vector<std::uint8_t> rgb(kWidth * kHeight * 3);
    for (int y = 0; y < kHeight; ++y) {
        std::array<std::uint8_t, kWidth> bits{};
        std::array<std::uint8_t, 40> banks{};
        for (int col = 0; col < 40; ++col) {
            const auto b = page[hgrOffset(col * 7, y)]; banks[col] = b >> 7;
            for (int bit = 0; bit < 7; ++bit) bits[col * 7 + bit] = (b >> bit) & 1u;
        }
        for (int x = 0; x < kWidth; x += 2) {
            const int code = bits[x] | (bits[x + 1] << 1);
            const auto c = kPalette[banks[x / 7]][code];
            for (int q = 0; q < 2; ++q) {
                const int i = (y * kWidth + x + q) * 3;
                rgb[i] = c.r; rgb[i+1] = c.g; rgb[i+2] = c.b;
            }
        }
    }
    return rgb;
}

int usage()
{
    std::cerr << "usage:\n"
              << "  scoswamp_hgr convert INPUT.png OUTPUT.HGR.RLE.BIN [PREVIEW.png]\n"
              << "  scoswamp_hgr encode INPUT.HGR.BIN OUTPUT.HGR.RLE.BIN\n"
              << "  scoswamp_hgr decode INPUT.HGR.RLE.BIN OUTPUT.HGR.BIN\n"
              << "  scoswamp_hgr validate INPUT.HGR.RLE.BIN\n";
    return 2;
}

} // namespace

int main(int argc, char** argv)
{
    if (argc < 3) return usage();
    const std::string command = argv[1];
    std::vector<std::uint8_t> input, raw;
    std::string error;

    if (command == "convert") {
        if (argc < 4 || argc > 5) return usage();
        int w = 0, h = 0, channels = 0;
        stbi_uc* pixels = stbi_load(argv[2], &w, &h, &channels, 4);
        if (!pixels) { std::cerr << "cannot decode " << argv[2] << "\n"; return 1; }
        raw = imageToHgr(pixels, w, h);
        stbi_image_free(pixels);
        const auto packed = encodeRle(raw);
        if (!writeFile(argv[3], packed)) { std::cerr << "cannot write output\n"; return 1; }
        if (argc == 5) {
            const auto preview = renderHgr(raw);
            if (!stbi_write_png(argv[4], kWidth, kHeight, 3, preview.data(), kWidth * 3)) {
                std::cerr << "cannot write preview\n"; return 1;
            }
        }
        std::cout << argv[3] << ": " << packed.size() << " bytes ("
                  << (100.0 * packed.size() / kHgrBytes) << "%)\n";
        return 0;
    }
    if (!readFile(argv[2], input)) { std::cerr << "cannot read input\n"; return 1; }
    if (command == "encode") {
        if (argc != 4 || input.size() != kHgrBytes) {
            std::cerr << "raw HGR input must be exactly 8192 bytes\n"; return 1;
        }
        if (!writeFile(argv[3], encodeRle(input))) return 1;
        return 0;
    }
    if (command == "decode" || command == "validate") {
        if ((command == "decode" && argc != 4) || (command == "validate" && argc != 3))
            return usage();
        if (!decodeRle(input, raw, error)) { std::cerr << error << "\n"; return 1; }
        if (command == "decode" && !writeFile(argv[3], raw)) return 1;
        std::cout << argv[2] << ": valid HGRR v1, 8192 bytes decoded\n";
        return 0;
    }
    return usage();
}
