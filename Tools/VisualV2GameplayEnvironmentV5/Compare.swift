// Labelled layout of real Unreal images, preserving proportions; no synthesis.
import AppKit
import Foundation
let root=CommandLine.arguments[1]
let data=try Data(contentsOf:URL(fileURLWithPath:CommandLine.arguments[2]))
var sites=try JSONSerialization.jsonObject(with:data) as! [[Any]]

func canvas(_ width:Int,_ height:Int)->NSBitmapImageRep {
 let b=NSBitmapImageRep(bitmapDataPlanes:nil,pixelsWide:width,pixelsHigh:height,bitsPerSample:8,samplesPerPixel:4,hasAlpha:true,isPlanar:false,colorSpaceName:.deviceRGB,bytesPerRow:0,bitsPerPixel:0)!
 NSGraphicsContext.current=NSGraphicsContext(bitmapImageRep:b)!;NSColor(calibratedWhite:0.06,alpha:1).setFill();NSRect(x:0,y:0,width:width,height:height).fill();return b
}
let output=URL(fileURLWithPath:root+"/Comparisons",isDirectory:true);try FileManager.default.createDirectory(at:output,withIntermediateDirectories:true)
for site in sites {
 let name=site[0] as! String;let b=canvas(1920,580)
 for (i,folder) in ["BeforeAtlas","AfterAtlas03"].enumerated(){
  guard let im=NSImage(contentsOfFile:root+"/"+(name=="HeilhausSued" ? (i==0 ? "BeforeExtra":"AfterExtra02"):folder)+"/"+name+".png")else{fatalError(name)}
  let x=CGFloat(i)*960;im.draw(in:NSRect(x:x,y:0,width:960,height:540),from:.zero,operation:.copy,fraction:1)
  (name+(i==0 ? " — vorher":" — nachher") as NSString).draw(at:NSPoint(x:x+12,y:552),withAttributes:[.font:NSFont.systemFont(ofSize:18),.foregroundColor:NSColor.white])
 }
 try b.representation(using:.png,properties:[:])!.write(to:output.appendingPathComponent(name+".png"))
}
let rows=(sites.count+2)/3;let all=canvas(1440,rows*300)
for (i,site) in sites.enumerated(){
 let n=site[0]as! String;let x=CGFloat(i%3)*480,y=CGFloat(rows-1-i/3)*300;let im=NSImage(contentsOfFile:root+"/"+(n=="HeilhausSued" ? "AfterExtra02":"AfterAtlas03")+"/"+n+".png")!;im.draw(in:NSRect(x:x,y:y,width:480,height:270),from:.zero,operation:.copy,fraction:1)
 (n as NSString).draw(at:NSPoint(x:x+8,y:y+278),withAttributes:[.font:NSFont.systemFont(ofSize:14),.foregroundColor:NSColor.white])
}
try all.representation(using:.png,properties:[:])!.write(to:URL(fileURLWithPath:root+"/WholeMapContactSheet.png"))
