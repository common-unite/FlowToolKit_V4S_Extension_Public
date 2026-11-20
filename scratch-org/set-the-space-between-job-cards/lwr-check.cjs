// Guest check on an LWR site (no login): which finder host is on the page, the job card grid geometry, and the Shift Range strings on the cards.
// Usage: node lwr-check.cjs <siteUrl> [width]. Prints one JSON line.
const { chromium } = require('/Users/common-unite/.claude/skills/record-release-media/.runtime/node_modules/playwright-core');

(async () => {
    const [siteUrl, width = '1440'] = process.argv.slice(2);
    const browser = await chromium.launch({ channel: 'chrome', headless: true });
    const page = await browser.newPage({ viewport: { width: Number(width), height: 1200 } });
    await page.goto(siteUrl, { waitUntil: 'load', timeout: 90000 });
    await page.waitForTimeout(15000);
    const report = await page.evaluate(() => {
        const all = [];
        const walk = root => root.querySelectorAll('*').forEach(node => { all.push(node); if (node.shadowRoot) walk(node.shadowRoot); });
        walk(document);
        const tags = [...new Set(all.map(node => node.tagName.toLowerCase()).filter(tag => /volunteer-jobs-finder|flow-form-repeat|lightning-flow|flowruntime/.test(tag)))];
        const repeaters = all.filter(node => /flow-form-repeat$/i.test(node.tagName)).map(repeater => {
            const inner = [];
            const innerWalk = root => root.querySelectorAll('*').forEach(node => { inner.push(node); if (node.shadowRoot) innerWalk(node.shadowRoot); });
            innerWalk(repeater.shadowRoot || repeater);
            const cards = inner.filter(node => /flow-form$/i.test(node.tagName)).map(node => node.getBoundingClientRect()).filter(rect => rect.width > 50 && rect.height > 20);
            const rows = [...new Set(cards.map(rect => Math.round(rect.top)))].sort((a, b) => a - b);
            const firstRow = cards.filter(rect => Math.round(rect.top) === rows[0]).sort((a, b) => a.left - b.left);
            const secondRow = cards.filter(rect => Math.round(rect.top) === rows[1]);
            return {
                cards: cards.length,
                cardWidth: firstRow[0] ? Math.round(firstRow[0].width) : null,
                pitch: firstRow[1] ? Math.round(firstRow[1].left - firstRow[0].left) : null,
                columnGap: firstRow[1] ? Math.round(firstRow[1].left - firstRow[0].right) : null,
                rowGap: secondRow[0] ? Math.round(secondRow[0].top - firstRow[0].bottom) : null
            };
        });
        const month = '(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\\.?';
        const datePart = `(?:${month} \\d{1,2}, \\d{4}|\\d{1,2}/\\d{1,2}/\\d{2,4})`;
        const rangePattern = new RegExp(`${datePart}(?: - ${datePart})?`);
        const texts = all.filter(node => node.childNodes.length && [...node.childNodes].some(child => child.nodeType === 3 && rangePattern.test(child.textContent)))
            .map(node => [...node.childNodes].filter(child => child.nodeType === 3).map(child => child.textContent.trim()).join(' ').trim())
            .filter(text => rangePattern.test(text) && text.length < 80);
        const shapes = texts.map(text => text.replace(new RegExp(month, 'g'), 'Mon').replace(/\d/g, '9'));
        return { tags, repeaters, shiftRanges: { count: texts.length, formats: [...new Set(shapes)], sample: texts[0] || null } };
    });
    console.log(JSON.stringify({ width: Number(width), ...report }));
    await browser.close();
})().catch(error => { console.error('check failed:', error.message); process.exit(1); });
