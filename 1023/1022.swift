import SwiftUI
import PlaygroundSupport

struct ContentView: View {
    @State private var text = ""
    var body: some View {
        VStack(spacing: 30) {
            Rectangle()
                .fill(Color.white)
                .frame(width: 200, height: 200)
                .shadow(radius: 3)
            TextField("請輸入文字", text: $text)
                .textFieldStyle(.roundedBorder)
                .padding(.horizontal, 40)
        }
        .padding()
        .background(Color(.systemGroupedBackground))
    }
}

PlaygroundPage.current.setLiveView(ContentView())

