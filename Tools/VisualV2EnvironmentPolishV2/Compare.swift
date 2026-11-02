// Proportional copies of genuine matched Unreal images; no image synthesis.
import AppKit
import Foundation
let root=CommandLine.arguments[1]
let scenes=[("Dorf","Dorf und Weg"),("Flussufer","Bachufer und Sicht"),("Lebensraum","Lebensraum und Dekoration")]
let bitmap=NSBitmapImageRep(bitmapDataPlanes:nil,pixelsWide:1600,pixelsHigh:1470,bitsPerSample:8,samplesPerPixel:4,hasAlpha:true,isPlanar:false,colorSpaceName:.deviceRGB,bytesPerRow:0,bitsPerPixel:0)!
NSGraphicsContext.saveGraphicsState(); NSGraphicsContext.current=NSGraphicsContext(bitmapImageRep:bitmap)!
NSColor(calibratedWhite:0.07,alpha:1).setFill();NSRect(x:0,y:0,width:1600,height:1470).fill()
for (i,s) in scenes.enumerated(){
 for (j,profile) in ["NativeBefore01","NativeFinal01"].enumerated(){
  let im=NSImage(contentsOfFile:root+"/"+profile+"/"+s.0+".png")!
  let x=CGFloat(j)*800,y=CGFloat(2-i)*490
  im.draw(in:NSRect(x:x,y:y,width:800,height:450),from:.zero,operation:.copy,fraction:1)
  let title=s.1+(j==0 ? " - vorher":" - nachher")
  (title as NSString).draw(at:NSPoint(x:x+14,y:y+462),withAttributes:[.font:NSFont.systemFont(ofSize:17,weight:.medium),.foregroundColor:NSColor.white])
 }
}
NSGraphicsContext.restoreGraphicsState();try bitmap.representation(using:.png,properties:[:])!.write(to:URL(fileURLWithPath:root+"/VorherNachher.png"))
