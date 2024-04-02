import { Database } from "bun:sqlite"
import { randomUUID } from 'crypto';


export interface RawJob {
    url: string
    title: string
    source: string
}


export interface Job extends RawJob {
    applied: number
    ignored: number
    timestamp: string
}


export class Repo {
    db: Database

    constructor(dbPath: string = "./jobs.db") {
        this.db = Repo.initialize_jobs_database(dbPath)
    }

    static initialize_jobs_database(dbPath: string) {

        const db = new Database(dbPath, { create: true })
        db.exec("PRAGMA journal_mode = WAL;")

        db.query(`
        CREATE TABLE IF NOT EXISTS jobs (
            jobid TEXT,
            url TEXT,
            title TEXT,
            source TEXT,
            applied BOOLEAN,
            ignored BOOLEAN,
            timestamp TEXT);
        `).run()


        db.query(`
        CREATE TABLE IF NOT EXISTS scrape (
            url TEXT,
            scrapping BOOLEAN,
            timestamp TEXT);
        `).run()

        db.query(`CREATE UNIQUE INDEX IF NOT EXISTS url_IDX ON "jobs" (url)`).run()

        return db

    }

    scrappingInProgress() {
        return this.db.query(`SELECT * FROM scrape WHERE scrapping = $scrapping`).get({ $scrapping: 1 })
    }

    setScrapping(url: string, started: number) {
        const currentDate = new Date().toISOString()
        const exists: any = this.db.query(`SELECT * FROM scrape WHERE url = $url`).get({ $url: url })

        if (exists) {
            this.db.query(
                `UPDATE scrape SET scrapping = ${started}, timestamp = "${currentDate}"  WHERE url = "${url}"`
            ).run()
        } else {
            this.db.query(
                `INSERT INTO scrape(url, scrapping, timestamp) VALUES("${url}", ${started}, "${currentDate}")`
            ).run()
        }
    }


    updateJobIdStatus(jobid: string, field: string, status: number) {
        this.db.query(
            `UPDATE jobs SET ${field} = ${status} WHERE jobid = "${jobid}"`
        ).run()
    }

    toggleApplied(jobid: string) {
        const applied = this.db.query(
            `SELECT * FROM jobs WHERE jobid = $jobid AND applied = $applied`
        ).get({ $jobid: jobid, $applied: 1 })

        if (applied) {
            this.updateJobIdStatus(jobid, "applied", 0)
            return 0
        } else {
            this.updateJobIdStatus(jobid, "applied", 1)
            return 1
        }
    }

    toggleIgnored(jobid: string) {
        const ignored = this.db.query(
            `SELECT * FROM jobs WHERE jobid = $jobid AND ignored = $ignored`
        ).get({ $jobid: jobid, $ignored: 1 })

        if (ignored) {
            this.updateJobIdStatus(jobid, "ignored", 0)
            return 0
        } else {
            this.updateJobIdStatus(jobid, "ignored", 1)
            return 1
        }
    }

    static getLimitOffsetFromPage(page: number, itemsPerPage: number = 100) {
        try {
            page = Math.abs(Number(page))
            if (page <= 0) page = 1
        } catch (error) {
            page = 1
        }
        const limit = itemsPerPage
        const offset = page == 1 ? 0 : (page - 1) * itemsPerPage
        return { limit, offset }
    }

    saveJobs(rawJobs: Array<RawJob>) {

        const currentDate = new Date().toISOString()
        const urlQuery = this.db.query(`SELECT * FROM jobs WHERE url = $url`)

        const sources: Set<string> = new Set([])
        const values: Array<string> = []
        for (const rawjob of rawJobs) {

            sources.add(rawjob.source)

            if (urlQuery.get({ $url: rawjob.url })) continue

            const job = { ...rawjob, jobid: randomUUID(), applied: 0, ignored: 0, timestamp: currentDate }

            values.push(`("${job.jobid}", "${job.url}", "${job.title}", "${job.source}", ${job.applied}, ${job.ignored}, "${job.timestamp}")`)
        }

        for (const src of sources) {
            this.setScrapping(src, 0)
        }

        if (values.length == 0) return

        this.db.query(`
        INSERT INTO jobs(jobid, url, title, source, applied, ignored, timestamp) 
        VALUES ${values.join(", ") + ";"}`
        ).run()

    }

    getJobs(jobType: string, page: number = 1) {

        const { limit, offset } = Repo.getLimitOffsetFromPage(page)

        let filters: string
        if (jobType == "new") {
            filters = "applied = 0 AND ignored = 0"
        } else if (jobType == "applied") {
            filters = "applied = 1"
        } else if (jobType == "ignored") {
            filters = "ignored = 1"
        } else {
            throw Error("Only new, applied, ignored are known")
        }

        const rows = this.db.query(
            `SELECT * FROM jobs WHERE ${filters} LIMIT ${limit} OFFSET ${offset}; `
        ).all()
        return rows
    }

    getNewJobs(page: number = 1) {
        return this.getJobs("new", page)
    }

    getAppliedJobs(page: number = 1) {
        return this.getJobs("applied", page)
    }

    getIgnoredJobs(page: number = 1) {
        return this.getJobs("ignored", page)
    }

}
