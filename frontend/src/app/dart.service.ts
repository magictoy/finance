import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';

@Injectable()
export class DartService {
    constructor(private http: Http) { }

    getRecord(id: number): Observable<string> {
        return this.http
            .get('http://localhost:8002/entities/dart_report:' + id)
            .map((resp: Response) => resp.json());
    }

    getRecords(): Observable<string[]> {
        return this.http
            .get('http://localhost:8002/entities/dart_report')
            .map((resp: Response) => resp.json());
    }
}
