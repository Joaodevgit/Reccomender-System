import {Injectable} from "@angular/core";
import {HttpClient, HttpParams} from '@angular/common/http';
import {Observable} from 'rxjs';
import {Movie} from "../model/Movie";

@Injectable({
  providedIn: 'root',
})

export class UserProfileService {

  constructor(private http: HttpClient) {
  }

  /**
   * Service that will be responsible for getting all movies watched and rated by the user
   * @param user_id user id
   */
  getUserWatchedAndRatedMovies(user_id: number): Observable<Movie> {
    let params = new HttpParams().set('userID', user_id);
    return this.http.get<Movie>(
      'http://localhost:5000/api/userProfile', {params: params}
    );
  }

}
