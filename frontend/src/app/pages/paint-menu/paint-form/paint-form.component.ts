import { Component, OnInit, Input } from '@angular/core';
import { Paint, PaintsService } from 'src/app/services/paints.service';
import { ModalController } from '@ionic/angular';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-paint-form',
  templateUrl: './paint-form.component.html',
  styleUrls: ['./paint-form.component.scss'],
})
export class PaintFormComponent implements OnInit {
  @Input() paint: Paint;
  @Input() isNew: boolean;

  constructor(
    public auth: AuthService,
    private modalCtrl: ModalController,
    private paintService: PaintsService
    ) { }

  ngOnInit() {
    if (this.isNew) {
      this.paint = {
        id: -1,
        title: '',
        recipe: []
      };
      this.addIngredient();
    }
  }

  customTrackBy(index: number, obj: any): any {
    return index;
  }

  addIngredient(i: number = 0) {
    this.paint.recipe.splice(i + 1, 0, {name: '', color: 'white', parts: 1});
  }

  removeIngredient(i: number) {
    this.paint.recipe.splice(i, 1);
  }

  closeModal() {
    this.modalCtrl.dismiss();
  }

  saveClicked() {
    this.paintService.savePaint(this.paint);
    this.closeModal();
  }

  deleteClicked() {
    this.paintService.deletePaint(this.paint);
    this.closeModal();
  }
}
