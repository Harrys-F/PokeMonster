// Deterministic map-local lookup for static route distances/widths.
// No model/texture source is altered. PNG uses lossless RGBA8, linear UNORM.
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <random>
#include <vector>
#include <zlib.h>
struct Segment { double ax,ay,bx,by,width; };
std::array<double,2> nearest(double x,double y,const std::vector<Segment>& ss) {
 double d=100000,w=120;
 for(const auto&s:ss){double vx=s.bx-s.ax,vy=s.by-s.ay;double t=std::clamp(((x-s.ax)*vx+(y-s.ay)*vy)/(vx*vx+vy*vy),0.,1.);double a=x-s.ax-vx*t,b=y-s.ay-vy*t;double q=std::hypot(a,b);if(q<d){d=q;w=s.width;}}
 return {d,w};
}
void be32(std::ofstream&f,uint32_t x){char b[]={char(x>>24),char(x>>16),char(x>>8),char(x)};f.write(b,4);}
void chunk(std::ofstream&f,const char*type,const std::vector<uint8_t>&v){be32(f,uint32_t(v.size()));f.write(type,4);f.write((const char*)v.data(),v.size());uLong c=crc32(0,(const Bytef*)type,4);if(!v.empty())c=crc32(c,v.data(),v.size());be32(f,uint32_t(c));}
int main(int argc,char**argv){
 if(argc!=4)return 2;std::ifstream in(argv[1]);std::vector<Segment>ss;Segment s;while(in>>s.ax>>s.ay>>s.bx>>s.by>>s.width)ss.push_back(s);if(ss.size()!=118)return 3;
 constexpr int N=2048;constexpr double X=-7000,Y=-5000,W=11000,H=10000,DR=8192,WR=256;std::vector<uint8_t>pixels(N*N*4);
 for(int y=0;y<N;y++)for(int x=0;x<N;x++){
  auto v=nearest(X+(x+.5)*W/N,Y+(y+.5)*H/N,ss);uint16_t d=uint16_t(std::llround(std::clamp(v[0]/DR,0.,1.)*65535)),w=uint16_t(std::llround(v[1]/WR*65535));size_t i=(size_t(y)*N+x)*4;pixels[i]=d>>8;pixels[i+1]=d&255;pixels[i+2]=w>>8;pixels[i+3]=w&255;
 }
 std::vector<uint8_t>scan((N*4+1)*N);for(int y=0;y<N;y++){size_t row=size_t(y)*(N*4+1);scan[row]=1;for(int x=0;x<N*4;x++)scan[row+1+x]=uint8_t(pixels[size_t(y)*N*4+x]-(x>=4?pixels[size_t(y)*N*4+x-4]:0));}
 uLongf size=compressBound(scan.size());std::vector<uint8_t>zip(size);if(compress2(zip.data(),&size,scan.data(),scan.size(),6)!=Z_OK)return 4;zip.resize(size);
 std::ofstream f(argv[2],std::ios::binary);const unsigned char sig[]={137,80,78,71,13,10,26,10};f.write((const char*)sig,8);std::vector<uint8_t>ihdr={uint8_t(N>>24),uint8_t(N>>16),uint8_t(N>>8),uint8_t(N),uint8_t(N>>24),uint8_t(N>>16),uint8_t(N>>8),uint8_t(N),8,6,0,0,0};chunk(f,"IHDR",ihdr);chunk(f,"IDAT",zip);chunk(f,"IEND",{});f.close();
 auto decode=[&](int x,int y,int channel){x=std::clamp(x,0,N-1);y=std::clamp(y,0,N-1);size_t i=(size_t(y)*N+x)*4+channel;return double(pixels[i]*256+pixels[i+1])/65535*(channel?WR:DR);};
 auto lookup=[&](double x,double y,int c){double u=(x-X)/W*N-.5,v=(y-Y)/H*N-.5;int ix=int(std::floor(u)),iy=int(std::floor(v));double a=u-ix,b=v-iy;return (1-b)*((1-a)*decode(ix,iy,c)+a*decode(ix+1,iy,c))+b*((1-a)*decode(ix,iy+1,c)+a*decode(ix+1,iy+1,c));};
 std::mt19937 rng(584110);std::uniform_real_distribution<double>rx(-6500,3500),ry(-4500,4500);double maxD=0,meanD=0,maxW=0,maxNearD=0;int near=0;std::vector<double>errors;for(int i=0;i<20000;i++){double x=rx(rng),y=ry(rng);auto v=nearest(x,y,ss);double e=std::abs(lookup(x,y,0)-v[0]),we=std::abs(lookup(x,y,2)-v[1]);maxD=std::max(maxD,e);maxW=std::max(maxW,we);meanD+=e;errors.push_back(e);if(v[0]<300){near++;maxNearD=std::max(maxNearD,e);}}
 std::sort(errors.begin(),errors.end());std::ofstream proof(argv[3]);proof<<"{\"resolution\":[2048,2048],\"bounds_cm\":[-7000,-5000,4000,5000],\"segments\":"<<ss.size()<<",\"samples\":20000,\"distance_max_error_cm\":"<<maxD<<",\"distance_mean_error_cm\":"<<meanD/20000<<",\"distance_p95_error_cm\":"<<errors[19000]<<",\"near_path_samples\":"<<near<<",\"near_path_max_error_cm\":"<<maxNearD<<",\"width_max_interpolation_error_cm\":"<<maxW<<",\"resident_bytes_without_mips\":"<<pixels.size()<<",\"png_bytes\":"<<zip.size()+57<<",\"distance_range_cm\":8192,\"width_range_cm\":256,\"interpolation_is_approximate\":true}";std::cout<<"Generated "<<argv[2]<<", max distance error "<<maxD<<" cm\n";
}
