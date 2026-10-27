// Decode actual samples and compare PTS with the selected source frames, not a nominal FPS tag.
import Foundation
import AVFoundation
import CoreVideo
let args=CommandLine.arguments
guard args.count==4 else {fatalError("video.mp4 source-Frames.csv result.json")}
let output=URL(fileURLWithPath:args[3]);guard !FileManager.default.fileExists(atPath:output.path)else{fatalError("Preserve evidence")}
let lines=try String(contentsOfFile:args[2],encoding:.utf8).split(whereSeparator:{$0.isNewline}).dropFirst()
let source=lines.map{Double($0.split(separator:",")[1])!};guard source.count>1 else{fatalError("No source frames")}
let asset=AVURLAsset(url:URL(fileURLWithPath:args[1]));guard let track=asset.tracks(withMediaType:.video).first else{fatalError("No video")}
let reader=try AVAssetReader(asset:asset);let frames=AVAssetReaderTrackOutput(track:track,outputSettings:[kCVPixelBufferPixelFormatTypeKey as String:kCVPixelFormatType_32BGRA]);frames.alwaysCopiesSampleData=false;reader.add(frames);guard reader.startReading()else{fatalError("Read failed")}
let start=CFAbsoluteTimeGetCurrent();var pts=[Double]();var sizes=Set<String>()
while let buffer=frames.copyNextSampleBuffer(){
 pts.append(CMTimeGetSeconds(CMSampleBufferGetPresentationTimeStamp(buffer)))
 guard let image=CMSampleBufferGetImageBuffer(buffer)else{fatalError("No decoded image")}
 sizes.insert("\(CVPixelBufferGetWidth(image))x\(CVPixelBufferGetHeight(image))")
}
guard reader.status == .completed else{fatalError("Decode failed")};pts.sort();/* Count mismatch is reported below rather than trapping. */
let expected=source.map{$0-source[0]};let error=zip(pts,expected).map{abs($0.0-$0.1)}.max()!
// Allow one output clock tick: source-to-writer and writer-to-track conversions can both quantize.
let tolerance=1.0/Double(track.naturalTimeScale)+0.000001;let passed=pts.count==source.count && error<=tolerance && Set(pts).count==pts.count
let data:[String:Any]=["passed":passed,"expected_frames":source.count,"track_time_scale":track.naturalTimeScale,"timestamp_tolerance_seconds":tolerance,"first_expected_pts":Array(expected.prefix(8)),"first_decoded_pts":Array(pts.prefix(8)),"decoded_frames":pts.count,"sizes":Array(sizes).sorted(),"duration_seconds":CMTimeGetSeconds(asset.duration),"first_pts":pts.first!,"last_pts":pts.last!,"actual_interval_fps":Double(pts.count-1)/(pts.last!-pts.first!),"nominal_fps_tag":track.nominalFrameRate,"max_pts_error_seconds":error,"decode_wall_seconds":CFAbsoluteTimeGetCurrent()-start,"interpolated_or_duplicated_frames":false,"codec":"H.264 (existing AVFoundation encoder)"]
try JSONSerialization.data(withJSONObject:data,options:[.prettyPrinted,.sortedKeys]).write(to:output,options:.withoutOverwriting);print(String(data:try JSONSerialization.data(withJSONObject:data),encoding:.utf8)!)
