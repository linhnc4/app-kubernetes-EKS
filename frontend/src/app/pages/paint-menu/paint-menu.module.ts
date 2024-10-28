import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';

import { IonicModule } from '@ionic/angular';

import { PaintMenuPage } from './paint-menu.page';
import { PaintGraphicComponent } from './paint-graphic/paint-graphic.component';
import { PaintFormComponent } from './paint-form/paint-form.component';

const routes: Routes = [
  {
    path: '',
    component: PaintMenuPage
  }
];

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    RouterModule.forChild(routes)
  ],
  entryComponents: [paintFormComponent],
  declarations: [PaintMenuPage, PaintGraphicComponent, PaintFormComponent],
})
export class paintMenuPageModule {}
