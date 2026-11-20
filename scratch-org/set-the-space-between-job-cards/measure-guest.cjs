// Opens the Volunteer Portal as the site guest (no login) and prints the job card grid geometry as text:
// per category list, card width, column pitch, column gap and row gap. Usage: node measure-guest.cjs <siteUrl> [width]
const { chromium } = require('/Users/common-unite/.claude/skills/record-release-media/.runtime/node_modules/playwright-core');

(async () => {
    const [siteUrl, width = '1440'] = process.argv.slice(2);
    const browser = await chromium.launch({ channel: 'chrome', headless: true });
    const page = await browser.newPage({ viewport: { width: Number(width), height: 1200 } });
    await page.goto(siteUrl, { waitUntil: 'networkidle', timeout: 90000 });
    await page.waitForTimeout(6000);
    const report = await page.evaluate(() => {
        const all = [];
        const collect = root => {
            root.querySelectorAll('*').forEach(node => {
                all.push(node);
                if (node.shadowRoot) collect(node.shadowRoot);
            });
        };
        collect(document);
        const repeaters = all.filter(node => /flow-form-repeat$/i.test(node.tagName));
        return repeaters.map(repeater => {
            const inner = [];
            const walk = root => root.querySelectorAll('*').forEach(node => { inner.push(node); if (node.shadowRoot) walk(node.shadowRoot); });
            walk(repeater.shadowRoot || repeater);
            const cards = inner.filter(node => /flow-form$/i.test(node.tagName))
                .map(node => node.getBoundingClientRect())
                .filter(rect => rect.width > 50 && rect.height > 20);
            const rows = [...new Set(cards.map(rect => Math.round(rect.top)))].sort((a, b) => a - b);
            const firstRow = cards.filter(rect => Math.round(rect.top) === rows[0]).sort((a, b) => a.left - b.left);
            const secondRow = cards.filter(rect => Math.round(rect.top) === rows[1]);
            return {
                cards: cards.length,
                cardWidth: firstRow[0] ? Math.round(firstRow[0].width) : null,
                pitch: firstRow[1] ? Math.round(firstRow[1].left - firstRow[0].left) : null,
                columnGap: firstRow[1] ? Math.round(firstRow[1].left - firstRow[0].right) : null,
                rowGap: secondRow[0] ? Math.round(secondRow[0].top - firstRow[0].bottom) : null,
                firstCardTopOffset: firstRow[0] ? Math.round(firstRow[0].top - repeater.getBoundingClientRect().top) : null
            };
        });
    });
    console.log(JSON.stringify({ width: Number(width), repeaters: report }));
    await browser.close();
})().catch(error => { console.error('measure failed:', error.message); process.exit(1); });
