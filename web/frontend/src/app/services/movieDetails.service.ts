import {Injectable} from "@angular/core";
import {HttpClient, HttpParams} from '@angular/common/http';
import {Observable} from 'rxjs';
import {Movie} from "../model/Movie";


@Injectable({
  providedIn: 'root',
})

export class MovieDetailsService {

  constructor(private http: HttpClient) {
  }


  /**
   * Service that will be responsible for getting all the movie details data
   */
  getMovieDetails(movieId: number, user_id: number): Observable<Movie> {
    let params = new HttpParams().set('userID', user_id);
    return this.http.get<Movie>(
      `http://localhost:5000/api/movieDetails/${movieId}`, {params: params}
    );
  }

  /**
   * Service that will be responsible for associating movie to  a user
   */
  setUserWatchedMovie(movieId: number, userId: number): Observable<any> {
    return this.http.post<any>(
      `http://localhost:5000/api/movieDetails/${movieId}/${userId}`, ""
    );
  }

  /**
   * Service that will be responsible for associating a rating value assigned by a user to a movie
   * @param movieId movie id
   * @param userId user id
   * @param rating rating value assigned by the user
   */
  setUserRatedMovie(movieId: number, userId: number, rating: number): Observable<any> {
    return this.http.post<any>(
      `http://localhost:5000/api/movieDetails/rate/${movieId}/${userId}`, {rating}
    );
  }
}
