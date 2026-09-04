#include "hgrpaint/HgrConvert.h"
#include "hgrpaint/HgrPaintModel.h"

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

#include <algorithm>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

namespace {
constexpr std::size_t kDhgrBytes = 16384;
constexpr std::size_t kHgrBytes = 8192;
struct Rgb { std::uint8_t r, g, b; };
constexpr Rgb kPalette[16] = {
    {0x00,0x00,0x00},{0xa7,0x0b,0x40},{0x40,0x1c,0xf7},{0xe6,0x28,0xff},
    {0x00,0x74,0x40},{0x80,0x80,0x80},{0x19,0x90,0xff},{0xbf,0x9c,0xff},
    {0x40,0x63,0x00},{0xe6,0x6f,0x00},{0x80,0x80,0x80},{0xff,0x8b,0xbf},
    {0x19,0xd7,0x00},{0xbf,0xe3,0x08},{0x58,0xf4,0xbf},{0xff,0xff,0xff}
};

bool writeFile(const std::filesystem::path& p, const std::vector<std::uint8_t>& v) {
    std::error_code ec; std::filesystem::create_directories(p.parent_path(), ec);
    std::ofstream out(p, std::ios::binary | std::ios::trunc);
    return out && static_cast<bool>(out.write(reinterpret_cast<const char*>(v.data()), v.size()));
}

bool readFile(const std::filesystem::path& p, std::vector<std::uint8_t>& v) {
    std::ifstream in(p, std::ios::binary);
    if (!in) return false;
    in.seekg(0, std::ios::end); const auto n=in.tellg(); if (n<0) return false;
    v.resize(static_cast<std::size_t>(n)); in.seekg(0, std::ios::beg);
    return v.empty() || static_cast<bool>(in.read(reinterpret_cast<char*>(v.data()), v.size()));
}

bool decode(const std::vector<std::uint8_t>& in, std::vector<std::uint8_t>& raw) {
    static const std::uint8_t hdr[8]={'D','H','R','R',1,0,0,0x40};
    if (in.size()<8 || !std::equal(hdr,hdr+8,in.begin())) return false;
    raw.clear(); raw.reserve(kDhgrBytes);
    for (std::size_t i=8; raw.size()<kDhgrBytes && i<in.size();) {
        const auto t=in[i++];
        if (t&0x80) { const std::size_t n=(t&0x7f)+3; if(i>=in.size()||n>kDhgrBytes-raw.size()) return false; raw.insert(raw.end(),n,in[i++]); }
        else { const std::size_t n=t+1; if(n>in.size()-i||n>kDhgrBytes-raw.size()) return false; raw.insert(raw.end(),in.begin()+i,in.begin()+i+n); i+=n; }
        if (raw.size()==kDhgrBytes) return i==in.size();
    }
    return false;
}

bool decodeHgr(const std::vector<std::uint8_t>& in, std::vector<std::uint8_t>& raw) {
    static const std::uint8_t hdr[8]={'H','G','R','R',1,0,0,0x20};
    if (in.size()<8 || !std::equal(hdr,hdr+8,in.begin())) return false;
    raw.clear(); raw.reserve(kHgrBytes);
    for (std::size_t i=8; raw.size()<kHgrBytes && i<in.size();) {
        const auto t=in[i++];
        if (t&0x80) { const std::size_t n=(t&0x7f)+3; if(i>=in.size()||n>kHgrBytes-raw.size()) return false; raw.insert(raw.end(),n,in[i++]); }
        else { const std::size_t n=t+1; if(n>in.size()-i||n>kHgrBytes-raw.size()) return false; raw.insert(raw.end(),in.begin()+i,in.begin()+i+n); i+=n; }
        if (raw.size()==kHgrBytes) return i==in.size();
    }
    return false;
}

std::size_t hgrOffset(int col,int y) {
    return std::size_t((y&7)<<10)+std::size_t((y&0x38)<<4)+std::size_t((y>>6)*40)+col;
}

std::vector<std::uint8_t> renderOldHgr(const std::vector<std::uint8_t>& page) {
    static constexpr Rgb banks[2][4]={
        {{0,0,0},{0xaa,0x1a,0xd1},{0x6f,0xe6,0x2c},{255,255,255}},
        {{0,0,0},{0,0x8a,0xb5},{0xff,0x72,0x47},{255,255,255}}
    };
    std::vector<std::uint8_t> rgba(280*192*4,255);
    for(int y=0;y<192;++y){std::uint8_t bits[280]{},bank[40]{};
        for(int col=0;col<40;++col){const auto b=page[hgrOffset(col,y)];bank[col]=b>>7;for(int k=0;k<7;++k)bits[col*7+k]=(b>>k)&1;}
        for(int x=0;x<280;x+=2){const auto c=banks[bank[x/7]][bits[x]|(bits[x+1]<<1)];for(int q=0;q<2;++q){auto o=(y*280+x+q)*4;rgba[o]=c.r;rgba[o+1]=c.g;rgba[o+2]=c.b;}}
    }
    return rgba;
}

std::vector<std::uint8_t> encode(const std::vector<std::uint8_t>& raw) {
    std::vector<std::uint8_t> out{'D','H','R','R',1,0,0,0x40};
    for (std::size_t i = 0; i < raw.size();) {
        std::size_t run = 1;
        while (i + run < raw.size() && raw[i + run] == raw[i] && run < 130) ++run;
        if (run >= 3) { out.push_back(std::uint8_t(0x80 + run - 3)); out.push_back(raw[i]); i += run; continue; }
        const auto begin = i; i += run;
        while (i < raw.size() && i - begin < 128) {
            run = 1; while (i + run < raw.size() && raw[i + run] == raw[i] && run < 130) ++run;
            if (run >= 3) break; i += run;
        }
        out.push_back(std::uint8_t(i - begin - 1));
        out.insert(out.end(), raw.begin() + begin, raw.begin() + i);
    }
    return out;
}

std::vector<std::uint8_t> preview(const std::vector<std::uint8_t>& pair) {
    constexpr int w = 280, h = 192;
    std::vector<std::uint8_t> rgb(w * h * 3);
    for (int y = 0; y < h; ++y) for (int x = 0; x < 140; ++x) {
        const auto c = kPalette[hgrpaint::dhgrColorAt(pair.data(), x, y) & 15];
        for (int q = 0; q < 2; ++q) { const auto o = (y * w + x * 2 + q) * 3; rgb[o]=c.r; rgb[o+1]=c.g; rgb[o+2]=c.b; }
    }
    return rgb;
}
}

int main(int argc, char** argv) {
    if (argc>=3 && std::string(argv[1])=="validate") {
        std::vector<std::uint8_t> packed,raw;
        if(!readFile(argv[2],packed)||!decode(packed,raw)){std::cerr<<"invalid DHRR v1 stream\n";return 1;}
        std::cout<<argv[2]<<": valid DHRR v1, 16384 bytes decoded\n"; return 0;
    }
    if (argc==4 && std::string(argv[1])=="migrate-hgr") {
        std::vector<std::uint8_t> packed,hgr;
        if(!readFile(argv[2],packed)||!decodeHgr(packed,hgr)){std::cerr<<"invalid HGRR v1 stream\n";return 1;}
        const auto rgba=renderOldHgr(hgr); std::vector<std::uint8_t> pair(kDhgrBytes);
        hgrpaint::ImportOptions opt; opt.stretch=true; opt.dither=false;
        hgrpaint::imageToDhgrPage(rgba.data(),280,192,opt,pair.data());
        if(!writeFile(argv[3],encode(pair))) return 1;
        return 0;
    }
    if (argc < 4 || std::string(argv[1]) != "convert") {
        std::cerr << "usage:\n  scoswamp_dhgr convert INPUT.png OUTPUT.DHGR.RLE.BIN [PREVIEW.png]\n  scoswamp_dhgr migrate-hgr INPUT.HGR.RLE.BIN OUTPUT.DHGR.RLE.BIN\n  scoswamp_dhgr validate INPUT.DHGR.RLE.BIN\n"; return 2;
    }
    int w=0,h=0,n=0; auto* rgba = stbi_load(argv[2], &w, &h, &n, 4);
    if (!rgba) { std::cerr << "cannot decode " << argv[2] << "\n"; return 1; }
    std::vector<std::uint8_t> pair(kDhgrBytes);
    hgrpaint::ImportOptions opt; opt.stretch=true; opt.dither=false; opt.chromaWeight=2.4f;
    hgrpaint::imageToDhgrPage(rgba, w, h, opt, pair.data()); stbi_image_free(rgba);
    const auto packed = encode(pair);
    if (!writeFile(argv[3], packed)) { std::cerr << "cannot write output\n"; return 1; }
    if (argc >= 5) { const auto rgb=preview(pair); if (!stbi_write_png(argv[4],280,192,3,rgb.data(),280*3)) return 1; }
    std::cout << argv[3] << ": " << packed.size() << " bytes (DHGR 140x192, 16 colours)\n";
    return 0;
}
