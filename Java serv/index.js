const bodyParser = require('body-parser');
const puppeteer = require('puppeteer');

const app = express();
const PORT = 3003;

app.use(bodyParser.json());

// Обробка GET-запитів для друку дешборду
app.get('/print-dashboard', async (req, res) => {
    const { url, output } = req.query;

    if (!url || !output) {
        return res.status(400).json({ error: 'URL і шлях для збереження PDF потрібні' });
    }

    try {
        const browser = await puppeteer.launch();
        const page = await browser.newPage();
        await page.goto(url, { waitUntil: 'networkidle2' });
        await page.pdf({ path: output, format: 'A4' });

        await browser.close();
        res.status(200).json({ message: 'PDF створено успішно', path: output });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Помилка при створенні PDF' });
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});