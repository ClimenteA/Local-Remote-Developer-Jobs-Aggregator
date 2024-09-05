const defaultWait = 3000;
const largeWait = 6000;

// https://wellfound.com/jobs
// https://jobs.workable.com/

const JOB_BOARDS = [
  {
    url: "https://remotive.com/remote-jobs/software-dev",
    wait: defaultWait,
  },
  {
    url: "https://remoteok.com/remote-golang-jobs?order_by=date",
    wait: defaultWait,
  },
  {
    url: "https://remoteok.com/remote-python-jobs?order_by=date",
    wait: defaultWait,
  },
  {
    url: "https://remoteok.com/remote-javascript-jobs?order_by=date",
    wait: defaultWait,
  },
  {
    url: "https://remoteok.com/remote-front-end-jobs?order_by=date",
    wait: defaultWait,
  },
  {
    url: "https://remoteok.com/remote-backend-jobs?order_by=date",
    wait: defaultWait,
  },
  {
    url: "https://remoteok.com/remote-dev-jobs?order_by=date",
    wait: defaultWait,
  },
  {
    url: "https://remoteok.com/remote-dev-jobs?order_by=date",
    wait: defaultWait,
  },
  {
    url: "https://devjob.ro/",
    wait: defaultWait,
  },
  {
    url: "https://remote.co/remote-jobs/developer/",
    wait: defaultWait,
  },
  {
    url: "https://weworkremotely.com/categories/remote-full-stack-programming-jobs",
    wait: defaultWait,
  },
  {
    url: "https://weworkremotely.com/categories/remote-front-end-programming-jobs",
    wait: defaultWait,
  },
  {
    url: "https://weworkremotely.com/categories/remote-back-end-programming-jobs",
    wait: defaultWait,
  },
  {
    url: "https://www.workingnomads.com/jobs?category=development&location=anywhere,europe",
    wait: defaultWait,
  },
  {
    url: "https://www.remote.io/remote-software-development-jobs?pg=1",
    wait: defaultWait,
  },
  {
    url: "https://www.remote.io/remote-software-development-jobs?pg=2",
    wait: defaultWait,
  },
  {
    url: "https://builtin.com/jobs/remote/dev-engineering/golang/javascript/python/mid-level/senior?daysSinceUpdated=3",
    wait: defaultWait,
  },
  {
    url: "https://builtin.com/jobs/remote/dev-engineering/golang/javascript/python/mid-level/senior?daysSinceUpdated=3&page=2",
    wait: defaultWait,
  },
  {
    url: "https://www.pyjobs.com/?remoteLevel[0]=1&remoteLevel[1]=2&date=72&regions[0]=RO",
    wait: defaultWait,
  },
  {
    url: "https://remote.works-hub.com/jobs/search?page=1&remote=true&tags=JavaScript;Python",
    wait: largeWait,
  },
  {
    url: "https://justremote.co/remote-developer-jobs",
    wait: defaultWait,
  },
  {
    url: "https://www.glassdoor.com/Job/romania-python-jobs-SRCH_IL.0,7_IN203_KO8,14.htm?sortBy=date_desc&fromAge=1",
    wait: defaultWait,
  },
  {
    url: "https://www.glassdoor.com/Job/romania-javascript-jobs-SRCH_IL.0,7_IN203_KO8,18.htm?fromAge=1",
    wait: defaultWait,
  },
  {
    url: "https://www.glassdoor.com/Job/romania-typescript-jobs-SRCH_IL.0,7_IN203_KO8,18.htm?fromAge=1",
    wait: defaultWait,
  },
  {
    url: "https://remoters.net/jobs/software-development/filters?jobs-location=anywhere",
    wait: defaultWait,
  },
  {
    url: "https://www.linkedin.com/jobs/collections/?f_WT=2",
    wait: largeWait,
  },
  {
    url: "https://www.linkedin.com/jobs/collections/?f_WT=2&start=24",
    wait: largeWait,
  },
  {
    url: "https://www.linkedin.com/jobs/collections/?f_WT=2&start=48",
    wait: largeWait,
  },
  {
    url: "https://www.linkedin.com/jobs/collections/?f_WT=2&start=72",
    wait: largeWait,
  },
  // {
  //   url: "https://nodesk.co/remote-jobs/engineering/",
  //   wait: defaultWait,
  // },
  // {
  //   url: "https://landing.jobs/jobs?page=1&gr=true&fr=true&match=all&con=true&hd=false&t_co=false&t_st=false",
  //   wait: defaultWait,
  // },
  // {
  //   url: "https://euremotejobs.com/jobs/remote-software-engineering-jobs/",
  //   wait: defaultWait,
  // },
  // {
  //   url: "https://vuejobs.com/jobs",
  //   wait: defaultWait,
  // },
  // {
  //   url: "https://reactjobs.io/jobs/javascript?search=Javascript&isRemote=true",
  //   wait: defaultWait,
  // },
  // {
  //   url: "https://reactjobs.io/jobs/javascript?search=Javascript&isRemote=true&page=2",
  //   wait: defaultWait,
  // },
  // {
  //   url: "https://reactjobs.io/jobs/javascript?search=Javascript&isRemote=true&page=3",
  //   wait: defaultWait,
  // },
  // {
  //   url: "https://jsjobbs.com/jobs/remote-javascript-jobs",
  //   wait: defaultWait,
  // },
  // {
  //   url: "https://berlinstartupjobs.com/skill-areas/javascript/",
  //   wait: defaultWait,
  // },
  // {
  //   url: "https://berlinstartupjobs.com/skill-areas/python/",
  //   wait: defaultWait,
  // },
  // {
  //   url: "https://berlinstartupjobs.com/skill-areas/typescript/",
  //   wait: defaultWait,
  // },
  // {
  //   url: "https://www.workatastartup.com/companies?demographic=any&hasEquity=any&hasSalary=any&industry=any&interviewProcess=any&jobType=any&layout=list-compact&query=Python&remote=only&role=eng&role_type=be&role_type=fe&role_type=fs&sortBy=keyword&tab=any&usVisaNotRequired=any",
  //   wait: defaultWait,
  // },
  // {
  //   url: "https://www.workatastartup.com/companies?demographic=any&hasEquity=any&hasSalary=any&industry=any&interviewProcess=any&jobType=any&layout=list-compact&query=Python&remote=only&role=eng&role_type=be&role_type=fe&role_type=fs&sortBy=keyword&tab=any&usVisaNotRequired=any",
  //   wait: defaultWait,
  // },
  // {
  //   url: "https://www.workatastartup.com/companies?demographic=any&hasEquity=any&hasSalary=any&industry=any&interviewProcess=any&jobType=any&layout=list-compact&query=Golang&remote=only&role=eng&role_type=be&role_type=fe&role_type=fs&sortBy=keyword&tab=any&usVisaNotRequired=any",
  //   wait: defaultWait,
  // },
  // {
  //   url: "https://justjoin.it/all-locations/python/remote_yes",
  //   wait: defaultWait,
  // },
  // {
  //   url: "https://justjoin.it/all-locations/javascript/remote_yes",
  //   wait: defaultWait,
  // },
  // {
  //   url: "https://justjoin.it/all-locations/go/remote_yes",
  //   wait: defaultWait,
  // },
  // {
  //     url: "https://www.eurotechjobs.com/job_search/category/developer/category/python_developer/category/web_developer/keyword/remote",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://workinstartups.com/job-board/jobs/developers/freelance",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://startup.jobs/?remote=true",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://www.startupjobs.com/jobs?seniority=medior,senior&technologies=python,javascript,go,typescript&form-of-collaboration=freelance,remote",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://4dayweek.io/remote-jobs/engineering/europe/fully-remote",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://www.reed.co.uk/jobs/work-from-home-python-jobs?parentSectorIds=52&dateCreatedOffSet=lastthreedays",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://www.reed.co.uk/jobs/work-from-home-javascript-jobs?parentSectorIds=52&dateCreatedOffSet=lastthreedays",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://www.reed.co.uk/jobs/work-from-home-typescript-jobs?parentSectorIds=52&dateCreatedOffSet=lastthreedays",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://www.reed.co.uk/jobs/work-from-home-go-jobs?parentSectorIds=52&dateCreatedOffSet=lastthreedays",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://dynamitejobs.com/remote-jobs?text=Python&page=1",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://dynamitejobs.com/remote-jobs?text=Python&page=2",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://dynamitejobs.com/remote-jobs?text=Python&page=3",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://dynamitejobs.com/remote-jobs?text=Python&page=4",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://dynamitejobs.com/remote-jobs?text=Javascript&page=1",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://dynamitejobs.com/remote-jobs?text=Javascript&page=2",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://dynamitejobs.com/remote-jobs?text=Javascript&page=3",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://dynamitejobs.com/remote-jobs?text=Javascript&page=4",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://dynamitejobs.com/remote-jobs?text=Golang&page=1",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://dynamitejobs.com/remote-jobs?text=Golang&page=2",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://himalayas.app/jobs/worldwide/python?type=full-time%2Cpart-time%2Ccontractor%2Ctemporary&experience=mid-level%2Csenior%2Cmanager&sort=recent",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://himalayas.app/jobs/worldwide/python?type=full-time%2Cpart-time%2Ccontractor%2Ctemporary&experience=mid-level%2Csenior%2Cmanager&sort=recent&page=2",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://himalayas.app/jobs/worldwide/python?type=full-time%2Cpart-time%2Ccontractor%2Ctemporary&experience=mid-level%2Csenior%2Cmanager&sort=recent&page=3",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://himalayas.app/jobs/worldwide/javascript?type=full-time%2Cpart-time%2Ccontractor%2Ctemporary&experience=mid-level%2Csenior%2Cmanager&sort=recent",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://himalayas.app/jobs/worldwide/javascript?type=full-time%2Cpart-time%2Ccontractor%2Ctemporary&experience=mid-level%2Csenior%2Cmanager&sort=recent&page=2",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://himalayas.app/jobs/worldwide/javascript?type=full-time%2Cpart-time%2Ccontractor%2Ctemporary&experience=mid-level%2Csenior%2Cmanager&sort=recent&page=3",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://himalayas.app/jobs/worldwide/golang?type=full-time%2Cpart-time%2Ccontractor%2Ctemporary&experience=mid-level%2Csenior%2Cmanager&sort=recent",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://himalayas.app/jobs/worldwide/golang?type=full-time%2Cpart-time%2Ccontractor%2Ctemporary&experience=mid-level%2Csenior%2Cmanager&sort=recent&page=2",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://www.totaljobs.com/jobs/remote-python?sort=2&action=sort_publish",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://www.totaljobs.com/jobs/remote-python?page=2&sort=2&action=sort_publish",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://www.totaljobs.com/jobs/remote-python?page=3&sort=2&action=sort_publish",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://www.totaljobs.com/jobs/remote-javascript?sort=2&action=sort_publish",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://www.totaljobs.com/jobs/remote-javascript?sort=2&action=sort_publish",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://www.totaljobs.com/jobs/remote-javascript?page=2&sort=2&action=sort_publish",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://www.totaljobs.com/jobs/remote-javascript?page=3&sort=2&action=sort_publish",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://www.totaljobs.com/jobs/remote-golang?sort=2&action=sort_publish",
  //     wait: defaultWait,
  // },
  // {
  //     url: "https://www.ejobs.ro/locuri-de-munca/remote/it-software/mid-level,senior-level/sort-publish",
  //     wait: defaultWait,
  // },
];

chrome.runtime.onInstalled.addListener(() => {
  console.log("Service Worker installed");
});

chrome.runtime.onMessage.addListener(async function (
  request,
  sender,
  sendResponse
) {
  if (request.msg === "startScrapping") {
    for (const { url, wait } of JOB_BOARDS) {
      // Debug line
      // if (!url.includes("justjoin.it")) continue;

      // Use chrome.storage to save url close state
      // ONLY when `Open job boards` button is clicked
      chrome.storage.sync.get(["urls"], function (items) {
        let urlStates = [];
        if (items.urls?.length > 0) {
          let foundUrl = false;
          for (let i = 0; items.urls.length > i; i++) {
            if (items.urls[i].url == url) {
              foundUrl = true;
              items.urls[i].close = true;
            }
          }
          if (!foundUrl) {
            items.urls.push({ url: url, close: true });
          }
          urlStates = items.urls;
        } else {
          urlStates.push({ url: url, close: true });
        }
        chrome.storage.sync.set({ urls: urlStates });
      });

      chrome.tabs.create({ url: url });
      await new Promise((res, rej) => setTimeout(() => res(), wait));
    }
    sendResponse({ status: "scrapping started" });
    return true; // Keeps the message channel open for sendResponse
  } else if (request.msg === "closeTab") {
    // Close tab only if scrapping was finished
    console.log("closeTab event was received");

    chrome.storage.sync.get(["urls"], function (items) {
      if (!items.urls?.length > 0) return;
      for (let i = 0; items.urls.length > i; i++) {
        if (items.urls[i].url == sender.tab.url) {
          items.urls[i].close = false;
          chrome.storage.sync.set({ urls: items.urls });
          break;
        }
      }
    });

    chrome.storage.sync.get(["urls"], function (items) {
      if (!items.urls?.length > 0) return;
      for (const u of items.urls) {
        if (u.url == sender.tab.url) {
          chrome.tabs.remove(sender.tab.id);
          break;
        }
      }
    });

    sendResponse({ status: "tab closed" });
    return true; // Keeps the message channel open for sendResponse
  }
});
