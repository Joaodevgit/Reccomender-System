import {NgModule} from '@angular/core';
import {Routes, RouterModule} from '@angular/router';
import {MainMenuComponent} from "./main-menu/main-menu.component";
import {MovieDetailsComponent} from "./movie-details/movie-details.component";
import {LoginComponent} from "./login/login.component";
import {UserProfileComponent} from "./user-profile/user-profile.component";
import {SignUpComponent} from "./sign-up/sign-up.component";
import {SearchResultsComponent} from "./search-results/search-results.component";

const routes: Routes = [
  {path: '', component: LoginComponent},
  {path: 'signup', component: SignUpComponent},
  {path: 'mainMenu', component: MainMenuComponent},
  {path: 'movieDetails/:movie_id', component: MovieDetailsComponent},
  {path: 'userProfile', component: UserProfileComponent},
  {path: 'searchResults/:search_result', component: SearchResultsComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
