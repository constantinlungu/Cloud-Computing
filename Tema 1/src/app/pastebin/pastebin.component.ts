import { Component, OnInit } from '@angular/core';
import { PastebinService } from '../pastebin.service';

@Component({
  selector: 'app-pastebin',
  templateUrl: './pastebin.component.html',
  styleUrls: ['./pastebin.component.scss']
})
export class PastebinComponent implements OnInit {

  text: Object;

  constructor(private pastebin: PastebinService) { }

  ngOnInit() {
  }

  pastebinClicked(){
    this.pastebin.post().subscribe(pastebin => { 
      this.text = pastebin
      console.log(this.text)
    })
  }

  
}
