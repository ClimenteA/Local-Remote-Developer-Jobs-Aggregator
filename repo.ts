import { Database } from "bun:sqlite"


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

    constructor(dbPath: string = "./jobs.db"){
        this.db = Repo.initialize_jobs_database(dbPath)
    }

    static initialize_jobs_database(dbPath: string){

        const db = new Database(dbPath, { create: true })
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

        return db

    }

    static getLimitOffsetFromPage(page: number, itemsPerPage: number = 100) {
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

    saveJobs(rawJobs: Array<RawJob>){

        const currentDate = new Date().toISOString()
        const urlQuery = this.db.query(`SELECT * FROM jobs WHERE url = $url`)
    
        const values: Array<string> = []
        for (const rawjob of rawJobs){
    
            if (urlQuery.get({$url: rawjob.url})) continue
    
            const job = {...rawjob, applied: 0, ignored: 0, timestamp: currentDate}
    
            values.push(`("${job.url}", "${job.title}", "${job.source}", ${job.applied}, ${job.ignored}, "${job.timestamp}")`)     
        }
    
        if (values.length == 0) return
    
        this.db.query(`
        INSERT INTO jobs (url, title, source, applied, ignored, timestamp) 
        VALUES ${values.join(", ") + ";"}`
        ).run()
    
    }

    getJobs(jobType: string, page: number = 1){

        const {limit, offset} = Repo.getLimitOffsetFromPage(page)

        let filters: string
        if (jobType == "new"){
            filters = "applied = 0 AND ignored = 0"
        } else if (jobType == "applied") {
            filters = "applied = 1"
        } else if (jobType == "ignored") {
            filters = "ignored = 1"
        } else {
            throw Error("Only new, applied, ignored are known")
        }

        const rows = this.db.query(
            `SELECT * FROM jobs WHERE ${filters} LIMIT ${limit} OFFSET ${offset};`
        ).all()
        return rows
    }

    getNewJobs(page: number = 1){
        return this.getJobs("new", page)
    }

    getAppliedJobs(page: number = 1){
        return this.getJobs("applied", page)
    }
    
    getIgnoredJobs(page: number = 1){
        return this.getJobs("ignored", page)
    }
    
}
