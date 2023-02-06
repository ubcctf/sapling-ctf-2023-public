import puppeteer from 'puppeteer';
import { URL } from 'url';

const url = new URL(process.env.HOSTED_URL || "http://localhost:1337");

const poem = `My local lover, you light up my days
With your smile and your touch in so many ways
You are my home, my refuge, my guide
In your arms, I am safe and I can hide

From the world and its troubles, you're my escape
With you, my heart is full, it can't be replaced
Your love is my compass, my north star
In your embrace, I feel loved, safe and far

You are the one that makes my heart sing
With you, I feel like I can do anything
I am yours, my love, forever and always
With you, my heart is full of love and praise.`; // thanks chatgpt lmao

const present = {
    name: 'present',
    value: encodeURIComponent(poem),
    domain: url.hostname,
    path: '/fraternize',
    httpOnly: true, // well packaged and secured
    secure: false,
    sameSite: 'Lax',
}

// it is my time
export default async function visit(url) {
    // uses chromium by default
    try {
        const browser = await puppeteer.launch({
            headless: true,
            args: [
                '--no-sandbox', 
                '--disable-setuid-sandbox'
            ],
            executablePath: process.env.CHROMIUM_PATH || undefined
        });
        const page = await browser.newPage();
        console.log(`Visiting: ${url.href}`);
        await page.setCookie(present);
        await page.goto(url.href, {
            waitUntil: 'networkidle0',
            timeout: 30000,
        });
        await page.close();
        await browser.close();
        return true;
    } catch (e) {
        console.log(e)
    } finally {
        return true;
    }
}
