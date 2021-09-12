import {Component, OnInit} from '@angular/core';
import {AuthService} from "../auth/auth.service";
import {first} from "rxjs/operators";
import {User} from "../model/User";
import {Router} from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  private usernameInput: HTMLInputElement;
  private passwordInput: HTMLInputElement;

  constructor(private router: Router, private authService: AuthService) {
  }

  ngOnInit(): void {

    let usernameInput = document.getElementById(
      'userNameForm'
    ) as HTMLInputElement;

    let passwordInput = document.getElementById(
      'passwordForm'
    ) as HTMLInputElement;

    this.usernameInput = usernameInput;
    this.passwordInput = passwordInput;
  }

  /**
   * When user presses the button "Login"
   */
  onLogin(): void {
    const loginUser: User = {
      username: this.usernameInput.value,
      password: this.passwordInput.value,
    };
    if (this.usernameInput.value != "" && this.passwordInput.value != "") {
      this.authService.login(loginUser)
        .pipe(first())
        .subscribe(
          data => {
            // Receive data from the backend
            localStorage.setItem("currentUser", data["token"])
            this.router.navigate(['/mainMenu']);
          },
          error => {
            alert("Username and/or Email doesn't exists");
          });
    }
  }
}

