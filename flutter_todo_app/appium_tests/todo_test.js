const { remote } = require('webdriverio');

// Appium 配置
const capabilities = {
    platformName: 'Android',
    'appium:automationName': 'Flutter',
    'appium:deviceName': 'Android Emulator',
    'appium:app': '../build/app/outputs/flutter-apk/app-debug.apk',
    'appium:autoGrantPermissions': true,
    'appium:noReset': false,
    'appium:fullReset': true
};

const wdOpts = {
    hostname: '127.0.0.1',
    port: 4723,
    logLevel: 'info',
    capabilities,
};

async function runTest() {
    let driver;

    try {
        console.log('🚀 啟動 Appium 測試...');

        // 連接到 Appium server
        driver = await remote(wdOpts);
        console.log('✅ 成功連接到 Appium server');

        // 等待應用啟動
        await driver.pause(3000);
        console.log('✅ 應用已啟動');

        // 測試 1: 驗證初始狀態
        console.log('\n📝 測試 1: 驗證初始狀態');
        const totalCount = await driver.$('~totalCount');
        const totalText = await totalCount.getText();
        console.log(`   總計: ${totalText}`);
        if (!totalText.includes('0')) {
            throw new Error('初始總計應該為 0');
        }
        console.log('   ✅ 初始狀態正確');

        // 測試 2: 新增第一個待辦事項
        console.log('\n📝 測試 2: 新增第一個待辦事項');
        const inputField = await driver.$('~todoInput');
        await inputField.click();
        await inputField.setValue('買菜');

        const addButton = await driver.$('~addButton');
        await addButton.click();
        await driver.pause(1000);

        const newTotalText = await totalCount.getText();
        console.log(`   總計: ${newTotalText}`);
        if (!newTotalText.includes('1')) {
            throw new Error('新增後總計應該為 1');
        }
        console.log('   ✅ 成功新增待辦事項');

        // 測試 3: 新增第二個待辦事項
        console.log('\n📝 測試 3: 新增第二個待辦事項');
        await inputField.click();
        await inputField.setValue('寫程式');
        await addButton.click();
        await driver.pause(1000);

        const secondTotalText = await totalCount.getText();
        console.log(`   總計: ${secondTotalText}`);
        if (!secondTotalText.includes('2')) {
            throw new Error('新增後總計應該為 2');
        }
        console.log('   ✅ 成功新增第二個待辦事項');

        // 測試 4: 完成一個待辦事項
        console.log('\n📝 測試 4: 完成待辦事項');
        const checkbox = await driver.$('~checkbox_0');
        await checkbox.click();
        await driver.pause(1000);

        const completedCount = await driver.$('~completedCount');
        const completedText = await completedCount.getText();
        console.log(`   已完成: ${completedText}`);
        if (!completedText.includes('1')) {
            throw new Error('已完成計數應該為 1');
        }
        console.log('   ✅ 成功標記為已完成');

        // 測試 5: 取消完成狀態
        console.log('\n📝 測試 5: 取消完成狀態');
        await checkbox.click();
        await driver.pause(1000);

        const uncompletedText = await completedCount.getText();
        console.log(`   已完成: ${uncompletedText}`);
        if (!uncompletedText.includes('0')) {
            throw new Error('已完成計數應該恢復為 0');
        }
        console.log('   ✅ 成功取消完成狀態');

        // 測試 6: 刪除待辦事項
        console.log('\n📝 測試 6: 刪除待辦事項');
        const deleteButton = await driver.$('~deleteButton_0');
        await deleteButton.click();
        await driver.pause(1000);

        const finalTotalText = await totalCount.getText();
        console.log(`   總計: ${finalTotalText}`);
        if (!finalTotalText.includes('1')) {
            throw new Error('刪除後總計應該為 1');
        }
        console.log('   ✅ 成功刪除待辦事項');

        // 測試 7: 新增多個待辦事項
        console.log('\n📝 測試 7: 新增多個待辦事項');
        const items = ['運動', '閱讀', '購物'];
        for (const item of items) {
            await inputField.click();
            await inputField.setValue(item);
            await addButton.click();
            await driver.pause(500);
        }

        const multipleTotalText = await totalCount.getText();
        console.log(`   總計: ${multipleTotalText}`);
        if (!multipleTotalText.includes('4')) {
            throw new Error('新增多個項目後總計應該為 4');
        }
        console.log('   ✅ 成功新增多個待辦事項');

        console.log('\n✅ 所有測試通過！');
        console.log('='.repeat(50));
        console.log('測試摘要:');
        console.log('- ✅ 驗證初始狀態');
        console.log('- ✅ 新增待辦事項');
        console.log('- ✅ 完成待辦事項');
        console.log('- ✅ 取消完成狀態');
        console.log('- ✅ 刪除待辦事項');
        console.log('- ✅ 批量新增待辦事項');
        console.log('='.repeat(50));

    } catch (error) {
        console.error('\n❌ 測試失敗:', error.message);
        console.error(error.stack);
        process.exit(1);
    } finally {
        if (driver) {
            await driver.deleteSession();
            console.log('🔚 測試會話已結束');
        }
    }
}

// 執行測試
runTest();
