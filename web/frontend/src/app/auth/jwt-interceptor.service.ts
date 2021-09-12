import {Injectable} from "@angular/core";
import {HttpClient, HttpEvent, HttpHandler, HttpInterceptor, HttpParams, HttpRequest} from '@angular/common/http';
import {BehaviorSubject, Observable} from 'rxjs';


@Injectable({
  providedIn: 'root',
})

export class JwtInterceptorService implements HttpInterceptor {
  intercept(
    request: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    let currentUser = localStorage.getItem('currentUser') || '{}';
    // console.log('HttpInterpreter: ' + JSON.stringify(currentUser));
    if (currentUser) {
      request = request.clone({
        setHeaders: {
          Authorization: `Bearer ${currentUser}`,
        },
      });
    }

    return next.handle(request);
  }


}
