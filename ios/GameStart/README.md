# GameStart iOS App

This directory contains a minimal SwiftUI iOS application that displays a stylised game start screen for an imaginary title called **Edge Quest**.

## Structure

```
GameStart/
├── GameStartApp.swift        // Entry point for the SwiftUI app
├── StartScreen.swift         // Main start screen view
└── Assets.xcassets/          // Accent colour and placeholder app icon definitions
```

## Usage

1. Open the `ios/GameStart` folder in Xcode.
2. Create a new Xcode project (App template) named **GameStart**, targeting iOS 16 or later.
3. Replace the generated SwiftUI files with the versions in this repository.
4. Add the provided asset catalog items to your project's asset catalog.
5. Run the app on the simulator to see the animated start screen with "Start Game" and "Settings" actions.

The `startGame()` and `openSettings()` actions are marked with `TODO:` comments where navigation or presentation logic can be added.
