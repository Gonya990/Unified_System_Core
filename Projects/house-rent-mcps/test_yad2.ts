import { addExtra } from 'puppeteer-extra';
import vanillaPuppeteer from 'puppeteer-core';
import StealthPlugin from 'puppeteer-extra-plugin-stealth';
import { execSync } from 'child_process';

const puppeteer = addExtra(vanillaPuppeteer);
puppeteer.use(StealthPlugin());

const USER_AGENT = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36";

async function main() {
    console.log("Starting Yad2 Data Dump...");

    let chromePath = '';
    try {
        chromePath = execSync('which chromium').toString().trim();
    } catch {
        chromePath = execSync('which google-chrome-stable').toString().trim();
    }

    const browser = await puppeteer.launch({
        headless: false,
        executablePath: chromePath,
        userDataDir: './yad2-session-data',
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-blink-features=AutomationControlled'
        ]
    });

    try {
        const page = await browser.newPage();
        await page.setUserAgent(USER_AGENT);
        await page.setViewport({ width: 375, height: 812, isMobile: true, hasTouch: true });

        console.log("Navigating to Search Page...");
        const cityEncoded = encodeURIComponent("קרית ביאליק");
        const searchUrl = `https://www.yad2.co.il/realestate/rent?city=${cityEncoded}`;

        await page.goto(searchUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });

        if (await page.title() === "ShieldSquare Captcha") {
            console.log("Blocked by Captcha. Please solve in the browser window.");
            await new Promise(r => setTimeout(r, 30000));
        }

        const data = await page.evaluate(() => {
            const nextData = document.getElementById('__NEXT_DATA__');
            return nextData ? JSON.parse(nextData.innerHTML) : null;
        });

        if (data && data.props?.pageProps) {
            const props = data.props.pageProps;
            console.log("Writing props to yad2_props.json...");
            // Use node fs since Bun.write might be tricky in some environments or if Bun types are missing
            const fs = require('fs');
            fs.writeFileSync('yad2_props.json', JSON.stringify(props, null, 2));
            console.log("Done. Keys:", Object.keys(props));
        } else {
            console.log("No data found.");
            await page.screenshot({ path: 'no_data.png' });
        }

    } catch (error) {
        console.error("Error:", error);
    } finally {
        await browser.close();
    }
}

main();
