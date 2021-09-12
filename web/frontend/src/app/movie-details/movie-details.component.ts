import {Component, OnInit} from '@angular/core';
import {MovieDetailsService} from "../services/movieDetails.service";
import {Router} from '@angular/router';
import {AuthService} from "../auth/auth.service";
import {User} from "../model/User";


@Component({
  selector: 'app-movie-details',
  templateUrl: './movie-details.component.html',
  styleUrls: ['./movie-details.component.css']
})
export class MovieDetailsComponent implements OnInit {

  public isLoaded = false;
  private movieID: number;
  public movieDetails: any;
  public movieGenres: string;
  public hasWatchedMovie = false;
  public currentUser: User;
  private userID: number;
  currentRate: number;


  constructor(private router: Router, private movieDetailsService: MovieDetailsService, private authService: AuthService) {
    this.movieID = parseInt(this.router.url.split('/')[2])
  }

  ngOnInit(): void {
    this.authService.getToken().subscribe(tokenInfo => {
      this.currentUser = tokenInfo
      this.movieDetailsService.getMovieDetails(this.movieID, tokenInfo["user_id"]).subscribe(moviesDetailsInfo => {
        this.movieGenres = moviesDetailsInfo["genres"].toString()
        this.movieDetails = moviesDetailsInfo["movieInfo"]
        this.hasWatchedMovie = moviesDetailsInfo["hasWatched"]
        this.userID = tokenInfo["user_id"];
        this.currentRate = moviesDetailsInfo["movieRating"];
        this.isLoaded = true;
      });
    });
  }

  /**
   * When uer clicks in button "Rate" to rate a movie
   * @param userRating rating value assigned by the user
   */
  updateClientRatings(userRating) {
    if (userRating != 0) {
      this.movieDetailsService.setUserRatedMovie(this.movieID, this.userID, userRating)
        .subscribe(userMovieRatedInfo => {
          // console.log(userMovieRatedInfo["message"])
          alert(userMovieRatedInfo["message"])
          window.location.reload();
        });
    }
  }


  /**
   * When uer clicks in button "Watch"
   */
  updateClientMoviesWatched() {
    this.movieDetailsService.setUserWatchedMovie(this.movieID, this.userID)
      .subscribe(userMovieWatchedInfo => {
        alert(userMovieWatchedInfo["message"])
        window.location.reload();
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
