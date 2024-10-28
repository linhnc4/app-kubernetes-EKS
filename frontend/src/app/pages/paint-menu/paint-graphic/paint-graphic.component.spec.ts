import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PaintGraphicComponent } from './paint-graphic.component';

describe('PaintGraphicComponent', () => {
  let component: PaintGraphicComponent;
  let fixture: ComponentFixture<PaintGraphicComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PaintGraphicComponent ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PaintGraphicComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
