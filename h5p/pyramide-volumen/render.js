const { chromium } = require('playwright'); const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
for (const [svg,out,w,h,type] of JSON.parse(process.argv[2])) {
 await p.setViewportSize({width:w,height:h});
 await p.goto('file://'+path.resolve(svg));
 await p.screenshot({path:out,type,quality:type==='jpeg'?85:undefined});
}
await b.close();})();
