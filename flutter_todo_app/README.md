# Flutter Todo List App with Appium Tests

一個完整的 Flutter Todo List Android 應用，包含 Appium E2E 自動化測試。

## 📋 功能特性

- ✅ 新增待辦事項
- ✅ 標記完成/未完成
- ✅ 刪除待辦事項
- ✅ 顯示總計和已完成數量
- ✅ 完整的 Appium E2E 測試

## 🏗️ 專案結構

```
flutter_todo_app/
├── lib/
│   └── main.dart                 # Flutter 主應用程式碼
├── android/                      # Android 專案配置
│   ├── app/
│   │   ├── build.gradle         # App 級別 Gradle 配置
│   │   └── src/main/
│   │       ├── AndroidManifest.xml
│   │       └── kotlin/
│   ├── build.gradle             # 專案級別 Gradle 配置
│   ├── settings.gradle
│   └── gradle.properties
├── appium_tests/                # Appium 測試目錄
│   ├── package.json            # Node.js 依賴
│   └── todo_test.js            # E2E 測試腳本
├── pubspec.yaml                # Flutter 依賴配置
└── README.md                   # 本文件
```

## 🚀 快速開始

### 前置需求

1. **Flutter SDK** (3.0.0 或更高版本)
   ```bash
   flutter --version
   ```

2. **Android Studio** 和 **Android SDK**
   - 需要安裝 Android SDK 34
   - 配置 Android 模擬器或連接實體設備

3. **Node.js** (16.0.0 或更高版本)
   ```bash
   node --version
   ```

4. **Appium 2.x**
   ```bash
   npm install -g appium
   appium --version
   ```

5. **Appium Flutter Driver**
   ```bash
   appium driver install flutter
   ```

### 安裝步驟

#### 1. 設置 Flutter 專案

```bash
cd flutter_todo_app

# 安裝 Flutter 依賴
flutter pub get

# 檢查 Flutter 環境
flutter doctor
```

#### 2. 配置 Android 本地屬性

創建 `android/local.properties` 文件：

```properties
sdk.dir=/path/to/your/Android/sdk
flutter.sdk=/path/to/your/flutter
```

例如：
```properties
sdk.dir=/Users/username/Library/Android/sdk
flutter.sdk=/Users/username/development/flutter
```

#### 3. 構建 Android APK

```bash
# 構建 debug APK
flutter build apk --debug

# APK 將生成在: build/app/outputs/flutter-apk/app-debug.apk
```

#### 4. 安裝 Appium 測試依賴

```bash
cd appium_tests
npm install
```

## 📱 運行應用

### 使用 Flutter 運行

```bash
# 啟動模擬器或連接設備後
flutter run

# 或指定設備
flutter devices
flutter run -d <device-id>
```

### 直接安裝 APK

```bash
# 安裝到連接的設備
adb install build/app/outputs/flutter-apk/app-debug.apk

# 啟動應用
adb shell am start -n com.example.flutter_todo_app/.MainActivity
```

## 🧪 運行 Appium 測試

### 步驟 1: 啟動 Appium Server

在一個終端視窗中：

```bash
appium
```

你應該看到：
```
[Appium] Welcome to Appium v2.x.x
[Appium] Appium REST http interface listener started on 0.0.0.0:4723
```

### 步驟 2: 準備 Android 設備

**使用模擬器：**
```bash
# 查看可用的模擬器
emulator -list-avds

# 啟動模擬器
emulator -avd <avd_name>
```

**使用實體設備：**
- 啟用開發者選項
- 啟用 USB 調試
- 連接設備並確認授權

驗證設備連接：
```bash
adb devices
```

### 步驟 3: 運行測試

在另一個終端視窗中：

```bash
cd appium_tests
npm test
```

## ✅ 測試涵蓋範圍

Appium 測試包含以下測試案例：

1. **驗證初始狀態** - 確認應用啟動時總計為 0
2. **新增待辦事項** - 測試新增單個待辦事項
3. **新增多個待辦事項** - 測試批量新增功能
4. **完成待辦事項** - 測試標記完成功能
5. **取消完成狀態** - 測試取消完成功能
6. **刪除待辦事項** - 測試刪除功能
7. **計數器驗證** - 驗證總計和已完成計數正確

### 測試輸出範例

```
🚀 啟動 Appium 測試...
✅ 成功連接到 Appium server
✅ 應用已啟動

📝 測試 1: 驗證初始狀態
   總計: 總計: 0
   ✅ 初始狀態正確

📝 測試 2: 新增第一個待辦事項
   總計: 總計: 1
   ✅ 成功新增待辦事項

...

✅ 所有測試通過！
==================================================
測試摘要:
- ✅ 驗證初始狀態
- ✅ 新增待辦事項
- ✅ 完成待辦事項
- ✅ 取消完成狀態
- ✅ 刪除待辦事項
- ✅ 批量新增待辦事項
==================================================
```

## 🔧 故障排除

### Flutter 問題

**問題：** `flutter command not found`
```bash
# 添加 Flutter 到 PATH
export PATH="$PATH:/path/to/flutter/bin"
```

**問題：** 依賴衝突
```bash
flutter clean
flutter pub get
```

### Android 問題

**問題：** SDK not found
- 確認 `android/local.properties` 路徑正確
- 檢查 Android SDK 安裝完整

**問題：** 構建失敗
```bash
cd android
./gradlew clean
cd ..
flutter build apk --debug
```

### Appium 問題

**問題：** Cannot connect to Appium server
- 確認 Appium server 正在運行（端口 4723）
- 檢查防火牆設置

**問題：** Flutter driver not found
```bash
appium driver list
appium driver install flutter
```

**問題：** App not found
- 確認 APK 路徑正確
- 重新構建 APK: `flutter build apk --debug`

**問題：** 設備連接問題
```bash
# 重啟 adb server
adb kill-server
adb start-server
adb devices
```

## 📝 自定義測試

修改 `appium_tests/todo_test.js` 來添加更多測試案例：

```javascript
// 範例：測試輸入驗證
console.log('\n📝 測試: 空白輸入驗證');
await addButton.click();  // 不輸入內容直接點擊
const emptyTotalText = await totalCount.getText();
// 驗證不應該新增空白項目
```

## 🔑 關鍵配置

### Appium Capabilities

```javascript
{
    platformName: 'Android',
    'appium:automationName': 'Flutter',
    'appium:deviceName': 'Android Emulator',
    'appium:app': '../build/app/outputs/flutter-apk/app-debug.apk',
    'appium:autoGrantPermissions': true,
    'appium:noReset': false,
    'appium:fullReset': true
}
```

### Flutter Key 標記

在 `main.dart` 中使用 `Key` 來標記測試元素：

```dart
TextField(
  key: const Key('todoInput'),
  // ...
)
```

## 📚 相關資源

- [Flutter 官方文檔](https://flutter.dev/docs)
- [Appium 官方文檔](https://appium.io/docs/en/latest/)
- [Appium Flutter Driver](https://github.com/appium/appium-flutter-driver)
- [WebdriverIO](https://webdriverio.com/)

## 📄 授權

MIT License

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！
