import {Component, OnInit} from '@angular/core';
import {User} from "../model/User";
import {first} from "rxjs/operators";
import {AuthService} from "../auth/auth.service";
import {Router} from '@angular/router';


@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})
export class SignUpComponent implements OnInit {

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
   * When user presses the button "Sign up"
   */
  onRegister(): void {

    const loginUser: User = {
      username: this.usernameInput.value,
      password: this.passwordInput.value,
    };

    if (this.usernameInput.value != "" && this.passwordInput.value != "") {
      this.authService.register(loginUser)
        .pipe(first())
        .subscribe(
          data => {
            alert(data["message"])
            this.router.navigate(['']);
          },
          error => {
            alert("Username and/or Email doesn't exists");
          });
    } else {
      alert("Please fill in all fields")
    }
  }
}
