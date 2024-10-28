import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TabsPage } from './tabs.page';

const routes: Routes = [
  {
    path: 'tabs',
    component: TabsPage,
    children: [
      { path: 'paint-menu', loadChildren: '../paint-menu/paint-menu.module#PaintMenuPageModule' },
      { path: 'user-page', loadChildren: '../user-page/user-page.module#UserPagePageModule' }, 
      {
        path: '',
        redirectTo: '/tabs/paint-menu',
        pathMatch: 'full'
      }
    ]
  },
  {
    path: '',
    redirectTo: '/tabs/paint-menu',
    pathMatch: 'full'
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [RouterModule]
})
export class TabsPageRoutingModule {}
