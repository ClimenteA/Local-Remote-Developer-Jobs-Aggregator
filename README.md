# Local Remote Developer Jobs Aggregator

Easily keep track the jobs you've applied in one place. 
No more questions like: "Did I applied to this job before? Hmm... looks familiar". 
If you know a bit of javascript - clone repo and modify it with your prefered job boards and jobs types.


## Quickstart

- (One-time task) clone this repo;
- (One-time task) [install bunjs](https://bun.sh/docs/installation);
- (One-time task) load extension in browser (`edge://extensions/` or `chrome://extensions/` then `Load unpacked` point to `chrome-extension` folder). Hit reload extension if you make some mofifications on the extension code;
- (One-time task) open each website from `service-wrker.js` accept pop-ups/cookies/make account;
- (One-time task) checkout `ignorekeywords.txt` and add your own keywords;
- (One-time task) run `bun install`;
- run `bun server.ts`;
- click `Collect jobs` button (let it do it's thing);
- after it's done, keep the server running and click `View jobs` button (TIP: install [DB Browser](https://sqlitebrowser.org/) and perform operations in bulk);

You can checkout the remote job boards scrapped in the `chrome-extension/service-wrker.js` the `JOB_BOARDS` const. Add/remove/modify it for your needs. Make sure for each new website you add to create a scrape function in `chrome-extension/content-script.js`  


The extension:

![](./pics/popup.png)

The interface:

![](./pics/board.png)



## How it works?

When you click on the extension button `Collect jobs` a chrome runtime event `startScrapping` is sent to the `service-worker.js` which opens in a new tab a job board url. 
Once the url is loaded in a new window `content-script.js` will be invoked and the page will be scrapped based on the `hostMapper` object. Data scrapped is sent to the server (built with [HonoJs](https://hono.dev/)) and saved into a sqlite database.
The `content-script.js` once is finished scrapping and sending the data will also emit a chrome runtime event `closeTab` to `service-worker.js` which will close the tab opened.
If something goes wrong an alert popup will be invoked on the website with the issue and if posible the error will be sent and saved on the server. Click 'Reset storage' button in case 'Collect jobs' failed or job websites close on load.

**Note:** 
After scrapping is finised deactivate `job collection`. 
While looking at the collected jobs activate `description scanning` (an alert will appear if one of the ignored keywords if found). After you are done with the job application process deactivate `job collection` and `description scanning` so it won't bother you.



## Why a chrome extension and not pupeteer, playwright, selenium?

I tried doing that, but the amount of dependencies just to get it working is absurd (in ubuntu a ton of lib* files were needed).
Some websites have heavy protection for bots, scrappers which complicates even further the setup and code.
With the chrome extension you can bypass a lot of those and just act "like a user" on the website.
No cookies to accept, login session and so on because it uses the session already available in the browser.


**😁 Good luck job hunting!**
