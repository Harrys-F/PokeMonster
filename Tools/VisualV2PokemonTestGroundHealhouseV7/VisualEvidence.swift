// Compositions of actual Unreal frames and a clearly labelled measured route chart.
import AppKit
import Foundation
let root=CommandLine.arguments[1]
let out=URL(fileURLWithPath:root+"/Comparisons",isDirectory:true)
try FileManager.default.createDirectory(at:out,withIntermediateDirectories:true)
func canvas(_ w:Int,_ h:Int)->NSBitmapImageRep {let b=NSBitmapImageRep(bitmapDataPlanes:nil,pixelsWide:w,pixelsHigh:h,bitsPerSample:8,samplesPerPixel:4,hasAlpha:true,isPlanar:false,colorSpaceName:.deviceRGB,bytesPerRow:0,bitsPerPixel:0)!;NSGraphicsContext.current=NSGraphicsContext(bitmapImageRep:b)!;NSColor(calibratedWhite:0.06,alpha:1).setFill();NSRect(x:0,y:0,width:w,height:h).fill();return b}
func text(_ s:String,_ x:CGFloat,_ y:CGFloat,_ size:CGFloat=18){(s as NSString).draw(at:NSPoint(x:x,y:y),withAttributes:[.font:NSFont.systemFont(ofSize:size),.foregroundColor:NSColor.white])}
for angle in [0,90,180,270,45] {
 // Two full-aspect images side by side with readable labels, no image synthesis.
 let c=canvas(2560,760)
 for (i,label) in ["EditorRoomBefore01","PIEInterior01"].enumerated(){let image=NSImage(contentsOfFile:root+"/"+label+"/After_Heilhaus_"+String(angle)+".png")!;image.draw(in:NSRect(x:CGFloat(i*1280),y:0,width:1280,height:720),from:.zero,operation:.copy,fraction:1);text(i==0 ? "VORHER — Heilhaus \(angle)°":"NACHHER — Heilhaus \(angle)°",CGFloat(i*1280+14),732)}
 try c.representation(using:.png,properties:[:])!.write(to:out.appendingPathComponent("Heilhaus_\(angle).png"))
}
func load(_ path:String)throws->[String:Any]{try JSONSerialization.jsonObject(with:Data(contentsOf:URL(fileURLWithPath:path)))as![String:Any]}
let b=canvas(1200,660)
for (i,label) in ["NativePondBefore01","NativePondFinal01"].enumerated(){let result=try load(root+"/"+label+"/Result.json");let check=(result["checks"]as![[String:Any]]).first{$0["samples"] != nil}!;let samples=check["samples"]as![[String:Any]];let zone=check["zone"]as![Double];let extent=check["zone_extent"]as![Double];let x=CGFloat(i*600+40);let cx=x+260,cy:CGFloat=335
 func point(_ xx:Double,_ yy:Double)->NSPoint{NSPoint(x:cx+CGFloat(xx-zone[0])*0.29,y:cy+CGFloat(yy-zone[1])*0.29)}
 NSColor(calibratedRed:0.12,green:0.27,blue:0.30,alpha:1).setFill();NSBezierPath(ovalIn:NSRect(x:cx-CGFloat(extent[0])*0.29,y:cy-CGFloat(extent[1])*0.29,width:CGFloat(extent[0])*0.58,height:CGFloat(extent[1])*0.58)).fill()
 if i==1 {let grid=try load(root+"/"+label+"/SwimmableGrid.json");NSColor(calibratedRed:0.55,green:0.78,blue:0.57,alpha:1).setFill();for g in grid["points"]as![[String:Any]]{if let foot=g["safe_foot"]as?[Double]{let p=point(foot[0],foot[1]);NSBezierPath(ovalIn:NSRect(x:p.x-2,y:p.y-2,width:4,height:4)).fill()}}}
 let path=NSBezierPath();var distance=0.0;var previous:[Double]?=nil
 for s in samples {let foot=s["foot"]as![Double];let p=point(foot[0],foot[1]);if let q=previous{path.line(to:p);distance+=hypot(foot[0]-q[0],foot[1]-q[1])}else{path.move(to:p)};previous=foot}
 NSColor(calibratedRed:1,green:0.82,blue:0.44,alpha:1).setStroke();path.lineWidth=2;path.stroke();let first=samples[0]["foot"]as![Double];let p=point(first[0],first[1]);NSColor.white.setFill();NSBezierPath(ovalIn:NSRect(x:p.x-5,y:p.y-5,width:10,height:10)).fill();text(i==0 ? "Vorher: 240 Sekunden":"Final: 360 Sekunden; entfernter Uferstandpunkt",x,620,17);text(String(format:"Beobachtete Route %.1f m; %d blockierte Schritte",distance/100,check["blocked"]as!Int),x,85,16)
}
text("DATENGRAFIK aus echten Positionen — kein Unreal-Spielbild",40,32,17);text("Grün: tiefen-/kollisionsgeprüfte Rasterpunkte. Weiß: Start.",40,10,15)
try b.representation(using:.png,properties:[:])!.write(to:URL(fileURLWithPath:root+"/KarpadorRoute.png"))
