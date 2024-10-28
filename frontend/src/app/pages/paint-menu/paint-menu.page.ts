import { Component, OnInit } from '@angular/core';
import { PaintsService, Paint } from '../../services/paints.service';
import { ModalController } from '@ionic/angular';
import { PaintFormComponent } from './paint-form/paint-form.component';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-paint-menu',
  templateUrl: './paint-menu.page.html',
  styleUrls: ['./paint-menu.page.scss'],
})
export class PaintMenuPage implements OnInit {
  Object = Object;

  constructor(
    private auth: AuthService,
    private modalCtrl: ModalController,
    public paints: PaintsService
    ) { }

  ngOnInit() {
    this.paints.getPaints();
  }

  async openForm(activepaint: Paint = null) {
    if (!this.auth.can('get:paints-detail')) {
      return;
    }

    const modal = await this.modalCtrl.create({
      component: PaintFormComponent,
      componentProps: { paint: activepaint, isNew: !activepaint }
    });

    modal.present();
  }

}
