import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class C3DService {
  private endPoint = 'http://50.18.103.109:3800'
  constructor(private http: HttpClient) {  }


  public consumirAnalizador(entrada: any) {
    return this.http.post<any>(this.endPoint + '/entrada', entrada);
}
}

