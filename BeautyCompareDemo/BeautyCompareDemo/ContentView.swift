import SwiftUI

// MARK: - 留言資料模型
struct Review: Identifiable {
    let id = UUID()
    let user: String
    let content: String
    let rating: Double
    let date: String
}

// MARK: - 產品資料模型
struct Product: Identifiable {
    let id = UUID()
    let name: String
    let price: Int
    let subtitle: String
    let imageSystemName: String
    let rating: Double
    let reviews: [Review]
}

// MARK: - 假資料
let planA: [Product] = [
    Product(
        name: "亮白精華 30ml",
        price: 1680,
        subtitle: "溫和淡斑・日間輕薄",
        imageSystemName: "sparkles",
        rating: 4.6,
        reviews: [
            Review(user: "小婷", content: "用了三週覺得氣色變好！", rating: 4.5, date: "10/25"),
            Review(user: "Yuna", content: "香味很淡，不會刺鼻～", rating: 5.0, date: "10/28")
        ]
    ),
    Product(
        name: "深層保濕霜 50ml",
        price: 1380,
        subtitle: "乾肌救星・夜間修護",
        imageSystemName: "drop.fill",
        rating: 4.4,
        reviews: [
            Review(user: "Jill", content: "晚上擦完早上不會乾！", rating: 4.3, date: "10/22")
        ]
    )
]
// A 總價 3060

let planB: [Product] = [
    Product(
        name: "玻尿酸精華 30ml",
        price: 1180,
        subtitle: "補水澎潤・不黏膩",
        imageSystemName: "circle.grid.3x3.fill",
        rating: 4.5,
        reviews: [
            Review(user: "Lina", content: "超補水！保濕力滿分～", rating: 4.7, date: "10/29"),
            Review(user: "匿名", content: "有一點點油但還能接受", rating: 3.9, date: "10/30")
        ]
    ),
    Product(
        name: "維他命C乳 50ml",
        price: 880,
        subtitle: "提亮膚色・勻淨",
        imageSystemName: "sun.max.fill",
        rating: 4.2,
        reviews: [
            Review(user: "Sharon", content: "提亮蠻有感，會回購！", rating: 4.3, date: "10/20")
        ]
    )
]
// B 總價 2060

// MARK: - 主畫面
struct ContentView: View {
    @State private var didCheckIn = false
    var totalA: Int { planA.reduce(0) { $0 + $1.price } }
    var totalB: Int { planB.reduce(0) { $0 + $1.price } }

    var body: some View {
        NavigationView {
            VStack(spacing: 12) {
                // 標題
                Text("產品比對區")
                    .font(.title.bold())
                    .padding(.top, 8)
                
                // 比對區：每欄上方有總價
                ScrollView {
                    HStack(alignment: .top, spacing: 12) {
                        VStack(alignment: .leading, spacing: 10) {
                            PriceBadge(title: "方案 A 總價", value: totalA)
                            ProductColumnView(title: "方案 A", products: planA, tint: .blue)
                        }
                        VStack(alignment: .leading, spacing: 10) {
                            PriceBadge(title: "方案 B 總價", value: totalB)
                            ProductColumnView(title: "方案 B", products: planB, tint: .green)
                        }
                    }
                    .padding(.horizontal)
                }

                // 打卡按鈕
                Button {
                    didCheckIn = true
                } label: {
                    Text(didCheckIn ? "今日已打卡 ✅" : "每日打卡")
                        .font(.headline)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(didCheckIn ? Color.gray.opacity(0.25) : Color.accentColor)
                        .foregroundColor(didCheckIn ? .primary : .white)
                        .clipShape(RoundedRectangle(cornerRadius: 12))
                }
                .padding()
                .alert("打卡成功", isPresented: $didCheckIn) {
                    Button("知道了", role: .cancel) {}
                } message: {
                    Text("已完成今日任務。")
                }
            }
            .navigationBarHidden(true)
        }
    }
}

// MARK: - 總價徽章
struct PriceBadge: View {
    let title: String
    let value: Int
    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(title).font(.caption)
            Text("NT$ \(value)")
                .font(.headline)
                .padding(.horizontal, 8).padding(.vertical, 6)
                .background(Color.secondary.opacity(0.12))
                .clipShape(RoundedRectangle(cornerRadius: 8))
        }
    }
}

// MARK: - 單欄容器
struct ProductColumnView: View {
    let title: String
    let products: [Product]
    let tint: Color

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text(title)
                .font(.headline)
                .padding(.horizontal, 8)
                .padding(.vertical, 4)
                .background(tint.opacity(0.15))
                .clipShape(RoundedRectangle(cornerRadius: 8))

            ForEach(products) { product in
                ProductCard(product: product)
            }
        }
    }
}

// MARK: - 單一卡片（含評論按鈕）
struct ProductCard: View {
    let product: Product
    @State private var showReviews = false

    var body: some View {
        VStack(spacing: 8) {
            // 圖片
            ZStack {
                RoundedRectangle(cornerRadius: 12)
                    .fill(Color.secondary.opacity(0.08))
                    .frame(height: 100)
                Image(systemName: product.imageSystemName)
                    .resizable()
                    .scaledToFit()
                    .frame(width: 40, height: 40)
                    .foregroundColor(.accentColor)
            }

            // 文字描述
            VStack(alignment: .leading, spacing: 4) {
                Text(product.name)
                    .font(.subheadline.bold())
                Text(product.subtitle)
                    .font(.caption)
                    .foregroundColor(.secondary)
                HStack {
                    Image(systemName: "star.fill")
                        .font(.caption2)
                        .foregroundColor(.yellow)
                    Text(String(format: "%.1f", product.rating))
                        .font(.subheadline)
                    Spacer()
                    Button {
                        showReviews = true
                    } label: {
                        Text("查看評論")
                            .font(.caption)
                            .foregroundColor(.blue)
                    }
                }
                Text("NT$ \(product.price)")
                    .font(.subheadline)
                    .foregroundColor(.blue)
            }
            .padding(.horizontal, 6)
            .padding(.bottom, 6)
        }
        .padding(8)
        .background(Color.white.opacity(0.9))
        .clipShape(RoundedRectangle(cornerRadius: 14))
        .shadow(color: .black.opacity(0.05), radius: 3, y: 2)
        // 彈出評論視窗
        .sheet(isPresented: $showReviews) {
            ReviewSheet(product: product)
        }
    }
}

// MARK: - 留言區視窗
struct ReviewSheet: View {
    let product: Product
    @Environment(\.dismiss) private var dismiss
    @State private var newComment = ""

    var body: some View {
        NavigationView {
            VStack(alignment: .leading, spacing: 12) {
                Text(product.name)
                    .font(.headline)
                    .padding(.top)
                
                ScrollView {
                    ForEach(product.reviews) { review in
                        VStack(alignment: .leading, spacing: 4) {
                            HStack {
                                Text(review.user).font(.subheadline.bold())
                                Spacer()
                                Text(review.date).font(.caption).foregroundColor(.secondary)
                            }
                            HStack(spacing: 3) {
                                Image(systemName: "star.fill")
                                    .foregroundColor(.yellow)
                                    .font(.caption2)
                                Text(String(format: "%.1f", review.rating))
                                    .font(.caption)
                            }
                            Text(review.content)
                                .font(.subheadline)
                                .padding(.bottom, 4)
                            Divider()
                        }
                    }
                }

                // 新留言區
                HStack {
                    TextField("輸入你的評論...", text: $newComment)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                    Button("送出") {
                        newComment = ""
                    }
                    .buttonStyle(.borderedProminent)
                }
                .padding(.vertical)

                Spacer()
            }
            .padding(.horizontal)
            .navigationTitle("評論區")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("關閉") { dismiss() }
                }
            }
        }
    }
}

// MARK: - 預覽
#Preview {
    ContentView()
}
