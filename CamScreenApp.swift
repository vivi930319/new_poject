//
//  CamScreenApp.swift
//  CamScreen
//
//  Created by Yunn on 2025/10/29.
//

import SwiftUI

@main
struct CamScreenApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

struct ContentView: View {
    @State private var isFrontCamera = false   // false=後置(灰)，true=前置(淺藍)
    @State private var shotFlash = false       // 拍照閃爍（純視覺效果）
    
    var body: some View {
        GeometryReader { geo in
            VStack(spacing: 0) {
                // MARK: 上方假鏡頭畫面 (80%)
                ZStack {
                    Rectangle()
                        .fill(isFrontCamera
                              ? Color.blue.opacity(0.25)   // 淺藍（前置鏡頭）
                              : Color.gray.opacity(0.80))  // 灰色（後置鏡頭）
                        .frame(height: geo.size.height * 0.8)
                        .overlay(
                            VStack(spacing: 8) {
                                Image(systemName: "camera.fill")
                                    .resizable()
                                    .scaledToFit()
                                    .frame(width: 70, height: 70)
                                    .foregroundColor(.white.opacity(0.9))
                                Text("Camera Preview (示意)")
                                    .foregroundColor(.white)
                                    .font(.headline)
                                Text(isFrontCamera ? "前置鏡頭（淺藍）" : "後置鏡頭（灰色）")
                                    .foregroundColor(.white.opacity(0.95))
                                    .font(.subheadline)
                            }
                        )
                    
                    // 拍照閃爍白光效果
                    if shotFlash {
                        Color.white.opacity(0.25)
                            .frame(height: geo.size.height * 0.8)
                            .transition(.opacity)
                            .allowsHitTesting(false)
                    }
                }
                
                // MARK: 下方控制列 (20%)
                VStack {
                    Spacer()
                    HStack {
                        // 左：相簿按鈕
                        Button {
                            print("Open Album (mock)")
                        } label: {
                            VStack(spacing: 4) {
                                Image(systemName: "photo.on.rectangle")
                                    .font(.title2)
                                Text("相簿")
                                    .font(.caption)
                            }
                            .frame(width: 60, height: 60)
                        }
                        
                        Spacer()
                        
                        // 中：快門按鈕（閃爍動畫）
                        Button {
                            withAnimation(.easeOut(duration: 0.12)) { shotFlash = true }
                            DispatchQueue.main.asyncAfter(deadline: .now() + 0.12) {
                                withAnimation(.easeIn(duration: 0.12)) { shotFlash = false }
                            }
                        } label: {
                            ZStack {
                                Circle().stroke(lineWidth: 6).frame(width: 90, height: 90)
                                Circle().fill(Color.white).frame(width: 70, height: 70)
                            }
                        }
                        .buttonStyle(.plain)
                        
                        Spacer()
                        
                        // 右：切換鏡頭按鈕
                        Button {
                            isFrontCamera.toggle()
                            print("Switched to \(isFrontCamera ? "Front (Blue)" : "Back (Gray)") camera")
                        } label: {
                            VStack(spacing: 4) {
                                Image(systemName: "arrow.triangle.2.circlepath.camera")
                                    .font(.title2)
                                Text(isFrontCamera ? "前置" : "後置")
                                    .font(.caption)
                            }
                            .frame(width: 60, height: 60)
                        }
                    }
                    .padding(.horizontal, 30)
                    .padding(.bottom, 25)
                }
                .frame(height: geo.size.height * 0.2)
                .background(Color(UIColor.systemBackground))
            }
            .ignoresSafeArea(edges: .top)
        }
    }
}
