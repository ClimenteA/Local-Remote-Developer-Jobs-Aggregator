import { Hono } from 'hono'
import { serveStatic } from 'hono/bun'
import { logger } from 'hono/logger'
import { cors } from 'hono/cors'
import { Repo, RawJob } from './repo'


const app = new Hono()
const repo = new Repo()

app.use(logger())
app.use('/api/*', cors())
app.get('/', serveStatic({ path: './index.html' }))


app.get('/api/new/:page', (c) => {
    const page = Number(c.req.param('page'))
    const newJobs = repo.getNewJobs(page)
    return c.json({ jobs: newJobs, page: page })
})

app.get('/api/applied/:page', (c) => {
    const page = Number(c.req.param('page'))
    const appliedJobs = repo.getAppliedJobs(page)
    return c.json({ jobs: appliedJobs, page: page })
})

app.get('/api/ignored/:page', (c) => {
    const page = Number(c.req.param('page'))
    const ignoredJobs = repo.getIgnoredJobs(page)
    return c.json({ jobs: ignoredJobs, page: page })
})


app.post('/api/save-jobs', async (c) => {
    const jobs: Array<RawJob> = await c.req.json()
    repo.saveJobs(jobs)
    return c.json({ jobs: jobs.length })
})


Bun.serve({
    port: 3000,
    hostname: "127.0.0.1",
    development: true,
    fetch: app.fetch
})