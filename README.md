# Local Remote Developer Jobs Aggregator

Easily keep track the jobs you've applied in one place. Modify it with your own prefered job boards.


### Quickstart

- clone this repo;
- [install bunjs](https://bun.sh/docs/installation);
- load extension in browser (`edge://extensions/` or `chrome://extensions/` then `Load unpacked` point to `chrome-extension` folder);
- run `bun server.ts`;
- click `Open job boards` button (let it do it's thing);
- after it's done, keep the server running and click `View collected jobs` button;

You can checkout the remote job boards scrapped in the chrome-extension/manifest.json file `content_scripts.matches` and in the `service-worker.js` in `JOB_BOARDS` constant.


