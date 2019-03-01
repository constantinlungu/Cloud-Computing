import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { JokesComponent } from './jokes/jokes.component';
import { TriviaComponent } from './trivia/trivia.component';
import { PastebinComponent } from './pastebin/pastebin.component';

const routes: Routes = [
  { path: '', component: JokesComponent},
  { path: 'trivia', component: TriviaComponent},
  { path: 'pastebin', component: PastebinComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
