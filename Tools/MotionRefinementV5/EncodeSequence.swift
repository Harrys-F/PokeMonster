// Encode genuine Unreal framebuffer frames using their recorded game timestamps.
// Uses only macOS AVFoundation / ImageIO. No frame interpolation or synthetic frames.
import Foundation
import AVFoundation
import CoreVideo
import ImageIO
import CoreGraphics

let args=CommandLine.arguments
guard args.count==3 else { fatalError("directory output.mp4") }
let directory=URL(fileURLWithPath:args[1])
let output=URL(fileURLWithPath:args[2])
guard !FileManager.default.fileExists(atPath:output.path) else { fatalError("Preserve existing video") }
guard FileManager.default.fileExists(atPath: directory.appendingPathComponent("Frames.csv").path) else {
 print("REVIEW_NOT_EXECUTED: optional Frames.csv is absent; restore archived frames into a separate replay directory or capture new gameplay. Not an animation test pass.")
 exit(ProcessInfo.processInfo.environment["POKEMONSTER_REQUIRE_EVIDENCE"] == "1" ? 2 : 0)
}
let lines=try String(contentsOf:directory.appendingPathComponent("Frames.csv")).split(whereSeparator: {$0.isNewline}).dropFirst()
let rows=lines.map{$0.split(separator:",").map{String($0).trimmingCharacters(in:.whitespacesAndNewlines)}}
guard let first=rows.first else { fatalError("No recorded frames") }
let missingFrames=rows.filter { !FileManager.default.fileExists(atPath:directory.appendingPathComponent($0[5]).path) }
if !missingFrames.isEmpty {
 print("REVIEW_NOT_EXECUTED: \(missingFrames.count) optional source frames absent. Use the verified archive or create a new recording. Not a test pass.")
 exit(ProcessInfo.processInfo.environment["POKEMONSTER_REQUIRE_EVIDENCE"] == "1" ? 2 : 0)
}
let width=Int(first[3])!,height=Int(first[4])!
let firstTime=Double(first[1])!
let writer=try AVAssetWriter(outputURL:output,fileType:.mp4)
let input=AVAssetWriterInput(mediaType:.video,outputSettings:[AVVideoCodecKey:AVVideoCodecType.h264,AVVideoWidthKey:width,AVVideoHeightKey:height,AVVideoCompressionPropertiesKey:[AVVideoAverageBitRateKey:18000000,AVVideoExpectedSourceFrameRateKey:20]])
input.expectsMediaDataInRealTime=false
let adaptor=AVAssetWriterInputPixelBufferAdaptor(assetWriterInput:input,sourcePixelBufferAttributes:[kCVPixelBufferPixelFormatTypeKey as String:kCVPixelFormatType_32BGRA,kCVPixelBufferWidthKey as String:width,kCVPixelBufferHeightKey as String:height,kCVPixelBufferCGImageCompatibilityKey as String:true,kCVPixelBufferCGBitmapContextCompatibilityKey as String:true])
writer.add(input);guard writer.startWriting() else {fatalError("Writer: \(String(describing:writer.error))")}
writer.startSession(atSourceTime:.zero)
for (index,row) in rows.enumerated() {
 while !input.isReadyForMoreMediaData {Thread.sleep(forTimeInterval:0.002)}
 try autoreleasepool {
  let url=directory.appendingPathComponent(row[5])
  guard let source=CGImageSourceCreateWithURL(url as CFURL,nil),let image=CGImageSourceCreateImageAtIndex(source,0,nil) else {fatalError("Image \(url)")}
  var buffer:CVPixelBuffer?
  guard CVPixelBufferPoolCreatePixelBuffer(kCFAllocatorDefault,adaptor.pixelBufferPool!,&buffer)==kCVReturnSuccess,let pixel=buffer else {fatalError("Pixel buffer")}
  CVPixelBufferLockBaseAddress(pixel,[])
  let context=CGContext(data:CVPixelBufferGetBaseAddress(pixel),width:width,height:height,bitsPerComponent:8,bytesPerRow:CVPixelBufferGetBytesPerRow(pixel),space:CGColorSpaceCreateDeviceRGB(),bitmapInfo:CGBitmapInfo.byteOrder32Little.rawValue|CGImageAlphaInfo.premultipliedFirst.rawValue)!
  context.draw(image,in:CGRect(x:0,y:0,width:width,height:height))
  CVPixelBufferUnlockBaseAddress(pixel,[])
  let pts=CMTime(seconds:Double(row[1])!-firstTime,preferredTimescale:60000)
  guard adaptor.append(pixel,withPresentationTime:pts) else {fatalError("Append \(String(describing:writer.error))")}
 }
 if index%200==0 {print("Encoded",index,"/",rows.count)}
}
input.markAsFinished();let finished=DispatchSemaphore(value:0)
writer.finishWriting{finished.signal()};finished.wait()
guard writer.status == .completed else {fatalError("Finish \(String(describing:writer.error))")}
let asset=AVURLAsset(url:output)
let generator=AVAssetImageGenerator(asset:asset)
let preview=try generator.copyCGImage(at:CMTime(seconds:1,preferredTimescale:600),actualTime:nil)
let dest=CGImageDestinationCreateWithURL(output.deletingPathExtension().appendingPathExtension("png") as CFURL,"public.png" as CFString,1,nil)!
CGImageDestinationAddImage(dest,preview,nil);CGImageDestinationFinalize(dest)
print("VIDEO_OK",output.path,"frames",rows.count,"duration",CMTimeGetSeconds(asset.duration),"size",width,height)
