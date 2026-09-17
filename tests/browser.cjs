// Optional visual QA. A fresh headless profile talks only to the local test server.
const assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {spawn}=require('node:child_process');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const root=path.resolve(__dirname,'..'),evidence=path.join(root,'evidence');
fs.mkdirSync(evidence,{recursive:true});
let server,browser,page;
const checks=[],errors=[],external=[];
function check(label,ok){assert.ok(ok,label);checks.push(label);}
async function screenshot(name){await page.screenshot({path:path.join(evidence,name+'.png'),fullPage:true});}
(async()=>{
 server=spawn(process.env.PYTHON_EXECUTABLE || 'python',['-X','utf8','preview.py','0'],{cwd:root,windowsHide:true,stdio:['ignore','pipe','pipe']});
 const base=await new Promise((resolve,reject)=>{let output='';const timer=setTimeout(()=>reject(Error('Preview did not start')),10000);server.stdout.on('data',chunk=>{output+=chunk;const match=output.match(/http:\/\/127\.0\.0\.1:\d+/);if(match){clearTimeout(timer);resolve(match[0]);}});server.on('error',reject);});
 browser=await chromium.launch({headless:true});
 const context=await browser.newContext({viewport:{width:1440,height:1000},locale:'de-AT',permissions:['clipboard-read','clipboard-write']});
 await context.route('**/*',route=>{if(new URL(route.request().url()).origin!==base){external.push(route.request().url());return route.abort();}return route.continue();});
 page=await context.newPage();page.on('pageerror',error=>errors.push(error.message));
 await page.goto(base+'/gratis-workflows/');await page.evaluate(()=>document.fonts.ready);
 check('All 15 starters visible',await page.locator('[data-starter]:visible').count()===15);
 check('Skip link keyboard accessible',(await page.keyboard.press('Tab'),await page.locator('.skip').evaluate(el=>el===document.activeElement)));
 await screenshot('library-desktop-dark');
 for(const theme of ['dark','light']){
  if(theme==='light')await page.locator('[data-theme-toggle]').click();
  for(const width of [320,390,768,1024,1440]){
   await page.setViewportSize({width,height:1000});
   check('Library width '+width+' '+theme,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
   if(width===390)await screenshot('library-mobile-'+theme);
  }
 }
 await page.locator('#format').selectOption('n8n');
 check('Format returns four n8n starters',await page.locator('[data-starter]:visible').count()===4);
 await page.locator('[data-category="Betrieb"]').click();
 check('Combined filters show empty state',await page.locator('#empty').isVisible());
 await page.locator('#reset').click();
 check('Reset restores all results and search focus',await page.locator('[data-starter]:visible').count()===15&&await page.locator('#search').evaluate(el=>el===document.activeElement));
 await page.locator('#search').fill('Kalender');
 check('Search narrows visible results',await page.locator('[data-starter]:visible').count()===1);
 await page.reload();
 check('Search survives URL reload',await page.locator('#search').inputValue()==='Kalender'&&await page.locator('[data-starter]:visible').count()===1);
 await page.locator('[data-starter]:visible a').click();
 check('Detail page has one heading',await page.locator('h1').count()===1);
 await page.bringToFront();
 await page.locator('[data-copy]').click();
 await page.waitForFunction(()=>document.querySelector('.codebox [role=status]').textContent.length>0);
 const copyFeedback=await page.locator('.codebox [role=status]').innerText();
 check('Copy gives meaningful feedback: '+copyFeedback,copyFeedback.includes('kopiert'));
 const command=await page.locator('#starter-command').innerText();
 check('Clipboard contains exact command',await page.evaluate(()=>navigator.clipboard.readText())===command);
 for(const theme of ['dark','light']){
  await page.evaluate(t=>document.documentElement.dataset.theme=t,theme);
  for(const width of [320,390,768,1024,1440]){
   await page.setViewportSize({width,height:1000});
   check('Detail width '+width+' '+theme,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  }
 }
 await screenshot('detail-desktop-light');
 const [download]=await Promise.all([page.waitForEvent('download'),page.getByRole('link',{name:'Starter herunterladen ↓',exact:true}).click()]);
 const bytes=fs.readFileSync(await download.path());
 const manifest=JSON.parse(fs.readFileSync(path.join(root,'site/downloads/manifest.json'),'utf8'));
 const slug=download.suggestedFilename().replace(/\.zip$/,'');
 check('Downloaded ZIP has published SHA-256',crypto.createHash('sha256').update(bytes).digest('hex')===manifest[slug].sha256);
 const catalog=JSON.parse(fs.readFileSync(path.join(root,'catalog.json'),'utf8'));
 for(const starter of catalog){const response=await page.goto(base+'/gratis-workflows/'+starter.id+'/');check('Detail works '+starter.id,response.ok()&&await page.locator('h1').innerText()===starter.title);}
 await page.goto(base+'/gratis-workflows/?q=%3Cscript%3Ealert(1)%3C%2Fscript%3E');
 check('Search markup remains inert',await page.locator('#empty').isVisible()&&await page.locator('script:not([src]):not([type="application/ld+json"])').count()===0);
 check('No uncaught page errors',errors.length===0);check('No external browser requests',external.length===0);
 const nojs=await browser.newContext({javaScriptEnabled:false}),plain=await nojs.newPage();
 await plain.goto(base+'/gratis-workflows/');check('All starters accessible without JavaScript',await plain.locator('[data-starter] a').count()===15);await nojs.close();
 fs.writeFileSync(path.join(evidence,'browser-results.json'),JSON.stringify({passed:true,browser:await browser.version(),checks,errors,external,date:new Date().toISOString()},null,2));
 console.log(JSON.stringify({passed:true,checks:checks.length}));
})().catch(async error=>{console.error(error.message);if(page)await screenshot('failure');process.exitCode=1;}).finally(async()=>{if(browser)await browser.close();if(server)server.kill();});
