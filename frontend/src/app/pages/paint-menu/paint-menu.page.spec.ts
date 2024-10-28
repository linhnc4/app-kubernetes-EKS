import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PaintMenuPage } from './paint-menu.page';

describe('PaintMenuPage', () => {
  let component: PaintMenuPage;
  let fixture: ComponentFixture<PaintMenuPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PaintMenuPage ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PaintMenuPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
