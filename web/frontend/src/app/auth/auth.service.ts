import {Injectable} from "@angular/core";
import {HttpClient} from '@angular/common/http';
import {BehaviorSubject, Observable} from 'rxjs';
import {User} from "../model/User";


@Injectable({
  providedIn: 'root',
})

export class AuthService {

  constructor(private http: HttpClient) {
  }

  /**
   * Service that will be responsible for the user's login
   * @param user user object
   */
  login(user: User) {
    return this.http.post<any>(
      'http://localhost:5000/api/login', {user}
    );
  }

  /**
   * Service that will be responsible for the user's registry
   * @param user user object
   */
  register(user: User) {
    return this.http.post<any>(
      'http://localhost:5000/api/register', {user}
    );
  }

  /**
   * Service that will be responsible for getting the token authentication
   */
  getToken() {
    return this.http.get<any>(
      'http://localhost:5000/api/me'
    );
  }

  /**
   * Service that will be responsible for user's logout
   */
  logout() {
    localStorage.removeItem('currentUser');
  }

}
