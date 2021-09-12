import {Component, OnInit} from '@angular/core';
import {AuthService} from "../auth/auth.service";
import {User} from "../model/User";
import {Router} from '@angular/router';
import {UserProfileService} from "../services/userProfile.service";

@Component({
  selector: 'app-user-profile',
  templateUrl: './user-profile.component.html',
  styleUrls: ['./user-profile.component.css']
})
export class UserProfileComponent implements OnInit {

  public currentUser: User;
  public userWatchedMovies: any[] = [];
  public userRatedMovies: any[] = [];
  public isLoaded = false;
  public hasWatchedMovies;
  public hasRatedMovies;

  constructor(private router: Router, private authService: AuthService, private profileService: UserProfileService) {
  }

  ngOnInit(): void {

    this.authService.getToken().subscribe(tokenInfo => {
      this.currentUser = tokenInfo
      this.profileService.getUserWatchedAndRatedMovies(tokenInfo["user_id"]).subscribe(userMoviesInfo => {
        if (userMoviesInfo["userWatchedMovies"].length != 0) {
          this.userWatchedMovies = userMoviesInfo["userWatchedMovies"]
          this.hasWatchedMovies = true;
        } else {
          this.hasWatchedMovies = false;
        }
        if (userMoviesInfo["userRatedMovies"].length != 0) {
          this.userRatedMovies = userMoviesInfo["userRatedMovies"]
          this.hasRatedMovies = true;
        } else {
          this.hasRatedMovies = false;
        }
        this.isLoaded = true;
      });
    });
  }

  /**
   * When user click in the button "Logout"
   */
  logout() {
    this.authService.logout();
    this.router.navigate(['']);
  }

}
