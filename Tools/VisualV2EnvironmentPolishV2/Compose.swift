// Thumbnail sheet of real Unreal frames; only proportional resizing and labels.
import AppKit
import Foundation
let root = CommandLine.arguments[1]
let entries = [("Blumenwiese","Blumenwiese"),("Waldrand","Waldrand"),("Bachbett","Bach und Ufer"),("Felsgruppe","Felsgruppe"),("Kraeutergarten","Dorf / Kraeutergarten"),("Lebensraum","Pokemon-Lebensraum")]
let bitmap = NSBitmapImageRep(bitmapDataPlanes:nil,pixelsWide:1600,pixelsHigh:1470,bitsPerSample:8,samplesPerPixel:4,hasAlpha:true,isPlanar:false,colorSpaceName:.deviceRGB,bytesPerRow:0,bitsPerPixel:0)!
let ctx = NSGraphicsContext(bitmapImageRep:bitmap)!
NSGraphicsContext.saveGraphicsState(); NSGraphicsContext.current=ctx
NSColor(calibratedWhite:0.07,alpha:1).setFill(); NSRect(x:0,y:0,width:1600,height:1470).fill()
for (i,e) in entries.enumerated() {
 let image = NSImage(contentsOfFile:root+"/NativeFinal01/"+e.0+".png")!
 let x=CGFloat(i%2)*800, y=CGFloat(2-i/2)*490
 image.draw(in:NSRect(x:x,y:y,width:800,height:450),from:.zero,operation:.copy,fraction:1)
 (e.1 as NSString).draw(at:NSPoint(x:x+14,y:y+462),withAttributes:[.font:NSFont.systemFont(ofSize:17,weight:.medium),.foregroundColor:NSColor.white])
}
NSGraphicsContext.restoreGraphicsState()
let data=bitmap.representation(using:.png,properties:[:])!
try data.write(to:URL(fileURLWithPath:root+"/Ergebnisuebersicht.png"))
print(root+"/Ergebnisuebersicht.png")
