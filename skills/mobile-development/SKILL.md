---
name: mobile-development
description: Build modern mobile applications with React Native, Flutter, Swift/SwiftUI, and Kotlin/Jetpack Compose. Covers mobile-first design principles, performance optimization (battery, memory, network), offline-first architecture, platform-specific guidelines (iOS HIG, Material Design), testing strategies, security best practices, accessibility, app store deployment, and mobile development mindset. Use when building mobile apps, implementing mobile UX patterns, optimizing for mobile constraints, or making native vs cross-platform decisions.
---

# Mobile Development

Production-ready mobile development with modern frameworks and mobile-first patterns.

## Framework Selection

| Need | Choose |
|------|--------|
| JavaScript team, web sharing | React Native |
| Performance-critical, animations | Flutter |
| Maximum iOS performance | Swift/SwiftUI |
| Maximum Android performance | Kotlin/Compose |
| Rapid prototyping | React Native + Expo |
| Desktop + mobile | Flutter |

## Performance Targets

- App launch: <2 seconds (70% abandon if >3s)
- Memory: <100MB typical screens
- Animation: 60 FPS (16.67ms/frame)
- Battery: <5% drain/hour active use

## Mobile Mindset (10 Commandments)

1. Performance is foundation, not feature
2. Every kilobyte/millisecond matters
3. Offline-first by default
4. User context > developer environment
5. Platform awareness without lock-in
6. Iterate, don't perfect
7. Security and accessibility by design
8. Test on real devices (simulators lie)
9. Architecture scales with complexity
10. Continuous learning is survival

## Reference Documentation

| Document | Description |
|----------|-------------|
| [mobile-frameworks.md](references/mobile-frameworks.md) | React Native, Flutter, Swift, Kotlin comparison |
| [mobile-ios.md](references/mobile-ios.md) | Swift 6, SwiftUI, iOS HIG, App Store |
| [mobile-android.md](references/mobile-android.md) | Kotlin, Compose, Material Design 3 |
| [mobile-best-practices.md](references/mobile-best-practices.md) | Performance, offline-first, security, testing |
| [mobile-debugging.md](references/mobile-debugging.md) | Tools, profiling, crash analysis |
| [mobile-mindset.md](references/mobile-mindset.md) | Thinking patterns, decision frameworks |

## Architecture

- Small-medium apps: MVVM
- Large apps: MVVM + Clean Architecture
- State: Zustand (RN), Riverpod 3 (Flutter), StateFlow (Android)

## Security (OWASP Mobile Top 10)

- OAuth 2.0 + JWT + Biometrics
- Keychain (iOS) / KeyStore (Android)
- Certificate pinning
- Never hardcode credentials

## Common Pitfalls

1. Testing only on simulators
2. Ignoring platform conventions
3. No offline handling
4. Poor memory management
5. Hardcoded credentials
6. No accessibility (excludes 15%+ users)

## Resources

- [React Native](https://reactnative.dev/) | [Flutter](https://flutter.dev/)
- [iOS HIG](https://developer.apple.com/design/human-interface-guidelines/)
- [Material Design](https://m3.material.io/) | [OWASP Mobile](https://owasp.org/www-project-mobile-top-10/)
