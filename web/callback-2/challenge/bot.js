// puppeteer bot that sets httponly cookie
import puppeteer from 'puppeteer';
import { URL } from 'url';

const FLAG = process.env.FLAG || 'maple{fake_flag}';

const DOMAIN = new URL(process.env.HOSTED_URL || 'http://localhost:1337/');
const username = 'admin';
const password = '5t709cgsb9j9zvemjppwos';

const flagCookie = {
    name: 'flag',
    value: FLAG,
    domain: DOMAIN.hostname,
    httpOnly: false,
    secure: false,
    sameSite: 'Lax',
    priority: 'High',
}

export default async function visit(url) {
    try {
        // uses chromium by default
        const browser = await puppeteer.launch({
            headless: true,
            args: ['--no-sandbox', '--disable-setuid-sandbox'],
            executablePath: process.env.CHROME_BIN || undefined,
        });
        const loginPage = await browser.newPage();
        await loginPage.goto(`${DOMAIN.href}login`, {
            waitUntil: 'networkidle0',
        });
        await loginPage.type('[name="username"]', username);
        await loginPage.type('[name="password"]', password);
        await loginPage.click('#login-btn');
        await loginPage.close();

        const page = await browser.newPage();
        await page.setCookie(flagCookie);
        await page.goto(url.href, {
            waitUntil: 'networkidle0',
        });
        await browser.close();
        return true;
    } catch (e) {
        console.log(e);
        return false;
    }
}
