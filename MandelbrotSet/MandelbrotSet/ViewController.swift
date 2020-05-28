//
//  ViewController.swift
//  Mandelbrot Set
//
//  Created by Sai Hemanth Bheemreddy on 26/05/20.
//  Copyright © 2020 Sai Hemanth Bheemreddy. All rights reserved.
//

import Cocoa
import Metal
import MetalKit

let floatSize = MemoryLayout<Float>.size

class ViewController: NSViewController, MTKViewDelegate {
    
    @IBOutlet weak var display: NSTextField!
    @IBOutlet weak var mtkView: View!
    
    var device: MTLDevice!
    var commandQueue: MTLCommandQueue!
    var computePSO: MTLComputePipelineState!
    var previousTime: Date?

    override func viewDidLoad() {
        super.viewDidLoad()
        
        device = MTLCreateSystemDefaultDevice()!
        commandQueue = device.makeCommandQueue()!
        computePSO = (try? device.makeComputePipelineState(function: device.makeDefaultLibrary()!.makeFunction(name: "compute")!))!
        
        display.isEditable = false
        
        mtkView.parameters = Parameters(size: mtkView.drawableSize,
                                        scale: (x: 0.002, y: 0.002),
                                        pan: (dx: 0, dy: 0),
                                        maxIterations: 64)
        mtkView.device = device
        mtkView.clearColor = MTLClearColor(red: 0, green: 0, blue: 0, alpha: 1)
        mtkView.enableSetNeedsDisplay = true
        mtkView.isPaused = true
        mtkView.framebufferOnly = false
        mtkView.delegate = self
        
        NotificationCenter.default.addObserver(self, selector: #selector(appMovedToBackground), name: NSWindow.didResignMainNotification, object: nil)
        NotificationCenter.default.addObserver(self, selector: #selector(appMovedToForeground), name: NSWindow.didBecomeMainNotification, object: nil)
    }
    
    override func viewDidAppear() {
        mtkView.isPaused = false
    }
    
    override func viewDidDisappear() {
        mtkView.isPaused = true
    }
    
    @objc func appMovedToForeground() {
        mtkView.isPaused = false
    }
    
    @objc func appMovedToBackground() {
        mtkView.isPaused = true
    }
    
    func mtkView(_ view: MTKView, drawableSizeWillChange size: CGSize) {
        let view = view as! View
        view.parameters.set(size: size)
    }
    
    func draw(in view: MTKView) {
        let drawable = view.currentDrawable!
        let view = view as! View
        updateParameters(view)
        
        var buffer: MTLBuffer!
        withUnsafePointer(to: mtkView.parameters) { ptr in
            buffer = device.makeBuffer(bytes: ptr, length: MemoryLayout<Parameters>.size, options: .storageModeShared)
        }
        
        let commandBuffer = commandQueue.makeCommandBuffer()!
        let commandEncoder = commandBuffer.makeComputeCommandEncoder()!
        commandEncoder.setComputePipelineState(computePSO)
        commandEncoder.setTexture(drawable.texture, index: 0)
        commandEncoder.setBuffer(buffer, offset: 0, index: 0)
        
        let threadgroupSizeHeight = 10
        let threadgroupSizeWidth = computePSO.maxTotalThreadsPerThreadgroup / threadgroupSizeHeight
        let gridSize = MTLSize(width: Int(mtkView.parameters.width), height: Int(mtkView.parameters.height), depth: 1)
        let threadgroupSize = MTLSize(width: threadgroupSizeWidth, height: threadgroupSizeHeight, depth: 1)
        commandEncoder.dispatchThreads(gridSize, threadsPerThreadgroup: threadgroupSize)
        commandEncoder.endEncoding()
        
        commandBuffer.present(drawable)
        commandBuffer.addCompletedHandler { [weak self] _ in
            self?.updateDisplay()
        }
        
        commandBuffer.commit()
            
    }
    
    func updateDisplay() {
        guard let previousTime = previousTime else {
            self.previousTime = Date()
            return
        }
            
        let toc = Date()
        let duration = DateInterval(start: previousTime, end: toc).duration * 1000
        DispatchQueue.main.async {
            self.display.stringValue =
            """
            FPS: \(1000 / duration, format: "%.0f")
            Time: \(duration, format: "%.3f") ms
            Max Iterations: \(self.mtkView.parameters.maxIterations)
            """
        }
        self.previousTime = toc
    }
    
    func updateParameters(_ view: View) {
        let heldKeys = view.heldKeys
                
        if heldKeys[12] ?? false || heldKeys[14] ?? false { // Q (zoom out) and E (zoom in)
            let scaleXBy: Float = (heldKeys[12] ?? false) ? 1.01 : 0.99
            let scaleYBy: Float = (heldKeys[12] ?? false) ? 1.01 : 0.99

            view.parameters.scaleX *= scaleXBy
            view.parameters.scaleY *= scaleYBy
        }
        
        if heldKeys[13] ?? false || heldKeys[01] ?? false { // W and S
            view.parameters.panY += 100 * ((heldKeys[13] ?? false) ? 1 : -1)
        }
        
        if heldKeys[00] ?? false || heldKeys[02] ?? false { // A and D
            view.parameters.panX += 100 * ((heldKeys[00] ?? false) ? 1 : -1)
        }
        
        if heldKeys[15] ?? false { // R
            view.parameters = Parameters(size: mtkView.drawableSize,
                                         scale: (x: 0.002, y: 0.002),
                                         pan: (dx: 0, dy: 0),
                                         maxIterations: 64)
        }
    }
    
}

struct Parameters {
    var width: Float
    var height: Float
    var scaleX: Float
    var scaleY: Float
    var panX: Float
    var panY: Float
    var maxIterations: UInt
    
    init(size: CGSize, scale: (x: Float, y: Float), pan: (dx: Float, dy: Float), maxIterations: UInt) {
        self.width = Float(size.width)
        self.height = Float(size.height)
        self.scaleX = scale.x
        self.scaleY = scale.y
        self.panX = Float(size.width / 2) + pan.dx
        self.panY = Float(size.height / 2) + pan.dy
        self.maxIterations = maxIterations
    }
    
    mutating func set(size: CGSize) {
        self.width = Float(size.width)
        self.height = Float(size.height)
    }
}

class View: MTKView {
    
    var parameters: Parameters!
    var heldKeys = [UInt16:Bool]()
    
    override var acceptsFirstResponder: Bool {
        return true
    }
    
    override func keyUp(with event: NSEvent) {
        heldKeys[event.keyCode] = false
    }
    
    override func keyDown(with event: NSEvent) {
        heldKeys[event.keyCode] = true
        
        if heldKeys[06] ?? false { // Z
            parameters.maxIterations += 64
            parameters.maxIterations = max(64, min(2048, parameters.maxIterations))
        }
        
        if heldKeys[07] ?? false { // X
            parameters.maxIterations -= 64
            parameters.maxIterations = max(64, min(2048, parameters.maxIterations))
        }
    }
    
}

extension String.StringInterpolation {
    
    mutating func appendInterpolation(_ value: Double, format: String) {
        appendLiteral(String(format: format, value))
    }
    
}
