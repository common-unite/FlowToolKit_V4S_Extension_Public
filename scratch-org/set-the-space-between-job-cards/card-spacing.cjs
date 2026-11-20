/**Card spacing walkthrough: in Experience Builder on the Volunteer Portal Home page, select the Volunteer Job Finder, set Card Spacing Beside to x-small and Below to small, publish, then show the tighter grid on the live site as the guest**/
const pace = require(require('os').homedir() + '/.claude/skills/walkthrough/scripts/pace.cjs');
const common = require('./common.cjs');

const FINDER = 'flowtoolkit-volunteer-jobs-finder-page, c-volunteer-jobs-finder-page';
const GRID = 'flowtoolkit-flow-form-repeat, c-flow-form-repeat';
const canvas = page => page.frameLocator('iframe[name="sitePreviewFrame"]');
const canvasFinder = page => canvas(page).locator(FINDER).first();

/**Smooth-scrolls a document so the first three-per-row job list (the one after Featured) and its heading fill the view**/
const scrollToGrid = locator => locator.evaluate(element => {
    const top = element.getBoundingClientRect().top + window.scrollY - 90;
    window.scrollTo({ top, behavior: 'smooth' });
});

async function choose(page, demo, label, size) {
    const box = page.getByRole('combobox', { name: label });
    await demo.scrollTo(box);
    await demo.click(box);
    await page.waitForTimeout(600);
    await demo.click(page.getByRole('option', { name: size, exact: true }));
}

exports.prepare = async ({ page }) => {
    common.resetSite();
    await common.openBuilder(page);
    await page.mouse.click(1279, 235); /**closes the Build Your Own Site tour card**/
    await page.waitForTimeout(1000);
};

exports.record = async ({ page, demo, mark }) => {
    const line = pace('card-spacing', page, mark);
    await line('intro', async () => {
        await scrollToGrid(canvas(page).locator(GRID).nth(1));
    }, { at: 5000 });
    await line('select', async () => {
        const box = await canvasFinder(page).boundingBox();
        const x = box.x + box.width / 2;
        const y = Math.max(box.y, 100) + 40;
        await demo.moveTo(x, y, { duration: 800 });
        await page.mouse.click(x, y);
        await page.getByText('Card Spacing', { exact: true }).waitFor({ timeout: 30000 });
    }, { at: 600 });
    await line('layout', async () => {
        const heading = page.getByText('Card Spacing', { exact: true });
        await demo.scrollTo(page.getByRole('combobox', { name: 'Beside' }));
        await demo.point(heading);
    }, { at: 1200 });
    await line('beside', () => choose(page, demo, 'Beside', 'x-small'), { at: 300 });
    await line('below', () => choose(page, demo, 'Below', 'small'), { at: 200 });
    await line('publish', async () => {
        await demo.click(page.getByRole('button', { name: 'Publish' }).first());
        await page.waitForTimeout(1500);
        await demo.click(page.getByRole('dialog').getByRole('button', { name: 'Publish' }));
    }, { at: 300 });
    await line('live', async () => {
        await page.waitForTimeout(4000);
        await page.goto(common.SITE_URL, { waitUntil: 'domcontentloaded', timeout: 90000 });
        await page.locator(FINDER).first().waitFor({ timeout: 90000 });
    }, { at: 1500 });
    await line('result', async () => {
        await page.waitForTimeout(800);
        await scrollToGrid(page.locator(GRID).nth(1));
    }, { at: 600 });
    await line('close', async () => {
        /**Text verdict for the frame review: the live column gap, which x-small Beside makes 16 px (Default is 32)**/
        const gaps = await page.evaluate(() => {
            const all = [];
            const walk = root => root.querySelectorAll('*').forEach(node => { all.push(node); if (node.shadowRoot) walk(node.shadowRoot); });
            walk(document);
            const cards = all.filter(node => /flow-form$/i.test(node.tagName)).map(node => node.getBoundingClientRect()).filter(rect => rect.width > 50 && rect.width < 600);
            const top = Math.min(...cards.map(rect => rect.top));
            const row = cards.filter(rect => Math.abs(rect.top - top) < 2).sort((a, b) => a.left - b.left);
            return row.length > 1 ? Math.round(row[1].left - row[0].right) : null;
        });
        console.log('live column gap px', gaps);
    }, { at: 200 });
};
