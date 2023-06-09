import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class InterpretarService {
  private endPoint = 'http://localhost:5000'
  constructor(private http: HttpClient) {  }


  public consumirAnalizador(entrada: any) {
    return this.http.post<any>(this.endPoint + '/entrada', entrada);
}
}

