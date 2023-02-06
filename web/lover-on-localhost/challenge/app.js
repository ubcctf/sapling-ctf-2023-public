import express from "express";
import cookieParser from "cookie-parser";
import bodyParser from "body-parser";
import { renderFile } from "ejs";
import visit from "./localhost-bot.js";
import morgan from "morgan";

const PORT = process.env.PORT || 1337;
const FLAG = process.env.FLAG || "maple{fake_flag}";

const app = express();
app.use(cookieParser());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static("public"));

app.engine("ejs", renderFile);
app.set("view engine", "ejs");

app.use(morgan("short"));

app.get("/", (req, res) => {
    let response = [];
    response.push(`Welcome to my humble abode.`);
    const referer = decodeURIComponent(req.get("Referer"));
    if (referer && referer != "undefined") {
        if (referer === "127.0.0.1" || referer === "::1") {
            response.push(
                `Local host sent you? I'm flattered. Tell them to come <a href="/fraternize">fraternize</a> with me.`
            );
        } else {
            response.push(
                `Give my thanks to ${referer}, but tell them only local host is right for me.`
            );
        }
    } else {
        response.push(
            `I'm waiting for my local host to come <a href="/fraternize">fraternize</a> with me.`
        );
    }
    res.set("Content-Security-Policy", "default-src 'none'; img-src 'self' data:; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';");
    res.render("index.ejs", { response: response });
});

app.get("/fraternize", (req, res) => {
    const remoteIP = req.socket.remoteAddress;
    const present = req.cookies.present;
    let response = [];
    if (remoteIP !== "127.0.0.1" && remoteIP !== "::1" && remoteIP !== "::ffff:127.0.0.1") {
        response.push(`You're not my local host.`);
        response.push(`What'd you even bring?`);
        response.push(decodeURIComponent(present));
        response.push(`I don't want this. Go away.`);
        response.push(`I'll only wait for my local host.`);
        res.status(418).render("index.ejs", { response: response });
        return;
    }
    response.push(`My local host! I'm glad you could make it.`);
    response.push(`Ooh, you brought with you a present? Let me see...`);
    response.push(decodeURIComponent(present));
    response.push(`My, how lovely! Thank you!`);
    response.push(`Here, take this with you: ${FLAG} *happy grin*`);
    response.push(`Take care, and come back sometime!`);
    res.render("index.ejs", { response: response });
    return;
});

app.get("/messenger", (req, res) => {
    const response = [
        "I can help you forward an address to my local host...",
        "Just give me the address you want to give them...",
    ];
    res.render("index.ejs", { response: response });
});

app.post("/messenger", async (req, res) => {
    try {
        const url = new URL(req.body.url ?? "about:blank");
        if (url.protocol !== "http:" && url.protocol !== "https:") {
            res.status(400).render("index.ejs", {
                response: [
                    "I'm sorry, i couldn't send that address to local host.",
                    "The post bird didn't like it, so maybe try again later?",
                ],
            });
            return;
        }
        await visit(url);
        const response = [
            "I've sent it.",
            "Let's hope local host drops by sometime soon~",
        ];
        res.render("index.ejs", { response: response });
    } catch (e) {
        const response = [
            "I'm sorry, i couldn't send that address to local host.",
            "The post bird didn't make it, so maybe try again later?",
        ];
        res.status(500).render("index.ejs", { response: response });
    }
});

app.get('/healthz', (req, res) => {
    res.send('OK');
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
