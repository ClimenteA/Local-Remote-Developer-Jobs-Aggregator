import { Database } from "bun:sqlite"
import { Hono } from 'hono'
import { serveStatic } from 'hono/bun'

// DB

const db = new Database("./jobs.db", { create: true })
db.exec("PRAGMA journal_mode = WAL;")


db.query(`
CREATE TABLE IF NOT EXISTS jobs (
    url TEXT,
    title TEXT,
    source TEXT,
    applied BOOLEAN,
    ignored BOOLEAN,
    timestamp TEXT);
`).run()

db.query(`CREATE UNIQUE INDEX IF NOT EXISTS url_IDX ON "jobs" (url)`).run()

 
interface RawJob {
    url: string
    title: string
    source: string
}


function insertJobs(rawJobs: Array<RawJob>){

    const currentDate = new Date().toISOString()
    const urlQuery = db.query(`SELECT * FROM jobs WHERE url = $url`)

    const values: Array<string> = []
    for (const rawjob of rawJobs){

        if (urlQuery.get({$url: rawjob.url})) continue

        const job = {...rawjob, applied: 0, ignored: 0, timestamp: currentDate}

        values.push(`("${job.url}", "${job.title}", "${job.source}", ${job.applied}, ${job.ignored}, "${job.timestamp}")`)     
    }

    if (values.length == 0) return

    db.query(`
    INSERT INTO jobs (url, title, source, applied, ignored, timestamp) 
    VALUES ${values.join(", ") + ";"}`
    ).run()

}


interface Job extends RawJob {
    applied: number
    ignored: number
    timestamp: string
}


function getLimitOffsetFromPage(page: number, itemsPerPage: number = 100) {
    try {
        page = Math.abs(Number(page))
        if (page <= 0) page = 1
    } catch (error) {
        page = 1
    }
    const limit = itemsPerPage
    const offset = page == 1 ? 0: (page - 1) * itemsPerPage
    return {limit, offset}
}


function getNewJobs(page: number = 1){
    const {limit, offset} = getLimitOffsetFromPage(page)
    const rows = db.query(
        `SELECT * FROM jobs WHERE applied = 0 AND ignored = 0 LIMIT ${limit} OFFSET ${offset};`
    ).all()
    return rows
}


function getAppliedJobs(page: number = 1){
    const {limit, offset} = getLimitOffsetFromPage(page)
    const rows = db.query(
        `SELECT * FROM jobs WHERE applied = 1 LIMIT ${limit} OFFSET ${offset};`
    ).all()
    return rows
}


function getIgnoredJobs(page: number = 1){
    const {limit, offset} = getLimitOffsetFromPage(page)
    const rows = db.query(
        `SELECT * FROM jobs WHERE ignored = 1 LIMIT ${limit} OFFSET ${offset};`
    ).all()
    return rows
}


// Web

const app = new Hono()

app.get('/', serveStatic({ path: './jobs.html' }))

app.get('/api/new/:page', (c) => {
    const page = Number(c.req.param('page'))
    const newJobs = getNewJobs(page)
    return c.json({ jobs: newJobs, page: page })
})

app.get('/api/applied/:page', (c) => {
    const page = Number(c.req.param('page'))
    const appliedJobs = getAppliedJobs(page)
    return c.json({ jobs: appliedJobs, page: page })
})


app.get('/api/ignored/:page', (c) => {
    const page = Number(c.req.param('page'))
    const ignoredJobs = getIgnoredJobs(page)
    return c.json({ jobs: ignoredJobs, page: page })
})



Bun.serve({
    port: 3000, 
    hostname: "127.0.0.1",
    development: true,
    fetch(req) {
        return app.fetch(req)
    }
})
