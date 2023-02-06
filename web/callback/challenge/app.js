import express from 'express'
import { renderFile } from 'ejs'
import bodyParser from 'body-parser'
import session from 'express-session'
import crypto from 'crypto'
import visit from './bot.js'
import { URL } from 'url'
import sha1 from 'sha1'
import morgan from 'morgan'

const PORT = process.env.PORT || 1337;

const app = express();

app.set('view engine', 'ejs');
app.engine('html', renderFile);

app.use(express.static('public'));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(session({
    secret: crypto.randomBytes(64).toString('hex'),
    resave: false,
    saveUninitialized: true,
}));

app.use(morgan('short'));

const currentPosts = {};

const pwned = {
    "Fox Viewer": 1, // their leaf gave me static shock dangit
    "Apartment door pager": 2,
    "Maple Insurance": 3,
    "A bank or smth": 4,
    "Maple Store": 5,
}

app.get('/', (req, res) => {
    // read all the files in the public articles directory
    // and render them
    res.render('index', { articles: pwned });
});

app.get('/help', (req, res) => {
    res.send("our representatives are currently unavailable. Please leave a message and we will get back to you as soon as possible.");
});

app.post('/leave-message', (req, res) => {
    const { name, phone, message } = req.body;
    if (!name || !phone || !message) {
        res.status(400).send('Need name, phone, and message');
        return;
    }
    const key = sha1(name);
    if (!currentPosts[key]) {
        currentPosts[key] = {
            name: name,
            phone: phone,
            messages: [],
        };
    }
    currentPosts[key]["messages"].push(message);
    res.send('ok done');
});

app.get('/login', (req, res) => {
    res.render('login');
});

app.post('/login', (req, res) => {
    const { username, password } = req.body;
    if (!(username === 'admin' && password === '5t709cgsb9j9zvemjppwos')) {
        res.status(401).send('Unauthorized');
        return;
    }
    req.session.admin = true;
    res.redirect('/admin-panel');
});

app.get('/admin-panel', (req, res) => {
    if (!req.session.admin) {
        res.redirect('/login');
        return;
    }
    const { key } = req.query;
    if (!key) {
        res.render('messages', { people: Object.keys(currentPosts) });
        return;
    }
    if (!currentPosts[key]) {
        res.send('No messages for that person');
        return;
    }
    const currentPost = currentPosts[key];
    delete currentPosts[key];
    res.render('messages', { name: currentPost["name"], phone: currentPost["phone"], messages: currentPost["messages"] });
    return;
});

app.post('/report', (req, res) => {
    const { url } = req.body;
    if (!url) {
        res.sendStatus(400).send('Need url');
        return;
    }
    try {
        const urlObj = new URL(url);
        // check if starts with javascript
        if (urlObj.protocol === 'javascript:') {
            res.sendStatus(400).send('Invalid url');
            return;
        }
        visit(urlObj);
        res.status(200).send('ok done');
    } catch (e) {
        res.status(400).send('Invalid url');
        return;
    }
})

app.get('/healthz', (req, res) => {
    res.sendStatus(200);
})

app.listen(PORT, () => {
    console.log(`Listening on port ${PORT}`);
});