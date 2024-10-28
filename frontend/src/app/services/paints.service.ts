import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { AuthService } from './auth.service';
import { environment } from 'src/environments/environment';

export interface Paint {
  id: number;
  title: string;
  recipe: Array<{
          binder: string,
          pigment: string,
          extender: string,
          solvent: string,
          additives: string
        }>;
}

@Injectable({
  providedIn: 'root'
})
export class PaintsService {

  url = environment.apiServerUrl;

  public items: {[key: number]: Paint} = {};

  constructor(private auth: AuthService, private http: HttpClient) { }

  getHeaders() {
    const header = {
      headers: new HttpHeaders()
        .set('Authorization',  `Bearer ${this.auth.activeJWT()}`)
    };
    return header;
  }

  getPaints() {
    if (this.auth.can('get:paints-detail')) {
      this.http.get(this.url + '/paints-detail', this.getHeaders())
      .subscribe((res: any) => {
        this.paintsToItems(res.paints);
        console.log(res);
      });
    } else {
      this.http.get(this.url + '/paints', this.getHeaders())
      .subscribe((res: any) => {
        this.paintsToItems(res.paints);
        console.log(res);
      });
    }

  }

  savePaint(paint: Paint) {
    if (paint.id >= 0) { // patch
      this.http.patch(this.url + '/paints/' + paint.id, paint, this.getHeaders())
      .subscribe( (res: any) => {
        if (res.success) {
          this.paintsToItems(res.paints);
        }
      });
    } else { // insert
      this.http.post(this.url + '/paints', paint, this.getHeaders())
      .subscribe( (res: any) => {
        if (res.success) {
          this.paintsToItems(res.paints);
        }
      });
    }

  }

  deletePaint(paint: Paint) {
    delete this.items[paint.id];
    this.http.delete(this.url + '/paints/' + paint.id, this.getHeaders())
    .subscribe( (res: any) => {

    });
  }

  paintsToItems( paints: Array<Paint>) {
    for (const paint of paints) {
      this.items[paint.id] = paint;
    }
  }
}
