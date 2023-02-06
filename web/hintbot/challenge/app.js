import express from "express";
import { renderFile } from "ejs";
import bodyParser from "body-parser";
import morgan from "morgan";
import { WebSocketServer } from "ws";
import { createServer } from "http";

const PORT = process.env.PORT || 1337;
let HOSTED_URL = process.env.HOSTED_URL || `http://localhost:${PORT}`;
let FLAG = process.env.FLAG || "maple{fake_flag}";
FLAG = FLAG.replace(/[\{\}_]/g, " ");
FLAG = FLAG.substring(0, FLAG.length - 1);
console.log(FLAG);

const websocketHost = HOSTED_URL.replace("http", "ws");

const app = express();

app.set("view engine", "ejs");
app.engine("html", renderFile);

app.use(bodyParser.json());

app.use(express.static("public"));

app.use(morgan("short"));

// for consistency with other hints, this flag has a reduced charset of [a-z], underscores and curly braces

const BASE_THRESHOLD = 2;

// replace spaces with underscores, wrap part after maple in curly
// maple fake flag becomes maple{fake_flag}

const hints = {
    welcome: "well welcome to you too, no hints here though",
    help: "take a rest. you're doing great, but sometimes it just takes a break and a fresh mind to unstuck yourself",
    "": "nothing? you gotta prove you know at least something",

    "web help pls": "f12 and ur g2g",
    "pwn help pls": "saem its literally magic to me",
    "crypto help pls": "just find the right paper kekw",
    "misc help pls":
        "its all just google/bing/duckduckgo or whatever you like to use",
    "rev help pls": "ghidra will do all your magic for you",

    "cookie tossing":
        "you can't just toss cookies around like that, you need to be careful with them",
    "tls poisoning into localhost ftp server into rce through redis":
        "deranged thoughts, i like it",
    "fetch force cache":
        "might want to take a look at BF-caching and disk-caching",
    "cookie xss payload":
        "probably just a malformed payload... oh wait that was for the 1337 challs... nevermind",
    "bgp poisoning":
        "nawh we don't have the kind of budget to host that sort of chall... or do we :)",
    "php filter chains": "dunno I'd just throw tools at it :)",
    "java deserialization": "kinda complex and not for this chall",
    "prototype pollution":
        "vuln loved by gooses everywhere, requires either being able to set arbitrary attributes on any object, or some kind of unsafe recursive merge function between objects controlled by you",
    "xss": "sus",
    "dns rebinding":
        "useful if you want to bypass a restriction against accessing some private ip address",
};

hints[FLAG] = "looks like you're winning";

app.get("/", (req, res) => {
    res.render("index.ejs", { websocketHost: websocketHost });
});

app.get("/healthz", (req, res) => {
    res.send("ok");
});

const server = createServer(app);

const wss = new WebSocketServer({ noServer: true });

server.on("upgrade", (req, socket, head) => {
    wss.handleUpgrade(req, socket, head, (ws) => {
        wss.emit("connection", ws, req);
    });
});

wss.on("connection", (ws) => {
    ws.on("message", (message) => {
        try {
            let { msg, debug } = JSON.parse(message);
            let hint = (msg ?? "").toLowerCase();
            let lowestDist = -1;
            for (let h in hints) {
                const threshold = BASE_THRESHOLD;
                const dist = levenshteinDistance(hint, h);
                const diff = dist - threshold;
                if (diff <= 0) {
                    ws.send(JSON.stringify({ msg: hints[h] }));
                    return;
                } else if (lowestDist === -1 || diff < lowestDist) {
                    lowestDist = diff;
                }
            }
            let response = {
                msg: "no match",
            };
            if (debug) {
                response["dist"] = lowestDist;
            }
            ws.send(JSON.stringify(response));
        } catch (e) {
            console.log(e);
            ws.send(JSON.stringify({ msg: "error" }));
        }
    });
});


server.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}`);
});

// https://stackoverflow.com/questions/11919065/sort-an-array-by-the-levenshtein-distance-with-best-performance-in-javascript/11958496#11958496
const levenshteinDistance = function (s, t) {
    var d = []; //2d matrix

    // Step 1
    var n = s.length;
    var m = t.length;

    if (n == 0) return m;
    if (m == 0) return n;

    //Create an array of arrays in javascript (a descending loop is quicker)
    for (var i = n; i >= 0; i--) d[i] = [];

    // Step 2
    for (var i = n; i >= 0; i--) d[i][0] = i;
    for (var j = m; j >= 0; j--) d[0][j] = j;

    // Step 3
    for (var i = 1; i <= n; i++) {
        var s_i = s.charAt(i - 1);

        // Step 4
        for (var j = 1; j <= m; j++) {
            //Check the jagged ld total so far
            if (i == j && d[i][j] > 4) return n;

            var t_j = t.charAt(j - 1);
            var cost = s_i == t_j ? 0 : 1; // Step 5

            //Calculate the minimum
            var mi = d[i - 1][j] + 1;
            var b = d[i][j - 1] + 1;
            var c = d[i - 1][j - 1] + cost;

            if (b < mi) mi = b;
            if (c < mi) mi = c;

            d[i][j] = mi; // Step 6

            //Damerau transposition
            if (
                i > 1 &&
                j > 1 &&
                s_i == t.charAt(j - 2) &&
                s.charAt(i - 2) == t_j
            ) {
                d[i][j] = Math.min(d[i][j], d[i - 2][j - 2] + cost);
            }
        }
    }

    // Step 7
    return d[n][m];
};
