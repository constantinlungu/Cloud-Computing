import { Component, OnInit } from '@angular/core';
import { JokesService } from '../jokes.service'

@Component({
  selector: 'app-jokes',
  templateUrl: './jokes.component.html',
  styleUrls: ['./jokes.component.scss']
})
export class JokesComponent implements OnInit {

  text: Object;

  constructor(private joke: JokesService) { }

  ngOnInit() {
  }

  jokeClicked(){
    this.joke.getJoke().subscribe(joke => { 
      this.text = joke
      console.log(this.text)
    })
  }

}
