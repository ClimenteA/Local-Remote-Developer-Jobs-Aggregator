import { Database } from "bun:sqlite"
import { randomUUID } from 'crypto'


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


const jobTypeFilter = {
    new: "applied = 0 AND ignored = 0",
    applied: "applied = 1",
    ignored: "ignored = 1"
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

        db.query(`CREATE UNIQUE INDEX IF NOT EXISTS url_IDX ON "jobs" (url)`).run()

        return db

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

        for (const rawjob of rawJobs) {

            const job = { ...rawjob, jobid: randomUUID(), applied: 0, ignored: 0, timestamp: currentDate }

            const values = `("${job.jobid}", "${job.url}", "${job.title}", "${job.source}", ${job.applied}, ${job.ignored}, "${job.timestamp}")`

            try {
                this.db.query(`
                INSERT INTO jobs (jobid, url, title, source, applied, ignored, timestamp) VALUES ${values};`
                ).run()
            } catch (error) {
                console.log("Already in database. Skipping... ", values)
            }

        }


    }

    getJobs(jobType: string, page: number = 1) {

        const { limit, offset } = Repo.getLimitOffsetFromPage(page)

        const rows = this.db.query(
            `SELECT * FROM jobs WHERE ${jobTypeFilter[jobType]} ORDER BY datetime(timestamp) DESC LIMIT ${limit} OFFSET ${offset};`
        ).all()

        return rows
    }

    countJobs() {


        const countRows = (jobType: string) => {
            const response: any = this.db.query(
                `SELECT COUNT(*) FROM jobs WHERE ${jobTypeFilter[jobType]};`
            ).get()
            if (response["COUNT(*)"]) return response["COUNT(*)"]
            return 0
        }


        const newJobsCount = Number(countRows("new"))
        const appliedJobsCount = Number(countRows("applied"))
        const ignoredJobsCount = Number(countRows("ignored"))

        const counted: { [key: string]: number } = {
            new: newJobsCount,
            applied: appliedJobsCount,
            ignored: ignoredJobsCount
        }

        return counted
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
