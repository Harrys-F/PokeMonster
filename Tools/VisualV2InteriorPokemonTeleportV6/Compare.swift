// Layout of genuine Unreal frames only. No generated or retouched scene content.
import AppKit
import Foundation
let root=CommandLine.arguments[1]
func canvas(_ w:Int,_ h:Int)->NSBitmapImageRep {
 let b=NSBitmapImageRep(bitmapDataPlanes:nil,pixelsWide:w,pixelsHigh:h,bitsPerSample:8,samplesPerPixel:4,hasAlpha:true,isPlanar:false,colorSpaceName:.deviceRGB,bytesPerRow:0,bitsPerPixel:0)!
 NSGraphicsContext.current=NSGraphicsContext(bitmapImageRep:b)!;NSColor(calibratedWhite:0.05,alpha:1).setFill();NSRect(x:0,y:0,width:w,height:h).fill();return b
}
func label(_ text:String,_ x:CGFloat,_ y:CGFloat){(text as NSString).draw(at:NSPoint(x:x,y:y),withAttributes:[.font:NSFont.systemFont(ofSize:18),.foregroundColor:NSColor.white])}
let output=URL(fileURLWithPath:root+"/Comparisons");try FileManager.default.createDirectory(at:output,withIntermediateDirectories:true)
for yaw in stride(from:0,to:360,by:45){
 let b=canvas(1920,580)
 for (i,folder)in ["PIEBefore02/Before_Heilhaus_","PIERoomPreview01/After_Heilhaus_"].enumerated(){
  let image=NSImage(contentsOfFile:root+"/"+folder+String(yaw)+".png")!;let x=CGFloat(i)*960;image.draw(in:NSRect(x:x,y:0,width:960,height:540),from:.zero,operation:.copy,fraction:1);label("Heilhaus \(yaw)° — \(i==0 ? "vorher":"nachher")",x+12,552)
 }
 try b.representation(using:.png,properties:[:])!.write(to:output.appendingPathComponent("Heilhaus_\(yaw).png"),options:.withoutOverwriting)
}
let b=canvas(1920,580)
for(i,folder)in ["NativeBefore01","NativeAfter01"].enumerated(){let im=NSImage(contentsOfFile:root+"/"+folder+"/Heilhaus.png")!;let x=CGFloat(i)*960;im.draw(in:NSRect(x:x,y:0,width:960,height:540),from:.zero,operation:.copy,fraction:1);label("Heilhaus 12:00 / QHD C75 — \(i==0 ? "vorher":"nachher")",x+12,552)}
try b.representation(using:.png,properties:[:])!.write(to:output.appendingPathComponent("Heilhaus_NativeNoon.png"),options:.withoutOverwriting)
let files=try FileManager.default.contentsOfDirectory(atPath:root+"/PIEImports03").filter{$0.hasPrefix("Import_")&&$0.hasSuffix(".png")}.sorted();guard files.count==49 else{fatalError("Incomplete candidate evidence")}
for page in 0..<3 {
 let subset=Array(files.dropFirst(page*18).prefix(18));let rows=(subset.count+2)/3;let sheet=canvas(1920,rows*400)
 for(i,file)in subset.enumerated(){let x=CGFloat(i%3)*640,y=CGFloat(rows-1-i/3)*400;let im=NSImage(contentsOfFile:root+"/PIEImports03/"+file)!;im.draw(in:NSRect(x:x,y:y,width:640,height:360),from:.zero,operation:.copy,fraction:1);label(file.replacingOccurrences(of:"Import_",with:"").replacingOccurrences(of:".png",with:"")+" — statisch",x+10,y+372)}
 try sheet.representation(using:.png,properties:[:])!.write(to:output.appendingPathComponent("ImportOverview_\(page+1).png"),options:.withoutOverwriting)
}
