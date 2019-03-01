import { Component, OnInit } from '@angular/core';
import { TriviaService } from '../trivia.service';

@Component({
  selector: 'app-trivia',
  templateUrl: './trivia.component.html',
  styleUrls: ['./trivia.component.scss']
})
export class TriviaComponent implements OnInit {

  text: Object;

  constructor(private trivia: TriviaService) { }

  ngOnInit() {
  }

  yearClicked(){
    this.trivia.getFact().subscribe(trivia => { 
      this.text = trivia
      console.log(this.text)
    })
  }

}
