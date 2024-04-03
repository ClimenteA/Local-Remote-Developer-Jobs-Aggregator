import { Hono } from 'hono'
import { logger } from 'hono/logger'
import { cors } from 'hono/cors'
import { Repo, RawJob } from './repo'
import nunjucks from 'nunjucks'

const app = new Hono()
const repo = new Repo()

app.use(logger())
app.use('*', cors())

nunjucks.configure('templates', { autoescape: true })

app.get('/', (c) => {
    const newJobs = repo.getNewJobs()
    return c.html(nunjucks.render('jobs.html',
        { jobs: newJobs, jobType: 'new', page: 1, nextPage: 2, prevPage: 1 }))
})

app.get('/new/:page', (c) => {
    const page = Number(c.req.param('page'))
    const newJobs = repo.getNewJobs(page)
    return c.html(nunjucks.render('jobs.html',
        { jobs: newJobs, jobType: 'new', page: page, nextPage: page + 1, prevPage: page - 1 }))
})

app.get('/applied/:page', (c) => {
    const page = Number(c.req.param('page'))
    const appliedJobs = repo.getAppliedJobs(page)
    return c.html(nunjucks.render('jobs.html',
        { jobs: appliedJobs, jobType: 'applied', page: page, nextPage: page + 1, prevPage: page - 1 }))
})

app.get('/ignored/:page', (c) => {
    const page = Number(c.req.param('page'))
    const ignoredJobs = repo.getIgnoredJobs(page)
    return c.html(nunjucks.render('jobs.html',
        { jobs: ignoredJobs, jobType: 'ignored', page: page, nextPage: page + 1, prevPage: page - 1 }))
})


app.post('/api/save-jobs', async (c) => {
    const jobs: Array<RawJob> = await c.req.json()
    try {
        repo.saveJobs(jobs)
        c.status(201)
        return c.json({ status: "success" })
    } catch (error) {
        console.error(error)
        c.status(500)
        return c.json({ status: "failed" })
    }
})

app.post('/api/applied/:jobid', async (c) => {
    const jobid = c.req.param('jobid')
    const status = repo.toggleApplied(jobid)
    return c.json({ status: status })
})

app.post('/api/ignored/:jobid', async (c) => {
    const jobid = c.req.param('jobid')
    const status = repo.toggleIgnored(jobid)
    return c.json({ status: status })
})


console.log("\nHono server started...\n")
Bun.serve({
    port: 3000,
    hostname: "127.0.0.1",
    development: false,
    fetch: app.fetch
})