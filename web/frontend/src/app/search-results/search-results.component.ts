import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {SearchResultsService} from "../services/searchResults.service";
import {User} from "../model/User";
import {AuthService} from "../auth/auth.service";


@Component({
  selector: 'app-search-results',
  templateUrl: './search-results.component.html',
  styleUrls: ['./search-results.component.css']
})
export class SearchResultsComponent implements OnInit {

  public isLoaded = false;
  private search_words: string;
  public moviesSearched: any;
  public inputSearchBar: HTMLInputElement;
  public currentUser: User;

  constructor(private router: Router, private searchResultsService: SearchResultsService, private authService: AuthService) {
    this.search_words = this.router.url.split('/')[2]

  }

  ngOnInit(): void {
    this.authService.getToken().subscribe(tokenInfo => {
      this.currentUser = tokenInfo
      this.searchResultsService.getSearchResultsMovies(this.search_words).subscribe(searchResultsInfo => {
        this.moviesSearched = searchResultsInfo["moviesSearched"]
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
