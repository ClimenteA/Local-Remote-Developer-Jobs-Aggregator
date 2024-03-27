import playwright from 'playwright';

// node scrapper.js

(async () => {

    console.log("open browser")
    const browser = await playwright.chromium.launch({ headless: false });
    const page = await browser.newPage();

    console.log("go to url")
    await page.goto("https://vuejobs.com/jobs");
    console.log("page loaded")

    console.log("get remote label")
    const elem = page.getByLabel("Remote", { exact: true }).first()

    console.log("elem", elem)
    console.log("click")
    await elem.click()

    console.log("click")

    await page.waitForLoadState("networkidle")

    await browser.close();


})();

