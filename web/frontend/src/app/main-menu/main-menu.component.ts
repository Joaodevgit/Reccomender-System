import {Component, OnInit} from '@angular/core';
import {MainMenuService} from "../services/mainMenu.service";
import {Router} from '@angular/router';
import {AuthService} from "../auth/auth.service";
import {User} from "../model/User";


@Component({
  selector: 'app-main-menu',
  templateUrl: './main-menu.component.html',
  styleUrls: ['./main-menu.component.css']
})
export class MainMenuComponent implements OnInit {

  public popularActionMovies: any[] = [];
  public popularComedyMovies: any[] = [];
  public userRecommendedMovies: any[] = [];
  public isLoaded = false;
  public inputSearchBar: HTMLInputElement;
  public currentUser: User;

  constructor(private router: Router, private mainMenuService: MainMenuService, private authService: AuthService) {
  }

  ngOnInit(): void {
    this.authService.getToken().subscribe(tokenInfo => {
      this.currentUser = tokenInfo
      this.mainMenuService.getMainMenuMovies(tokenInfo["user_id"]).subscribe(menuMoviesInfo => {
        this.popularActionMovies = menuMoviesInfo["popularActionMovies"]
        this.popularComedyMovies = menuMoviesInfo["popularComedyMovies"]
        this.userRecommendedMovies = menuMoviesInfo["recommendedUserMovies"]
        this.isLoaded = true;
      });
    });

    let inputSearchBar = document.getElementById(
      'searchBar'
    ) as HTMLInputElement;

    this.inputSearchBar = inputSearchBar;
  }


  /**
   * When user searchs for a movie in search bar
   */
  public searchForMovies() {
    this.router.navigate(['/searchResults/' + this.inputSearchBar.value]);
  }

  /**
   * When user click in the button "Logout"
   */
  logout() {
    this.authService.logout();
    this.router.navigate(['']);
  }

}
