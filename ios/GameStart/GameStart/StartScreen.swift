import SwiftUI

struct StartScreen: View {
    @State private var isAnimating = false

    var body: some View {
        ZStack {
            LinearGradient(
                gradient: Gradient(colors: [Color("AccentColor"), Color(red: 0.18, green: 0.2, blue: 0.45)]),
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()

            VStack(spacing: 32) {
                VStack(spacing: 12) {
                    Text("Edge Quest")
                        .font(.system(size: 48, weight: .heavy, design: .rounded))
                        .foregroundStyle(.white)
                        .shadow(color: .black.opacity(0.4), radius: 12, x: 0, y: 6)

                    Text("Sharpen your skills and ride the perfect line")
                        .font(.title3.weight(.medium))
                        .multilineTextAlignment(.center)
                        .foregroundStyle(.white.opacity(0.85))
                        .padding(.horizontal, 32)
                }

                Spacer()

                VStack(spacing: 20) {
                    Button(action: startGame) {
                        Text("Start Game")
                            .font(.title2.weight(.bold))
                            .padding(.vertical, 16)
                            .padding(.horizontal, 64)
                            .background(
                                Capsule()
                                    .fill(Color.white)
                                    .shadow(color: .black.opacity(0.3), radius: 12, x: 0, y: 10)
                            )
                            .foregroundStyle(Color(red: 0.16, green: 0.21, blue: 0.4))
                    }
                    .scaleEffect(isAnimating ? 1.04 : 1.0)
                    .animation(
                        .easeInOut(duration: 1.4)
                        .repeatForever(autoreverses: true),
                        value: isAnimating
                    )

                    Button(action: openSettings) {
                        Label("Settings", systemImage: "gearshape.fill")
                            .font(.headline)
                            .padding(.horizontal, 24)
                            .padding(.vertical, 12)
                            .background(
                                Capsule()
                                    .strokeBorder(Color.white.opacity(0.6), lineWidth: 1.5)
                            )
                            .foregroundStyle(Color.white.opacity(0.9))
                    }
                }

                Spacer()

                HStack(spacing: 16) {
                    InfoPill(title: "Story Mode", subtitle: "Explore the frozen city")
                    InfoPill(title: "Time Attack", subtitle: "Beat your best run")
                }
                .padding(.bottom, 32)
                .padding(.horizontal, 16)
            }
            .padding(.top, 80)
            .padding(.horizontal, 16)
        }
        .onAppear {
            isAnimating = true
        }
    }

    private func startGame() {
        // TODO: Hook into navigation stack or coordinator.
    }

    private func openSettings() {
        // TODO: Present settings sheet.
    }
}

struct InfoPill: View {
    let title: String
    let subtitle: String

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(title)
                .font(.headline)
                .foregroundStyle(.white)
            Text(subtitle)
                .font(.subheadline)
                .foregroundStyle(.white.opacity(0.8))
        }
        .padding()
        .frame(maxWidth: .infinity)
        .background(Color.white.opacity(0.18))
        .background(.thinMaterial, in: RoundedRectangle(cornerRadius: 18, style: .continuous))
        .overlay(
            RoundedRectangle(cornerRadius: 18, style: .continuous)
                .stroke(Color.white.opacity(0.25), lineWidth: 1)
        )
    }
}

#Preview {
    StartScreen()
}
