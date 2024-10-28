import { Component, OnInit, Input } from '@angular/core';
import { Paint } from 'src/app/services/paints.service';

@Component({
  selector: 'app-paint-graphic',
  templateUrl: './paint-graphic.component.html',
  styleUrls: ['./paint-graphic.component.scss'],
})
export class PaintGraphicComponent implements OnInit {
  @Input() paint: Paint;

  constructor() { }

  ngOnInit() {}

}
