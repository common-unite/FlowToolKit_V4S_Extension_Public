/**Shared by the card spacing scenarios: org ids, the default-spacing site bundle, and opening Experience Builder on the Volunteer Portal**/
const { execFileSync } = require('child_process');
const path = require('path');
const os = require('os');

const ORG = 'FlowToolKit_V4S_Ext__dev';
const NETWORK = '0DBQL0000015EeT4AU';
const SITE_ID = '0DMQL000000hic64AA';
const MY_DOMAIN = 'https://business-customization-9444.scratch.my.salesforce.com';
const SITE_URL = 'https://business-customization-9444.scratch.my.site.com/volunteers/s/';
const KIT = __dirname;
const REPO = path.resolve(KIT, '..', '..');
const run = (cmd, args) => execFileSync(cmd, args, { cwd: REPO, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
const switchTo = start => `${MY_DOMAIN}/servlet/networks/switch?networkId=${NETWORK}&startURL=${encodeURIComponent(start)}`;

/**The Home page back to the finder at Default spacing (no spacing keys), published, so every take starts where a site is today**/
exports.resetSite = () => {
    run('python3', [path.join(os.homedir(), '.claude/tools/sfdeploy.py'), path.join(KIT, 'site/experiences/Volunteer_Portal1'), '--org', ORG, '--issue', '46']);
    run('python3', [path.join(os.homedir(), '.claude/tools/site-publish.py'), 'Volunteer Portal', '-o', ORG]);
};

exports.openBuilder = async page => {
    await page.goto(`${MY_DOMAIN}/sfsites/picasso/core/config/commeditor.jsp?siteId=${SITE_ID}`, { waitUntil: 'domcontentloaded', timeout: 90000 });
    await page.getByRole('button', { name: /Publish/ }).first().waitFor({ timeout: 120000 });
    await page.waitForTimeout(15000);
};

exports.canvas = page => page.frameLocator('iframe[name="previewIFrame"], iframe.preview-iframe, iframe').first();
exports.SITE_URL = SITE_URL;
