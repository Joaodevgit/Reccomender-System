import {Injectable} from "@angular/core";
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {Movie} from "../model/Movie";

@Injectable({
  providedIn: 'root',
})

export class SearchResultsService {

  constructor(private http: HttpClient) {
  }

  /**
   * Service that will be responsible for getting the results from the search bar input
   * @param searchResults search bar content
   */
  getSearchResultsMovies(searchResults: string): Observable<Movie> {
    return this.http.get<Movie>(
      `http://localhost:5000/api/searchResults/${searchResults}`
    );
  }
}
