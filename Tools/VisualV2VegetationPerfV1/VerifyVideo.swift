import Foundation
import AVFoundation
import AppKit
let input = CommandLine.arguments[1]
let output = CommandLine.arguments[2]
guard !FileManager.default.fileExists(atPath: output) else { print("VERIFY_NOT_WRITTEN: preserve existing preview; choose a new output path"); exit(2) }
let asset = AVURLAsset(url: URL(fileURLWithPath: input))
guard let track = asset.tracks(withMediaType: .video).first else { fatalError("No video track") }
let generator = AVAssetImageGenerator(asset: asset)
generator.appliesPreferredTrackTransform = true
let image = try generator.copyCGImage(at: CMTime(seconds: 0.5, preferredTimescale: 600), actualTime: nil)
let bitmap = NSBitmapImageRep(cgImage: image)
guard let data = bitmap.representation(using: .png, properties: [:]) else { fatalError("No preview") }
try data.write(to: URL(fileURLWithPath: output), options: .withoutOverwriting)
let metadata: [String: Any] = ["width": Int(track.naturalSize.width), "height": Int(track.naturalSize.height), "duration_seconds": CMTimeGetSeconds(asset.duration), "preview_decoded": true]
let json = try JSONSerialization.data(withJSONObject: metadata, options: .sortedKeys)
print(String(data: json, encoding: .utf8)!)
